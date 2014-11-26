from urllib.request import urlopen
from pygeocoder import Geocoder
from bs4 import BeautifulSoup
import sys, codecs
import json

#stupid shit because the windows console can't print stuff properly
sys.stdout = codecs.getwriter('cp850')(sys.stdout.buffer, 'xmlcharrefreplace')
sys.stderr = codecs.getwriter('cp850')(sys.stderr.buffer, 'xmlcharrefreplace')

# Get the list of practices for Hawkes Bay
# First URL for getting feeds
listUrl = urlopen('http://www.healthhb.co.nz/fees/').read()
listUrlSouped = BeautifulSoup(listUrl)

# Create a dictionary to map practice name to URL
practiceListUrlOpened = urlopen("http://www.healthhb.co.nz/our-practices/").read()
practiceListUrlSouped = BeautifulSoup(practiceListUrlOpened)
practiceList = practiceListUrlSouped.find('ul', {'id': 'menu-practices'}).find_all('ul')
practices_dict = {}

for thing in practiceList:
	list_items = thing.find_all('li');
	for thing2 in list_items:
		list_item = thing2.find('a');
		practices_dict.update({list_item.get_text(): list_item.get('href')})

rows = listUrlSouped.find('div', {'class': 'site-inner'}).find('table').find_all('tr')
rows.pop(0)
rows.pop(0)
practices_list = []
failed_list =[]

print("Iterating table...")
for row in rows:
	coord = (0.000, 0.000)
	cells = row.find_all('td')
	name = cells[0].get_text().replace("&#8211;", "-").replace("’", "'")
	if(name is "" or name is None):
		continue

	print("Found: " + name)
	practiceURL = practices_dict.get(name)
	print(practiceURL)

	if (practiceURL is None):
		failed_list.append(name + ": Could not map URL.")
		continue

	####### GOING IN DEEP #######
	practiceUrlOpened = urlopen(practiceURL).read()
	practiceUrlSouped = BeautifulSoup(practiceUrlOpened)
	relevant_section = practiceUrlSouped.find_all('div', {'class': 'wpb_text_column wpb_content_element '})[0]
	addressElement = relevant_section.find_all('p')[0]
	try:
		phone = relevant_section.find_all('p')[1].get_text(strip=True)
	except IndexError:
		phone = "None supplied"

	if addressElement is None:
		failed_list.append(name + ": Could not find address element.")
		continue

	try:
		result_array = Geocoder.geocode(addressElement.get_text() + ", New Zealand")
		coord = result_array[0].coordinates
	except:
		failed_list.append(name + ": Could not geocode address.")
		continue

	# Make the dictionary object

	practice = {
		'name': name,
		'url': practiceURL,
		'address': addressElement.get_text(),
		'phone': phone.replace("Telephone: ", ""),
		'pho': "Health Hawke's Bay",
		'coordinates': coord,
		'prices': [
			{
			'age': 0,
			'price': 0,
			},
			{
			'age': 6,
			'price': float(cells[2].get_text(strip=True).replace("Free", "0").replace("$", "")),
			},
			{
			'age': 18,
			'price': float(cells[3].get_text(strip=True).replace("Free", "0").replace("$", "")),
			},
			{
			'age': 25,
			'price': float(cells[4].get_text(strip=True).replace("Free", "0").replace("$", "")),
			},
			{
			'age': 45,
			'price': float(cells[5].get_text(strip=True).replace("$", "")),
			},
			{
			'age': 65,
			'price': float(cells[6].get_text(strip=True).replace("$", "")),
			},
		] 
	}

	practices_list.append(practice)
		
with open('data.json', 'w') as outFile:
	json.dump(practices_list, outFile, ensure_ascii=False, sort_keys=True, indent=4)

print("The following practices were not added: ")
for f in failed_list:
	print(f)