#!/usr/bin/env python

import urllib2
import os
import sys
import string
import re

import xml.dom.minidom as xml


_base = 'http://www.nfl.com/ajax/scorestrip?'


def fixTeamNames( home, visitor ) :
	'''
		fixTeamNames needs a description...

	'''
	parts = []
	parts.append( home[ 0 ].upper() )
	parts.append( home[ 1 : ] )
	home = ''.join( parts )

	parts = []
	parts.append( visitor[ 0 ].upper() )
	parts.append( visitor[ 1 : ] )
	visitor = ''.join( parts )

	return home, visitor


def doPage( options ) :
	'''
		doPage needs a description...

	'''
	url = '%sseason=%d&seasonType=%s&week=%d' % ( _base, options.year, options.season, options.week )
	#print url

	dom = xml.parse( urllib2.urlopen( url ))

	for game in dom.getElementsByTagName( 'g' ) :
		home = game.getAttribute( 'hnn' )
		away = game.getAttribute( 'vnn' )
		home, away = fixTeamNames( home, away )

		eid = game.getAttribute( 'eid' )
		gsis = game.getAttribute( 'gsis' )
		qtr = game.getAttribute( 'q' )
		score = '%s-%s' % ( game.getAttribute( 'vs' ), game.getAttribute( 'hs' ) )

		if qtr == 'FO' :
			qtr = 'F/OT'

		if qtr != 'P' :
			print away, '@', home, score, qtr
		else :
			print away, '@', home, gsis, eid




def doOptions() :
	'''
		doOptions needs a description...

	'''
	from optparse import OptionParser

	usage = "%prog [options] url"
	parser = OptionParser( usage = usage )
	parser.add_option( "-w", "--week", dest="week", default = 1,
						help="" )
	parser.add_option( "-y", "--year", dest="year", default = 2013,
						help="" )
	parser.add_option( "-s", "--season", dest="season", default = 'PRE',
						help="" )

	parser.add_option( "-f", "--format", dest="format", default = "%s %s @ %s %s-%s",
						help="determines the format of the scores data (\"%s,%s,%s,%s,%s\" generates CSV data)" )
	parser.add_option( "-c", "--csv", dest="csvOut", default = False, action="store_true",
						help="Force CSV formatting" )
	( options, args ) = parser.parse_args()

	options.week = int( options.week )
	options.year = int( options.year )

	return options





def main() :
	'''
		Make sure we have a url and then go do something useful

	'''
	options = doOptions()
	if options.csvOut :
		options.format = "%s,%s,%s,%s,%s,"
	doPage( options )





if __name__ == '__main__':
	main()


