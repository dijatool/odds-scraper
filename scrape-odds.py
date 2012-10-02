#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib2
# import os
# import sys
# import string
# import re

from BeautifulSoup import BeautifulSoup as bs

import odds


def printFpOdds( oddsList ) :
	'''
		printFpOdds needs a description...

	'''
	for theOdds in oddsList :
		print theOdds.oddsLineForFp()


def main() :
	'''
		Pull the page and parse it into the pieces we need.
	'''
	from optparse import OptionParser

	usage = "%prog [options]"
	parser = OptionParser( usage = usage )
	parser.add_option( "-g", "--genOddsText", dest="genOddsText", default = False,
						action="store_true",
						help="Determine if we generate text for pasting into the FP story" )
	( options, args ) = parser.parse_args()

	url = "http://www.oddsshark.com/nfl/odds"
	#url = "http://localhost/odds.html"
	opener = urllib2.build_opener()
	link = opener.open( url )
	page = link.read()
	soup = bs( page )

	print "Opening odds..."
	opening = odds.openingOdds( soup )
	if not options.genOddsText :
		for theOdds in opening :
			print theOdds
	else :
		printFpOdds( opening )

	print; print "Current odds..."
	current = odds.currentOdds( soup )
	if not options.genOddsText :
		for theOdds in current :
			print theOdds
	else :
		printFpOdds( current )


if __name__ == '__main__':
	main()


