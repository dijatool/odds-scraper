#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
#	Pull apart press gazette articles as their firewall has made this a
#	giant PIA
#

import os
import urllib2
import cookielib
from BeautifulSoup import BeautifulSoup as bs

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
	print
	print title
	print

	# grab the text and print all the paragraphs
	text = soup.findChild( None, { 'class' : 'gel-content' })
	paras = text.findAll( 'p' )
	for p in paras :
		print cleanText( p.getText( " " ))

	# cookieJar.save( kCookieFile )


def main() :
	'''
		Make sure we have a url and then pull the page and parse it into the
		pieces we need.

	'''
	import sys
	# fix my unicode errors on pipes
	# it works but I'm not sure if I'm going to use it
	# import codecs
	# sys.stdout = codecs.getwriter( 'utf8' )( sys.stdout )

	if len( sys.argv ) < 2 :
		appName = os.path.basename( sys.argv[ 0 ] )
		print "\tUsage:", appName, "url to scrape"
	else :
		url = sys.argv[ 1 ]
		download( url )


if __name__ == '__main__':
	main()


