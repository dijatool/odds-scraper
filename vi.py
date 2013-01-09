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


def main() :
	'''
		Pull the page and parse it into the pieces we need.

			td class="viBodyBorderNorm"
			find the second table...
				find all the tr's

	'''
	from optparse import OptionParser

	usage = "%prog [options]"
	parser = OptionParser( usage = usage )
	parser.add_option( "-e", "--extendedOdds", dest="extendedOdds", default = False,
						action="store_true",
						help="Determine if we show all the extra data." )

	( options, args ) = parser.parse_args()

	url = "http://www.vegasinsider.com/nfl/odds/las-vegas/"
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

				try :
					viOdds = cols[ 2 ].findChild( 'a' )
					odssItems = viOdds.getText( "|" ).split( "|" )
					awayOdds, homeOdds = fixOdds( odssItems[ 1 ], odssItems[ 2 ] )
				except :
					pass

				print visitor, "@", home, homeOdds
				oddsOut.append( "%s %s" % ( home, homeOdds ))


		except Exception as ex :
			print "We had an exception!", ex

	print
	print "Home odds"
	print

	for aRow in oddsOut :
			print aRow


if __name__ == '__main__':
	main()


