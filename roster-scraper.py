#!/usr/bin/env python

import urllib2
import os
import sys
import string
import re
from BeautifulSoup import BeautifulSoup as bs

# Run like so...
#
#	~/github/local/odds-scraper/roster-scraper.py > /tmp/packers-roster-plain.txt
#	md5 /tmp/packers-roster-plain.txt
#


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


def download( url ) :
	'''
		Pull the page and parse it into the pieces we need.
	'''
	loopRegEx = re.compile( ' loop-' )		# each row has the class tag ' loop-*'

	soup = loadPage( url )
	mainBodyObj = soup.findChild( None, { "class" : "game-roster-large" }).findChild( None, { "class" : "bd" })

	# find the sections...
	sections = mainBodyObj.findAll( None, { "class" : "mod-title-nobackground" })
	for i, aSection in enumerate( sections ) :
		print cleanMsg( aSection )
		# now get at the table stuff just below each section...
		aTable = aSection.findNextSibling( 'table' )
		rows = aTable.findChildren( 'tr', { "class" : loopRegEx })
		for aRow in rows :
			# print aRow
			name = aRow.findChild( 'td', { "class" : "col-name" })
			number = aRow.findChild( 'td', { "class" : "col-jersey" })
			print cleanMsg( number ), cleanMsg( name )
		print


def main() :
	'''
		Go do something useful.

	'''
	url = "http://www.packers.com/team/players.html"
	download( url )


if __name__ == '__main__':
	main()

