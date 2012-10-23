# -*- coding: utf-8 -*-

#
# http://www.webdevelopersnotes.com/design/list_of_HTML_character_entities.php3
#

# 
# 	TODO
# 		a nice replacement for my method of fixing text in cleanText
# 		does it all in one pass!!!
# 
# 	http://stackoverflow.com/questions/6116978/python-replace-multiple-strings
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
				'&nbsp;'	: '',
				'&frac12;'	: ' 1/2',
				'&frac14;'	: ' 1/4',
				'&frac34;'	: ' 3/4',
				'&#233;'	: 'e',
				'&hellip;'	: '...',
				'&gt;'		: '>',
				'&lt;'		: '<',
				'&amp;'		: '&',
				'&bull;'	: 'o ',
				'&diams;'	: 'o ',
				'&#x25A0;'	: 'o ',
				}


def cleanText( inText, forPrint = True ) :
	'''
		Do some basic html substitution

	'''
	if forPrint :
		cleanText = inText.encode( 'ascii', 'xmlcharrefreplace' )
	else :
		cleanText = inText

	for clean in _cleanItems :
		cleanText = cleanText.replace( clean, _cleanItems.get( clean ))
	return cleanText


