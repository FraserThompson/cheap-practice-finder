from bs4 import BeautifulSoup, Comment
import json
import requests
from urllib.request import urlopen, Request
import re
import codecs
from pygeocoder import Geocoder

def getFirstNumber(string):
	return float(re.findall('[-+]?\d*\.\d+|\d+', string)[0])

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
	print('Trying to get healthpoint url: ' + name)
	url = 'https://api.datamarket.azure.com/Bing/Search/v1/Web?Query=%27site%3Ahealthpoint.co.nz%20' + urlify(name) + '%27&$format=json'
	req = requests.get(url, auth=('iltXKGGVYlV3VSnhXT8jbNZe97rvjDRkdte68cM7fJU', 'iltXKGGVYlV3VSnhXT8jbNZe97rvjDRkdte68cM7fJU'))
	if req.status_code != 200:
		return ''
	results = req.json()['d']['results']
	if len(results) == 0:
		return ''
	else:
		return results[0]['Url']

def scrapeHealthpointDetails(url):
	print("trying to scrape from: " + url)
	soup = openAndSoup(url)
	try:
		address = soup.find('ul', {'class':'contact-list'}).find('p').get_text()
		map_div = soup.find('section', {'class':'service-map'}).find('div', {'class':'map'})
		phone = map_div.find('p').get_text()
		coord = map_div.get('data-position').split(', ')
		if coord[0] != '' and coord[0] != 0:
			coord = [float(string) for string in coord]
		else:
			return 0
	except AttributeError:
		return 0
	return [phone, address, coord]

def openAndSoup(url):
	print("Accessing URL: " + url)
	req = Request(url, None, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Safari/537.36'})
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
	return re.sub('[^0-9a-zA-Z ]+', '', input.strip().lower().replace('mt ', 'mount '))

	
def geolocate(address):
	# Try find the coordinates of the address for Google Maps to display
	try:
		result_array = Geocoder.geocode(address + ", New Zealand")
		coord = result_array[0].coordinates
	except:
		print("Could not geocode address: " + address)
		return [0, 0]
	return coord

def replaceSpacesWithDashes(input):
	normal = re.sub('[^0-9a-zA-Z ]+', '', input.strip())
	return normal.lower().replace(' ', '-') + "/"

def replaceSpacesWithPluses(input):
	normal = re.sub('[^0-9a-zA-Z ]+', '', input.strip())
	return normal.lower().replace(' ', '+')

def urlify(input):
	return input.replace("'", '%27').replace('"', '%27').replace('+', '%2b').replace(' ', '%20').replace(':', '%3a')

def getFirstNumber(string):
	return float(re.findall('[-+]?\d*\.\d+|\d+', string)[0])