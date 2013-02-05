#!/usr/bin/env python

#
#	Pull a CHTV posting and all the comments.
#
# 	I'm just tired of green
#

import os
import urllib2
import cookielib

from BeautifulSoup import BeautifulSoup as bs
from BeautifulSoup import NavigableString as ns

from misc import cleanText

kCookieFile = '/tmp/cookies/cookies.lwp'


def printEndLine() :
	'''
		printEndLine needs a description...
	
	'''
	print "----------------"


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

	# grab the text and print all the paragraphs
	top = soup.findChild( None, { 'id' : 'content' })

	text = soup.findChild( None, { 'class' : 'entry clearfix' })

	paras = text.findAll()
	for p in paras :
		if 'p' == p.name[ 0 ] or 'h' == p.name[ 0 ] :
			print cleanText( p.getText( " " ))
			print
		li = p.findChildren( 'li' )
		if None != li :
			for anItem in li :
				print "o %s" % cleanText( anItem.getText( " " ))
				print
	printEndLine()

	# comments
	comments = top.findChildren( None, { 'class' : 'comment-body' })
	for aComment in comments :
		author = aComment.findChild( None, { 'class' : 'comment-author vcard' }).getText( " " ).rstrip()
		author = author.lstrip()
		date = aComment.findChild( None, { 'class' : 'comment-meta commentmetadata' }).getText( " " ).rstrip()
		print "On ", date
		print author
		print

		for p in aComment :
			if not isinstance( p, ns ) :
				if 'p' == p.name[ 0 ] :
					print cleanText( p.getText( " " ))
					print
		printEndLine()

#	cookieJar.save( kCookieFile )


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
		urlParts = url.split( "?" )
		url = urlParts[ 0 ]
		download( url )


if __name__ == '__main__':
	main()


