boomscraper
===========

The purpose of this program is to scrape [CowBoom](www.cowboom.com), an electronics retail website, for it's current inventory.

There are four files here:

- main - Imports functions from all the other files and runs a scan of the entire site
- scanForSections - Scans cowboom.com for categories and subcategories (such as 'Electronics': 'Home Electronics')
- scanForProducts - Scans subcategories for products (such as 'Sanyo 47 LCD TV')
- scanForItems - Scans products for individual purchasable items

You can run `python main.py` to scan the whole site or all of the scripts can also run on their own. The scanEntireSite function in main.py makes use of all of the functionality in the project.

This program was broken up into functions so that different types of scans could be run at different intervals. For instance, if you were to automate this, scanning the main site for new products probably doesn't need to run with the same frequency as scanning the 'hot' products for new purchasable stock. Obviously, this would be a personal choice of anybody making use of this code to implement it that way.

This was all written in Python2 and is free to reuse and repurpose per the MIT License.

How to use this programs?
