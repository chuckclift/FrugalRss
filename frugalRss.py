#!/usr/bin/python3

import time
import requests
import htmlParser

with open("newsURL.txt") as f:
    urls = f.read().split("\n")


# accessing each of the urls of the rss web pages
# these will be used to get the links to the articles
site_html = []
for i in urls:
    if len(i) > 0:
        container = requests.get(i)
        container = container.text
        site_html.append(container)


metadata = []

for html in site_html:
    items = html.split("<item>")

    items = items[1:-1]  ##removing the first element (where ther are no items)
    site_data = []
    for it in items:
        title = it.split("<title>")[1].split("</title>")[0]
        link = it.split("<link>")[1].split("</link>")[0]
        site_data.append((title,link))


    # adding the list of links/titles to a larger list this makes
    # a 2d "matrix" that allows the sites to be separate
    metadata.append(site_data)
sitesRemoved = 0



# getting the article html documents
# the urls are shuffled so that the program is
# not accessing any one server consecutively
# except at the end

html_data = []
while metadata:

    # each iteration of the while loop it goes
    # through the current list of sites
    for site in metadata:
        if len(site) > 0:
            workingData = site.pop()
            html = requests.get(workingData[1])
            print(workingData[1])
            html = html.text
            html_data.append((workingData[0],html))

            # this prevents the program from hitting one
            # server consecutively too quickly
            if len(metadata) > 2:
                time.sleep(3)

        # Removing empty lists
        else:
            metadata.remove(site)



# extracting the text from the html in html_data
article_text = ""
headlineText = ""
for i in html_data:
    
    article_text = article_text + ("<title>" + i[0] + "</title>" +
               "<article>" + htmlParser.get_paragraphs(i[1]) + "</articles>")
    headlineText = headlineText + i[0] + "\n"

# writing the results to files
with open("articles.txt", "w", encoding="utf-8") as a:
    a.write(article_text)

with open("headlines.txt", "w", encoding="utf-8") as h:
    h.write(headlineText)



