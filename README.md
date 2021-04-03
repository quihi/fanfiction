# fanfiction
This is where I am posting the various code I've written for fandom purposes, primarily scripts for scraping AO3 and FFN, but also a few other things.

I know how much of a struggle it can be to get computer-y stuff working, so don't hesitate to message me (on discord, FFN, tumblr, or dreamwidth) if you have any questions, no matter how big or small.

## downloads
I've written some scripts, mainly in python, to scrape data off fanfiction.net and archiveofourown.org.

* ffn_reviews.py : download a copy of a fic's reviews from FFN, saving them as a TSV and as HTML files (with FFN's mobile formatting)
* requests_spreadsheet.py : download the requests in an exchange on AO3, creating a spreadsheet that's easily searched
  * it's set up to put each requested character in their own column, and can be rearranged a bit if you'd like to prioritize a different set of tags
* bookmarks_spreadsheet.py : create a spreadsheet summarizing all of the bookmarks in a collection

## skins
I haven't gotten very deep in Archive of Our Own skins, but the ones I have are here.

Includes:
* article.css : a basic news article format; they're a dime a dozen
* spoilers.css : spoiler text that becomes visible when highlighted
* siteskin.css : my site skin, which:
  * puts summaries and tags into scroll boxes after a certain length
  * makes tags smaller
  * does not underline tags
  * slightly compresses fic blurbs

## ublock
I use uBlock Origin as an adblocker and add my own filters to enhance websites.

See here to:
* regain the ability to highlight text on fanfiction.net
* filter out all explicit works on Archive of Our Own
