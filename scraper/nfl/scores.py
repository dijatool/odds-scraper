#!/usr/bin/env python

import urllib2
import os
import sys
import string
import re

import xml.dom.minidom as xml


_scores = 'http://www.nfl.com/liveupdate/scorestrip/ss.xml'


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
	url = _scores

	dom = xml.parse( urllib2.urlopen( url ))

	for game in dom.getElementsByTagName( 'g' ) :
		home = game.getAttribute( 'hnn' )
		away = game.getAttribute( 'vnn' )
		home, away = fixTeamNames( home, away )

		qtr = game.getAttribute( 'q' )
		time = game.getAttribute( 'k' )
		vs = game.getAttribute( 'vs' )
		hs = game.getAttribute( 'hs' )
		dt = '%s %s' % ( game.getAttribute( 'd' ), game.getAttribute( 't' ) )

		
		if options.csvOut :
			if qtr == 'FO' :
				qtr = 5
			elif qtr == 'F' :
				qtr = 4
			elif qtr == 'P' :
				qtr = 0
			print '%s,%s,%s,%s,%s' % ( away, home, vs, hs, qtr )

		else :
			if qtr == 'FO' :
				qtr = 'F/OT'

			if qtr != 'P' :
				if qtr[ 0 ] != 'F' or options.showFinals :
					aways = '%11s %3s' % ( away, vs )
					homes = '%11s %3s   %s %s' % ( home, hs, qtr, time )
					print aways
					print homes
					print
			else :
				if options.showFuture :
					print '%11s' % away
					print '%11s  %s' % ( home, dt )
					print


def doOptions() :
	'''
		Generate and parse some options.

	'''
	from optparse import OptionParser

	usage = "%prog [options] url"
	parser = OptionParser( usage = usage )

	parser.add_option( "-s", "--showFuture", dest="showFuture", default = False, action="store_true",
						help="Show future games." )
	parser.add_option( "-f", "--showFinals", dest="showFinals", default = False, action="store_true",
						help="Show final games." )
	parser.add_option( "-c", "--csv", dest="csvOut", default = False, action="store_true",
						help="Force CSV formatting" )
	( options, args ) = parser.parse_args()

	return options


def main() :
	'''
		Go do something useful

	'''
	options = doOptions()
	doPage( options )


if __name__ == '__main__':
	main()


