#!/usr/bin/env python

import urllib2
import os
import sys
import string
import re

from BeautifulSoup import BeautifulSoup as bs

#
# Run like so...
#
#	~/github/local/odds-scraper/roster.py http://www.packers.com/team/players.html > /tmp/packers-roster-plain.txt
#	md5 /tmp/packers-roster-plain.txt
#
#	~/github/local/odds-scraper/roster.py http://www.chicagobears.com/team/roster.html --csv
#	~/github/local/odds-scraper/roster.py http://www.chicagobears.com/team/roster.html
#

_baseUrl = "none"


def cleanMsg( obj ) :
	'''
		Take the object and strip everything to make it clean text
	'''
	return ''.join( bs( str( obj )).findAll( text=True )).strip()


def writeWinFile( filePath, data ) :
	'''
		Write out an array of text using windows linefeeds.

		Using the io classes forces us to convert to unicode

	'''
	import io

	theFile = io.open( filePath, mode='w', newline='\r\n' )
	for aLine in data :
		theFile.write( unicode( "%s\n" % aLine ))
	theFile.close()


def loadPage( url ) :
	'''
		Given a url returns a soup object

	'''
	opener = urllib2.build_opener()
	link = opener.open( url )
	page = link.read()
	soup = bs( page )

	return soup

_names = [ 'last', 'first', 'number', 'position', 'height', 'weight', 'college', 'link', ]


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
	linkUrl = "%s%s" % ( _baseUrl, link[ 'href' ] )
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
	height = data
	try :
		height = 12 * int( hInfo[ 0 ] ) + int( hInfo[ 1 ] )
	except :
		# sometimes we get bad data
		pass
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

	playerList = []

	buf = StringIO.StringIO()
	writer = csv.writer( buf, quoting=csv.QUOTE_ALL )
	dictWriter = csv.DictWriter( buf, _names, quoting=csv.QUOTE_ALL )

	loopRegEx = re.compile( ' loop-' )		# each row has the class tag ' loop-*'

	soup = loadPage( url )
	mainBodyObj = soup.findChild( None, { "class" : "game-roster-large" }).findChild( None, { "class" : "bd" })

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
				playerList.append( playerDict )
			else :
				print playerDict[ 'number' ], "%s, %s" % ( playerDict[ 'last' ], playerDict[ 'first' ], )

		if not options.csv :
			print

	if options.csv :
		if options.outputToFile :
			outData = []
			outData.append( toCsvRow( writer, buf, _names ))
			for aPlayer in playerList :
				outData.append( toCsvRow( dictWriter, buf, aPlayer ))
			writeWinFile( options.csvFile, outData )
		else :
			print toCsvRow( writer, buf, _names )
			for aPlayer in playerList :
				print toCsvRow( dictWriter, buf, aPlayer )


def doOptions() :
	'''
		Handle the options for this app

	'''
	from optparse import OptionParser

	url = None

	usage = "  %prog [options] team-url"
	parser = OptionParser( usage = usage )
	parser.add_option( "-c", "--csv", dest="csv", default = False,
						action="store_true",
						help="Determine if we dump a CSV version of the data." )
	parser.add_option( "", "--csvFile", dest="csvFile", default = None,
						help="Path to output a CSV file." )

	( options, args ) = parser.parse_args()
	setattr( options, 'outputToFile', False )

	if len( args ) < 1 :
		parser.print_help()
		import sys
		sys.exit( 0 )
	else :
		url = args[ 0 ]

	if options.csv and options.csvFile :
		options.outputToFile = True

	return options, url


def main() :
	'''
		Go do something useful.

	'''
	import urlparse

	global _baseUrl

	options, url = doOptions()
	parseUrl = urlparse.urlparse( url )
	_baseUrl = '%s://%s' % ( parseUrl.scheme, parseUrl.netloc )

	download( url, options )


if __name__ == '__main__':
	main()


