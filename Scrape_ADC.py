#!/usr/bin/python
# -*- coding: utf8 -*-

from urllib.request import urlopen
from bs4 import BeautifulSoup
import bs4
import requests
from datetime import datetime
import datetime
import csv
import time
import re
import json

def save_to_file(data, filename):
    text_file = open(filename, "w")
    text_file.write(data)
    text_file.close()
    
def getlinks ():
	addresses = []
	for counter in range (0, 45): #when this scraper was written, there were altogether 44 pages
		print ('getting links page '  + str (counter))
		txt_doc='http://www.entwicklung.at/nc/zahlen-daten-und-fakten/projektliste/?tx_sysfirecdlist_pi1%5Btest%5D=test&tx_sysfirecdlist_pi1%5Bmode%5D=1&tx_sysfirecdlist_pi1%5Bsort%5D=uid%3A1&tx_sysfirecdlist_pi1%5Bpointer%5D=' + str(counter)
		soup = BeautifulSoup(urlopen(txt_doc), 'html.parser')
		for item in soup.find_all ('a'):
			if 'href' in item.attrs:
				if "http://www.entwicklung.at/zahlen-daten-und-fakten/projektliste/?" in item['href']:
					addresses.append (item['href'])
	return addresses

def striphtml (data):
    p = re.compile(r'<.*?>')
    return p.sub('', data)
    

if __name__ == "__main__":
	addresses = getlinks ()
	data = []
	
	l = len (addresses)
	k = 1
	print ("downloaded %s addresses" % str (l))
	
	for address in addresses:
		elem = {}
		response = requests.get (address)
		soup2 = bs4.BeautifulSoup (response.text)
		content = soup2.find_all ('div', {'cdcontentdiv'})
		
		aktualisierung = soup2.find_all ('div', id= 'c3936')
		div = aktualisierung [0].find_all('div')
		date=div[0].contents
		Aktualisierungsdatum = date[0].replace('\xa0', '') 
		
		elem["Link"] = address
		elem["Vertragsnummer"] = striphtml (str (content [0]))
		elem["Vertragstitel"]= striphtml (str (content [1]))
		elem["LandRegion"]= striphtml (str (content [2]))
		elem["Vertragspartner"]= striphtml (str (content [3]))
		elem["Vertragssumme"]= striphtml (str (content [4]))
		elem["Beschreibung"]= striphtml (str(content [5]))
		ts = time.time()
		elem["Timestamp"] = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
		elem["Aktualisierungsdatum"]=Aktualisierungsdatum
		print ("downloaded %s of %s entries" % (k, l))
		k = k+1
		
		data.append(elem)
	save_to_file(json.dumps(data, indent=2), 'Entwicklunghilfe.json')
