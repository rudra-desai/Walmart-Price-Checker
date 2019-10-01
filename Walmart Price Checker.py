import requests
from urllib.request import urlopen as uReq
import time
from bs4 import BeautifulSoup as soup
import re

def find_nth_overlapping(haystack, needle, n):
    start = haystack.find(needle)
    while start >= 0 and n > 1:
        start = haystack.find(needle, start+1)
        n -= 1
    return start


title_or_link = int(input("Enter 1 to search the price by title or 2 to search the price by link: "))
name = ""

if title_or_link == 2:
    url = input("Paste the url from walmart: ")
    uClient = uReq(url)
    page = uClient.read()
    uClient.close()
    soup = soup(page, "html.parser")
    nameLine = str(soup.findAll("h2", {"class" : "prod-ProductTitle no-margin font-normal heading-b"}))
    name = (nameLine[nameLine.index('content=')+9 : nameLine.index('">')])
    priceLine = str(soup.findAll("span", {"class" : re.compile("^price display-inline-block arrange-fit price")}))
    price = float(priceLine[priceLine.index("$")+1:priceLine.index("</")])
    print ("\n" + name)
    print (price)
    
elif title_or_link == 1:
    search = input("Search by Title: ").replace(" " , "+")
    link = ("https://www.walmart.com/search/?query=%s" % search)
    uClient = uReq(link)
    page = uClient.read()
    uClient.close()
    links_with_text = []
    soup = soup(page, "html.parser")
    nameLine = soup.findAll('a', attrs={'href': re.compile("^/ip")})
    allProducts = {}
    prodcutName = ""
    counter = 1
    for links in soup.findAll('a', attrs={'href': re.compile("^/ip")}):
        link_with_name = str(links.get('href'))
        actualLink = str("https://www.walmart.com" + link_with_name)
        prodcutName = (link_with_name[link_with_name.index("ip/")+3 : find_nth_overlapping(link_with_name, "/", 3)])
        allProducts[str(counter) + ": " + prodcutName] = actualLink
        counter+=1
    for key in allProducts:
        print(key)
    whichOne = input("Which product would you like to check the price for?: ")
    if [value for key, value in allProducts.items() if whichOne in key.lower()]:
        for key in allProducts:
            if whichOne in key.lower():
                getPrice = allProducts[key]
                name = key
    
    print(getPrice)            
    uClient = uReq(getPrice)
    page = uClient.read()
    uClient.close()
    priceLine = str(soup.findAll("span", {"class" : re.compile("^price display-inline-block arrange-fit price")}))
    price = float(priceLine[priceLine.index("$")+1:priceLine.index("</")])
    print("\n" + name)
    print (price)



   
