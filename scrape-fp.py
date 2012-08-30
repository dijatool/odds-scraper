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


def doArticle( soup ) :
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
	print articleMsg
	print " =============================="
	print " =============================="

	# debug ... need a better cleaning mechanism for the main article
	# lists are causing all the issues!!
	# 	print articleContentObj
	# 	print " =========="


def doComments( soup ) :
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
		print msg

		print " =============================="


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
	soup = loadPage( url )

	doArticle( soup )

	# how many pages?
	pageInfo = soup.findChild( None, { "class" : "comments_page_nav_css" }).findChild( None, { "class" : "popupctrl" })
	pageText = cleanMsg( pageInfo )
	pageInfo = re.findall( r'\b\d+\b', pageText )
	pageCount = int( pageInfo[1] )

	doComments( soup )

	if pageCount > 1 :
		thisPage = 1
		while thisPage < pageCount :
			thisPage += 1
			newUrl = "%s?page=%s" % ( url, thisPage )
			soup = loadPage( newUrl )
			doComments( soup )


if __name__ == '__main__':
# 	url = "http://footballpros.com/content.php/1797-FP-Upset-Special-Challenge-Our-Scrubs-Are-Better-Than-Your-Scrubs-Edition-PS-Week-4"
#
# a longer test url
# http://footballpros.com/showthread.php/10011-Article-FootballPros-com-Upset-Special-Challenge-Week-13
# http://footballpros.com/content.php/1203-FootballPros.com-Upset-Special-Challenge-Week-13
#
	url = "http://footballpros.com/content.php/1203-FootballPros.com-Upset-Special-Challenge-Week-13"
	download( url )


