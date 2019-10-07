import requests
from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup
import re
import smtplib
import time

def get_Price_by_link (urlLink):
    uClient = uReq(urlLink)
    page = uClient.read()
    uClient.close()
    soup = BeautifulSoup(page, "html.parser")
    nameLine = str(soup.findAll("h2", {"class": "prod-ProductTitle no-margin font-normal heading-b"}))
    name = (nameLine[nameLine.index('content=') + 9: nameLine.index('">')])
    priceLine = str(soup.findAll("span", {"class": re.compile("^price display-inline-block arrange-fit price")}))
    price = float(priceLine[priceLine.index("$") + 1:priceLine.index("</")])
    return (str(name), int(price) , str(urlLink))

def get_Price_by_title(search):
    link = ("https://www.walmart.com/search/?cat_id=0&grid=true&page=1&query=%s" % search)
    uClient = uReq(link)
    page = uClient.read()
    uClient.close()
    links_with_text = []
    soup = BeautifulSoup(page, "html.parser")
    nameLine = soup.findAll('a', attrs={'class': "product-title-link line-clamp line-clamp-2"})
    allProducts = {}
    prodcutName = ""
    counter = 1
    for links in soup.findAll('a', attrs={'href': re.compile("^/ip")}):
        link_with_name = str(links.get('href'))
        actualLink = str("https://www.walmart.com" + link_with_name)
        prodcutName = (link_with_name[link_with_name.index("ip/") + 3: find_nth_occurence(link_with_name, "/", 3)])
        if (str(counter - 1) + ": " + prodcutName) not in allProducts.keys():
            allProducts[str(counter) + ": " + prodcutName] = actualLink
            counter += 1
    for key in allProducts:
        print(key)
    whichOne = input("Which product would you like to check the price for?: ")
    if [value for key, value in allProducts.items()]:
        for key2 in allProducts:
            if whichOne in key2.lower():
                productLink = allProducts[key2]
                name = key2
                break
    return (get_Price_by_link(productLink)[0], get_Price_by_link(productLink)[1], get_Price_by_link(productLink)[2])


def find_nth_occurence(a, b, n):
    start = a.find(b)
    while start >= 0 and n > 1:
        start = a.find(b, start+1)
        n -= 1
    return start

def sendEmail(msg, productName , url):
    server = smtplib.SMTP('smtp.gmail.com', '587')
    server.ehlo()
    server.starttls()
    server.ehlo()

    #replace abc@gmail.com with the sender's email and password with google app passwords
    server.login('abc@gmail.com', "password")
    subject = "Price drop notification!"
    body = "Price went down, The price is now: $" + str(msg) + " for " + productName + "\n" + str(url)

    msg= f"Subject: {subject}\n\n{body}"

    #replace abc@gmail.com and xyz@gmail.com with the sender's and the reciever's email
    server.sendmail("abc@gmail.com","xyz@gmail.com", msg)
    server.quit()


userSelection = int(input("Enter 1 to receive an email when the price drops, Enter 2 to search the price by title or 3 to search the price by link: "))

if userSelection == 1:
    product = int(input("Enter 1 to retrieve product price by title or 2 to retrieve product price by link: "))
    if (product == 1):
        search = input("Search by Title: ").replace(" ", "+")
        productInfo =  get_Price_by_title(search)
        print("\nThe current price of " + productInfo[0] + " is: $" + str(productInfo[1]))
        desiredPrice = int(input("At what price would you like to be notified about the price drop?: "))
        while(True):
            productInfo = get_Price_by_link(productInfo[2])
            if(desiredPrice >= productInfo[1]):
                print("\nThe price went down! You have been emailed!")
                sendEmail(productInfo[1], productInfo[0] , productInfo[2])
                time.sleep(86400)
            else:
                print("\nThe price has not dropped yet, will check again tomorrow")
                time.sleep(86400)

    else:
        actualLink = input("Paste the url from walmart: ")
        productInfo =  get_Price_by_link(actualLink)
        print("\nThe current price of " + productInfo[0] + " is: $" + str(productInfo[1]))
        desiredPrice = int(input("At what price would you like to be notified about the price drop?: "))
        while (True):
            productInfo = get_Price_by_link(productInfo[2])
            if (desiredPrice >= productInfo[1]):
                print("\nThe price went down! You have been emailed!")
                sendEmail(productInfo[1] , productInfo[0] , productInfo[2])
                time.sleep(86400)
            else:
                print("\nThe price has not dropped yet, will check again tomorrow")
                time.sleep(86400)

elif userSelection == 3:
   returnVal = get_Price_by_link(input("Paste the url from walmart: "))
   print("\n{}: ${}".format(returnVal[0], returnVal[1]))
    
elif userSelection == 2:
    search = input("Search by Title: ").replace(" ", "+")
    returnVal =  get_Price_by_title(search)
    print("\n{}: ${}".format(returnVal[0], returnVal[1]))
