#!/usr/bin/env python


#	python ~/github/local/odds-scraper/scraper/salon.py http://www.salon.com/2013/04/21/idolatry_of_god_author_modern_religion_is_a_macguffin_partner/
#


# @<div class="featuredMedia">

from misc import cleanText


from BeautifulSoup import BeautifulSoup as bs


def toTextWithNewlines( elem ) :
	'''
		toTextWithNewlines needs a description...

	'''
	text = ''
	for e in elem.recursiveChildGenerator() :
		if isinstance( e, basestring ) :
			# this is horrible
			text += e.strip()
		elif e.name == 'br' :
			text += '\n'

	return text


def loadPage( url ) :
	'''
		Given a url returns a soup object

	'''
	import urllib2

	opener = urllib2.build_opener()
	link = opener.open( url )
	page = link.read()

	# eat <br /> items... otherwise they cause issues later
	# import re
	# pattern = re.compile( "<br \/>\n" )
	# page = re.sub( pattern, "", page )

	soup = bs( page )

	return soup


#
# Handle scraping from Football Pro's Articles section
#

def download( url ) :
	'''
		Pull the page and parse it into the pieces we need.
	'''

	soup = loadPage( url )
	# print soup

	title = cleanText( soup.findChild( 'title' ).text )

	print title
	print
	print url
	print

	main = soup.findChild( None, { "class" : "articleContent" })

	paras = main.findAll()
	for p in paras :
		if 'p' == p.name[0] or 'h' == p.name[0] :
			print cleanText( p.getText( ' ' ))
			print


def main() :
	'''
		Make sure we have a url and then go do something useful

	'''
	import os, sys

	if len( sys.argv ) < 2 :
		import os

		appName = os.path.basename( sys.argv[ 0 ] )
		print "\tUsage:", appName, "url to scrape"
	else :
		url = sys.argv[ 1 ]
		download( url )


if __name__ == '__main__':
	main()


