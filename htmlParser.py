
def getParagraphs(html):    
    pContent = ""

    ##getting everything that is inside of the p tags
    while True:
        tagOpen = html.find("<p")
        tagClose = html.find("</p")

        pContent = pContent + html[tagOpen:tagClose]
        html = html[tagClose + 3:]

        if tagClose == -1:
            break

    ##getting rid of all tags so the text is readable
    while True:
        tagOpen = pContent.find("<")
        tagClose = pContent.find(">")

        if tagOpen == 0:
            pContent = pContent[tagClose + 1:]
            
        elif tagClose < tagOpen:
            pContent = pContent[tagClose + 1:]
            
        else:
            pContent = pContent[:tagOpen - 1] + pContent[tagClose + 1:]
            
        if tagOpen == -1 or tagClose == -1:
            break
        
    return pContent
        

    
if __name__ == "__main__":
    
    htmlFile = open("html.txt", encoding="utf-8")
    htmlText = htmlFile.read()
    htmlFile.close()
    print(getParagraphs(htmlText))
