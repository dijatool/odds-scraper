#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import urllib2
import cookielib
from BeautifulSoup import BeautifulSoup as bs

from misc import cleanText

kCookieFile = '/tmp/cookies/cookies.lwp'


def getTooltipHeadingText( th ) :
	'''
		BeautifulSoup is being confused by row headings with gobs of tooltip text.

		Pull what we can and strip the brackety stuff in front

		So blah, (Passes Attempted)">Cmp% ==> Cmp%
	'''
	import string

	text = ''.join( th.findAll( text=True ))
	try :
		last = string.rindex( text, '">' )
		text = text[ last + 2 : ]
	except :
		pass
	return text


def printRow( list ) :
	'''
		printRow needs a description...

	'''
	if False :
		for item in list :
			print item,
		print
	else :
		print ','.join( list )


def trimTeamName( name ) :
	'''
		Trim the name down to the nickname I use everywhere else...

	'''
	names = name.split( ' ' )
	return names[ len( names ) - 1 ]


def dumpTable( soup, idName ) :
	'''
		dumpTable needs a description...

	'''
	top = soup.findChild( None, { 'class' : "stw", 'id' : idName })
	#print top.prettify()

	name = top.findChild( 'h2' ).text
	print
	print name
	print

	rowList = []

	passTable = top.findChild( 'table' )
	rows = passTable.findChildren( 'tr' )
	for row in rows :
		rowData = []
		ths = row.findChildren( 'th' )
		if len( ths ) > 0 :
			for th in ths :
				rowData.append( getTooltipHeadingText( th ))
		else :
			tds = row.findChildren( 'td' )
			for td in tds :
				rowData.append( td.text )
		del rowData[ 0 ]					# dump the rank
		#printRow( rowData )
		rowList.append( rowData )

	# dump the last 3 rows
	rowList = rowList[ : -3 ]
	for aRow in rowList :
		aRow[ 0 ] = trimTeamName( aRow[ 0 ])
		printRow( aRow )


def loadSoap( url ) :
	'''
		Load the soup from a URL

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

	return soup


def download( url, tags, csv=False ) :
	'''
		Pull the page and parse it into the pieces we need.
	'''
	soup = loadSoap( url )

	for tag in tags :
		dumpTable( soup, tag )


def main() :
	'''
		Make sure we have a url and then pull the page and parse it into the
		pieces we need.

	'''
	urls = {
			#'file:///tmp/pack/index.html' : [ 'all_team_stats', 'all_passing', 'all_rushing', 'all_returns', 'all_scoring' ],
			#'file:///tmp/pack/opp.htm' : [ 'all_team_stats', 'all_passing', 'all_rushing', 'all_scoring' ],
			'http://www.pro-football-reference.com/years/2013/' : [ 'all_team_stats', 'all_passing', 'all_rushing', 'all_scoring' ],
			'http://www.pro-football-reference.com/years/2013/opp.htm' : [ 'all_team_stats', 'all_passing', 'all_rushing', 'all_scoring' ],
			}

	for url in urls :
		download( url, urls[ url ], csv=True )


if __name__ == '__main__':
	main()


