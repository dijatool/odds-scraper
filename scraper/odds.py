#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib2
import os
import sys
import string
import re

try :
	from BeautifulSoup import BeautifulSoup as bs
except :
	from bs4 import BeautifulSoup as bs


from datetools import dateFromTextMoDay


_teamNames = {	'Buffalo' :			'Bills',
				'Miami' :			'Dolphins',
				'New England' :		'Patriots',
				'NY Jets' :			'Jets',
				'N.Y. Jets' :		'Jets',
				'New York Jets' :	'Jets',
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
				'N.Y. Giants' :		'Giants',
				'New York Giants' :	'Giants',
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

_teamLongitude = {	'Bills' :		-78.786944,
					'Patriots' :	-71.264344,
					'Jets' :		-74.074444,
					'Dolphins' :	-80.238889,
					'Bengals' :		-84.516039,
					'Ravens' :		-76.622778,
					'Steelers' :	-80.015833,
					'Browns' :		-81.699444,
					'Texans' :		-95.410833,
					'Colts' :		-86.163806,
					'Titans' :		-86.771389,
					'Jaguars' :		-81.6375,
					'Chargers' :	-117.119444,
					'Broncos' :		-105.02,
					'Chiefs' :		-94.483889,
					'Raiders' :		-122.200556,
					'Eagles' :		-75.1675,
					'Redskins' :	-76.864444,
					'Cowboys' :		-97.092778,
					'Giants' :		-74.074444,
					'Vikings' :		-93.258056,
					'Packers' :		-88.062222,
					'Bears' :		-87.616667,
					'Lions' :		-83.045556,
					'Falcons' :		-84.400833,
					'Buccaneers' :	-82.503333,
					'Panthers' :	-80.852778,
					'Saints' :		-90.081111,
					'Cardinals' :	-112.2625,
					'49ers' :		-122.386111,
					'Seahawks' :	-122.331667,
					'Rams' :		-90.188611,
					}


class GameOdds( object ) :
	'''
		class GameOddsData

			...class description here...
			Hold onto the data for a single game

		@author	Dave Ely <dely@dijatool.com>
		@date	Tue, September 25, 2012

	'''
	def __init__( self, date = None, time = None, away = None,
					home = None, awayOdds = None, homeOdds = None ):
		self._date = dateFromTextMoDay( date )
		self._time = time
		self._away = away
		self._home = home
		self._awayOdds = awayOdds
		self._homeOdds = homeOdds
		self._gameInfo = self.oddsLine()


	def __repr__( self ) :
		'''
			Standard string representation

		'''
		return self.oddsLine()


 	def __unicode__( self ) :
		'''
			Standard string representation

		'''
		return self.oddsLine()


	def oddsLine( self ) :
		'''
			A full single line representation

		'''
		return "%s %s" % ( self.dateTime(), self.gameWithOdds() )


	def dateTime( self ) :
		'''
			Just the date and time

		'''
		return "%s %s" % ( self._date.strftime( "%a %b %d" ), self._time )


	def game( self ) :
		'''
			Away @ Home

		'''
		return "%s @ %s" % ( self._away, self._home )


	def gameWithOdds( self ) :
		'''
			Away @ Home with a positive odds display

		'''
		away = self.teamWithOdds( self._away, self._awayOdds )
		home = self.teamWithOdds( self._home, self._homeOdds )

		return "%s @ %s" % ( away, home )


	def teamWithOdds( self, team, odds ) :
		'''
			Get the team name and if the odds are positive, the odds in parentheses

		'''
		oddsTmpl = " (%s)"
		oddsStr = ""
		if odds[ 0 ] != '-' :
			oddsStr = oddsTmpl % odds

		return "%s%s" % ( team, oddsStr )


	def isUnderDog( self, odds ) :
		'''
			isUnderDog needs a description...

		'''
		dog = False
		if odds[ 0 ] != '-' and odds[ 0 ] != 'e' :
			dog = True
		return dog


	def dogAndPoints( self ) :
		'''
			Dump the underdog and the points all by itself

		'''
		team = ""
		odds = ""
		if self.isUnderDog( self._awayOdds ) :
			team, odds = ( self._away, self._awayOdds )
		else :
			team, odds = ( self._home, self._homeOdds )
		odds = self._stripPlus( odds )
		return "%s %s" % ( team, odds )


	def homeAndPoints( self ) :
		'''
			Dump the home team and the points all by itself

		'''
		team, odds = ( self._home, self._homeOdds )
		odds = self._stripPlus( odds )
		return "%s %s" % ( team, odds )


	def oddsLineForFp( self ) :
		'''
			Away @ Home with a positive odds display

			Game has a [*] prefix
			Underdog has a bold wrapper
		'''
		return "%s %s" % ( self.dateTime(), self.gameWithOddsForFp() )


	def gameWithOddsForFp( self ) :
		'''
			Away @ Home with a positive odds display

			Game has a [*] prefix
			Underdog has a bold wrapper
		'''
		away = self.teamWithOdds( self._away, self._awayOdds )
		if self.isUnderDog( self._awayOdds ) :
			away = "[b]%s[/b]" % away

		home = self.teamWithOdds( self._home, self._homeOdds )
		if self.isUnderDog( self._homeOdds ) :
			home = "[b]%s[/b]" % home

		return "[*]%s @ %s" % ( away, home )


	def _stripPlus( self, odds ) :
		'''
			_stripPlus needs a description...

		'''
		if odds[ 0 ] == '+' :
			odds = odds[ 1 : ]
		return odds


def compareGames( game ) :
	'''
		compareGames needs a description...

	'''
	return ''.join( ( str( game._date ), game._time, str( _teamLongitude.get( game._home, 0 ))))


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
	if oddsArray[ 1 ] != ' ' :
		homeOdds = oddsArray[ 2 ]
	else :
		homeOdds = oddsArray[ 3 ]

	awayOdds = fixOdds( awayOdds )
	homeOdds = fixOdds( homeOdds )
	return awayOdds, homeOdds


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

				oddsList.append( GameOdds( date, time, visitor, home, awayOdds, homeOdds ))

		# if unpacking something causes an error because of empty data just eat
		# the error and move on
		except ValueError :
			pass

		except IndexError :
			pass

	oddsList.sort( key=compareGames )
	return oddsList


def openingOdds( soup ) :
	'''
		openingOdds needs a description...

	'''
	oddsList = []
	oddsContainer = soup.findChild( None, { "class" : "content" })
	oddsRows = oddsContainer.findAll( None, { "class" : "oddsshark-odds-table allodds-odds" })
	for i, game in enumerate( oddsRows ) :
		try :
			visitor, home = teamNames( game, i )
			date, time = dateAndTime( game, i )
			awayOdds, homeOdds = theOdds( game, i )

			oddsList.append( GameOdds( date, time, visitor, home, awayOdds, homeOdds ))

		# if unpacking something causes an error because of empty data just eat
		# the error and move on
		except ValueError :
			pass

		except IndexError :
			pass

	oddsList.sort( key=compareGames )
	return oddsList


