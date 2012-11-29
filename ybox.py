#!/usr/bin/env python

import os
import urllib2
import cookielib
from BeautifulSoup import BeautifulSoup as bs

from misc import cleanText

kCookieFile = '/tmp/cookies/cookies.lwp'

def tableToArray( tableSoup ) :
	'''
		tableToArray needs a description...

	'''
	table = []
	rows = tableSoup.findChildren( 'tbody' )[ 0 ].findChildren( 'tr' )
	for row in rows :
		rowArray = []
		tds = row.findChildren( 'td' )
		for td in tds :
			rowArray.append( cleanText( td.getText( ' ' )))
		table.append( rowArray )

	return table


def printTableArray( table ) :
	'''
		printTableArray needs a description...

	'''
	for row in table :
		for item in row :
			print item,
		print


def scoreSummary( soup ) :
	'''
		scoreSummary needs a description...

	'''
	scores = soup.findChildren( None, { 'id' : 'ysp-reg-box-game_details-scoring_summary' } )

	scoreItems = scores[ 0 ].findChildren( recursive=False )
	for i, item in enumerate( scoreItems ) :
		if 0 == i :
			print item.getText( " " )
		else :
			children = item.findChildren( recursive=False )
			for child in children :
				if 'h' == child.name[ 0 ] :
					print cleanText( child.getText( " " ))
				elif 'table' == child.name :
					printTableArray( tableToArray( child ))
				print


def passing( soup ) :
	'''
		passing needs a description...

	'''
	# <div id="ysp-reg-box-game_details-game_stats" class="ysp-mod ysp-data">

	top = soup.findChildren( None, { 'id' : 'ysp-reg-box-game_details-game_stats' } )
	tables = top[ 0 ].findChildren( 'table' )

	print "Passing"
	printTableArray( tableToArray( tables[ 0 ] ))
	printTableArray( tableToArray( tables[ 1 ] ))
	print

	print "Rushing"
	printTableArray( tableToArray( tables[ 2 ] ))
	printTableArray( tableToArray( tables[ 3 ] ))
	print

	print "Receiving"
	printTableArray( tableToArray( tables[ 4 ] ))
	printTableArray( tableToArray( tables[ 5 ] ))
	print


def download( url ) :
	'''
		download needs a description...

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

	scoreSummary( soup )
	passing( soup )


def main() :
	'''
		Go do something useful.

	'''
	#url = "http://sports.yahoo.com/nfl/boxscore?gid=20120909009"
	#url = "file:///tmp/pack/boxscore?gid=20120909009"
	# download( url )

	import sys

	if len( sys.argv ) < 2 :
		appName = os.path.basename( sys.argv[ 0 ] )
		print "\tUsage:", appName, "url to scrape"
	else :
		url = sys.argv[ 1 ]
		download( url )


if __name__ == '__main__':
	main()


