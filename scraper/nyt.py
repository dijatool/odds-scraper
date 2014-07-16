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

	print title
	print
	print url
	print

	author = soup.findChildren( None, { 'class' : 'byline' })
	if author is not None :
		try :
			print cleanText( author[ 0 ].getText( " " ))
		except :
			pass
	date = soup.findChildren( None, { 'class' : 'dateline' })
	if date is not None :
		print cleanText( date[ 0 ].getText( " " ))
	print

	# should find a better starting point... past the end of the first group of items...
	moreItems = soup.findChildren( None, { 'itemprop' : 'articleBody' })
	if None != moreItems :
		for anItem in moreItems :
			if 'p' == anItem.name[0] or 'h' == anItem.name[0] :
				print cleanText( anItem.getText( " " ))
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
		download( url )


if __name__ == '__main__':
	main()


