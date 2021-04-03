#!/usr/bin/env python3

'''
    Hello!  This is for downloading reviews from fanfiction.net.
    Just run this file with the URL, where you want to save it,
    and how many pages there are, or -1 or blank for just one page.

    Examples:
    ./save.py https://www.fanfiction.net/r/11911497/ first_page
    ./save.py https://www.fanfiction.net/r/11911497/ tff_reviews_chapter 15
    ./save.py https://www.fanfiction.net/r/11911497/0/ tff_reviews 336

    The output file name should have no ending, like "file"

    If you just want one page, it downloads the exact URL given:
        https://www.fanfiction.net/r/13520979/
    If there's multiple, make sure to go to a later page, then copy the URL
        except for the last number and /.  It'll look like this before:
        https://www.fanfiction.net/r/13520979/0/2/
    The /0/ means reviews of all chapters and the /2/ means the second page.
    To download it all, delete the 2/ so the URL looks like this:
        https://www.fanfiction.net/r/13520979/0/
        and write how many pages of reviews there are as the next parameter.
    Alternatively, to download all reviews chapter by chapter
        (like if there's a ton of reviews per chapter),
        do a multi-page download with the base URL and # of chapters:
        https://www.fanfiction.net/r/13520979/ 15

'''

from bs4 import BeautifulSoup
import cloudscraper
from datetime import datetime
import random
import sys
import time

# specify if you want a TSV, one page HTML file, and/or each page separately
TSV = True
ONE_PAGE = True
MULTIPLE = True
DEBUG = False
PROGRESS = False

def main():
    # if there are not 2-3 arguments, exit
    if len(sys.argv) != 4 and len(sys.argv) != 3:
        print("Usage: ./save.py <url> <file> <pages>")
        exit(1)
    else:
        url = sys.argv[1]
        out_file = sys.argv[2]
        if len(sys.argv) == 4:
            pages = int(sys.argv[3])
        else:
            pages = -1
        if pages == 1:
            pages = -1

    # create scraper to bypass cloudflare, always download mobile pages
    options = {"desktop": False, "browser": "chrome", "platform": "android"}
    scraper = cloudscraper.create_scraper(browser=options)

    # also create tab-separated file of reviews
    # format: chapter   date    user    userid  review
    if TSV:
        tsv = open(out_file + ".tsv", "w")
        tsv.write("Chapter\tDate\tUser\tUser ID\t Review\t{}\n".format(url))


    # if there is only one page, save it
    if pages == -1:
        page = scraper.get(url).text
        # save file
        if ONE_PAGE or MULTIPLE:
            with open(out_file + "html", "w") as f:
                f.write(page)
        # process and write to tsv
        if TSV:
            write_tsv(tsv, page)

    # if there are multiple pages download 1-n
    else:
        mixed_soup = None

        for p in range(1, pages+1):
            page = scraper.get(url + str(p) + "/").text

            # if saving as one page, they'll have to be parsed.
            if ONE_PAGE:
                mixed_soup = write_one_page_html(mixed_soup, page, p)

            if MULTIPLE:
                # if saving as multiple pages, add number to end of file names
                numbered_file = out_file + "_" + str(p) + ".html"
                soup = write_multipage_html(page, p, out_file)
                with open(numbered_file, "w") as f:
                    f.write(soup.prettify())

            # process and write to tsv
            if TSV:
                write_tsv(tsv, page)

            # print dot to indicate progress; pause between requests
            if PROGRESS:
                print(".", end="", flush=True)
            if p != pages:
                time.sleep(9 + random.randint(1, 11))
        if PROGRESS:
            print()

        if ONE_PAGE:
            with open(out_file + ".html", "w") as f:
                f.write(mixed_soup.prettify())


    if TSV:
        tsv.close()


