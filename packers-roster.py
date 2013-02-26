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


def listToCsvRow( writer, buffer, aList ) :
	'''

		Yuck ... need an object to wrap this all up in

	'''
	writer.writerow( aList )
	row = buffer.getvalue().rstrip()
	buffer.truncate( 0 )

	return row


def buildList( last, first, number, link, position, height, weight, college ) :
	'''
		buildList needs a description...

	'''
	aList = []

	aList.append( last )
	aList.append( first )
	aList.append( number )
	aList.append( link )
	aList.append( position )
	aList.append( height )
	aList.append( weight )
	aList.append( college )

	return aList


def download( url, options, printLink=False, printSchool=False ) :
	'''
		Pull the page and parse it into the pieces we need.
	'''
	import csv
	import StringIO

	buf = StringIO.StringIO()
	writer = csv.writer( buf, quoting=csv.QUOTE_ALL )

	loopRegEx = re.compile( ' loop-' )		# each row has the class tag ' loop-*'

	soup = loadPage( url )
	mainBodyObj = soup.findChild( None, { "class" : "game-roster-large" }).findChild( None, { "class" : "bd" })

	if options.csv :
		#print the names of all the columns so we have a real csv file
		print listToCsvRow( writer, buf, _names )

	# find the sections...
	sections = mainBodyObj.findAll( None, { "class" : "mod-title-nobackground" })
	for i, aSection in enumerate( sections ) :
		if not options.csv :
			print cleanMsg( aSection )
		# now get at the table stuff just below each section...
		aTable = aSection.findNextSibling( 'table' )
		rows = aTable.findChildren( 'tr', { "class" : loopRegEx })
		for aRow in rows :
			name = aRow.findChild( 'td', { "class" : "col-name" })
			names = cleanMsg( name ).split( ',' )
			first = names[ 1 ].rstrip().lstrip()
			last = names[ 0 ]
			link = name.findChild( 'a' )
			linkUrl = "http://www.packers.com%s" % link[ 'href' ]
			number = cleanMsg( aRow.findChild( 'td', { "class" : "col-jersey" }))
			position = cleanMsg( aRow.findChild( 'td', { "class" : "col-position" }))
			experience = cleanMsg( aRow.findChild( 'td', { "class" : "col-exp" }))
			height = cleanMsg( aRow.findChild( 'td', { "class" : "col-height" }))
			weight = cleanMsg( aRow.findChild( 'td', { "class" : "col-weight" }))
			college = cleanMsg( aRow.findChild( 'td', { "class" : "col-college" }))

			if options.csv :
				datums = buildList( last, first, number, linkUrl, position, height, weight, college )
				print listToCsvRow( writer, buf, datums )
			else :
				print number, "%s, %s" % ( last, first, )
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


