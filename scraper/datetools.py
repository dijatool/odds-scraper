#!/usr/bin/env python

from datetime import date
import time


_months = {	'jan' :	1,
			'feb' :	2,
			'mar' :	3,
			'apr' :	4,
			'may' :	5,
			'jun' :	6,
			'jul' :	7,
			'aug' :	8,
			'sep' :	9,
			'oct' :	10,
			'nov' :	11,
			'dec' :	12,
			}

# these get filled in at runtime ...  kinda ugly, i don't care just now
_thisMonth = None
_thisYear = None


def convertDateStr( dateStr ) :
	'''
		convert from a simple string repr to a date object

	'''
	return date.fromtimestamp( time.mktime( time.strptime( dateStr, "%Y-%m-%d" )))


def dateFromMoDay( month, day ) :
	'''
		Build a date object given only a month and day

	'''
	global _thisMonth
	global _thisYear

	if None == _thisMonth :
		dateInfo = date.today().timetuple()
		_thisMonth = dateInfo.tm_mon
		_thisYear = dateInfo.tm_year

	year = _thisYear
	if 1 == month :
		if 12 == _thisMonth :
			year += 1

	return date( year, month, day )


def dateFromTextMoDay( dateStr ) :
	'''
	   Convert the short text to ints and then fill out a date object

	'''
	( month, day ) = dateStr.split( ' ' )
	month = _months.get( month.lower()[ : 3 ], 0 )
	day = int( day )

	return dateFromMoDay( month, day )


