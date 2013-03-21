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
#	~/github/local/odds-scraper/scraper/roster.py http://www.packers.com/team/players.html > /tmp/packers-roster-plain.txt
#	md5 /tmp/packers-roster-plain.txt
#
#	~/github/local/odds-scraper/scraper/roster.py http://www.chicagobears.com/team/roster.html --csv
#	~/github/local/odds-scraper/scraper/roster.py http://www.chicagobears.com/team/roster.html
#

_baseUrl = "none"
_loopRegEx = re.compile( ' loop-' )		# each row has the class tag ' loop-*'


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


#_names = [ u'last', u'first', u'number', u'position', u'height', u'weight', u'college', u'link', ]
_names = [ u'last', u'first', u'age', u'exp', u'number', u'position', u'height', u'weight', u'college', u'link', ]


def toCsvRow( writer, buffer, rowData ) :
	'''

		Yuck ... need an object to wrap this all up in

		This whole thing has become a train wreak and the problem is still around...
		May need to punt back to a totally different approach

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
	destDict[ u'first' ] = first
	last = names[ 0 ]
	destDict[ u'last' ] = last
	link = name.findChild( 'a' )
	linkUrl = u"%s%s" % ( _baseUrl, link[ 'href' ] )
	destDict[ destName ] = linkUrl


def getData( row, destDict, destName, srcName ) :
	'''
		getData needs a description...

	'''
	data = cleanMsg( row.findChild( 'td', { "class" : srcName }))
	destDict[ destName ] = data


def getHeight( row, destDict, destName, srcName ) :
	'''
		Get height in inches...

	'''
	data = cleanMsg( row.findChild( 'td', { "class" : srcName }))
	data = data.replace( '"', '' )
	data = data.replace( "'", '-' )
	hInfo = data.split( '-' )
	height = data
	try :
		height = 12 * int( hInfo[ 0 ] ) + int( hInfo[ 1 ] )
	except :
		pass
	destDict[ destName ] = unicode( height )


_builder = {	# we handle the names when we do the link
				u'link'		: [ getLink, 'None' ],
				u'age'		: [ getData, 'col-bd' ],
				u'exp'		: [ getData, 'col-exp' ],
				u'number'	: [ getData, 'col-jersey' ],
				u'position'	: [ getData, 'col-position' ],
				u'height'	: [ getHeight, 'col-height' ],
				u'weight'	: [ getData, 'col-weight' ],
				u'college'	: [ getData, 'col-college' ],
				}


def playerData( tableSoup, playerList, options ) :
	'''
		Pull each player and the associated data from the provided table...

	'''
	rows = tableSoup.findChildren( 'tr', { "class" : _loopRegEx })
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


def download( url, options ) :
	'''
		Pull the page and parse it into the pieces we need.
	'''
	import unicodecsv
	import StringIO
	import urlparse
	from operator import itemgetter

	global _baseUrl
	parseUrl = urlparse.urlparse( url )
	_baseUrl = '%s://%s' % ( parseUrl.scheme, parseUrl.netloc )

	playerList = []

	strBuffer = StringIO.StringIO()
	writer = unicodecsv.writer( strBuffer, quoting=unicodecsv.QUOTE_ALL )
	dictWriter = unicodecsv.DictWriter( strBuffer, _names, quoting=unicodecsv.QUOTE_ALL )

	soup = loadPage( url )
	mainBodyObj = soup.findChild( None, { "class" : "game-roster-large" }).findChild( None, { "class" : "bd" })

	# find the sections...
	sections = mainBodyObj.findAll( None, { "class" : "mod-title-nobackground" })

	if len( sections ) > 1 :
		for aSection in sections :
			if not options.csv :
				print cleanMsg( aSection )
			# now get at the table stuff just below each section...
			aTable = aSection.findNextSibling( 'table' )
			playerData( aTable, playerList, options )
	else :
		# miami and the bucs do things differently
		aTable = mainBodyObj.findChild( 'table' )
		playerData( aTable, playerList, options )

	if options.csv :
		playerList.sort( key=itemgetter( 'last','first' ))
		if options.outputToFile :
			myfile = open( options.csvFile, mode='w' )
			fileWriter = unicodecsv.DictWriter( myfile, _names, quoting=unicodecsv.QUOTE_ALL )
			fileWriter.writeheader()
			for aPlayer in playerList :
				fileWriter.writerow( aPlayer )
			myfile.close()

		else :
			print toCsvRow( writer, strBuffer, _names )
			for aPlayer in playerList :
				print toCsvRow( dictWriter, strBuffer, aPlayer )


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
	options, url = doOptions()

	download( url, options )


if __name__ == '__main__':
	main()


