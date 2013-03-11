#!/usr/bin/env python

from datetools import convertDateStr, dateFromMoDay, dateFromTextMoDay

def main() :
	'''
		Run the test here

	'''
	# "Oct 7"
	# "Oct 11"
	date1 = dateFromMoDay( 10, 7 )
	print date1

	date2 = dateFromTextMoDay( "Oct 11" )
	print date2


if __name__ == '__main__':
	main()


