#!/usr/bin/env python

import urllib2
import os
import sys
import string

from BeautifulSoup import BeautifulSoup as bs

# i wish I knew how to get rid of the tag data, but I don't so we're off to do it manually

_findStrs = [ 'blockquote', 'div', 'b' ]

# removeHtml



#
# Handle scraping from Football Pro's Articles section
#

def download() :
	'''
		Pull the page and parse it into the pieces we need.
	'''
	oddsStr = "(%s)"
	url = "http://footballpros.com/content.php/1797-FP-Upset-Special-Challenge-Our-Scrubs-Are-Better-Than-Your-Scrubs-Edition-PS-Week-4"
	opener = urllib2.build_opener()
	link = opener.open( url )
	page = link.read()
	soup = bs( page )

	commentBlock = soup.findChild( None, { "class" : "cms_none_comments" })
	commentRows = commentBlock.findAll( None, { "class" : "cms_comments_mainbox postcontainer" })
	for i, commentRow in enumerate( commentRows ) :

		userObj = commentRow.findChild( None, { "class" : "username" })
		user = userObj.findChild( text=True )
 		print user, ":"
		msgObj = commentRow.findChild( None, { "class" : "posttext restore" })
		msg = ''.join( bs( str( msgObj ) ).findAll( text=True ))
		msg = msg.strip()
		print msg

		print " =========="


if __name__ == '__main__':
	download()


