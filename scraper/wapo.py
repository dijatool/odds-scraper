#!/usr/bin/env python

#
#	Grad WaPo pieces by re-writing the URL and grabbing the data.
#

import os
import urllib2
import cookielib
try :
	from bs4 import BeautifulSoup as bs
except :
	from BeautifulSoup import BeautifulSoup as bs

from misc import cleanText

kCookieFile = '/tmp/cookies/cookies.lwp'


def download( url ) :
	'''
		Pull the page and parse it into the pieces we need.
	'''

	url = url.replace( '_story', '_print' )

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
		author = soup.findChild( 'span', { 'class' : 'author vcard' })
		print author.getText( " " )
	except :
		pass

	try :
		timestamp = soup.findChild( 'span', { 'class' : 'timestamp' })
		print timestamp.getText( " " )
	except :
		pass

	print

	# grab the text and print all the paragraphs
	text = soup.findChild( None, { 'id' : 'content' })

	paras = text.findAll()
	for p in paras :
		if 'p' == p.name[0] or 'h' == p.name[0] :
			print cleanText( p.getText( " " )).rstrip()
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


