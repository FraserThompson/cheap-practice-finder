import sys, codecs, os
import json
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '\\..\\')
import scrapers

#stupid shit because the windows console can't print stuff properly
sys.stdout = codecs.getwriter('cp850')(sys.stdout.buffer, 'xmlcharrefreplace')
sys.stderr = codecs.getwriter('cp850')(sys.stderr.buffer, 'xmlcharrefreplace')

# Get the list of practices for Wellington
listUrlSouped = scrapers.openAndSoup('http://www.centralpho.org.nz/PracticesandFees/PracticeFees.aspx')
rows = listUrlSouped.find('table', {'class': 'FeesTable'}).find_all('tr')

practices_list = []
error_list = []
warning_list = []
current_dir = os.path.dirname(os.path.abspath(sys.argv[0]))

for row in rows:
	cells = row.findAll('td')
	if len(cells) > 0:
		coord = (0.000, 0.000)
		practiceURL = cells[0].find('a').get('href')
		print("Found: " + practiceURL)

		######## FIND IF ENROLLING PATIENTS #########
		print("Navigating to: " + 'http://www.centralpho.org.nz/PracticesandFees/tabid/90/Default.aspx?search=' + cells[0].find('a').get_text().replace(" ", "+").replace("&", "%26"))
		openBooksSouped = scrapers.openAndSoup('http://www.centralpho.org.nz/PracticesandFees/tabid/90/Default.aspx?search=' + cells[0].find('a').get_text().replace(" ", "+").replace("&", "%26"))
		notEnrolling = openBooksSouped.find('img', {'id': 'dnn_ctr700_View_PracticeGrid_IsNotEnrollingImage_0'})
		if notEnrolling:
			error_list.append(practiceURL + ": Isn't enrolling patients.")
			continue

		######## GOING IN DEEP #######
		practiceUrlSouped = scrapers.openAndSoup(practiceURL)
		addressElement = practiceUrlSouped.find('span', {"id": "dnn_ctr484_Map_AddressLabel"})
		phoneElement = practiceUrlSouped.find('span', {"id": "dnn_ctr484_Map_PhoneLabel"})

		if addressElement is None:
			error_list.append(practiceURL + ": No address.")
			continue

		#### GOING IN REALLY DEEP ####
		scriptElement = practiceUrlSouped.find('body').findAll('script', {"type":"text/javascript"})
		first = scriptElement[2].text.split("LatLng(", 1)
		if (len(first) > 1):
			coord = first[1].split(");", 1)[0].split(", ");
			coord[0] = float(coord[0])
			coord[1] = float(coord[1])
		else:
			error_list.append(practiceURL +": Bad coords." + str(coord[0]) + ", " + str(coord[1]))
			continue

		if coord[0] == 0 or coord[1] == 0:
			error_list.append(practiceURL +": Bad coords." + str(coord[0]) + ", " + str(coord[1]))
			continue

		address =  addressElement.get_text(strip=True)
		phone = phoneElement.get_text(strip=True) if phoneElement else "None supplied"

		# Make the dictionary object
		practice = {
			'name': cells[0].find('a').get_text(),
			'url': practiceURL,
			'address': address,
			'phone': phone,
			'pho': 'Central PHO',
			'coordinates': coord,
			'prices': [
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
				},
			] 
		}

		practices_list.append(practice)

with open(current_dir + '\\data.json', 'w') as outFile:
	json.dump(practices_list, outFile, ensure_ascii=False, sort_keys=True, indent=4)

scrapers.dealWithFailure(error_list, warning_list, current_dir)