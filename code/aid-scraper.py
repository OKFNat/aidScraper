#!/bin/env python2
# -*- coding: utf-8 -*-

"""
Fetches, parses and stores the data from the austrian aid projects website since January 1st 2010. 
"""

import urllib2
import bs4
from bs4 import BeautifulSoup
from datetime import datetime
import re
import json
import os
import string
import time

__author__ = "Christian Goebel, Stefan Kasberger"
__copyright__ = "Copyright 2015"
__license__ = "MIT"
__version__ = "0.3"
__maintainer__ = "Stefan Kasberger"
__email__ = "mail@stefankasberger.at"
__status__ = "Production" # 'Development', 'Production' or 'Prototype'

###    GLOBAL   ###

ROOT_FOLDER = os.path.dirname(os.getcwd())
FOLDER_RAW_HTML = ROOT_FOLDER + '/data/raw/html/'
FOLDER_CSV = ROOT_FOLDER + '/data/csv/'
FOLDER_JSON = ROOT_FOLDER + '/data/json/'
FILENAME_BASE = 'aid-data'
BASE_URL = 'http://www.entwicklung.at/nc/zahlen-daten-und-fakten/projektliste/'
QUERY_URL = BASE_URL + '?tx_sysfirecdlist_pi1[test]=test&tx_sysfirecdlist_pi1[mode]=1&tx_sysfirecdlist_pi1[sort]=uid%3A1&tx_sysfirecdlist_pi1[pointer]='
DELAY_TIME = 5 # in seconds
# TS = datetime.now().strftime('%Y-%m-%d-%H-%M')
TS = '2016-04-03-03-05'

###    FUNCTIONS   ###

def SetupEnvironment():
	"""Sets up the folder structure and working environment.
	"""
	if not os.path.exists(FOLDER_RAW_HTML):
		os.makedirs(FOLDER_RAW_HTML)
	if not os.path.exists(FOLDER_JSON):
		os.makedirs(FOLDER_JSON)
	if not os.path.exists(FOLDER_CSV):
		os.makedirs(FOLDER_CSV)

def FetchHtml(url):
	"""Fetches html url via urllib2.
	
	Args:
		url: url to fetch (string).
	
	Returns:
		html: html string as unicode.
	"""
	response = urllib2.urlopen(url)
	html = response.read().decode('utf-8')
	time.sleep(DELAY_TIME)
	
	return html

def FetchHtmlTables(url, folder, pageCounter = 0):
	"""Fetches each overview page with the table of the projects and saves the html locally.
	
	Args:
		url: string to fetch.
		folder: directory to save the html files in.
		pageCounter: counter for the actual number of the page (int).
	"""
	# the url has a page-counter at the end, so just increase the counter and fetch one page after another
	rawHtml = FetchHtml(url+str(pageCounter))

	if not os.path.exists(folder+TS):
		os.makedirs(folder+TS)
	Save2File(rawHtml, folder+TS+'/'+TS+'_table-'+str(pageCounter)+'.html')
	# checks if there is a "weiter" (more) anchor, cause this means a next page exists
	isWeiter = re.findall(r'<a href="(.*)" >weiter &gt;</a></div></div>', rawHtml)
	if isWeiter:
		pageCounter += 1
		FetchHtmlTables(url, folder, pageCounter)

def FetchHtmlProjects(aidData, folder):
	"""Fetches html of the project pages and saves the html locally.
	
	Args:
		aidData: list[] of dict{} of aid projects.
		folder: directory to save the html files in.
	
	Returns:
		aidData: list[] of dict{} of aid projects.
	"""
	if not os.path.exists(folder+TS):
		os.makedirs(folder+TS)
	# iterate over every list element to fetch and store the project page
	for idx, project in enumerate(aidData):
		html = FetchHtml(project['url'])
		Save2File(html, folder+TS+'/'+TS+'_project-'+str(idx)+'.html')

	return aidData

def Save2File(data, filename):
	"""Saves a file locally.
	
	Args:
		data: string to save.
		filename: name of the file with path.
	"""
	text_file = open(filename, "w")
	text_file.write(data.encode('utf-8'))
	text_file.close()

def ReadFile(filename):
	"""Reads a file and returns the string.
	
	Args:
		filename: name of the file
	
	Returns:
		string: file as text-string.
	"""
	f = open(filename, 'r')
	string = f.read()
	
	return string

def ReadTableFilesInFolder(folder):
	"""Reads in all table html-files from a folder.
	
	Args:
		folder: folder where the html-files are stored in.
	
	Returns:
		sortedList: list[] of sorted html texts.
	"""
	htmlList = []
	sortedList = []

	for filename in os.listdir(folder):
		if filename.find(TS+'_table') >= 0:
			rawHtml = ReadFile(folder+'/'+filename)
			fileIndex = filename.split('.')[0].split('-')[5]
			htmlList.append((int(fileIndex), rawHtml))
	# sort list of duppels after first element (the filename postfix) and store to list[]
	htmlList = sorted(htmlList, key=lambda htmlList: htmlList[0])
	for idx, html in htmlList:
		sortedList.append(html)

	return sortedList

def ReadProjectFilesInFolder(aidData, folder):
	"""Reads in all table html-files from a folder.
	
	Args:
		aidData: list[] of dict{} of aid projects.
		folder: folder where the html-files are stored in.
	
	Returns:
		sortedList: list[] of sorted html texts.
	"""
	htmlList = []
	sortedList = []

	for filename in os.listdir(folder):
		if filename.find(TS+'_project') >= 0:
			rawHtml = ReadFile(folder+'/'+filename)
			fileIndex = filename.split('.')[0].split('-')[5]
			htmlList.append((int(fileIndex), rawHtml))
	
	# sort list of duppels after first element (the filename postfix) and store to list[]
	htmlList = sorted(htmlList, key=lambda htmlList: htmlList[0])
	for idx, html in htmlList:
		sortedList.append(html)

	return sortedList

