"""
	setup.py

		Manage the packing for the scrapers

"""

#
# work in develop mode?
#	python setup.py develop
# remove the module for normal install?
#	python setup.py develop --uninstall
#
from setuptools import setup, find_packages


_longDesc = """
A set of scraper and utility functions used to scrape various places around the web.
"""
_version = __import__( 'scraper' ).__version__


setup (
	name = 'scraper',
	# version = '0.1',
	version = _version,
	description = 'Basic scraping tools and utilities',
	long_description = _longDesc,
	author = 'Dave Ely',
	author_email='dely@dijatool.com',
	#packages = [ 'scraper' ],
	packages = find_packages(),
	license='BSD License',

	# need to add dependency information...
	# needs 'unicodecsv'
	# anything else?
	# soup!!

	classifiers = [	'Development Status :: 2 - Pre-Alpha',
					'Intended Audience :: Developers',
					'License :: OSI Approved :: BSD License',
					'Natural Language :: English',
					'Programming Language :: Python :: 2.5',
					'Programming Language :: Python :: 2.6',
					'Programming Language :: Python :: 2.7',
					'Programming Language :: Python :: Implementation :: CPython', ],
	)


