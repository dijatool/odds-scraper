#!/usr/bin/env python

import urllib2
import os
import sys
import string
import re
from BeautifulSoup import BeautifulSoup as bs

# Run like so...
#
#	packers-roster.py > /tmp/packers-roster-plain.txt
#	md5 /tmp/packers-roster-plain.txt
#
#	~/github/local/odds-scraper/packers-roster.py --csv


def cleanMsg( obj ) :
	'''
		Take the object and strip everything to make it clean text
	'''
	return ''.join( bs( str( obj )).findAll( text=True )).strip()


def loadPage( url ) :
	'''
		Given a url returns a soup object

	'''
	opener = urllib2.build_opener()
	link = opener.open( url )
	page = link.read()
	soup = bs( page )

	return soup

_names = [ 'last', 'first', 'number', 'link', 'position', 'height', 'weight', 'college',  ]


def toCsvRow( writer, buffer, rowData ) :
	'''

		Yuck ... need an object to wrap this all up in

	'''
	writer.writerow( rowData )
	row = buffer.getvalue().rstrip()
	buffer.truncate( 0 )

	return row


# what follows are a set of callbacks to get data from the soup into a dictionary

def getLink( row, destDict, destName, srcName ) :
	'''
		getLink needs a description...

	'''
	name = row.findChild( 'td', { "class" : "col-name" })
	names = cleanMsg( name ).split( ',' )
	first = names[ 1 ].rstrip().lstrip()
	destDict[ 'first' ] = first
	last = names[ 0 ]
	destDict[ 'last' ] = last
	link = name.findChild( 'a' )
	linkUrl = "http://www.packers.com%s" % link[ 'href' ]
	destDict[ destName ] = linkUrl


def getData( row, destDict, destName, srcName ) :
	'''
		getData needs a description...

	'''
	data = cleanMsg( row.findChild( 'td', { "class" : srcName }))
	destDict[ destName ] = data


def getHeight( row, destDict, destName, srcName ) :
	'''
		getHeight needs a description...

	'''
	data = cleanMsg( row.findChild( 'td', { "class" : srcName }))
	hInfo = data.split( '-' )
	height = 12 * int( hInfo[ 0 ] ) + int( hInfo[ 1 ] )
	destDict[ destName ] = height


_builder = {	# we handle the names when we do the link
				# 'last'		:
				# 'first'		:
				'link'		: [ getLink, 'None' ],
				'number'	: [ getData, 'col-jersey' ],
				'position'	: [ getData, 'col-position' ],
				'height'	: [ getHeight, 'col-height' ],
				'weight'	: [ getData, 'col-weight' ],
				'college'	: [ getData, 'col-college' ],
				}


def download( url, options, printLink=False, printSchool=False ) :
	'''
		Pull the page and parse it into the pieces we need.
	'''
	import csv
	import StringIO

	buf = StringIO.StringIO()
	writer = csv.writer( buf, quoting=csv.QUOTE_ALL )
	dictWriter = csv.DictWriter( buf, _names, quoting=csv.QUOTE_ALL )

	loopRegEx = re.compile( ' loop-' )		# each row has the class tag ' loop-*'

	soup = loadPage( url )
	mainBodyObj = soup.findChild( None, { "class" : "game-roster-large" }).findChild( None, { "class" : "bd" })

	if options.csv :
		#print the names of all the columns so we have a real csv file
		print toCsvRow( writer, buf, _names )

	# find the sections...
	sections = mainBodyObj.findAll( None, { "class" : "mod-title-nobackground" })
	for i, aSection in enumerate( sections ) :
		if not options.csv :
			print cleanMsg( aSection )
		# now get at the table stuff just below each section...
		aTable = aSection.findNextSibling( 'table' )
		rows = aTable.findChildren( 'tr', { "class" : loopRegEx })
		for aRow in rows :
			playerDict = {}
			for aName in _names :
				funcRef, scrName = _builder.get( aName, [ None, "" ] )
				if None != funcRef :
					funcRef( aRow, playerDict, aName, scrName )

			if options.csv :
				print toCsvRow( dictWriter, buf, playerDict )
			else :
				print playerDict[ 'number' ], "%s, %s" % ( playerDict[ 'last' ], playerDict[ 'first' ], )

		print


def doOptions() :
	'''
		Handle the options for this app

	'''
	from optparse import OptionParser

	usage = "  %prog [options]"
	# appName = os.path.basename( sys.argv[ 0 ] )
	parser = OptionParser( usage = usage )
	parser.add_option( "-c", "--csv", dest="csv", default = False,
						action="store_true",
						help="Determine if we dump a CSV version of the data." )

	( options, args ) = parser.parse_args()
	return options


def main() :
	'''
		Go do something useful.

	'''
	options = doOptions()

	url = "http://www.packers.com/team/players.html"
	download( url, options )


if __name__ == '__main__':
	main()


