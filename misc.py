# -*- coding: utf-8 -*-

_cleanItems = {	'llsquo;' :		'\'',
				'lldquo;' :		'"',
				'rlsquo;' :		'\'',
				'rldquo;' :		'"',
				'rrdquo;' :		'"',
				'rrsquo;' :		'\'',
				'&ldquo;' :		'"',
				'&lsquo;' :		'\'',
				'&rsquo;' :		'\'',
				'&rdquo;' :		'"',
				'&mdash;' :		'--',
				'&quot;' :		'"',
				'&nbsp;' :		'',
				'&frac12;' :	' 1/2',
				'&#233;' :		'e',
				'&hellip;' :	'...',
				'&gt;' :		'>',
				'&lt;' :		'<',
				'&amp;' :		'&',
				'&bull;' :		'o ',
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


