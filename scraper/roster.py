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
	"Active/Non-Football Illness" : 'NFI',
	"Active/Non-Football Injury" : 'NFI',
	"Reserve/Non-Football Illness" : 'NFI',
	"Reserve/Non-Football Injury" : 'NFI',
	"Reserve/Suspended by Club" : 'SUC',
	"Reserve/Suspended by Commissioner" : 'SUS',
	"Reserve/Retired" : 'RET',
	"Reserve/Left Squad" : 'LS',
	"Reserve/Did Not Report" : 'DNR',
	"Reserve/Future" : 'FUT',
	"RESERVE/FUTURE" : 'FUT',
	"Waivers/No Recall" : 'WAV',		# a new wrinkle by the Chiefs...
	"Cut" : 'WAV',						# a new wrinkle by the Chiefs...
	# there will likely be other variants too...
	"Exempt" : 'ECP',					# Exempt Commissioner Permission
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

_namesAdd = [
	u'image',
	]

_namesV2 = _names + _namesAdd


def cleanMsg( obj ) :
	'''
		Take the object and strip everything to make it clean text
	'''
	return ''.join( bs( str( obj )).findAll( text = True )).strip()


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

	# sometimes extra commas show up (Jr's and so forth or just bad data)
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


def resetStatus() :
	'''
		resetStatus needs a description...

	'''
	global _status
	_status = 'ACT'


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
	data = heightFix( data )
	if None is data :
		data = u''

	destDict[ destName ] = data


def nameFix( destDict, sourceName ) :
	'''
		Clean up the name data and stick it into first and last

	'''
	names = sourceName.split( ',' )

	# sometimes extra commas show up (Jr's and so forth or just bad data)
	# eat them until only two name chunks remain
	while len( names ) > 2 :
		names[ 0 ] = '%s,%s' % ( names[ 0 ], names[ 1 ] )
		del names[ 1 ]

	first = names[ 1 ].rstrip().lstrip()
	destDict[ u'first' ] = first
	last = names[ 0 ].rstrip().lstrip()
	destDict[ u'last' ] = last


def heightFix( strHeight ) :
	'''
		Some teams just can't get the basics right ....

			like 6'2 instead of 6-2

		Must be cleaned up to move to an integer representation

	'''
	strHeight = strHeight.replace( '"', '' )
	# call it the cowboys rule ... jesus
	strHeight = strHeight.replace( ' ', '' )
	if strHeight.find( "'" ) > 0 :
		strHeight = strHeight.replace( "'", '-' )

	if strHeight.find( "-" ) > 0 :
		hInfo = strHeight.split( '-' )
		height = 12 * int( hInfo[ 0 ] ) + int( hInfo[ 1 ] )
		strHeight = unicode( height )

	try :
		intHeight = int( strHeight )
	except :
		intHeight = 0

	if intHeight < 48 :
		strHeight = None

	return strHeight


def updateStatus( status ) :
	'''
		Update the global _status (it's dumb but simple)

	'''
	if status in _statusMap :
		global _status
		_status = _statusMap[ status ]
	else :
		print 'Unknown status: ', status
		_status = 'ACT'


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


