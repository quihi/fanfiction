#!/usr/bin/env python3

# This is python code that will download the requests in an exchange on Archive of Our Own and create a spreadsheet.
# (or, well, a tab-separated file that you can paste into Google Sheets or something.)
# To use, replace REQUESTS with the page that your requests are on
#         replace [user] in HEADERS with your username
#         replace PAGES with the number of pages of requests you want to summarize
#         replace the shortcuts on line 38-39 on ones for your fandoms, if you so desire
#         verify if you want to cut off parts of your tags - see lines 44 and 55

from bs4 import BeautifulSoup
import requests
import time

REQUESTS = "https://archiveofourown.org/collections/RigelBlackEx_Round3/requests?page="
HEADERS = { "User-Agent": "[user]-bot" }
PAGES = 10
DELAY = 10
DEBUG = False

def main():
    for p in range(1, PAGES+1):
        link = REQUESTS + str(p)
        r = requests.get(link, headers=HEADERS)
        soup = BeautifulSoup(r.text, "html5lib")

        reqs = soup.find_all("li", class_=" blurb group")
        for blurb in reqs:
            if DEBUG:
                print("\n\n\n\n\n\nBLURB")
                print(blurb)
            person = blurb.find("h4")
            person = person.text.replace("Request", "").replace("by ", "").strip()
            if DEBUG:
                print(person)
            fandom = blurb.find(class_="fandoms heading")
            fandom = fandom.text.replace("Fandom:", "").strip()
            fandom = fandom.replace("Revolutionary Arc - kitsunerei88", "Rev Arc")
            fandom = fandom.replace("Rigel Black Chronicles - murkybluematter", "RBC")
            if DEBUG:
                print(fandom)
            relationships = blurb.find_all("li", class_="relationships")
            relationships = map(lambda x: x.text, relationships)
            relationships = ", ".join(relationships).replace(" - Relationship", "")
            if DEBUG:
                print(relationships)
            characters = blurb.find_all("li", class_="characters")
            characters = map(lambda x: x.text, characters)
            characters = "\t".join(characters)
            if DEBUG:
                print(characters)
            mediums = blurb.find_all("li", class_="freeforms")
            mediums = map(lambda x: x.text, mediums)
            mediums = ", ".join(mediums)
            mediums = mediums.replace(" - Freeform", "").replace("Medium: ", "")
            if DEBUG:
                print(mediums)
            userstuff = blurb.find("blockquote", class_="userstuff summary")
            if userstuff == None:
                notes = "N/A"
                letter = "N/A"
            else:
                notes = userstuff
                notes = userstuff.text.strip().replace("\n", "⏎").replace("\t", " ")
                letter = userstuff.find_next_sibling("p")
                if letter == None:
                    letter = "N/A"
                else:
                    letter = letter.a.text
            if DEBUG:
                print(notes)
                print(letter)

            print("{}\t{}\t{}\t{}\t{}\t{}\t{}".format(person, fandom, relationships, mediums, notes, letter, characters))
        time.sleep(DELAY)



if __name__ == '__main__':
    main()
