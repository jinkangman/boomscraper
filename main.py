#!/usr/bin/python
from scanForSections import parseOrigin
from scanForSections import parseCategories
from scanForProducts import parseProductPages
from scanForItems import parseItemPages
from scanForItems import checkAvailability
from scanForItems import itemList

def main():
	scanEntireSite()

def scanEntireSite():
	"""This function is a script to run through the entire site, locating
	every single purchasable item.

	The site is structured like:
	Cowboom
	/ | \
	Categories
	/ | | \
	Subcategories
	/ / | | \
	Products (lists of items)
	/ / | | \ \
	Individual Items

	We breadth first search to the Subcategories layer and then Depth
	first search down to each item.

	Caveat: There is overlap of Products between different subcategories,
	so it would be wiser to build a list of unique products before scanning
	one layer deeper."""

	# Start at the front page
	categories = parseOrigin()
	print categories
	# If categories were found
	if categories:
		# Scan for subcategories
		siteStructure = parseCategories(categories)
		print siteStructure
		# If subcategories were found
		if siteStructure:
			for category, subcategories in siteStructure.iteritems():
				# Iterate through subcategories
				for subcategory in subcategories:
					# Parse each subcategory for products
					categoryStructure = parseProductPages(category,subcategory)
					print categoryStructure
					# Iterate through products in each subcategory
					for contentID, productName in categoryStructure.iteritems():
						# If in stock
						if checkAvailability(contentID):
							# Start a list of individual items for purchase
							items = itemList()
							items = parseItemPages(contentID,items)
							items.show()

							# Full scan took 19m20.344s
							#                15m34.936s

if __name__ == "__main__":
	main()