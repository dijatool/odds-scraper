#!/usr/bin/env python
# -*- coding: utf-8 -*-

from odds import teamsTranslate
from misc import cleanText

import string
import urllib2

from BeautifulSoup import BeautifulSoup as bs

#
# 	While debugging...
#
# 	python ~/github/local/odds-scraper/vi.py
#


#
#	So the page is gzip'd, created a quick work around for it
#
#	FeedParser does this well
#
# 	git clone https://code.google.com/p/feedparser/
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
		Replace instances of "&frac12;" with ".5" and trim any excess
	'''
	odds = string.replace( oddsStr, u'&frac12;', ".5" )
	odds = string.replace( odds, u'½', ".5" )
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

	( options, args ) = parser.parse_args()

	return options, url


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
	soup = bs( page )

	mainTable = soup.findChild( 'td', { "class" : "viBodyBorderNorm" })
	tables = mainTable.findAll( 'table' )

	oddsTable = tables[ 1 ]

	rows = oddsTable.findAll( 'tr' )

	oddsOut = []

	for aRow in rows :
		try :
			teams = aRow.findChildren( 'a', { "class" : "tabletext" })
			if None != teams and len( teams )  > 0 :
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

				oddsOut.append(( visitor, visitorOdds, home, homeOdds ))


		except Exception as ex :
			print "We had an exception!", ex

	for aRow in oddsOut :
		visitor, visitorOdds, home, homeOdds = aRow
		if len( visitorOdds ) :
			outs = ''
			if options.fpOdds :
				if visitorOdds[0] == '-' :
					outs = '%s @ %s (+%s)' % ( visitor, home, homeOdds )
				else :
					outs = '%s (+%s) @ %s' % ( visitor, visitorOdds, home )
			else :
				outs = '%s @ %s %s' % ( visitor, home, homeOdds )
			print outs
		
	if options.extendedOdds :
		print
		print 'Odds FP formatted...'
		print

		for aRow in oddsOut :
			visitor, visitorOdds, home, homeOdds = aRow
			if len( visitorOdds ) :
				if visitorOdds[0] == '-' :
					outs = '[*]%s @ [b]%s (+%s)[/b]' % ( visitor, home, homeOdds )
				else :
					outs = '[*][b]%s (+%s)[/b] @ %s' % ( visitor, visitorOdds, home )
				print outs


if __name__ == '__main__':
	main()


