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
fees_dict = {}
current_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
root = 'http://www.wboppho.org.nz/'
feesUrlSouped = scrapers.openAndSoup(root + 'medical-centres/what-is-primary-health-general-practice-fees/')
fees_rows = feesUrlSouped.find('div', {'class': 'col-md-8'}).find('table').find_all('tr')[3:]

for row in fees_rows:
	cells = row.find_all('td')
	name = cells[0].get_text(strip=True)
	if name == '':
		break
	print(name)

	prices = [
			{
			'age': 0,
			'price': float(cells[1].get_text(strip=True)),
			},
			{
			'age': 6,
			'price': float(cells[2].get_text(strip=True)),
			},
			{
			'age': 18,
			'price': float(cells[3].get_text(strip=True)),
			},
			{
			'age': 25,
			'price': float(cells[4].get_text(strip=True)),
			},
			{
			'age': 45,
			'price': float(cells[5].get_text(strip=True)),
			},
			{
			'age': 65,
			'price': float(cells[6].get_text(strip=True)),
			}
		]

	fees_dict[scrapers.normalize(name)] = prices

pracsURLSouped = scrapers.openAndSoup(root + 'medical-centres/')
pracs_rows = pracsURLSouped.find('div', {'class': 'col-md-8'}).find_all('article', {'class': re.compile('medicalList *')})

for row in pracs_rows:
	coord = [0,0]
	name = row.find('span', {'class': 'practice'}).get_text(strip=True)
	print(name)
	if row.find('span', {'class': 'accepting'}).get_text(strip=True) == 'No':
		warning_list.append(name + ': Not accepting patients.')
		continue

	try:
		url = row.find('a').get('href')
	except AttributeError:
		warning_list.append(name + ': Could not get website.')

	try:
		fees = scrapers.partial_match(scrapers.normalize(name), fees_dict)
	except:
		warning_list.append(name + ': Could not get fees.')

	address = row.find('span', {'class': 'address'}).get_text(strip=True) + " " + row.find('span', {'class': 'suburb'}).get_text(strip=True)
	phone = row.find('span', {'class': 'phone'}).get_text(strip=True)
	coord = scrapers.geolocate(address)
	if (coord[0] == 0):
		warning_list.append(name + ': Cannot get coordinates.')

	# Make the dictionary object
	practice = {
		'name': name,
		'url': url,
		'address': address,
		'phone': phone,
		'pho': 'Western Bay of Plenty PHO',
		'coordinates': coord,
		'prices': prices
	}

	practices_list.append(practice)

with io.open(current_dir + '\\data.json', 'w', encoding='utf8') as outFile:
	json.dump(practices_list, outFile, ensure_ascii=False, sort_keys=True, indent=4)

scrapers.dealWithFailure(error_list, warning_list, current_dir)