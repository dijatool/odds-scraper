#!/usr/bin/env python

import urllib2
import os
import sys

from BeautifulSoup import BeautifulSoup as bs


def download() :
	'''
		download needs a description...

	'''
	url = "http://www.oddsshark.com/nfl/odds"
	opener = urllib2.build_opener()
	# opener.addheaders = [("User-agent" , "Mozilla/5.0")]
	link = opener.open( url )
	page = link.read()

	soup = bs( page )
	
	#games = soup.findAll( None, { "class" : "game" } )
	#for game in enumerate( games ) :
	#	print game
	
	oddsContainer = soup.findChild( None, { "class" : "odds-tables-container" })
	# print oddsContainer
	oddsRows = oddsContainer.findAll( None, { "class" : "oddsshark-odds-table allodds-odds" })
	for game in enumerate( oddsRows ):
		print game
		print
		print "End of game!"
		print


if __name__ == '__main__':
	download()