# no buildr yet for the Cowboys style page ... not sure if we're doing it


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

	def _v2OutputName( options ) :
		'''
			adjust the output name when doing a V2 kind of record

		'''
		import re
		ending = re.compile( r'.csv$' )
		if ending.search( options.csvFile ) :
			options.csvFile = ending.sub( '-v2.csv', options.csvFile )
		else :
			options.csvFile = '%s-v2.csv' % options.csvFile


	global _baseUrl
	parseUrl = urlparse.urlparse( url )
	_baseUrl = '%s://%s' % ( parseUrl.scheme, parseUrl.netloc )

	playerList = []
	resetStatus()		# this is pretty bogus

	strBuffer = StringIO.StringIO()
	writer = unicodecsv.writer( strBuffer, quoting = unicodecsv.QUOTE_ALL )
	dictWriter = unicodecsv.DictWriter( strBuffer, _names, quoting = unicodecsv.QUOTE_ALL )

	soup = loadPage( url )
	try :
		mainBodyObj = soup.findChild( None, { "class" : "game-roster-large" }).findChild( None, { "class" : "bd" })

		# find the sections...
		sections = mainBodyObj.findAll( None, { "class" : "mod-title-nobackground" })

		if len( sections ) > 1 :
			for aSection in sections :
				if not options.csv :
					print cleanMsg( aSection )
				else :
					# stash the status somewhere and add it to every player
					updateStatus( cleanMsg( aSection ))

				# now get at the table stuff just below each section...
				aTable = aSection.findNextSibling( 'table' )
				playerData( aTable, playerList, options )
		else :
			# miami and the bucs do things differently
			aTable = mainBodyObj.findChild( 'table' )
			playerData( aTable, playerList, options )

		if options.csv :
			playerList.sort( key = itemgetter( 'last', 'first' ))
			if options.outputToFile :
				myfile = open( options.csvFile, mode = 'w' )
				fileWriter = unicodecsv.DictWriter( myfile, _names, quoting = unicodecsv.QUOTE_ALL )
				fileWriter.writeheader()
				for aPlayer in playerList :
					fileWriter.writerow( aPlayer )
				myfile.close()

			else :
				print toCsvRow( writer, strBuffer, _names )
				for aPlayer in playerList :
					print toCsvRow( dictWriter, strBuffer, aPlayer )

	except :
		# teams are moving to a new format ...
		# should try a second approach with the data

		# the section titles live at field--name-field-roster-status (inside h2 class pane-title)
		# the data lives inside each <tbody>
		# now moved to just before the table itself

		import re

		topSearch = re.compile( r'\b%s\b' % 'view-player-roster' )
		rosterWrapper = soup.findChild( 'div', { 'class' : topSearch })

		#doIt = False
		## DEBUG ##
		doIt = True

		if doIt :
			tabs = rosterWrapper.findChildren( 'table' )
			for aTab in tabs :
				#caption = aTab.findChild( 'caption' )
				caption = aTab.findPreviousSibling( 'h2', { 'class' : 'pane-title' })
				caption = cleanMsg( caption )
				updateStatus( caption )

				body = aTab.findChild( 'tbody' )
				rows = body.findChildren( 'tr' )
				for aRow in rows :

					def _grabData( destDict, tagObj, fieldName, dest ) :
						'''
							Gather data from inside various field names ...
							it is very repetitive

							# <div class=" ... field--name-field-XXXXXXXX ...." ... >

						'''
						srch = re.compile( r'\bfield--name-field-%s\b' % fieldName )
						data = tagObj.findChild( 'div', { 'class' : srch })
						destDict[ dest ] = cleanMsg( data )

					player = {}

					searchPlayerData = re.compile( r'\b%s\b' % 'field--name-field-player' )
					data = aRow.findChild( 'div', { 'class' : searchPlayerData })
					dataLink = data.findChild( 'a' )
					player[ 'link' ] = _baseUrl + dataLink[ 'href' ]
					player[ 'image' ] = dataLink[ 'data-player-image' ]
					nameFix( player, cleanMsg( data ))

					if player[ 'first' ] != '' and player[ 'last' ] != '' :
						_grabData( player, aRow, 'position', 'position' )
						_grabData( player, aRow, 'height', 'height' )
						player[ 'height' ] = heightFix( player[ 'height' ] )
						_grabData( player, aRow, 'weight', 'weight' )
						_grabData( player, aRow, 'birthday', 'age' )
						_grabData( player, aRow, 'experience', 'exp' )
						_grabData( player, aRow, 'jersey-number', 'number' )
						_grabData( player, aRow, 'college', 'college' )
						getStatus( aRow, player, 'status', None )

						playerList.append( player )

			playerList.sort( key = itemgetter( 'last', 'first' ))

			dictWriter = unicodecsv.DictWriter( strBuffer, _namesV2, quoting = unicodecsv.QUOTE_ALL )
			if options.csv :
				playerList.sort( key = itemgetter( 'last', 'first' ))
				if options.outputToFile :
					_v2OutputName( options )
					myfile = open( options.csvFile, mode = 'w' )
					fileWriter = unicodecsv.DictWriter( myfile, _namesV2, quoting = unicodecsv.QUOTE_ALL )
					fileWriter.writeheader()
					for aPlayer in playerList :
						fileWriter.writerow( aPlayer )
					myfile.close()
			else :
				print toCsvRow( writer, strBuffer, _namesV2 )
				for player in playerList :
					print toCsvRow( dictWriter, strBuffer, player )

		## DEBUG ##
		##
		## need to find a way to fold the two together
		## the sticking point is the name list passed to the CSV methods
		##
		## DEBUG ##

		pass


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


