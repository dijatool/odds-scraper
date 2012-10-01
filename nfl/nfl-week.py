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

		Should probably add a flag and a slow way to strip for articles... I'm mangling biggies stuff

	'''
	return ''.join( bs( str( obj )).findAll( text=True )).strip()


def getDate( tag ) :
	'''
		getDate needs a description...

	'''
	dateStr = '%s-%s-%s'

	date = tag[ 'id' ].split( '-' )[ 1 ]
	date = date[ : len( date ) - 2 ]

	return dateStr % ( date[ : 4 ], date[ 4 : 6 ], date[ 6 : 8 ] )


def nameScore( tag ) :
	'''
		nameScore needs a description...

	'''


	name = cleanMsg( tag.findChild( None, { 'class' : 'team-name' }) )
	score = cleanMsg( tag.findChild( None, { 'class' : 'total-score' }) )

	return name, score


def loadPage( url ) :
	'''
		Given a url returns a soup object

	'''
	opener = urllib2.build_opener()
	link = opener.open( url )
	page = link.read()
	soup = bs( page )

	return soup


def parsePage( url, formatStr = None ) :
	'''
		Pull the page and parse it into the pieces we need.
	'''
	soup = loadPage( url )
	mainScoresObj = soup.findChild( None, { 'id' : 'score-boxes' })

	scoreList = mainScoresObj.findChildren( None, { 'class' : 'scorebox-wrapper' })

	for i, row in enumerate( scoreList ) :
		try :
			top = row.findChild( None, { 'class' : 'new-score-box-wrapper' })
			date = getDate( top )

			away = top.findChild( None, { 'class' : 'away-team' })
			awayName, awayScore = nameScore( away )

			home = top.findChild( None, { 'class' : 'home-team' })
			homeName, homeScore = nameScore( home )

			if None == formatStr :
				formatStr = "%s %s @ %s %s-%s"	# normal use
				# formatStr = "%s,%s,%s,%s,%s"	# csv format
			print formatStr % ( date, awayName, homeName, awayScore, homeScore )

		except TypeError :
			pass


def main() :
	'''
		Make sure we have a url and then go do something useful

	'''
	from optparse import OptionParser

	usage = "%prog [options] url"
	parser = OptionParser( usage = usage )
	parser.add_option( "-f", "--format", dest="format", default = "%s %s @ %s %s-%s",
						help="determines the format of the scores data (\"%s,%s,%s,%s,%s\" generates CSV data)" )
	( options, args ) = parser.parse_args()

	if len( sys.argv ) < 2 :
		import os

		appName = os.path.basename( sys.argv[ 0 ] )
		print "  Usage:", appName, '"url to scrape"'
	else :
		formatStr = options.format
		url = args[ 0 ]
		parsePage( url, formatStr )


if __name__ == '__main__':
	main()


