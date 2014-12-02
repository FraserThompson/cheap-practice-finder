from urllib.request import urlopen
from bs4 import BeautifulSoup
import sys, codecs, os
import json

#stupid shit because the windows console can't print stuff properly
sys.stdout = codecs.getwriter('cp850')(sys.stdout.buffer, 'xmlcharrefreplace')
sys.stderr = codecs.getwriter('cp850')(sys.stderr.buffer, 'xmlcharrefreplace')

# Get the list of practices for Wellington
print("Opening URL for Wellington...")
listUrl = urlopen('http://www.compasshealth.org.nz/PracticesandFees/WellingtonPractices/PracticeFees.aspx').read()
listUrlSouped = BeautifulSoup(listUrl)
rows = listUrlSouped.find('table', {'class': 'FeesTable'}).find_all('tr')

practices_list = []
failed_list = []
current_dir = os.path.dirname(os.path.abspath(sys.argv[0]))

print("Iterating table...")
for row in rows:
	cells = row.findAll('td')
	if len(cells) > 0:
		coord = (0.000, 0.000)
		practiceURL = cells[0].find('a').get('href')
		name = cells[0].find('a').get_text()
		print("Found: " + practiceURL)

		######## FIND IF ENROLLING PATIENTS #########
		print("Navigating to: " + 'http://www.compasshealth.org.nz/PracticesandFees/WellingtonPractices/tabid/100/Default.aspx?search=' + cells[0].find('a').get_text().replace(" ", "+").replace("&", "%26"))
		openBooksURL = urlopen('http://www.compasshealth.org.nz/PracticesandFees/WellingtonPractices/tabid/100/Default.aspx?search=' + cells[0].find('a').get_text().replace(" ", "+").replace("&", "%26"))
		openBooksSouped = BeautifulSoup(openBooksURL)
		notEnrolling = openBooksSouped.find('img', {'id': 'dnn_ctr484_View_PracticeGrid_IsNotEnrollingImage_0'})
		if notEnrolling:
			failed_list.append("ERROR " + practiceURL + " " + name + ": Not enrolling patients.")
			continue

		######## GOING IN DEEP #######
		practiceUrlOpened = urlopen(practiceURL).read()
		practiceUrlSouped = BeautifulSoup(practiceUrlOpened)
		addressElement = practiceUrlSouped.find('span', {"id": "dnn_ctr484_Map_AddressLabel"})
		phoneElement = practiceUrlSouped.find('span', {"id": "dnn_ctr484_Map_PhoneLabel"})

		if addressElement is None:
			failed_list.append("ERROR " + practiceURL + " " + name +": No address.")
			continue

		#### GOING IN REALLY DEEP ####
		scriptElement = practiceUrlSouped.findAll('script', {"type":"text/javascript"})
		first = scriptElement[3].text.split("LatLng(", 1)
		if (len(first) > 1):
			coord = first[1].split(");", 1)[0].split(", ");
			coord[0] = float(coord[0])
			coord[1] = float(coord[1])

		address =  addressElement.get_text(strip=True)

		# Try find the coordinates of the address for Google Maps to display
		# try:
		# 	result_array = Geocoder.geocode(address + "Wellington, New Zealand")
		# 	coord = result_array[0].coordinates
		# except:
		# 	print("Could not geocode address: " + address)

		phone = phoneElement.get_text(strip=True) if phoneElement else "None supplied"

		# Make the dictionary object
		practice = {
			'name': name,
			'url': practiceURL,
			'address': address,
			'phone': phone,
			'pho': 'Compass Health',
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

# Get the list of practices for Wairapa
print("Opening URL for Wairapa...")
listUrl = urlopen('http://www.compasshealth.org.nz/PracticesandFees/WairarapaPractices/PracticeFees.aspx').read()
listUrlSouped = BeautifulSoup(listUrl)
rows = listUrlSouped.find('table', {'class': 'FeesTable'}).find_all('tr')

print("Iterating table...")
for row in rows:
	cells = row.findAll('td')
	if len(cells) > 0:
		coord = (0.000, 0.000)
		practiceURL = cells[0].find('a').get('href')
		name = cells[0].find('a').get_text()
		print("Found: " + practiceURL)

		######## FIND IF ENROLLING PATIENTS #########
		print("Navigating to: " + 'http://www.compasshealth.org.nz/PracticesandFees/WairarapaPractices/tabid/100/Default.aspx?search=' + cells[0].find('a').get_text().replace(" ", "+").replace("&", "%26"))
		openBooksURL = urlopen('http://www.compasshealth.org.nz/PracticesandFees/WairarapaPractices/tabid/100/Default.aspx?search=' + cells[0].find('a').get_text().replace(" ", "+").replace("&", "%26"))
		openBooksSouped = BeautifulSoup(openBooksURL)
		notEnrolling = openBooksSouped.find('img', {'id': 'dnn_ctr499_View_PracticeGrid_IsNotEnrollingImage_0'})
		if notEnrolling:
			failed_list.append("ERROR " + practiceURL + " " + name + ": Not enrolling patients.")
			continue

		######## GOING IN DEEP #######
		practiceUrlOpened = urlopen(practiceURL).read()
		practiceUrlSouped = BeautifulSoup(practiceUrlOpened)
		addressElement = practiceUrlSouped.find('span', {"id": "dnn_ctr499_Map_AddressLabel"})
		phoneElement = practiceUrlSouped.find('span', {"id": "dnn_ctr499_Map_PhoneLabel"})

		if addressElement is None:
			failed_list.append("ERROR " + practiceURL + " " + name + ": No address.")
			continue

		#### GOING IN REALLY DEEP ####
		scriptElement = practiceUrlSouped.findAll('script', {"type":"text/javascript"})
		first = scriptElement[3].text.split("LatLng(", 1)
		if (len(first) > 1):
			coord = first[1].split(");", 1)[0].split(", ");
			coord[0] = float(coord[0])
			coord[1] = float(coord[1])

		address =  addressElement.get_text(strip=True)

		phone = phoneElement.get_text(strip=True) if phoneElement else "None supplied"

		# Make the dictionary object
		practice = {
			'name': name,
			'url': practiceURL,
			'address': address,
			'phone': phone,
			'pho': 'Compass Health',
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


if (len(failed_list) > 0):
	print(str(len(failed_list)) +  " practices had errors: ")
	failed_file = open(current_dir + '\\failed_list.txt', 'w')
	for f in failed_list:
		failed_file.write("%s\n" % f)
		print(f)
	failed_file.close()