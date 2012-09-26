#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib2
# import os
# import sys
# import string
# import re

from BeautifulSoup import BeautifulSoup as bs

import odds


def main() :
	'''
		Pull the page and parse it into the pieces we need.
	'''
	url = "http://www.oddsshark.com/nfl/odds"
	#url = "http://localhost/odds.html"
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


if __name__ == '__main__':
	main()


