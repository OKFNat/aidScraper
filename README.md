Austrian aid scraper
==============================
The scraper extracts information from the EU arms export reports between 2005 and 2013, which is very hard to read for machines. The automatically extracted information is then stored in different data structures (network, country specific) and file formats (CSV, JSON), which are relevant for the next steps, like network analysis, visualization and statistical analysis.

Scrapes data for all development cooperation projects on Austrian Development Cooperation website

- Team: Gute Taten für gute Daten Project (Open Knowledge Austria)
- Status: Production
- Documentation: English
- License: [MIT License](http://opensource.org/licenses/MIT)
- Website: [Gute Taten für gute Daten project](http://okfn.at/gutedaten/) 

**Used software**
The sourcecode is written in Python 2. It was created with use of [iPython](http://ipython.org/), [BeautifulSoup4](http://www.crummy.com/software/BeautifulSoup/) and [urllib2](https://docs.python.org/2/library/urllib2.html).

**Copyright**

All content is openly licensed under the [Creative Commons Attribution 4.0](http://creativecommons.org/licenses/by/4.0/) license, unless otherwisely stated.

All sourcecode is openly licensed under the [MIT license](http://opensource.org/licenses/MIT), unless otherwisely stated.

## SCRAPER

**Description**

The scraper fetches the html passed in as urls from a csv file and stores them locally. The html is then parsed with BeautifulSoup4. Every table between the requested start country and end country is parsed out row by row, cell by cell and stored into a JSON structure with importing countries -> exporting countries -> arms classes -> data. The data structure is then  used to create nodes and edges files as JSON and CSV. This can also be used to extract country specific data to understand imports and exports from a country's perspective.

**Run scraper**
Go into the root folder of this repository and execute following commands in your terminal:
```
cd code
python aid-scraper.py
```

## DATA INPUT
The original data is from the project list of the austrian development agency (ADA) [published on their website](http://www.entwicklung.at/nc/zahlen-daten-und-fakten/projektliste/?tx_sysfirecdlist_pi1[test]=test&tx_sysfirecdlist_pi1[mode]=1&tx_sysfirecdlist_pi1[sort]=uid%3A1&tx_sysfirecdlist_pi1[pointer]=). The data consists of all contracts approved since January 1st of 2010 in chronological order. The date of the last update can be found on the first table page as "Datum der letzten Aktualisierung".

### The Tables
The tables are the basic data, where most of the data is parsed out. The data is published in the following structure (e. g. first project in the list).


| Vertragsnummer | Vertragstitel | Land/Region | OEZA/ADA-Vertragssumme | Vertragspartner |
|----------------|---------------|-------------|------------------------|-----------------|
| 2325-02/2016 | Programm zum Schutz der MenschenrechtsverteidigerInnen in der westlichen Region Guatemalas | Guatemala | EUR 64.300,00 | HORIZONT3000 - Österreichische Organisation für Entwicklungszusammena |

**Attributes**
- Vertragsnummer: contract number of project.
- Vertragstitel: title of project.
- Land/Region: country or region, where project takes place at.
- OEZA/ADA-Vertragssumme: amount of money granted by contract.
- Vertragspartner: partner(s) in the project.


### The project pages
When you click on the contract titel in a table you get to the project page. It consists of the same data as the table view, except the additional description text (named "Beschreibung").

### Soundness
- So far, we can not say anything about the data quality (completeness, accurateness, etc.), but there are also so far no reaseons to doubt the quality.

## DATA OUTPUT

**raw html**

The scraper downloads all raw html of each table and each project page.

**aid data JSON**

The parsed data is stored in an easy-to-read JSON file for further usage.
```
[
	{
		'contract-number': contract number of the project
		'contract-title': title of the project
		'country-region': country and/or region, where the project takes place
		'OEZA-ADA-contract-volume': amount of funding by austrian development agency
		'contract-partner': partner organisation(s)
		'description': description text of the project
		'url': url of the project page
	},
]
```

**aid data csv**

The parsed data is stored in a human-readable CSV file for further usage.

columns (see attribute description above):
- contract-number
- contract-title
- OEZA-ADA-contract-volume
- contract-partner
- country-region
- description
- url

row: one project each row.

## STRUCTURE
- [README.md](README.md): Overview of repository
- [CHANGELOG.md](README.md): Overview of repository

## TODO
**important**
- verify the data
- research: is there a difference between approved funding and paid one?

**optional**
- create dataset for network analyses: json, csv for gephi and networkX
- update code to Python3
- compare data from tables with data from project pages.

**new features**
- analyze and visualize the data: networkX, maps, Gephi
- add country namecodes for easier combinating with other data

## CHANGELOG
### Version 0.2 - 2015-10-29
**init repo**





