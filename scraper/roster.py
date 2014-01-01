#!/usr/bin/env python

import urllib2
import os
import sys
import string
import re
import traceback

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

_statusMap = {
	"Active" : 'ACT',
	"Inactive" : 'ACT',			# this is for the Bengals and anyone else that does this!	TODO take advantage of this somewhere down the line
	"Reserve/Injured" : 'IR',
	"Practice Squad/Injured" : 'IR',
	"Practice Squad" : 'PS',
	"Reserve/Designated to Return" : 'IRDR',
	"Reserve/Injured; Designated for Return" : 'IRDR',
	"Active/Physically Unable to Perform" : 'PUP',
	"Reserve/Physically Unable to Perform" : 'PUP',
	"Reserve/Non-Football Illness" : 'NFI',
	"Reserve/Non-Football Injury" : 'NFI',
	"Reserve/Suspended by Club" : 'SUC',
	"Reserve/Suspended by Commissioner" : 'SUS',
	"Reserve/Retired" : 'RET',
	"Reserve/Left Squad" : 	'LS',
	"Reserve/Future" : 'FUT',
	"RESERVE/FUTURE" : 'FUT',
	}


_status = 'ACT'

# field names we're accumulating
_names = [
	u'last',
	u'first',
	u'age',
	u'exp',
	u'number',
	u'position',
	u'height',
	u'weight',
	u'college',
	u'link',
	u'status',
	]


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

	# sometimes extra commas show up outta nowhere!
	# eat them until only two name chunks remain
	while len( names ) > 2 :
		names[ 0 ] = '%s,%s' % ( names[ 0 ], names[ 1 ] )
		del names[ 1 ]

	first = names[ 1 ].rstrip().lstrip()
	destDict[ u'first' ] = first
	last = names[ 0 ]
	destDict[ u'last' ] = last
	link = name.findChild( 'a' )
	linkUrl = u"%s%s" % ( _baseUrl, link[ 'href' ] )
	linkUrl = linkUrl.replace( ' ', '%20' )
	destDict[ destName ] = linkUrl


def getData( row, destDict, destName, srcName ) :
	'''
		getData needs a description...

	'''
	data = cleanMsg( row.findChild( 'td', { "class" : srcName }))
	destDict[ destName ] = data


def getStatus( row, destDict, destName, srcName ) :
	'''
		Get the status stashed in a global...

		Not ideal but it works for this approach

	'''
	global _status
	destDict[ destName ] = unicode( _status )


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
				u'status'	: [ getStatus, 'None' ],
				}


def playerData( tableSoup, playerList, options ) :
	'''
		Pull each player and the associated data from the provided table...

	'''
	rows = tableSoup.findChildren( 'tr', { "class" : _loopRegEx })
	for aRow in rows :
		ignorePlayer = False
		playerDict = {}
		for aName in _names :
			funcRef, scrName = _builder.get( aName, [ None, "" ] )
			if None != funcRef :
				funcRef( aRow, playerDict, aName, scrName )

		# if either names is empty ignore the record
		if playerDict[ 'first' ] == '' or playerDict[ 'last' ] == '' :
			ignorePlayer = True

		if not ignorePlayer :
			if options.csv :
				playerList.append( playerDict )
			else :
				try :
					print playerDict[ 'number' ], "%s, %s" % ( playerDict[ 'last' ], playerDict[ 'first' ], )
				except ( UnicodeError, UnicodeEncodeError ) as exCode :
					traceback.print_exc()
					print playerDict
				except Exception as exCode :
					print "Something went wrong but it's not unicode!!"
					traceback.print_exc()

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
			else :
				# stash the status somewhere and add it to every player
				status = cleanMsg( aSection )
				if status in _statusMap :
					global _status
					_status = _statusMap[ status ]
				else :
					print 'Unknown status: ', status
					_status = 'ACT'

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
	import codecs
	sys.stdout = codecs.getwriter( 'utf8' )( sys.stdout )

	options, url = doOptions()

	#import ipdb ; ipdb.set_trace()
	download( url, options )


if __name__ == '__main__':
	main()


