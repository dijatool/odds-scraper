#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import urllib2
import cookielib
from BeautifulSoup import BeautifulSoup as bs
from odds import teamNameTranslate
from misc import cleanText

kCookieFile = '/tmp/cookies/cookies.lwp'


_formatting = [	'%14s',
				'%6s',
				'%6s',
				'%6s',
				'%6s',
				'%6s',
				'%6s',
				'%6s',
				'%6s',
				'%6s',
				'%6s',
				'%6s',
				'%6s',
				'%6s',
				'%6s',
				'%6s',
				'%6s',
				'%6s',
				'%6s',
				'%6s',
				'%6s',
				'%6s',
				'%6s',
				'%6s',
				'%6s',
				]


def formatted( dataList, csv=False ) :
	'''
		formatted needs a description...
	
	'''
	finalStr = ""
	if csv :
		finalStr = ",".join( dataList )
	else :
		finalData = []
		for i, oneItem in enumerate( dataList ) :
			finalData.append( _formatting[ i ] % oneItem )
		finalStr = ''.join( finalData )

	return finalStr


def download( url, csv=False ) :
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

	top = soup.findChild( None, { "class" : "col-main" })
	#print top.prettify()
	name = soup.findChild( 'h4' ).text
	print name

	table = top.findChild( 'table' )
	rows = table.findChildren( 'tr' )
	for row in rows :
		# print row.prettify()
		datums = row.findChildren( 'td' )
		datumList = []
		datums = datums[ 1 : ]
		for i, aDatum in enumerate( datums ) :
			datumList.append( aDatum.text )
			if i == 0 :
				datumList[ i ] = teamNameTranslate( datumList[ i ] )

		print formatted( datumList, csv )

	# cookieJar.save( kCookieFile )


def main() :
	'''
		Make sure we have a url and then pull the page and parse it into the
		pieces we need.

	'''
	urls = [
				# 'file:///tmp/pack/rushing',
				# 'file:///tmp/pack/downs',
				'http://espn.go.com/nfl/statistics/team/_/stat/rushing',
				'http://espn.go.com/nfl/statistics/team/_/stat/downs',

				# 'file:///tmp/pack/defenser',
				# 'file:///tmp/pack/defensed',
				'http://espn.go.com/nfl/statistics/team/_/stat/rushing/position/defense',
				'http://espn.go.com/nfl/statistics/team/_/stat/downs/position/defense',
			]

	for url in urls :
		#download( url )
		download( url, csv=True )

if __name__ == '__main__':
	main()


