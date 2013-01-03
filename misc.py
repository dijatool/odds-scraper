# -*- coding: utf-8 -*-

#
# http://www.webdevelopersnotes.com/design/list_of_HTML_character_entities.php3
#

_cleanItems = {	'llsquo;'	: '\'',
				'lldquo;'	: '"',
				'rlsquo;'	: '\'',
				'rldquo;'	: '"',
				'rrdquo;'	: '"',
				'rrsquo;'	: '\'',
				'&ldquo;'	: '"',
				'&lsquo;'	: '\'',
				'&rsquo;'	: '\'',
				'&rdquo;'	: '"',
				'&mdash;'	: '--',
				'&#8212;'	: '--',
				'&ndash;'	: '-',
				'&quot;'	: '"',
				'&nbsp;'	: ' ',
				'&frac14;'	: ' 1/4',
				'&#188;'	: ' 1/4',
				'&frac12;'	: ' 1/2',
				'&#189;'	: ' 1/2',
				'&frac34;'	: ' 3/4',
				'&#190;'	: ' 3/4',
				'&#232;'	: 'e',
				'&eacute;'	: 'e',
				'&#233;'	: 'e',
				'&#239;'	: 'i',
				'&hellip;'	: '...',
				'&gt;'		: '>',
				'&lt;'		: '<',
				'&amp;'		: '&',
				'&bull;'	: 'o ',
				'&#8217;'	: '\'',
				'&#8226;'	: 'o ',
				'&diams;'	: 'o ',
				'&#x25A0;'	: 'o ',
				}


def cleanText( inText, forPrint = True ) :
	'''
		Do some basic html substitution

	'''
	import re

	if forPrint :
		cleanText = inText.encode( 'ascii', 'xmlcharrefreplace' )
	else :
		cleanText = inText

	#
	# Basic description of this method here:
	# 	http://stackoverflow.com/questions/6116978/python-replace-multiple-strings
	#
	# Note, we don't escape because that will break the search mechanism
	#
	pattern = re.compile( "|".join( _cleanItems.keys() ))
	cleanText = pattern.sub( lambda m: _cleanItems[ m.group( 0 ) ], cleanText )

	return cleanText

