#!/usr/bin/env python

#
#	Pull apart full Grantland articles.
#
#	python ~/github/local/odds-scraper/grantland.py url
#	python ~/github/local/odds-scraper/grantland.py http://www.grantland.com/story/_/id/8914700/ed-obannon-vs-ncaa
#
#

import os
import urllib2
import cookielib
from bs4 import BeautifulSoup as bs

from misc import cleanText

kCookieFile = '/tmp/cookies/cookies.lwp'


def download( url ) :
	'''
		Pull the page and parse it into the pieces we need.
	'''
	cookieJar = cookielib.LWPCookieJar()
	if os.path.isfile( kCookieFile ) :
		cookieJar.load( kCookieFile )
	else :
		cookieJar.save( kCookieFile )
	opener = urllib2.build_opener( urllib2.HTTPCookieProcessor( cookieJar ))

	link = opener.open( url )

	page = link.read()
	soup = bs( page )

	title = cleanText( soup.findChild( 'title' ).text )

	print title
	print
	print url
	print

	items = soup.findChildren( None, { 'class' : 'wrapper content' })

	# grab the text and print all the paragraphs
	# a special tag called article has some stuff we might want at some point
	for anItem in items :
		paras = anItem.findAll()
		for p in paras :
			#if 'p' == p.name[0] or 'h' == p.name[0] :
			if 'p' == p.name[0] :
				print cleanText( p.getText( " " ))
				print

#	cookieJar.save( kCookieFile )


def main() :
	'''
		Make sure we have a url and then pull the page and parse it into the
		pieces we need.

	'''
	import sys

	if len( sys.argv ) < 2 :
		appName = os.path.basename( sys.argv[ 0 ] )
		print "\tUsage:", appName, "url to scrape"
	else :
		url = sys.argv[ 1 ]
		download( url )


if __name__ == '__main__':
	main()


