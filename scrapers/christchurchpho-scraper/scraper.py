import sys, codecs, os
import json, io
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '\\..\\')
import scrapers

#stupid shit because the windows console can't print stuff properly
sys.stdout = codecs.getwriter('cp850')(sys.stdout.buffer, 'xmlcharrefreplace')
sys.stderr = codecs.getwriter('cp850')(sys.stderr.buffer, 'xmlcharrefreplace')

practices_list = []
error_list = []
warning_list = []
current_dir = os.path.dirname(os.path.abspath(sys.argv[0]))

root = 'http://www.chchpho.org.nz/'
listUrlSouped = scrapers.openAndSoup(root + "provider-burnside.php")
providers_rows = listUrlSouped.find('table', {'id': 'table_providers'}).find_all('tr')

for row in providers_rows:
	cells = row.find_all('td')
	url = root + cells[0].find('a').get('href')
	name = cells[0].get_text()
	address = cells[1].get_text()
	practiceSouped = scrapers.openAndSoup(url)
	infoTable = practiceSouped.find('div', {'id': 'information'})
	phone = infoTable.find('h4').get_text().split('Ph: ')[1]
	feesRows = infoTable.find('table').find_all('tr')[5:]

	coord = scrapers.geolocate(address)
	if (coord[0] == 0):
		error_list.append(name + ": Cannot geolocate address: " + address)
		continue

	prices = []
	prices.append({
		'age': 0,
		'price': 0
	})

	for tr in feesRows:
		cells = tr.find_all('td')
		try:
			if tr.get_text() == 'Hours':
				break
			age = scrapers.getFirstNumber(cells[0].get_text())
			# Really inefficient check to see if there's already one in there
			skip = 0
			for thing in prices:
				if thing['age'] == age:
					print(str(age) + ' equals ' + str(thing['age']))
					skip = 1
			if skip: continue
			prices.append({
				'age': age,
				'price': scrapers.getFirstNumber(cells[1].get_text())
			})
		except IndexError:
			print(tr.get_text())
			print("================================WTF====================")
			
	if len(prices) == 1:
		warning_list.append("WARNING " + url + ": Couldn't get any prices.")
	# Make the dictionary object
	practice = {
		'name': name,
		'url': url,
		'address': address,
		'phone': phone,
		'pho': 'Christchurch PHO',
		'coordinates': coord,
		'prices': prices
	}

	practices_list.append(practice)

with io.open(current_dir + '\\data.json', 'w', encoding='utf8') as outFile:
	json.dump(practices_list, outFile, ensure_ascii=False, sort_keys=True, indent=4)

scrapers.dealWithFailure(error_list, warning_list, current_dir)