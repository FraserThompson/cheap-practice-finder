import sys, codecs, os, re
import json
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '\\..\\')
import scrapers

def normalize(input):
	return scrapers.normalize(input).replace('st', 'street')

#stupid shit because the windows console can't print stuff properly
sys.stdout = codecs.getwriter('cp850')(sys.stdout.buffer, 'xmlcharrefreplace')
sys.stderr = codecs.getwriter('cp850')(sys.stderr.buffer, 'xmlcharrefreplace')
current_dir = os.path.dirname(os.path.abspath(sys.argv[0]))

# Get the list of practices for Hawkes Bay
# First URL for getting fees
listUrlSouped = scrapers.openAndSoup('http://www.healthhb.co.nz/fees/')

# Create a dictionary to map practice name to URL
practiceListUrlSouped = scrapers.openAndSoup('http://www.healthhb.co.nz/our-practices/')
practiceList = practiceListUrlSouped.find('ul', {'id': 'menu-practices'}).find_all('ul')
practices_dict = {}

for thing in practiceList:
	list_items = thing.find_all('li');
	for thing2 in list_items:
		list_item = thing2.find('a');
		practices_dict.update({normalize(list_item.get_text()): list_item.get('href')})

rows = listUrlSouped.find('div', {'class': 'site-inner'}).find('table').find_all('tr')
# oh man this is so bad but the first two are header rows and the last three have a weird timed
# fee scheme so they're going to be popped off because i am lazy
rows.pop(0)
rows.pop(0)
rows.pop(len(rows) - 1)
rows.pop(len(rows) - 1)
rows.pop(len(rows) - 1)
practices_list = []
error_list = []
warning_list= []

print("Iterating table...")
for row in rows:
	coord = (0.000, 0.000)
	cells = row.find_all('td')
	name = cells[0].get_text().replace("&#8211;", "-").replace("’", "'")
	if(name is "" or name is None):
		continue

	print("Found: " + name)
	practiceURL = practices_dict.get(normalize(name))
	print(practiceURL)

	if (practiceURL is None):
		error_list.append(name + ": Could not map URL.")
		continue

	####### GOING IN DEEP #######
	practiceUrlSouped = scrapers.openAndSoup(practiceURL)
	relevant_section = practiceUrlSouped.find_all('div', {'class': 'wpb_text_column wpb_content_element '})[0]
	
	if name != 'The Doctors, Napier':
		addressElement = relevant_section.find_all('p')[0]
		try:
			phone = relevant_section.find_all('p')[1].get_text(strip=True)
		except IndexError:
			phone = "None supplied"
	else:
		addressElement = relevant_section.find_all('p')[1]
		phone = relevant_section.find_all('p')[3].get_text(strip=True)

	if addressElement is None:
		error_list.append(practiceURL + ": Could not find address element.")
		continue

	coord = scrapers.geolocate(addressElement.get_text())
	if coord[0] == 0:
		error_list.append(practiceURL + " " + name + " " + addressElement.get_text() + ": Could not geocode address.")
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
		
with open(current_dir + '\\data.json', 'w') as outFile:
	json.dump(practices_list, outFile, ensure_ascii=False, sort_keys=True, indent=4)

scrapers.dealWithFailure(error_list, warning_list, current_dir)