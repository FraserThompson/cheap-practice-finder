from bs4 import BeautifulSoup
from urllib.request import urlopen, Request
import re
from pygeocoder import Geocoder

def partial_match(string, dictin):
	result = []
	for key in dictin:
		if key.startswith(string):
			result = dictin.get(key)
			break
	# Go for a less accurate search if nothing is found
	if len(result) == 0:
		for key in dictin:
			if key.startswith(' '.join(string.split()[:2])):
				result = dictin.get(key)
				break
	return result

def getHealthpointURL(name):
	url = 'http://www.faroo.com/api?q=site:www.healthpoint.co.nz+' + scrapers.toPlusURL(name) + '&start=1&length=5&l=en&src=web&i=false&f=json'
	req = Request(url, None, headers={'User-Agent': 'Practice Scraper'})
	opened = urlopen(req).read()
	return opened.results[0].url

def scrapeHealthpointDetails(url):
	soup = scrapers.openAndSoup(url)
	phone = soup.find('ul', {'class':'contact-list'}).find('p').get_text()
	map_div = soup.find('section', {'class':'service-map'}).find('div', {'class':'map'})
	address = map_div.find('p').get_text()
	coord = map_div.get('data-position').split(', ')
	return [phone, address, coord]

def openAndSoup(url):
	req = urllib.Request(url, None, headers={'User-Agent': 'Mozilla/5.0'})
	return BeautifulSoup(urlopen(req).read())

def dealWithFailure(error_list, warning_list, current_dir):
	if (len(error_list) > 0):
		errorcount = str(len(error_list))
		warningcount = str(len(warning_list))
		print(errorcount +  " practices had errors.")
		print(warningcount +  " practices had warnings.")
		failed_file = open(current_dir + '\\failed_list.txt', 'w')
		failed_file.write("============" + errorcount + "===========\n")
		for f in error_list:
			failed_file.write("ERROR %s\n" % f)
		failed_file.write("============" + warningcount + "===========\n")
		for w in warning_list:
			failed_file.write("WARNING %s\n" % w)
		failed_file.close()

def normalize(input):
	return re.sub('[^0-9a-zA-Z ]+', '', input.strip().lower().replace('mt', 'mount'))

	
def geolocate(address):
	# Try find the coordinates of the address for Google Maps to display
	try:
		result_array = Geocoder.geocode(address + ", New Zealand")
		coord = result_array[0].coordinates
	except:
		print("Could not geocode address: " + address)
		return [0, 0]
	return coord

def toDashURL(input):
	normal = re.sub('[^0-9a-zA-Z ]+', '', input.strip())
	return normal.lower().replace(' ', '-') + "/"

def toPlusURL(input):
	normal = re.sub('[^0-9a-zA-Z ]+', '', input.strip())
	return normal.lower().replace(' ', '+')

def getFirstNumber(string):
	return float(re.findall('[-+]?\d*\.\d+|\d+', string)[0])