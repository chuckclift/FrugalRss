#!/usr/bin/python3

import time
import requests
import htmlParser

urlFile = open("newsURL.txt")
urls = urlFile.read().split("\n")
urlFile.close()

##accessing each of the urls of the rss web pages
##these will be used to get the links to the articles
siteHtml = []
for i in urls:
    if len(i) > 0:
        container = requests.get(i)
        container = container.text
        siteHtml.append(container)


metaData = []

for html in siteHtml:
    items = html.split("<item>")
    items = items[1:-1]  ##removing the first element (where ther are no items)
    siteData = []

    for it in items:
        title = it.split("<title>")[1].split("</title>")[0]
        link = it.split("<link>")[1].split("</link>")[0]
        siteData.append((title,link))
    metaData.append(siteData)
sitesRemoved = 0



##getting the article html documents
##the urls are shuffled so that the program is
##not accessing any one server consecutively
##except at the end 


htmlData = []
while metaData:
    for site in metaData:
        if len(site) > 0:
            workingData = site.pop()
            html = requests.get(workingData[1])
            html = html.text
            htmlData.append((workingData[0],html))
            
            print(workingData[0])

            ##this prevents the program from hitting one
            ##server consecutively too quickly
            if len(metaData) > 2:
                time.sleep(3)
                
        else:
            metaData.remove(site)


##extracting the text from the html in htmlData
finalData = []
for i in htmlData:
    article = ( "<title>" + i[0] + "</title>" + 
              "<article>" + htmlParser.getParagraphs(i[1]) + "</articles>")
    finalData.append((i[0],article)) 

##writing the results to the text files
headlines = open("headlines.txt","w", encoding="utf-8")
articles = open("articles.txt","w", encoding="utf-8")

for i in finalData:
    headlines.write(i[0] + "\n")
    articles.write(i[1] + "\n")

headlines.close()
articles.close()
