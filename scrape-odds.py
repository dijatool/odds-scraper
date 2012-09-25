#!/usr/bin/env python
# -*- coding: utf-8 -*-

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
	odds = string.replace( odds, u'½', ".5" )
	odds = string.replace( odds, u'&nbsp;', "even" )
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


def oddsLine( date, time, away, home, awayOdds, homeOdds ) :
	'''
		generate a full line of odds data...

	'''
	oddsStr = " (%s)"
	awayOddsStr = ""
	homeOddsStr = ""
	finalOddsStr ="%s %s %s%s @ %s%s"

	if awayOdds[ 0 ] != '-' :
		awayOddsStr = oddsStr % awayOdds
	if homeOdds[ 0 ] != '-' :
		homeOddsStr = oddsStr % homeOdds

	return finalOddsStr % ( date, time, away, awayOddsStr, home, homeOddsStr )


def currentOdds( soup ) :
	'''
		currentOdds needs a description...

		gonna need a new approach to get at a different part of the page...

		<div id="events-wrapper">
			odd event-1 event-show
			even event-2 event-show
			odd event-3 event-show
			even event-14 event-hide
			odd event-15 event-hide

				upcoming-row
					upcoming-row-cell-teams
					upcoming-row-cell-line

			The perfect regex doesn't work... it's driving me batty!!
				((odd|even) event\-[\d]+ event\-(show|hide))

	'''
	oddsList = []

	oddsContainer = soup.findChild( None, { "id" : "events-wrapper" })
	# this is a shaky way to get what we want and yet it somehow works with bs4
	# we'll do some error checking on the list just in case...
	oddsRows = oddsContainer.findAll( None, { "class" : re.compile( "event\-\d+" ) })
	for i, game in enumerate( oddsRows ) :
		try :
			theClass = game[ 'class' ]
			if not isinstance( theClass, basestring ) :
				theClass = ' '.join( theClass )
			regEx = re.compile( "((odd|even) event\-[\d]+ event\-(show|hide))" )

			if regEx.match( theClass ) :
				gameData = game.findChild( None, { "class" : "upcoming-row" })
				( visitor, home ) = gameData.findChild( None, { "class" : "upcoming-row-cell-teams" }).findAll( text=True )
				( visitor, home ) = teamsTranslate( visitor, home )
				odds =  gameData.findChild( None, { "class" : "upcoming-row-cell-line" }).findAll( text=True )

				# should probably factor this out and use it in the other case too
				# nope, different way of messing things up here
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

				oddsList.append( oddsLine( date, time, visitor, home, awayOdds, homeOdds ) )

		except ValueError :
			pass

		except IndexError :
			pass

	return oddsList


def openingOdds( soup ) :
	'''
		openingOdds needs a description...

	'''
	oddsList = []
	oddsContainer = soup.findChild( None, { "class" : "odds-tables-container" })
	oddsRows = oddsContainer.findAll( None, { "class" : "oddsshark-odds-table allodds-odds" })
	for i, game in enumerate( oddsRows ) :
		try :
			visitor, home = teamNames( game, i )
			date, time = dateAndTime( game, i )
			awayOdds, homeOdds = theOdds( game, i )

			oddsList.append( oddsLine( date, time, visitor, home, awayOdds, homeOdds ) )

		# if unpacking something causes an error because of empty data just eat
		# the error and move on
		except ValueError :
			pass

		except IndexError :
			pass

	return oddsList


def main() :
	'''
		Pull the page and parse it into the pieces we need.
	'''
	url = "http://www.oddsshark.com/nfl/odds"
	#url = "file:///tmp/odds"
	opener = urllib2.build_opener()
	link = opener.open( url )
	page = link.read()
	soup = bs( page )

	print "Opening odds..."
	opening = openingOdds( soup )
	#print oddsList
	for odds in opening :
		print odds

	print; print "Current odds..."
	current = currentOdds( soup )
	for odds in current :
		print odds


if __name__ == '__main__':
	main()


