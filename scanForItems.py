#!/usr/bin/python
import sys
import urllib2
import re

def main():
	# Take user input from CLI
	if len(sys.argv) > 1:
		contentID=sys.argv[1]

		# if user input is an integer
		if contentID.isdigit():
			# if the product is in stock
			if checkAvailability(contentID):
				# create our list
				items = itemList()
				# start parsing the items out and appending them
				items = parseItemPages(contentID,items)
				# print the list to CLI
				items.show()
				exit(0)

	print "Usage: ./scanForItems.py contentID"
	print "Note: contentID must be numeric"

class itemList(object):
	"""This object holds detailed info about each of our items.

	As we scan items we use append() to add their info to a set of ordered
	lists: lotID, grade, price, notes

	These lists are stored in a dictionary and can be called by name."""
	
	def __init__(self):
		self.dictionary = {}
		self.dictionary['lotID'] = []
		self.dictionary['grade'] = []
		self.dictionary['price'] = []
		self.dictionary['notes'] = []

	def append(self, lotID, grade, price, notes):
		#Allows you to add to each of the item lists in one function call.
		self.dictionary['lotID'].append(lotID)
		self.dictionary['grade'].append(grade)
		self.dictionary['price'].append(price)
		self.dictionary['notes'].append(notes)

	def show(self):
		#Prints each of the item lists.
		for k,v in self.dictionary.iteritems():
			print str(k) + " - " + str(v)

def checkAvailability(contentID):
	"""This function checks at the product level to see if there are individual
	items in stock.

	Returns True if there are items in stock.

	Caveat: Our check returns true even if there are only 'New' items in stock,
	but parseItemPages() only looks for 'Used' items, sometimes causing '0 files
	found' from that function.

	Example URL:
	http://www.cowboom.com/product/1383907"""

	print "Checking availability of contentID: " + contentID

	# build the URL
	URL="http://www.cowboom.com/product/" + str(contentID)

	# download the page
	print "Downloading front page..."
	print "URL: " + URL
	page = urllib2.urlopen(URL)
	stream = page.readlines()

	# search for 'sold-out' marker
	for line in stream:
		# if found, exit 0
		if re.search('id="sold-out"', line):
			print "!!OUT OF STOCK!!"
			return False

	# not found, exit 1
	print "++IN STOCK++"
	return True

def parseItemPages(contentID,items):
	"""This function accepts a contentID and an empty items object and returns
	an items object containing a list of all the individual used items for sale.

	The item's stock at the site is divided up into 'n' pages of 11 items each.

	We scan through each line of each stock page, looking for 'keywords' to
	match individual items and their metadata. This function relies on regex to
	accomplish that and as such is brittle to changes at the site.

	If there are less than 11 items on a page, then we have reached the end."""

	print "Scanning inventory of contentID: " + contentID

	# build the URL
	baseURL="http://www.cowboom.com/store/productBestAvailable.cfm?"
	handle_contentID = "&contentID=" + contentID

	# initialize our variables
	page_number = 0
	last_page_bool = False
	max_items_per_page = 11

	# start scanning in a loop until we reach the last page
	while (last_page_bool != True):
		# increase page counter and rebuild the URL
		page_number = page_number + 1
		handle_pageno = "&pageno=" + str(page_number)
		URL = baseURL + str(handle_contentID) + str(handle_pageno)

		# download the page
		print "Downloading inventory page number: " + str(page_number)
		print "URL: " + URL
		page = urllib2.urlopen(URL)
		stream = page.readlines()

		# initialize temporary lists
		lotIDs = list()
		grades = list()
		prices = list()
		# we can't append to the notes list as we go, because not every item has a note
		# but we can preinitialize the notes list, because we know there are never more
		# than 'max_items_per_page'
		notesNext = False
		notes = [None]*max_items_per_page

		# walk through each line, parsing out our data
		for line in stream:
			# regex explanations in the comments
			if notesNext == True:
				# remove leading spaces
				line = re.sub('^\s+', "", line, re.M|re.S)
				# remove '<br>' and everything after
				line = re.sub('<br>.*',"", line, re.M|re.S)
				line = line.rstrip()
				notes[len(lotIDs)-1] = line
				notesNext = False
				continue
			if re.search("lotID", line):
				# remove from beginning of line to 'value='
				line = re.sub('^.*value="', "", line, re.M|re.S)
				# remove '"' and everything after
				line = re.sub('".*', "", line, re.M|re.S)
				line = line.rstrip()
				lotIDs.append(line)
				continue
			if re.search("Grade", line):
				# remove from beginning of line to '<BR>'
				line = re.sub('^.*<BR> ', "", line, re.M|re.S)
				# remove ' -' and everything after
				line = re.sub(' -.*', "", line, re.M|re.S)
				line = line.rstrip()
				grades.append(line)
				continue
			if re.search ("ProdPrice", line):
				# remove from beginning of line to '> $'
				line = re.sub('^.*>\s+\$', "", line, re.M|re.S)
				# remove '<' and everything after
				line = re.sub('<.*', "", line, re.M|re.S)
				line = line.rstrip()
				prices.append(line)
			if re.search("Notes", line):
				# if 'Notes' is found in a line, then the next line will contain 
				# the actual Note that we can parse out, we set notesNext = True
				# and on the next line we begin by parsing for the Note
				notesNext = True
				continue

		item_count = len(lotIDs)

		for i in range(item_count):
			print "++Found item++"
			print "lotID: " + lotIDs[i]
			print "Grade: " + grades[i]
			print "Price: " + prices[i]
			print "Notes: " + str(notes[i])
			items.append(lotIDs[i],grades[i],prices[i],notes[i])
			
		if item_count == 0 or item_count < max_items_per_page:
			last_page_bool = True
			print "Last page has been reached"

	total_item_count = str(len(items.dictionary['lotID']))
	print total_item_count + " items found for contentID: " + contentID

	return items

if __name__ == "__main__":
    main()