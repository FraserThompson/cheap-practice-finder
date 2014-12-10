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
root = 'http://www.ebpha.org.nz/'
feesUrlSouped = scrapers.openAndSoup(root + 'index.php?option=com_content&view=article&id=12&Itemid=139')
fees_rows = feesUrlSouped.find('table', {'class': 'table_style_yellow'}).find('tbody').find_all('tr')[1:]

for row in fees_rows:
	cells = row.find_all('td')
	name = cells[0].get_text(strip='true')
	if name == '':
		break
	print(name)

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

	fees_dict[scrapers.normalize(name)] = prices

pracsURLSouped = scrapers.openAndSoup(root + 'index.php?option=com_content&view=article&id=14&Itemid=125')
pracs_rows = pracsURLSouped.find_all('ul', {'class': 'nav-child unstyled small'})[1].find_all('li')

for row in pracs_rows:
	coord = [0,0]
	url = row.find('a').get('href')
	name = row.find('a').get_text(strip=True)
	print(name)
	try:
		fees = scrapers.partial_match(scrapers.normalize(name), fees_dict)
	except:
		warning_list.append(name + ': Could not get fees.')

	practiceSouped = scrapers.openAndSoup(root + url).find('div', {'itemprop': 'articleBody'})
	try:
		maps_url = practiceSouped.find_all('a')[1].get('href')
	except IndexError:
		error_list.append(name + ': Could not get coordinates.')
		continue

	try:
		address = maps_url.split('q=')[1].split('&')[0]
		coord = maps_url.split('ll=')[1].split('&')[0].split(',')
	except IndexError:
		try:
			address = maps_url.split('place/')[1].split('/@')[0]
			coord = maps_url.split('@')[1].split(',17z/')[0].split(',', maxsplit=1)
		except IndexError:
			error_list.append(name + ': Could not get address or coordinates.')
			continue

	coord[0] = float(coord[0])
	coord[1] = float(coord[1])

	address = address.replace('+', ' ')

	# Make the dictionary object
	practice = {
		'name': name,
		'url': url,
		'address': address,
		'phone': 'See website',
		'pho': 'Eastern Bay PHO',
		'coordinates': coord,
		'prices': prices
	}

	practices_list.append(practice)

with io.open(current_dir + '\\data.json', 'w', encoding='utf8') as outFile:
	json.dump(practices_list, outFile, ensure_ascii=False, sort_keys=True, indent=4)

scrapers.dealWithFailure(error_list, warning_list, current_dir)