import sys, codecs, os
import json, io
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '\\..\\')
import scrapers
import re

#stupid shit because the windows console can't print stuff properly
sys.stdout = codecs.getwriter('cp850')(sys.stdout.buffer, 'xmlcharrefreplace')
sys.stderr = codecs.getwriter('cp850')(sys.stderr.buffer, 'xmlcharrefreplace')

practices_list = []
error_list = []
warning_list = []
current_dir = os.path.dirname(os.path.abspath(sys.argv[0]))

root = 'http://www.rcpho.org.nz/practices/'
listUrlSouped = scrapers.openAndSoup(root)
providers_rows = listUrlSouped.find('table', {'id': 'tablepress-1'}).find('tbody').find_all('tr')

for row in providers_rows:
	cells = row.find_all('td')
	name = cells[0].get_text(strip='true')
	print(name)
	url = cells[0].find('a').get('href').replace('pracitces', 'practices')
	practiceSouped = scrapers.openAndSoup(url)
	try:
		infoTable = practiceSouped.find_all('table')[5].find('tbody').find_all('tr')
		address = ', '.join([infoTable[0].get_text(strip='true').replace('\t', ' '), infoTable[1].get_text(strip='true').replace('\t', ' ')])
		for tr in infoTable:
			if 'Phone: ' in tr.get_text(strip='true'):
				phone = tr.get_text(strip='true').split(': ')[1]
	except IndexError:
		error_list.append(name + ": Cannot find contact details.")
		continue

	coord = scrapers.geolocate(address)
	if (coord[0] == 0):
		error_list.append(name + ": Cannot geolocate address: " + address)
		continue

	prices = [
			{
			'age': 0,
			'price': float(cells[1].get_text(strip=True).replace("$", "")),
			},
			{
			'age': 6,
			'price': float(cells[2].get_text(strip=True).replace("$", "")),
			},
			{
			'age': 18,
			'price': float(cells[3].get_text(strip=True).replace("$", "")),
			},
			{
			'age': 25,
			'price': float(cells[4].get_text(strip=True).replace("$", "")),
			},
			{
			'age': 45,
			'price': float(cells[5].get_text(strip=True).replace("$", "")),
			},
			{
			'age': 65,
			'price': float(cells[6].get_text(strip=True).replace("$", "")),
			}
		]

	# Make the dictionary object
	practice = {
		'name': name,
		'url': url,
		'address': address,
		'phone': phone,
		'pho': 'Rural Canterbury PHO',
		'coordinates': coord,
		'prices': prices
	}

	practices_list.append(practice)

with io.open(current_dir + '\\data.json', 'w', encoding='utf8') as outFile:
	json.dump(practices_list, outFile, ensure_ascii=False, sort_keys=True, indent=4)

scrapers.dealWithFailure(error_list, warning_list, current_dir)