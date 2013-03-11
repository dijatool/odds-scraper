#!/usr/bin/env python

import urllib2
import os
import sys
import string
import re

from BeautifulSoup import BeautifulSoup as bs


kUrlBase = "http://www.nfl.com"


def loadSoup( url ) :
	'''
		Given a url returns a soup object

	'''
	opener = urllib2.build_opener()
	link = opener.open( url )
	page = link.read()
	soup = bs( page )

	return soup


def loadPage( url ) :
	'''
		Given a url returns a page object

	'''
	opener = urllib2.build_opener()
	link = opener.open( url )
	page = link.read()

	return page


def findGameBookLink( url ) :
	'''
		findGameBookLink needs a description...

	'''
	import StringIO
	import re

	bookLink = None

	bookSrch = re.compile( "gamebook" )
	
	done = False
	while not done :
		try :
			page = loadPage( url )
			done = True
		except :
			pass
			# deal with IncompleteRead exceptions from NFL.com.... just keep trying.

	buf = StringIO.StringIO( page )
	for aLine in buf :
		aLine = aLine.strip()
		if bookSrch.search( aLine ) :
			chunks = aLine.split( "'" )
			bookLink = "%s%s" % ( kUrlBase, chunks[ 1 ] )
			break

	return bookLink


def parsePage( url, formatStr = None ) :
	'''
		Pull the page and parse it into the pieces we need.
	'''
	soup = loadSoup( url )

	gamesList = soup.findChildren( None, { 'class' : 'game-center-area' })
	for aGame in gamesList :
		link = aGame.findChild( 'a', { 'class' : 'game-center-link' })
		link = "%s%s" % ( kUrlBase, link[ 'href' ] )
		bookLink = findGameBookLink( link )
		print bookLink


def main() :
	'''
		Make sure we have a url and then go do something useful

	'''
	formatStr = ""

	from optparse import OptionParser

	usage = "%prog [options] url"
	parser = OptionParser( usage = usage )
	( options, args ) = parser.parse_args()

	if len( sys.argv ) < 2 :
		import os

		appName = os.path.basename( sys.argv[ 0 ] )
		print "  Usage:", appName, '"url to scrape"'
	else :
		#formatStr = options.format
		url = args[ 0 ]
		parsePage( url, formatStr )


if __name__ == '__main__':
	main()


