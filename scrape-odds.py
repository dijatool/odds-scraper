#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib2

from BeautifulSoup import BeautifulSoup as bs

import odds


def main() :
	'''
		Pull the page and parse it into the pieces we need.
	'''
	from optparse import OptionParser

	usage = "%prog [options]"
	parser = OptionParser( usage = usage )
	parser.add_option( "-e", "--extendedOdds", dest="extendedOdds", default = False,
						action="store_true",
						help="Determine if we show all the extra data." )

	( options, args ) = parser.parse_args()

	url = "http://www.oddsshark.com/nfl/odds"
 	# url = "http://localhost/odds.html"
	opener = urllib2.build_opener()
	link = opener.open( url )
	page = link.read()
	soup = bs( page )

	print "Opening odds..."
	opening = odds.openingOdds( soup )
	for theOdds in opening :
		print theOdds

	print; print "Current odds..."
	current = odds.currentOdds( soup )
	for theOdds in current :
		print theOdds

	if options.extendedOdds :
		print
		print ; print "Current odds FP formatted..."
		for theOdds in current :
			print theOdds.gameWithOddsForFp()
		print
		for theOdds in current :
			print theOdds.dogAndPoints()
		print
		for theOdds in current :
			print theOdds.homeAndPoints()


if __name__ == '__main__':
	main()


