#!/usr/bin/env python3

'''
    This downloads metadata about the bookmarks in a collection on
        Archive of Our Own and creates a spreadsheet.
    It will likely work for a user's bookmark's but I haven't tried it.

    To use: replace BOOKMARKS with the URL that you want to summarize
                (be sure to include the ?page= part)
            replace [user] in HEADERS with your username
            replace PAGES with the number of pages of bookmarks there are.
            
            Word counts are not added for external bookmarks.
            This prints to standard output and should be redirected to a file.

            Lines 54-57 search for if a particular series is linked
                (i.e. the fic is in the series) and add a note based on that.
                You can delete that and your own other extra notes.
'''

from bs4 import BeautifulSoup
import requests
import time

BOOKMARKS = "https://archiveofourown.org/collections/RigelBlackComprehensive/bookmarks?page="
HEADERS = { "User-Agent": "[user]-bot" }
PAGES = 15
DEBUG = False

def main():
    for p in range(1, PAGES+1):
        link = BOOKMARKS + str(p)
        r = requests.get(link, headers=HEADERS)
        soup = BeautifulSoup(r.text, "html5lib")

        fics = soup.find_all(class_="bookmark blurb group")
        for blurb in fics:
            if DEBUG:
                print("BLURB")
                print("\n\n")
                print(blurb)
                print("\n\n\n\n\n")

            number = blurb["id"].strip("bookmark_")
            title = blurb.h4.a.string
            # Author is None for non-AO3 fics, since they're text and not links
            author = blurb.find(rel="author")
            if author == None:
                author = blurb.h4.a.next_sibling.replace("by", "").strip()
            else:
                author = author.string
            words = blurb.find(name="dd", class_="words")
            if words is None:
                words = ""
            else:
                words = words.string
            if "/series/1722145" in str(blurb):
                notes = "Rev Arc"
            else:
                notes = ""

            print("{}\t{}\t{}\t{}\t{}".format(number, title, author, words, notes))

        time.sleep(10)


if __name__ == '__main__':
    main()
