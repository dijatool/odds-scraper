#!/usr/bin/env python
# -*- coding: utf-8 -*-


import string
import urllib2

from BeautifulSoup import BeautifulSoup as bs

from odds import teamsTranslate
from misc import cleanText

from datetools import convertDateTimeStr	#, convertDateStr

#
#	The page is gzip'd, just a reminder
#

try:
    from io import BytesIO as _StringIO
except ImportError:
    try:
        from cStringIO import StringIO as _StringIO
    except ImportError:
        from StringIO import StringIO as _StringIO


def fixOddsStr( oddsStr ) :
	'''
		Replace instances anything that causes issues...
			"&frac12;" with ".5"
			etc
	'''
	odds = string.replace( oddsStr, u'&frac12;', ".5" )
	odds = string.replace( odds, u'½', ".5" )
	odds = string.replace( odds, u'PK', "0" )
	return odds.strip()


def fixOdds( awayOdds, homeOdds ) :
	'''
		fixOdds needs a description...

	'''
	awayOdds = cleanText( fixOddsStr( awayOdds ))
	homeOdds = cleanText( fixOddsStr( homeOdds ))
	if '-' == awayOdds[ 0 ] :
		awayOdds = awayOdds.split( " " )[0]
		homeOdds = awayOdds[ 1 : ]
	else :
		homeOdds = homeOdds.split( " " )[0]
		awayOdds = homeOdds[ 1 : ]

	return awayOdds, homeOdds


def doOptions() :
	'''
		doOptions needs a description...

	'''
	from optparse import OptionParser

	url = "http://www.vegasinsider.com/nfl/odds/las-vegas/"

	usage = "%prog [options]"
	parser = OptionParser( usage = usage )
	parser.add_option( "-e", "--extendedOdds", dest="extendedOdds", default = False,
						action="store_true",
						help="Determine if we show all the extra data." )
	parser.add_option( "-f", "--fp", dest="fpOdds", default = False,
						action="store_true",
						help="Should we print FP formatted odds?" )
	parser.add_option( "-d", "--dogs", dest="dogs", default = False,
						action="store_true",
						help="Should we dump the underdogs?" )

	parser.add_option( "-u", "--url", dest="url", default = None,
						help="Override for the url" )

	( options, args ) = parser.parse_args()

	if options.url :
		url = options.url
		print url

	return options, url


def getDateStr( dt ) :
	'''
		getDateStr needs a description...

	'''
	return dt.strftime( '%Y-%m-%d %H:%M' )


def fixDate( dateIn ) :
	'''
		fixDate needs a description...

		this hack is going to need fixing asap
	'''
	parts = dateIn.split( '  ' )
	theDate, theTime = parts[ 0 ], parts[ 1 ]
	parts[ 0 ] = '2013/%s' % theDate
	dt = convertDateTimeStr( ' '.join( parts ))
	return dt


def dumpPage( page, options ) :
	'''
		Parse the page into the pieces we need.

			td class="viBodyBorderNorm"
			find the second table...
				find all the tr's

	'''
	soup = bs( page )

	mainTable = soup.findChild( 'td', { "class" : "viBodyBorderNorm" })
	tables = mainTable.findAll( 'table' )

	oddsTable = tables[ 1 ]

	rows = oddsTable.findAll( 'tr' )

	oddsOut = []

	for aRow in rows :
		try :
			dates = aRow.findChildren( 'span', { 'class' : 'cellTextHot' })
			teams = aRow.findChildren( 'a', { "class" : "tabletext" })
			if None != teams and len( teams )  > 0 :

				gamedate = fixDate( dates[ 0 ].getText())

				visitor = teams[ 0 ].getText( " " )
				home = teams[ 1 ].getText( " " )
				( visitor, home ) = teamsTranslate( visitor, home )

				# find the proper column
				cols = aRow.findAll( 'td' )

				homeOdds = ""
				visitorOdds = ""

				try :
					viOdds = cols[ 2 ].findChild( 'a' )
					odssItems = viOdds.getText( "|" ).split( "|" )
					awayOdds, homeOdds = fixOdds( odssItems[ 1 ], odssItems[ 2 ] )
					visitorOdds = '-%s' % homeOdds
					if homeOdds[ 0 ] == '-' :
						visitorOdds = visitorOdds[ 2 : ]
				except :
					pass

				oddsOut.append(( gamedate, visitor, visitorOdds, home, homeOdds ))


		except Exception as ex :
			print "We had an exception!", ex

	lastDay = -1
	for aRow in oddsOut :
		gamedate, visitor, visitorOdds, home, homeOdds = aRow
		if gamedate.day != lastDay :
			print
			lastDay = gamedate.day
		dateStr = getDateStr( gamedate )
		if len( visitorOdds ) :
			outs = ''
			if options.fpOdds :
				if visitorOdds[0] == '-' :
					outs = '%s  %s @ %s (+%s)' % ( dateStr, visitor, home, homeOdds )
				else :
					outs = '%s  %s (+%s) @ %s' % ( dateStr, visitor, visitorOdds, home )
			else :
				outs = '%s  %s @ %s %s' % ( dateStr, visitor, home, homeOdds )
			print outs

	if options.extendedOdds :
		print
		print 'Odds FP formatted...'

		lastDay = -1

		for aRow in oddsOut :
			gamedate, visitor, visitorOdds, home, homeOdds = aRow
			if gamedate.day != lastDay :
				print
				lastDay = gamedate.day
				print gamedate.strftime( '%a %b %d' )
				print

			if len( visitorOdds ) :
				post = ''
				try :
					val = float( homeOdds )
					if val < 0 :
						val = val * -1
					#print val
					if val < 3 :
						post = ' XXX'
				except :
					pass

				if visitorOdds[0] == '-' :
					outs = '[*]%s @ [b]%s (+%s)[/b]' % ( visitor, home, homeOdds )
				else :
					outs = '[*][b]%s (+%s)[/b] @ %s' % ( visitor, visitorOdds, home )
				if len( post ) :
					outs = '%s%s' % ( outs, post )
				print outs

		print
		print 'Here for editing purposes only...'
		print
		print '[*]No Game Qualifies'
		print

	if options.dogs :
		print
		print 'Information for the sheet'
		print

		for aRow in oddsOut :
			gamedate, visitor, visitorOdds, home, homeOdds = aRow
			dog = None
			dogOdds = None
			val = float( homeOdds )
			if val <= 0 :
				dog, dogOdds = visitor, visitorOdds
			else :
				dog, dogOdds = home, homeOdds
			if dogOdds[ 0 ] == '-' :
				dogOdds = dogOdds[ 1 : ]
			print dog, dogOdds


def main() :
	'''
		Pull the page and parse it into the pieces we need.

			td class="viBodyBorderNorm"
			find the second table...
				find all the tr's

	'''
	options, url = doOptions()

	opener = urllib2.build_opener()
	response = opener.open( url )

	page = None

	if response.info().get( 'Content-Encoding' ) == 'gzip' :
		import gzip
		f = gzip.GzipFile( fileobj=_StringIO( response.read() ))
		page = f.read()
	else :
		page = response.read()

	dumpPage( page, options )


if __name__ == '__main__':
	main()


