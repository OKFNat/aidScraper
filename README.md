Austrian aid scraper
==============================
The scraper extracts information from the austrian development projects since 2010 from the austrian development agency website. The automatically extracted informations are stored in CSV and JSON files to make the further usage as easy as possible.

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

**Original sourcecode**

Thanks to Christian Goebel for the [original sourcecode](https://github.com/ChristianGoebel/Scrape_ADC), which got used for the final version.

### How the scraper works
**Configure the Scraper**

There are two global variables in [aid-scraper.py](code/aid-scraper.py) you may want to change to your needs.
- DELAY_TIME: To not overload the server or may get blocked because of too many request, you should set the delay time to fetch to 1-5 seconds, not less.
- TS: The timestamp as a string can be set to the last download. So you can use downloaded data over and over again and must not do it everytime. When you do it first time, you can set the value to ```datetime.now().strftime('%Y-%m-%d-%H-%M')```, so it is the timestamp when the scraper starts.

**Download the raw html data**

Here all the html raw data gets downloaded, stored locally and the basic data gets parsed.
- Download all overview pages with the tables (html). The navigation for the fetching runs through all overview pages by asking the existance of the "weiter" anchor and counting up an url variable.
- Open the downloaded files.
- Parse out the basic information about each project from the overview tables. This is necessary here, because the download of the project page needs the link from the overview table.
- Store the parsed data as JSON file.
- Download all project pages (html).

**Parse the html**

Here the description of the project gets added to the data.
- Open the JSON data.
- Open the project-pages files (html).
- Parse out the additional description information from the project pages.
- Store updated data as JSON file.

**Export as CSV**

Here the data gets exported as a CSV file.
- Open the data (JSON).
- Save the serialized data as CSV file.

## DATA INPUT
The original data is from the project list of the austrian development agency (ADA) [published on their website](http://www.entwicklung.at/zahlen-daten-und-fakten/projektliste/). The data consists of all contracts approved since January 1st of 2010.  in the list in chronologically descending order. The date of the last update can be found on the first table page as "Datum der letzten Aktualisierung".

### The Tables
The tables are the basic data, where most of the data is parsed out. The data is published in the following structure (e. g. first project).


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
So far, we can not say anything about the data quality (completeness, accurateness, etc.), but there are also so far no reaseons to doubt the quality.

**Data errors found**
- [Land/Region missing](http://www.entwicklung.at/zahlen-daten-und-fakten/projektliste/?tx_sysfirecdlist_pi1[showUid]=486&cHash=bcfc60e39b1543897f5492737913c8f0) 
- [Land/Region and Vertragsnummer missing](http://www.entwicklung.at/zahlen-daten-und-fakten/projektliste/?tx_sysfirecdlist_pi1%5BshowUid%5D=1249&cHash=0b453e3503d1f7f1e2e852ea2dece833)
- [Vertragsnummer missing](http://www.entwicklung.at/zahlen-daten-und-fakten/projektliste/?tx_sysfirecdlist_pi1%5BshowUid%5D=942&cHash=9493e43644fc91b324711888c3ea54c2)
- [Vertragssumme is in Partner field, Partner is missing](http://www.entwicklung.at/zahlen-daten-und-fakten/projektliste/?tx_sysfirecdlist_pi1[showUid]=1092&cHash=865e0122108c1411da8cc5c588441d73)
- [Vertragssumme is missing](http://www.entwicklung.at/zahlen-daten-und-fakten/projektliste/?tx_sysfirecdlist_pi1%5BshowUid%5D=646&cHash=fb5bb6e76b698da959f8894b5a417ce9)

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
- [code/aid-scraper.py](code/aid-scraper.py): scraper script in python
- [CHANGELOG.md](README.md): Overview of repository
- [LICENSE](README.md): MIT license text

## TODO
**important**
- verify the data
- research: is there a difference between approved funding and paid one?
- convert code to Python3: pay attention to encoding issues in i/o operations

**optional**
- create dataset for network analyses: json, csv for gephi and networkX
- compare data from tables with data from project pages.
- solve the encoding and CR issues. When saving the html table cells to the dict, it is done as unicode, so i did not work out how to replace the '\n' and '\r' characters. Did it then before storing to the CSV file, which is a quick and dirty solution. 

**new features**
- analyze and visualize the data: networkX, maps, Gephi
- add country namecodes for easier combinating with other data

## ACTUAL VERSION
See the [whole history](CHANGELOG.md).

### Version 0.3 - 2016-04-19
**extended scraper**
- aid-scraper.py: fixed the csv output bug caused by cariage return characters.
- update the README.md: add description of scraper.



