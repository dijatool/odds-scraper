#!/usr/bin/env python

#
#	Pull apart bloomberg articles
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
	print url
	print

	#dumpDivsIdClass( soup )
	#dumpDivs( soup )

	meta = soup.findChild( 'div', { 'id' : 'story_meta' })
	try :
		author = meta.findChild( 'span', { 'class' : 'last' })
		print author.getText( " " )
	except :
		pass

	try :
		timestamp = meta.findChild( 'span', { 'class' : 'datestamp' })
		print timestamp.getText( " " )
	except :
		pass

	print

	# grab the text and print all the paragraphs
	text = soup.findChild( None, { 'id' : 'story_display' })

	if None == text :
		text = soup.findChild( None, { 'id' : 'story_body' })

	paras = text.findAll()
	for p in paras :
		if 'p' == p.name[0] or 'h' == p.name[0] :
			print cleanText( p.getText( " " ))
			print
		li = p.findChildren( 'li' )
		if None != li :
			for anItem in li :
				print "o %s" % cleanText( anItem.getText( " " ))
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


