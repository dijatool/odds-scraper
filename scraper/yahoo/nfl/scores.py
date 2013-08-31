#!/usr/bin/env python

#
# parse the yahoo scoreboard pages
#

import os
import urllib2
import cookielib
from BeautifulSoup import BeautifulSoup as bs

from misc import cleanText
from odds import teamsTranslate


kCookieFile = '/tmp/cookies/cookies.lwp'


def isFuture( scoresArray ) :
	'''
		Is the game somewhere still in the future?

	'''
	future = False
	if len( scoresArray ) < 5 :
		future = True
	return future


def isFinal( scoresArray ) :
	'''
		Is the game finished (final)?

	'''
	final = False
	if 'Final' in scoresArray :
		final = True
	return final


def printLine( team, scores, rangeStart, rangeEnd ) :
	'''
		Print the team name and a run of score data.

	'''
	print "%11s" % team,
	for i, item in enumerate( scores[ rangeStart : rangeEnd ]) :
		print "%3s" % item,
	print "", scores[ rangeEnd ]


def printScores( away, home, scoresArray, description, skipFuture, skipFinished ) :
	'''
		Print the data from the game

	'''
	print 'Entering'	# debug
	doPrint = True
	if skipFinished :
		if isFinal( scoresArray ) :
			doPrint = False

	if doPrint :
		print 'doPrint!'	# debug
		( away, home ) = teamsTranslate( away, home )
		if isFuture( scoresArray ) :
			if False == skipFuture :
				print "%11s   %s" % ( away, scoresArray[ 1 ] )
				print "%11s   %s" % ( home, scoresArray[ 2 ] )
				print
		else :
			chunkSize = len( scoresArray ) / 3
			offset = chunkSize
			printLine( away, scoresArray, offset, offset + chunkSize - 1 )
			printLine( home, scoresArray, offset + chunkSize, offset + ( 2 * chunkSize ) - 1 )
			if len( description ) > 0 :
				print description
			print


def download( url, skipFuture=True, skipFinished=True ) :
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

	print 'Soup!'	# debug

	scores = soup.findChildren( 'table', { "class" : "scores" } )

	print 'scores!'	# debug
	
	for i, aSection in enumerate( scores ) :
	
		print aSection
	
		scoresArray = []
		away = ""
		home = ""
		teams = aSection.findChildren( None, { "class" : "yspscores team" } )
		
		for i, aTeam in enumerate( teams ) :
			name = aTeam.findChild( 'a' )
			if 0 == i :
				away = name.text
			else :
				home = name.text
		qtrScores = aSection.findChildren( None, { "class" : "yspscores" } )
		for i, qtr in enumerate( qtrScores ) :
			scoresArray.append( cleanText( qtr.text ))

		description = ""
		if not isFuture( scoresArray ) and not isFinal( scoresArray ) :
			#find the 2nd table and grab the content!
			tabs = aSection.parent.findChildren( 'table' )
			descTable = tabs[ 1 ]
			desc = descTable.findChildren( None, { "class" : "yspscores" } )[0]
			description = cleanText( desc.getText( " " ))

		printScores( away, home, scoresArray, description, skipFuture, skipFinished )
		


