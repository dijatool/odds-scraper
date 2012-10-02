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
	'''
	return ''.join( bs( str( obj )).findAll( text=True )).strip()


def loadPage( url ) :
	'''
		Given a url returns a soup object

	'''
	opener = urllib2.build_opener()
	link = opener.open( url )
	page = link.read()
	soup = bs( page )

	return soup


def teamName( data ) :
	'''
		teamName needs a description...
	
	'''
	at = cleanMsg( data[ 7 ] )
	# deal with the superbowl
	if at == 'N' :
		at = ""
	names = cleanMsg( data[ 8 ] ).split( ' ' )
	name = names[ len( names ) - 1 ]
	return at + name


def finalScore( data ) :
	'''
		scores needs a description...
	
	'''
	#score = "%s - %s"
	score = "%s %s"
	tmScore = cleanMsg( data[ 9 ] )
	oppScore = cleanMsg( data[ 10 ] )

	return score % ( tmScore, oppScore )


def parsePage( url ) :
	'''
		Pull the page and parse it into the pieces we need.
	'''
	soup = loadPage( url )
	mainScoresObj = soup.findChild( 'table', { 'id' : 'team_gamelogs' })
	
	# find the rows with a class name of "" (empty string)
	scoreRows = mainScoresObj.findChildren( 'tr', { 'class' : "" })
	for i, row in enumerate( scoreRows ) :
		data = row.findChildren( 'td' )
		try :
			# if this works, it's a game
			# <td align="left" csk="2011-11-28">November 28</td>
			dateTd = data[ 2 ]
			date = dateTd[ 'csk' ]
			team = teamName( data )
			scores = finalScore( data )
			print date, team, scores
		except IndexError :
			pass
		except KeyError :
			pass


def main() :
	'''
		Make sure we have a url and then go do something useful

	'''
	if len( sys.argv ) < 2 :
		import os

		appName = os.path.basename( sys.argv[ 0 ] )
		print "  Usage:", appName, '"url to scrape"'
	else :
		url = sys.argv[ 1 ]
		parsePage( url )


if __name__ == '__main__':
	main()


