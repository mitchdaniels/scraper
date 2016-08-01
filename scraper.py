#used to import / process input CSV
import csv
import pandas as pd

from Queue import Queue
from threading import Thread
import urllib2 #for threading and CSV import
import re

#used to scrap URLs
from lxml import html
import requests

import yaml

f = open('config.yml')
config = yaml.safe_load(f)
fields = config['fields']

response = urllib2.urlopen(config['csvURL'])
cr = csv.reader(response)

df = pd.read_csv(response)
urls = df['URL']

# Work queue where you push the URLs onto - size 100
url_queue = Queue(10)

with open(config['output'], 'w') as csvfile:
	writer = csv.DictWriter(csvfile, fieldnames=['URL']+fields.keys())
	writer.writeheader()

	def worker():
	    # Gets the next url from the queue and processes it
	    while True:
	        url = url_queue.get()
	        page = requests.get(url)
	        tree = html.fromstring(page.content)

	        row = {'URL': url}

	        for field in fields:
	        	try:
		        	if '(Y/N)' in field:
		        		row[field] = bool(tree.xpath(fields[field]))
		        	else:
		        		row[field] = tree.xpath(fields[field])[0].encode('utf-8')
		        except:
		        	row[field] = tree.xpath(fields[field])
	        writer.writerow(row)

	        print row

	        url_queue.task_done()

	# Start a pool of 20 workers
	for i in xrange(20):
	     t = Thread(target=worker)
	     t.daemon = True
	     t.start()

	# Change this to read your links and queue them for processing
	for url in urls:
	    url_queue.put(url)

	# Block until everything is finished.
	url_queue.join()  