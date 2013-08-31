# -*- coding: utf-8 -*-

#
# http://www.webdevelopersnotes.com/design/list_of_HTML_character_entities.php3
#

_cleanItems = {	'&#39;'		: '\'',
				'llsquo;'	: '\'',
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
				'&#8211;'	: '-',
				'&ndash;'	: '-',
				'&quot;'	: '"',
				'&#160;'	: '',
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
				'&#8230;'	: '...',
				'&hellip;'	: '...',
				'&gt;'		: '>',
				'&lt;'		: '<',
				'&amp;'		: '&',
				'&bull;'	: 'o ',
				'&#8216;'	: '\'',
				'&#8217;'	: '\'',
				'&#8220;'	: '"',
				'&#8221;'	: '"',
				'&#8233;'	: '',
				'&#8226;'	: 'o ',
				'&#8242;'	: '\'',
				'&#9632;'	: 'o ',
				'&diams;'	: 'o ',
				'&#x25A0;'	: 'o ',
				'&iuml;'	: 'i',
				'&shy;'		: '-',
				'&#65279;'	: '',
				}


def hexDump( data, indent = 0 ) :
	'''
		Dump a multiline hex representation of 'data' with trailing ascii.

	'''
	import binascii


	hexData = []
	asciiData = []
	count = 0
	lineLength = 0
	hexData.append( " " * indent )

	for byte in data :
		hexData.append( binascii.hexlify( byte ) )
		intVal = ord( byte )
		if intVal >= 32 and intVal < 127 :
			asciiData.append( byte )
		else :
			asciiData.append( '.' )
		count += 1
		lineLength += 1
		if ( 0 == ( count % 16 )) :
			hexData.append( " " * 4 )
			hexData.append( ''.join( asciiData ))
			asciiData = []
			hexData.append( '\n' )
			hexData.append( " " * indent )
			lineLength = 0

	hexData.append( "  " * ( 16 - lineLength ))
	hexData.append( " " * 4 )
	hexData.append( ''.join( asciiData ))

	print ''.join( hexData )


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

