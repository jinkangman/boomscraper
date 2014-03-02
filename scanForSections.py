#!/usr/bin/env python
import urllib2
import re

def main():
	categories = parseOrigin()

	if categories:
		siteStructure = parseCategories(categories)
		if siteStructure:
			print siteStructure
		else:
			print "No subcategories found. Exiting."
	else:
		print "No categories found. Exiting."

def parseOrigin():
	"""Scan the front page of www.cowboom.com looking for high-level categories
	and return a list of them, such as:
	
	['Computers', 'Gaming', 'Mobile & Cellular', 'Electronics', 'More']"""

	# Returns a list of product categories from cowboom.com
	print "Parsing the front page for new categories:"
	categories = []

	# build the URL
	URL="http://www.cowboom.com/"

	# download the page
	print "Downloading URL: " + URL
	page = urllib2.urlopen(URL)
	stream = page.readlines()

	# search for 'sold-out' marker
	for line in stream:
		if re.search('</span>', line):
			if re.search('<span>', line):
				line = re.sub('<span>(.*?)</span>','\\1', line, re.S)
				line = line.strip()
				#print line
				categories.append(line)

	return categories

def parseCategories(categories):
	"""Accept a list of categories and returns a dictionary of categories to
	subcategories, such as:
	
	{'Gaming': ['Video-Game-Consoles', 'Games', 'Game-Accessories'],
	 'Electronics': ['Portable-Electronics', 'Home-Electronics']}"""

	print "Parsing the category pages for subcategories:"

	dictionary = {}

	for category in categories:
		# Convert ' & ' in category name to '-' to match the URL structure
		category = re.sub('\s&\s', '-', str(category), re.M|re.S)
		
		subcategories = []

		# build the URL
		URL="http://www.cowboom.com/" + category

		# download the page
		print "Downloading URL: " + URL
		page = urllib2.urlopen(URL)
		stream = page.readlines()

		for line in stream:
			if re.search('subcat', line):
				line = re.sub('<div class="subcat"><a class="newsite" href="/'+category+'/(.*?)">.*$','\\1', line, re.S)
				line = line.strip()
				#print line
				subcategories.append(line)

		dictionary[category] = subcategories

	return dictionary

if __name__ == "__main__":
    main()