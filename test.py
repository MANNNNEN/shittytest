from bs4 import BeautifulSoup
import requests
import json

#&view=json
viewjson = "&view=json"
url = "https://www.proff.no/laglister?rf=-2486&rt=545948&pf=100&pt=183591045&ef=3&et=3&i=p47431&samplerFilter=true"+viewjson
proff = "https://www.proff.no"


keep_looping = True

#create list  scraped & nextpages
scraped = []
nextpages = []

while keep_looping:
    #normal vars
    page = requests.get(url)
    data = page.content
    soup = BeautifulSoup(data, "lxml")

    #json vars / get json
    jsonpage = requests.get(url)
    jsondata = jsonpage.content
    jsonsoup = BeautifulSoup(jsondata, "lxml")

    json_load = json.loads(jsonsoup.string) #

    scrape = json_load["createListSearchResult"]["resultList"] #loads the proper json strings
    #append to list scraped
    for item in scrape:
        uri = proff+item["uri"] #add proff link front

        scraped_urls = {
            uri
        }
        scraped.append(scraped_urls)
    
    grab_next = json_load["createListSearchResult"]["pagination"]["next"]["href"] #Grabs next href from json
    url_next = "https://proff.no/laglister/"+grab_next+"/?view=json" #Makes it a link

    if not grab_next:
        keep_looping = False
        print("Scrape Done!")
    else:
        url = url_next

    print(len(scraped))


'''
    for item in grabnext:
        nextpage = "https://proff.no/laglister/"+grabnext+"/?view=json"

        scraped_next = {
            nextpage
        }
        nextpages.append(scraped_next)

        nypage = requests.get(nextpage)
        nydata = nypage.content
        nysoup = BeautifulSoup(nydata, "lxml")

    nyjsonload = json.loads(nysoup.string)

    nygrabnext = nyjsonload["createListSearchResult"]["pagination"]["next"]["href"]

    print(nextpages)


#save the links to a txt file

#deal with pagignation

#proff.no/laglister/"string"/?view=json

'''
