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


def cleanTimeStamp( stampText ) :
	'''
		cleanTimeStamp needs a description...

	'''
	timestamp = stampText.getText( " " ).lstrip().rstrip()
	timestamp = timestamp.replace( "&nbsp;", "" )
	items = timestamp.split( '|' )
	timestamp = items[ 0 ].rstrip()

	return timestamp


def cleanAuthor( authorText ) :
	'''
		cleanAuthor needs a description...

	'''
	paras = authorText.findAll()
	author = paras[ 1 ]
	author = author.getText( " " ).lstrip().rstrip()
	return author


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

	try :
		author = soup.findChild( 'div', { 'id' : 'ody-byline-written-by' })
		print cleanAuthor( author )

		timestamp = soup.findChild( 'div', { 'class' : 'ody-arttime' })
		print cleanTimeStamp( timestamp )

		print
	except :
		pass


	# grab the text and print all the paragraphs
	text = soup.findChild( None, { 'class' : 'gel-content' })

	paras = text.findAll()
	#paras = text.findAll( 'p' )
	for p in paras :
		if 'p' == p.name[0] or 'h' == p.name[0] :
			outText = cleanText( p.getText( " " )).rstrip()
			if len( outText ) > 0 :
				print outText
				print

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


