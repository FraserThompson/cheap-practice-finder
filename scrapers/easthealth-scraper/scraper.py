import sys, codecs, os
import json
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '\\..\\')
import scrapers

#stupid shit because the windows console can't print stuff properly
sys.stdout = codecs.getwriter('cp850')(sys.stdout.buffer, 'xmlcharrefreplace')
sys.stderr = codecs.getwriter('cp850')(sys.stderr.buffer, 'xmlcharrefreplace')

# Get the list of practices for Wellington
listUrlSouped = scrapers.openAndSoup('http://www.easthealth.co.nz/about/locate/')
rows = listUrlSouped.find('ul', {'class': 'cggm_sidebar_list'}).find_all('li')

practices_list = []
error_list = []
warning_list = []
current_dir = os.path.dirname(os.path.abspath(sys.argv[0]))

print("Iterating table...")
for row in rows:
	prices = []
	coord = (0.000, 0.000)
	practiceURL = row.find('a').get('href')
	name = row.find('a').get_text()
	print("Found: " + practiceURL)

	######## GOING IN DEEP #######
	practiceUrlSouped = scrapers.openAndSoup(practiceURL)
	address = practiceUrlSouped.find('section', {"id": "content"}).find('p').get_text().split(':')[1].strip()
	phone = practiceUrlSouped.find('div', {"id": "phone"}).get_text().split('PHONE')[1]

	#### GOING IN REALLY DEEP ####
	scriptElement = practiceUrlSouped.find('body').find_all('script')
	first = scriptElement[3].text.split("LatLng(", 1)
	if (len(first) > 1):
		coord = first[1].split(")", 1)[0].split(",");
		coord[0] = float(coord[0])
		coord[1] = float(coord[1])

	if coord[0] == 0 or coord[1] == 0:
		error_list.append(practiceURL +": Bad coords." + str(coord[0]) + ", " + str(coord[1]))
		continue

	#### Fees ####
	try:
		fees_rows = practiceUrlSouped.find('table').find_all('tr')
		prices =  [
			{
			'age': 0,
			'price': float(fees_rows[0].find_all('td')[1].get_text(strip=True).replace("$", "").replace('Free', '0')),
			},
			{
			'age': 6,
			'price': float(fees_rows[1].find_all('td')[1].get_text(strip=True).replace("$", "")),
			},
			{
			'age': 18,
			'price': float(fees_rows[2].find_all('td')[1].get_text(strip=True).replace("$", "")),
			},
			{
			'age': 25,
			'price': float(fees_rows[3].find_all('td')[1].get_text(strip=True).replace("$", "")),
			},
			{
			'age': 45,
			'price': float(fees_rows[4].find_all('td')[1].get_text(strip=True).replace("$", "")),
			},
			{
			'age': 65,
			'price': float(fees_rows[5].find_all('td')[1].get_text(strip=True).replace("$", "")),
			},
		] 
	except AttributeError:
		print("no fees")

	if len(prices) == 0:
		warning_list.append(practiceURL +": No prices.")

	practice = {
		'name': name,
		'url': practiceURL,
		'address': address,
		'phone': phone,
		'pho': 'East Health Trust',
		'coordinates': coord,
		'prices': prices
	}

	practices_list.append(practice)
		
with open(current_dir + '\\data.json', 'w') as outFile:
	json.dump(practices_list, outFile, ensure_ascii=False, sort_keys=True, indent=4)


scrapers.dealWithFailure(error_list, warning_list, current_dir)