def write_multipage_html(page, p, out_file):
    soup = BeautifulSoup(page, "html5lib")
    # make links absolute, not relative, except for nav links
    for link in soup.find_all("a"):
        if link.parent.get("id") == "d_menu":
            n = link["href"].split("/")[-2]
            link["href"] = out_file + n + ".html"
        elif link.get("href") != None and link["href"].startswith("/"):
            link["href"] = "https://m.fanfiction.net" + link["href"]
    # delete extraneous stuff
    for s in soup.find_all("script"):
        s.decompose()
    for s in soup.find_all("link"):
        s.decompose()
    for img in soup.find_all(class_="mt"):
        if img.parent.name == "a":
            img.parent.decompose()
    img = soup.find(class_="mt")
    img.replace_with("Reviews")
    # add key css
    css = soup.find("style")
    css.append(".pull-right {float: right;}")
    css.append(".gray {color: #686868;}")
    css.append("a {color: #0f37a0; text-decoration: none;}")
    css.append("a:hover {border-bottom: solid 1px #357bd6;}")

    return soup


def write_one_page_html(mixed_soup, page, p):
    this_soup = BeautifulSoup(page, "html5lib")
    # make links absolute, not relative
    for link in this_soup.find_all("a"):
        if link.get("href") and link["href"].startswith("/"):
            link["href"] = "https://m.fanfiction.net" + link["href"]

    # If this is the first page, delete some extraneous stuff and return it
    if p == 1:
        for s in this_soup.find_all("script"):
            s.decompose()
        for s in this_soup.find_all("link"):
            s.decompose()
        for img in this_soup.find_all(class_="mt"):
            if img.parent.name == "a":
                img.parent.decompose()
        img = this_soup.find(class_="mt")
        img.replace_with("Reviews")
        nav = this_soup.find(id="d_menu")
        if nav:
            nav.decompose()
        # add key css
        css = this_soup.find("style")
        css.append(".pull-right {float: right;}")
        css.append(".gray {color: #686868;}")
        css.append("a {color: #0f37a0; text-decoration: none;}")
        css.append("a:hover {border-bottom: solid 1px #357bd6;}")

        return this_soup

    # Otherwise, pull out the reviews to add them.
    reviews = this_soup.select("div.bs.brb")
    for rev in reviews:
        # Every other page, flip the invisible coloring.
        if p % 2 == 0:
            if "alto" in rev["class"]:
                rev["class"].remove("alto")
            else:
                rev["class"].insert(1, "alto")
        # add them to the correct list
        rev_list = mixed_soup.find(id="content")
        rev_list.append(rev)

    return mixed_soup


def write_tsv(tsv, page):
    # format: chapter   date    user    userid  review
    soup = BeautifulSoup(page, "html5lib")
    reviews = soup.select("div.bs.brb")
    for rev in reviews:
        if DEBUG:
            print("\n\n\n\n\n\nREVIEW")
            print(rev)
        chapter = rev.span.text.split()[1].strip("c")
        # sometimes there's two spans and sometimes there's three
        date = rev.span.span
        if date.get("data-xutime") != None:
            date = int(date["data-xutime"])
        else:
            date = int(date.span["data-xutime"])
        date = datetime.utcfromtimestamp(date).strftime('%Y-%m-%d %H:%M:%S')
        user = rev.contents[1].string
        if rev.contents[1].name == "a":
            uid = rev.contents[1]["href"].split("/")[2]
        else:
            uid = -1
        # Okay, so this is annoying, but idk how else to do it.
        # This eliminates all tags (just <br/>s, as far as I know),
        # then replaces the newlines with <br/> tags so the file works.
        # You can sub \n for <br/> in Excel or Numbers.
        text = rev.contents[3:]
        text = "".join(filter(lambda x: x.name==None, text))
        text = text.replace("\n", "<br/>")

        tsv.write("{}\t{}\t{}\t{}\t{}\n".format\
            (chapter, date, user, uid, text))


if __name__ == '__main__':
    main()
