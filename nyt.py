#!/usr/bin/env python

#
#	Pull apart full NYTimes articles.
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
	items = soup.findChildren( None, { 'class' : 'articleBody' })
	for anItem in items :
		paras = anItem.findAll()
		for p in paras :
			if 'p' == p.name[0] or 'h' == p.name[0] :
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
		urlParts = url.split( "?" )
		if len( urlParts ) < 2 :
			urlParts.append( "pagewanted=all" )
		else :
			urlParts[ 1 ] = "pagewanted=all"
		#print url
		#print urlParts
		url = "?".join( urlParts )
		print url
		print
		download( url )


if __name__ == '__main__':
	main()


