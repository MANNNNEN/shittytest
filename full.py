import requests
import json
import csv
from bs4 import BeautifulSoup
from alive_progress import alive_bar

print('''

                   __  __                               
                  / _|/ _|                              
  _ __  _ __ ___ | |_| |_ ___  ___ _ __ __ _ _ __   ___ 
 | '_ \| '__/ _ \|  _|  _/ __|/ __| '__/ _` | '_ \ / _ \ 
 | |_) | | | (_) | | | |_\__ \ (__| | | (_| | |_) |  __/
 | .__/|_|  \___/|_| |_(_)___/\___|_|  \__,_| .__/ \___|
 | |                                        | |         
 |_|                                        |_|         

''')
print("Paste link from proff:")
userlink = input()
print()
print("Enter output filename:")
outputfile = input()+".csv"

viewjson = "&view=json"
url = userlink+viewjson
proff = "https://www.proff.no"


keep_looping = True

#create list scraped
scraped = []
print("")
print("Fetching urls")
with alive_bar(len(scraped)) as bar:
    while keep_looping:

        #json vars / get json
        jsonpage = requests.get(url)
        jsondata = jsonpage.text
        jsonsoup = BeautifulSoup(jsondata, "lxml")
        json_load = json.loads(jsonsoup.string) #
        scrape = json_load["createListSearchResult"]["resultList"] #loads the proper json strings
        
        #append to list scraped
        for item in scrape:
            uri = proff+item["uri"].strip() #add proff link front
            scraped_urls = uri
            scraped.append(scraped_urls)
            bar()

        if "next" not in json_load["createListSearchResult"]["pagination"].keys():
            keep_looping = False
        else:
            grab_next = json_load["createListSearchResult"]["pagination"]["next"]["href"] #Grabs next href from json
            url_next = "https://proff.no/laglister/"+grab_next+"/?view=json" #Makes it a link
            url = url_next

print("Done!")
print("")
print("Gathering data")

csvfile = open(outputfile, 'a', newline='')
csvwriter = csv.writer(csvfile)
csvwriter.writerow(["Orgnr", "firmanavn", "Daglig Leder", "Adresse", "Postadresse", "Telefon"])
tlfcount = 0

with alive_bar(len(scraped)) as bar:
    for url in scraped:

        page = requests.get(url)
        soup = BeautifulSoup(page.text, "lxml")

        #scrapes and formats content
        if (soup.find("em", text="Org nr:")):
            orgnr = soup.find("em", text="Org nr:").find_next_sibling().text.replace(" ", "")
        else:
            orgnr = ""

        if (soup.find("em", text="Juridisk navn:")):
            firmanavn = soup.find("em", text="Juridisk navn:").find_next_sibling().text
        else:
            firmanavn = ""
        
        if soup.find("em", text="Daglig leder"):
            daglig_leder = soup.find("em", text="Daglig leder").find_next_sibling().text.strip()
        else:
            daglig_leder = ""
        
        if soup.find("em", text="Adresse:"):
            adresse = soup.find("em", text="Adresse:").find_next_sibling().text
        else:
            adresse = ""

        if soup.find("em", text="Postadresse:"):
            postadresse = soup.find("em", text="Postadresse:").find_next_sibling().text
        else:
            postadresse = ""

        if soup.find("em", text="Telefon:"):
            tlf = soup.find("em", text="Telefon:").find_next_sibling().text.strip().replace(" ", "")
            tlfcount += 1
        else:
            tlf = ""

        #print(orgnr, firmanavn, daglig_leder, adresse, postadresse, tlf)
        csvwriter.writerow([orgnr, firmanavn, daglig_leder, adresse, postadresse, tlf])

        bar()

csvfile.close

print("Done!")
print("")
print("You gathered data from", len(scraped), "businesses")
print("Phonenumbers found:", tlfcount)
print("Data saved in", outputfile)
print("")
