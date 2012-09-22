#!/usr/bin/env python

import urllib2
import os
import sys
import string
import re

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


def teamNameTranslate( teamCity ) :
	'''
		Translate from the city name to the moniker used by the team

		If all else fails, fall back to the city data
	'''
	return _teamNames.get( teamCity, teamCity )


def teamsTranslate( awayTeam, homeTeam ) :
	'''
		teamsTranslate needs a description...

	'''
	visitor = teamNameTranslate( awayTeam )
	home = teamNameTranslate( homeTeam )
	return visitor, home


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
	return teamsTranslate( visitor, home )


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
	odds = string.replace( odds, u'&nbsp;', "ev" )
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


def printOdds( date, time, visitor, home, awayOdds, homeOdds ) :
	'''
		print a full line of odds data...

	'''
	oddsStr = "(%s)"

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


def currentOdds( soup ) :
	'''
		currentOdds needs a description...

		gonna need a new approach to get at a different part of the page...

		<div id="events-wrapper">
			odd event-1 event-
			even event-2 event-
				upcoming-row
					upcoming-row-cell-teams
					upcoming-row-cell-line


	'''
	rowRegx = re.compile( "event-\d+ event-" )

	oddsContainer = soup.findChild( None, { "id" : "events-wrapper" })
	oddsRows = oddsContainer.findAll( None, { "class" : rowRegx })
	for i, game in enumerate( oddsRows ) :
		gameData = game.findChild( None, { "class" : "upcoming-row" })
		( visitor, home ) = gameData.findChild( None, { "class" : "upcoming-row-cell-teams" }).findAll( text=True )
		( visitor, home ) = teamsTranslate( visitor, home )

		odds =  gameData.findChild( None, { "class" : "upcoming-row-cell-line" }).findAll( text=True )

		# should probably factor this out and use it in the other case too
		offset = 1
		if odds[ 0 ] != "+" :
			awayOdds = odds[ 0 ]
		else :
			awayOdds = "%s%s" % ( odds[ 0 ], odds[ 1 ] )
			offset += 1

		if odds[ offset ] != "+" :
			homeOdds = odds[ offset ]
		else :
			homeOdds = "%s%s" % ( odds[ offset ], odds[ offset + 1 ] )
			offset += 1

		awayOdds = fixOdds( awayOdds )
		homeOdds = fixOdds( homeOdds )
		dateObj = game.findChild( None, { "class" : "upcoming-row-cell-date" })
		( date, time ) = dateObj.findAll( text=True )
		date = string.replace( date, '@', '' )

		printOdds( date, time, visitor, home, awayOdds, homeOdds )


def openingOdds( soup ) :
	'''
		openingOdds needs a description...

	'''

	oddsContainer = soup.findChild( None, { "class" : "odds-tables-container" })
	oddsRows = oddsContainer.findAll( None, { "class" : "oddsshark-odds-table allodds-odds" })
	for i, game in enumerate( oddsRows ) :
		try :
			visitor, home = teamNames( game, i )
			date, time = dateAndTime( game, i )
			awayOdds, homeOdds = theOdds( game, i )

			printOdds( date, time, visitor, home, awayOdds, homeOdds )

		# if unpacking something causes an error because of empty data just eat
		# the error and move on
		except ValueError :
			pass

		except IndexError :
			pass


def main() :
	'''
		Pull the page and parse it into the pieces we need.
	'''
	url = "http://www.oddsshark.com/nfl/odds"
	opener = urllib2.build_opener()
	link = opener.open( url )
	page = link.read()
	soup = bs( page )

	print "Opening odds..."
	openingOdds( soup )

	print; print "Current odds..."
	currentOdds( soup )


if __name__ == '__main__':
	main()


