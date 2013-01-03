#!/usr/bin/env python

import urllib2
import os
import sys
import string
import re

from BeautifulSoup import BeautifulSoup as bs


def cleanMsg( obj ) :
	'''
		Take the object and strip everything to make it clean text

		Should probably add a flag and a slow way to strip for articles... I'm mangling biggies stuff

	'''
	return ''.join( bs( str( obj )).findAll( text=True )).strip()


def doArticleComments( soup ) :
	'''
		Gather all the data from a page of comments...

	'''
	commentBlock = soup.findChild( None, { "class" : "cms_none_comments" })

	commentRows = commentBlock.findAll( None, { "class" : "cms_comments_mainbox postcontainer" })
	for i, commentRow in enumerate( commentRows ) :

		userObj = commentRow.findChild( None, { "class" : "username" })
		user = userObj.findChild( text=True )
 		print user

		dateObj = commentRow.findChild( None, { "class" : "postdate" })
		date = dateObj.findChild( text=True )
 		print date ; print

 		# brute force strip all HTML data from message for now
		msgObj = commentRow.findChild( None, { "class" : "posttext restore" })
		msg = ''.join( bs( str( msgObj ) ).findAll( text=True )).strip()
		print msg.encode( 'ascii', 'ignore' )

		print " =============================="


def doThreadComments( soup ) :
	'''
		doThreadComments needs a description...

	'''
	commentBlock = soup.findChild( None, { "class" : "posts" })
	commentRows = commentBlock.findAll( None, { "class" : "postbit postbitim postcontainer old" })
	for i, commentRow in enumerate( commentRows ) :
		# print commentRow
		userObj = commentRow.findChild( None, { "class" : "popupmenu memberaction" })
		poster = userObj.findChild( None, { "class" : re.compile( 'username' ) } )
		poster = cleanMsg( poster )

		date = cleanMsg( commentRow.findChild( None, { "class" : "date" }))
		date = date.replace( "&nbsp;", " " )

		print poster
		print date
		print

		# brute force strip all HTML data from message for now
		msgObj = commentRow.findChild( None, { "class" : "postcontent restore" })
		msg = ''.join( bs( str( msgObj ) ).findAll( text=True )).strip()
		print msg.encode( 'ascii', 'ignore' )

		print " =============================="


def doArticle( url, soup ) :
	'''
		Extract the article information

	'''
	articleTitle = soup.findChild( None, { "class" : "article_width" }).findChild( None, { "class" : "title" })
	print cleanMsg( articleTitle )

	# the poster lives in a changing environment
	# just find a class with username inside the other elements
	articlePosterObj = soup.findChild( None, { "class" : "article_username_container_full" }).findChild( None, { "class" : "popupmenu memberaction" })
	poster = articlePosterObj.findChild( None, { "class" : re.compile( 'username' ) } )
	print cleanMsg( poster )

	articleDateObj = soup.findChild( None, { "class" : " article_username_container " })
	print cleanMsg( articleDateObj )
	print

	articleContentObj = soup.findChild( None, { "class" : "article cms_clear restore postcontainer" })
	articleMsg = cleanMsg( articleContentObj )
	print articleMsg.encode('ascii', 'ignore')
	print " =============================="
	print " =============================="

	# debug ... need a better cleaning mechanism for the main article
	# lists are causing all the issues!!
	# 	print articleContentObj
	# 	print " =========="

	# how many pages?
	pageInfo = soup.findChild( None, { "class" : "comments_page_nav_css" }).findChild( None, { "class" : "popupctrl" })
	pageText = cleanMsg( pageInfo )
	pageInfo = re.findall( r'\b\d+\b', pageText )
	try :
		pageCount = int( pageInfo[1] )
	except IndexError :
		pageCount = 1

	doArticleComments( soup )

	if pageCount > 1 :
		thisPage = 1
		while thisPage < pageCount :
			thisPage += 1
			newUrl = "%s?page=%s" % ( url, thisPage )
			soup = loadPage( newUrl )
			doArticleComments( soup )


def doThread( url, soup ) :
	'''
		Extract all the comments in a thread and handle additional pages.

	'''
	titleObj = soup.findChild( None, { "class" : "threadtitle" })
	print cleanMsg( titleObj )

	pageInfo = soup.findChild( None, { "class" : "pagination_top" }).findChild( None, { "class" : "popupctrl" })
	pageText = cleanMsg( pageInfo )
	pageInfo = re.findall( r'\b\d+\b', pageText )
	try :
		pageCount = int( pageInfo[1] )
	except IndexError :
		pageCount = 1

	print
	doThreadComments( soup )

	if pageCount > 1 :
		thisPage = 1
		while thisPage < pageCount :
			thisPage += 1
			newUrl = "%s?page=%s" % ( url, thisPage )
			soup = loadPage( newUrl )
			doThreadComments( soup )


def loadPage( url ) :
	'''
		Given a url returns a soup object

	'''
	opener = urllib2.build_opener()
	link = opener.open( url )
	page = link.read()
	soup = bs( page )

	return soup


#
# Handle scraping from Football Pro's Articles section
#

def download( url ) :
	'''
		Pull the page and parse it into the pieces we need.
	'''

	urlFragment = "showthread.php"
	soup = loadPage( url )

	if not urlFragment in url :
		doArticle( url, soup )
	else :
		doThread( url, soup )




def main() :
	'''
		Make sure we have a url and then go do something useful
	
	'''
	if len( sys.argv ) < 2 :
		import os

		appName = os.path.basename( sys.argv[ 0 ] )
		print "\tUsage:", appName, "url to scrape"
	else :
		url = sys.argv[ 1 ]
		download( url )


if __name__ == '__main__':
	main()

