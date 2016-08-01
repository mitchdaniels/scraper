# Scraper
A Python scraper that takes a list of URLs and XPaths and returns the associated data in CSV format. To use, update the config.yml file with:
* A source CSV with a column called 'URL' containing full hrefs
* Fields listing the specific XPaths to search against.
* Name of desired output CSV

## Requirements
* csv
* pandas
* Queue
* threading
* urllib2
* re
* lxml
* requests
* PyYAML