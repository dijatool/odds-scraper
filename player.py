#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import urllib2
import cookielib
from BeautifulSoup import BeautifulSoup as bs

from misc import cleanText
from odds import teamsTranslate
import config

kCookieFile = '/tmp/cookies/cookies.lwp'


def getHeaders( rowsList ) :
	'''
		Get the column headers from Yahoo...

		they might move around or get renamed...

	'''
	finalHeaders = []
	for i, row in enumerate( rowsList ) :
		rowClass = None
		try :
			rowClass = row['class']
		except :
			pass
		if 'column' != rowClass :
			headers = row.findChildren( 'th' )
			if len( headers ) > 0 :
				for aHeader in headers :
					finalHeaders.append( '"%s"' % aHeader.text )
				break

	return finalHeaders


def dumpGameStats( rowsList, year, isPlayoffs = False ) :
	'''
		dumpGameStats needs a description...

		Note that we don't grab the last item in the list, where Yahoo sticks a total

	'''
	finalList = []
	for i, row in enumerate( rowsList[ : -1 ] ) :
		rowClass = None
		try :
			rowClass = row['class']
		except :
			pass
		if 'column' != rowClass :
			dataList = []
			datums = row.findChildren( 'td' )
			if len( datums ) > 0 :
				if isPlayoffs :
					dataList.append( '"%s"' % str( i + 17 ))
				for aDatum in datums :
					dataList.append( '"%s"' % cleanText( aDatum.text ))

				# now we need to repair data in various ways
				date = dataList[ 1 ]
				date = '%s %s"' % ( date[ : -1 ], year )
				dataList[ 1 ] = date

				# split the result, PF and PA into seperate items
				# it may be empty if the game is unplayed
				result = dataList[ 3 ][ 1 : -1 ]
				if "" != result :
					wlPoints = result.split( " " )
					dataList[ 3 ] = '"%s"' % wlPoints[ 0 ]
					points = wlPoints[ 1 ].split( '-' )
					dataList.insert( 4, '"%s"' % points[ 0 ] )
					dataList.insert( 5, '"%s"' % points[ 1 ] )
				else :
					dataList.insert( 4, '""' )
					dataList.insert( 4, '""' )
				finalList.append( dataList )

	for i, aWeek in enumerate( finalList ) :
		if len( aWeek ) > 0 :
			print ",".join( aWeek )


def statsForPage( top, year ) :
	'''
		statsForPage needs a description...
		print the stats for a particular page where we've already located the top

	'''
	regular = top.find( None, { "id" : "player-game_log-season" } )
	rows = regular.findChildren( 'tr' )

	dumpGameStats( rows, year )

	# do playoffs if they exist
	playoffs = top.find( None, { "id" : "player-game_log-postseason" } )
	if None != playoffs :
		rows = playoffs.findChildren( 'tr' )
		dumpGameStats( rows, year, True )


def doChildPage( url, year ) :
	'''
		Do a child page of the stats (one for each year played)

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

	top = soup.find( None, { "id" : "yui-main" } )
	statsForPage( top, year )


def download( url, root="http://sports.yahoo.com" ) :
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

	top = soup.find( None, { "id" : "yui-main" } )

	nameData = top.find( None, { "id" : "ysp-reg-player-page_title" } )

	# yes, we're doing work twice but we need the headers
	regular = top.find( None, { "id" : "player-game_log-season" } )
	rows = regular.findChildren( 'tr' )
	headers = getHeaders( rows )
	print ",".join( headers )

	#"Week","Date","Opp","Result","PF","PA","QBRat","Comp","Att","Yds","Y/A","Lng","Int","TD","RushAtt","RushYds","RushY/A","RushLng","RushTD","Sack","SackYds","Fum","FumL"

	# we need to find all the other years of data...
	navLinks = top.find( None, { "class" : "nav-list" } ).findChildren( 'a' )
	otherPages = []
	for link in navLinks :
		otherPages.append( "%s%s" % ( root, link[ 'href' ] ))
	otherPages = sorted( otherPages )

	if config._doChildPages :
		for page in otherPages :
			year = page.split( "=" )[ 1 ]
			#print year
			doChildPage( page, year )

	year = "2012"
	statsForPage( top, year )


def main() :
	'''
		Make sure we have a url and then pull the page and parse it into the
		pieces we need.

	'''
	# Ben Roethlisberger
	url = "http://sports.yahoo.com/nfl/players/6770/gamelog"
	#url = "http://sports.yahoo.com/nfl/players/6770/gamelog?year=2010"
	#url = "http://sports.yahoo.com/nfl/players/6770/gamelog?year=2011"
	#url = "http://sports.yahoo.com/nfl/players/6770/gamelog?year=2004

	#url = "file:///tmp/stats/gamelog?year=2010"
	#url = "file:///tmp/stats/gamelog?year=2011"
	#url = "file:///tmp/stats/gamelog"


	download( url )


if __name__ == '__main__':
	main()


