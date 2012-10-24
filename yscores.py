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

	#url = "file:///tmp/scoreboard"
	url = "http://sports.yahoo.com/nfl/scoreboard"

	scores.download( url )


if __name__ == '__main__':
	main()