def ParseTables(html):
	"""Parses each row of the html table.
	
	Args:
		html: list[] of duppels (filename, html).
	
	Returns:
		aidData: list[] of dict{} of aid projects.
			'contract-number': contract number.
			'contract-title': title of the project.
			'country-region': country and/or region, where the project takes place.
			'OEZA-ADA-contract-volume': amount of funding.
			'contract-partner': partner organisation(s).
			'url': url of the project page.
	"""
	aidData = []
	counter = 1

	for page in html:
		soup = BeautifulSoup(page)
		table = soup.find_all('table')[1]
		for row in table.find_all('tr')[1:]:
			project = {}
			tds = row.find_all('td')
			project['unique-id'] = str(counter)
			project['contract-title'] = tds[1].div.text
			project['url'] =tds[1].div.a['href']
			project['country-region'] = tds[2].div.text
			project['OEZA-ADA-contract-volume'] = tds[3].div.text
			project['contract-partner'] = tds[4].div.text
			project['contract-number'] = tds[0].div.text
			aidData.append(project)
			counter += 1
	
	return aidData

def ParseProjects(aidData, htmlProjects):
	"""Parses the description of every project page.
	
	Args:
		aidData: list[] of dict{} of aid projects.
		htmlProjects: list[] of html texts.
	
	Returns:
		aidData: list[] of dict{} of aid projects.
			'unique-id': unique id for each project.
			'contract-number': contract number.
			'contract-title': title of the project.
			'country-region': country and/or region, where the project takes place.
			'OEZA-ADA-contract-volume': amount of funding.
			'contract-partner': partner organisation(s).
			'description': description text of the project.
			'url': url of the project page.
	"""
	for idx, html in enumerate(htmlProjects):
		soup = BeautifulSoup(html)
		aidData[int(idx)]['description'] = soup.find_all('table')[0].find_all('tr')[5].find_all('div')[1].text
	
	return aidData

def SaveAidData(aidData, filename):
	"""Saves the aid data as JSON file.
	
	Args:
		aidData: list[] of dict{} of aid projects.
		filename: filepath of the JSON file. 
	"""
	Save2File(json.dumps(aidData, indent=2, ensure_ascii=False), filename)
	print 'Aid data exported as JSON:',filename

def OpenAidData(filename):
	"""Opens the aid data JSON file.
	
	Args:
		filename: filepath of the JSON file.
	"""
	aidData = json.loads(ReadFile(filename))
	
	return aidData

def Save2CSV(data, filename):
	"""Exports the aid data into a csv file.
	
	Args:
		data: list[] of dict{} of aid projects.
		filename: filepath.
	"""
	csvString = '"unique-id","contract-number","contract-title","OEZA-ADA-contract-volume","contract-partner","country-region","description","url"\n'
	# iterate over each project
	for project in data:
		uniqueId = '""'
		number = '""'
		title = '""'
		funding = '""'
		partner = '""'
		region = '""'
		description = '""'
		url = '""'
		# read out each attribute
		for elem in project.keys():
			val = project[elem].replace('"', '').replace('\n', '').replace('\r', '') # replace apostrophes.
			if elem == 'unique-id':
				uniqueId = '"'+val+'"'
			if elem == 'contract-number':
				number = '"'+val+'"'
			if elem == 'contract-title':
				title = '"'+val+'"'
			if elem == 'OEZA-ADA-contract-volume':
				funding = '"'+val+'"'
			if elem == 'contract-partner':
				partner = '"'+val+'"'
			if elem == 'country-region':
				region = '"'+val+'"'
			if elem == 'description':
				description = '"'+val.strip('\n\r')+'"'
			if elem == 'url':
				url = '"'+val+'",'
			
		csvString += uniqueId+','+number+','+title+','+funding+','+partner+','+region+','+description+','+url+'\n'

	Save2File(csvString, filename)
	print 'Aid data exported as CSV:',filename

if __name__ == "__main__":

	# setup
	startTime = datetime.now()
	print 'start:', startTime
	aidData = []
	SetupEnvironment()
	DOWNLOAD_FILES = False
	PARSE_FILES = False
	STRUCTURE_DATA = True

	if DOWNLOAD_FILES:
		FetchHtmlTables(QUERY_URL, FOLDER_RAW_HTML) # html as string
		htmlTables = ReadTableFilesInFolder(FOLDER_RAW_HTML+TS) # html as string
		aidData = ParseTables(htmlTables)
		SaveAidData(aidData, FOLDER_JSON+'aid-data_'+TS+'.json')
		FetchHtmlProjects(aidData, FOLDER_RAW_HTML)
	
	if PARSE_FILES:
		htmlTables = ReadTableFilesInFolder(FOLDER_RAW_HTML+TS) # html as string
		aidData = ParseTables(htmlTables)
		htmlProjects = ReadProjectFilesInFolder(aidData, FOLDER_RAW_HTML+TS) # html as string
		aidData = ParseProjects(aidData, htmlProjects)
		SaveAidData(aidData, FOLDER_JSON+'aid-data_'+TS+'.json')

	if STRUCTURE_DATA:
		aidData = OpenAidData(FOLDER_JSON+'aid-data_'+TS+'.json')
		Save2CSV(aidData, FOLDER_CSV+'aid-data_'+TS+'.csv')
	
	print 'runtime:', (datetime.now() - startTime)
