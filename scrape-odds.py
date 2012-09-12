#!/usr/bin/env python

import urllib2
import os
import sys
import string

from BeautifulSoup import BeautifulSoup as bs

_teamNames = {	'Buffalo' :			'Bills',
				'Miami' :			'Dolphins',
				'New England' :		'Patriots',
				'NY Jets' :			'Jets',
				'Baltimore' :		'Ravens',
				'Cincinnati' :		'Bengals',
				'Cleveland' :		'Browns',
				'Pittsburgh' :		'Steelers',
				'Indianapolis' :	'Colts',
				'Houston' :			'Texans',
				'Jacksonville' :	'Jaguars',
				'Tennessee' :		'Titans',
				'Denver' :			'Broncos',
				'Kansas City' :		'Chiefs',
				'Oakland' :			'Raiders',
				'San Diego' :		'Chargers',
				'Philadelphia' :	'Eagles',
				'Dallas' :			'Cowboys',
				'NY Giants' :		'Giants',
				'Washington' :		'Redskins',
				'Chicago' :			'Bears',
				'Detroit' :			'Lions',
				'Green Bay' :		'Packers',
				'Minnesota' :		'Vikings',
				'Atlanta' :			'Falcons',
				'Carolina' :		'Panthers',
				'New Orleans' :		'Saints',
				'Tampa Bay' :		'Buccaneers',
				'Seattle' :			'Seahawks',
				'San Francisco' :	'49ers',
				'St. Louis' :		'Rams',
				'Arizona' :			'Cardinals',
		}


# def leaf( tag ):
# 	'''
# 		get text inside <tag><tag>... text
# 			<td>	<div><font size="2"><i><font color="#FFFFFF">
# 			+ + + + +</font></i></font></div></td>
# 		<td height="10"><font size="2"> Bierfeuerwerk <strong></strong> </font></td>
# 	'''
# 	leafText = ""
# 	for text in tag.findAll( text=True ) :
# 		text = text.strip()
# 		if text :
# 			leafText = text
#
# 	return leafText

def teamNameTranslate( teamCity ) :
	'''
		Translate from the city name to the moniker used by the team

		If all else fails, fall back to the city data
	'''
	return _teamNames.get( teamCity, teamCity )


def teamNames( tag, offset ) :
	'''
		Get the teamNames tuple

		It's stuffed inside "odds-row odds-row-odd odds-row-n-1" where n is a game offset
		and then "game-left"

		eg: Bears @ Browns
	'''
	newOffset = offset + 1

	classId = 'odds-row odds-row-odd odds-row-%s-1' % newOffset
	namesWrapper = tag.findChild( None, { "class" : classId } )
	namesObj = namesWrapper.findChild( None, { "class" : "game-left" } )
	( visitor, home ) = namesObj.findAll( text=True )
	visitor = teamNameTranslate( visitor )
	home = teamNameTranslate( home )
	return visitor, home


def dateAndTime( tag, offset ) :
	'''
		Get the date and time tuple

		It's stuffed inside "odds-row odds-row-even odds-row-n-2" where n is a game offset
		and then "game-left"

		eg: Aug 30 7:00 PM (in two separate items)
	'''
	newOffset = offset + 1

	classId = 'odds-row odds-row-even odds-row-%s-2' % newOffset
	dtWrapper = tag.findChild( None, { "class" : classId } )
	dtObj = dtWrapper.findChild( None, { "class" : "game-left" } )
	( date, time ) = dtObj.findAll( text=True )
	return date, time


def fixOdds( oddsStr ) :
	'''
		Replace instances of "&frac12;" with ".5" and trim any excess
	'''
	odds = string.replace( oddsStr, u'&frac12;', ".5" )
	return odds.strip()


def theOdds( tag, offset ) :
	'''
		Get the away and home odds

		They're stuff inside "book book-odd book-1" at text items 0 and 2 (of 0-3)
	'''
	newOffset = offset + 1

	classId = 'odds-row odds-row-even odds-row-%s-2' % newOffset
	wrapper = tag.findChild( None, { "class" : classId } )
	odds = wrapper.findChild( None, { "class" : "book book-odd book-1" } )
	
	oddsArray = odds.findAll( text=True )
	awayOdds = oddsArray[ 0 ]
	# sometimes this is the wrong one, but the site is inconsistent
	homeOdds = oddsArray[ 2 ]

	awayOdds = fixOdds( awayOdds )
	homeOdds = fixOdds( homeOdds )
	return awayOdds, homeOdds


def main() :
	'''
		Pull the page and parse it into the pieces we need.
	'''
	oddsStr = "(%s)"
	url = "http://www.oddsshark.com/nfl/odds"
	opener = urllib2.build_opener()
	link = opener.open( url )
	page = link.read()
	soup = bs( page )

	oddsContainer = soup.findChild( None, { "class" : "odds-tables-container" })
	oddsRows = oddsContainer.findAll( None, { "class" : "oddsshark-odds-table allodds-odds" })
	for i, game in enumerate( oddsRows ) :
		try :
			visitor, home = teamNames( game, i )
			date, time = dateAndTime( game, i )
			awayOdds, homeOdds = theOdds( game, i )
			print date, time, visitor,
			if awayOdds[ 0 ] != '-' :
				print oddsStr % awayOdds,
			print "@",
			print home,
			if homeOdds[ 0 ] != '-' :
				print oddsStr % homeOdds
			else :
				# finish the line
				print

		# if unpacking something causes an error because of empty data just eat
		# the error and move on
		except ValueError :
			pass


if __name__ == '__main__':
	main()


