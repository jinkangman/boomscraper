#!/usr/bin/env python
import sys
import urllib2
import re

def main():
	# Take user input from CLI
	if len(sys.argv) > 2:
		category = sys.argv[1]
		subcategory = sys.argv[2]

		categoryStructure = parseProductPages(category,subcategory)
		print categoryStructure
	else:
		print "Usage: ./scanForProducts.py category subcategory"

def parseProductPages(category,subcategory):
	"""This function takes in a category/subcategory in order to build URL's to be scraped
	 and returns a dictionary of all the Products in that category, such as:
	
	{'$contentID': '$productName', '1464470': 'Sony - PlayStation 3 Black Friday Bundle (Pre-owned)'}
	
	Example of the URL to be scanned here:
	http://www.cowboom.com/Mobile-Cellular/Cell-Phones-Smartphones/?page=1&order=price_high"""

	# Accepts a category and sub category and returns a dictionary of all products within
	print "Scanning category/subcategory: " + category + "/" + subcategory

	# build the base of the URL
	baseURL="http://www.cowboom.com/"
	handle_categories = category + "/" + subcategory + "/"

	# initialize our variables
	page_number = 0
	last_page_bool = False
	max_items_per_page = 20

	dictionary = {}

	# start scanning in a loop until we reach the last page
	while (last_page_bool != True):
		# increase page counter and rebuild the URL
		page_number = page_number + 1
		handle_pageno = "?page=" + str(page_number) + "&order=price_high"
		URL = baseURL + str(handle_categories) + str(handle_pageno)
		temporary_dict = {}

		# download the page
		print "Downloading product page number: " + str(page_number)
		print "URL: " + URL
		page = urllib2.urlopen(URL)
		stream = page.readlines()

                found = False

		# walk through each line, parsing out our data
		for line in stream:
                        if found == True:
				contentID = re.sub('^.*href="http://www.cowboom.com/product/', "", line, re.M|re.S)
				contentID = re.sub('/".*$', "", contentID, re.M|re.S)
				contentID = contentID.rstrip()
				title = re.sub('^.*href="http://www.cowboom.com/product/\d+/">', "", line, re.M|re.S)
				title = re.sub('</a>.*$', "", title, re.M|re.S)
				title = title.rstrip()
				#print contentID + " " + title
				temporary_dict[contentID] = title
                                found = False
			if re.search("snippet", line):
                                found = True


		item_count = len(temporary_dict)

		if item_count == 0 or item_count < max_items_per_page:
			last_page_bool = True
			print "Last page has been reached"

		dictionary.update(temporary_dict)

	total_item_count = str(len(dictionary))
	print total_item_count + " products found for subcategory: " + subcategory

	return dictionary

if __name__ == "__main__":
    main()
