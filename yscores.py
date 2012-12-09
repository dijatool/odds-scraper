#!/usr/bin/env python

import yahoo.nfl.scores as scores

def main() :
	'''
		Make sure we have a url and then pull the page and parse it into the
		pieces we need.

	'''
	# http://sports.yahoo.com/nfl/scoreboard
	# http://sports.yahoo.com/nfl/scoreboard?w=2
	# http://sports.yahoo.com/nfl/scoreboard?w=6
	# http://sports.yahoo.com/nfl/scoreboard?w=14

	from optparse import OptionParser

	skipFuture = True
	skipFinished = True

	usage = "%prog [options]"
	parser = OptionParser( usage = usage )
	parser.add_option( "-a", "--all", dest="allScores", default = False,
						action="store_true",
						help="Determine if we show all the extra data." )

	( options, args ) = parser.parse_args()

	if options.allScores :
		skipFuture = False
		skipFinished = False

	url = "http://sports.yahoo.com/nfl/scoreboard"

	scores.download( url, skipFuture, skipFinished )


if __name__ == '__main__':
	main()


