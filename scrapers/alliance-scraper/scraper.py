import sys, codecs, os
import json
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '\\..\\')
import scrapers

#stupid shit because the windows console can't print stuff properly
sys.stdout = codecs.getwriter('cp850')(sys.stdout.buffer, 'xmlcharrefreplace')
sys.stderr = codecs.getwriter('cp850')(sys.stderr.buffer, 'xmlcharrefreplace')

practices_list = []
error_list = []
warning_list = []
current_dir = os.path.dirname(os.path.abspath(sys.argv[0]))

# Access the URL
root = 'http://www.alliancehealth.org.nz'
listUrlSouped = scrapers.openAndSoup(root + '/clinics')
clinics = listUrlSouped.find('div', {'id': 'clinics-left'}).find('ul').find_all('li')

for clinic in clinics:
	coord = [0,0]
	prices_list = []

	# Coord and website
	clinic_data = clinic.find('a')
	coord[0] = float(clinic_data.get('data-lat'))
	coord[1] = float(clinic_data.get('data-lng'))
	url = root + clinic_data.get('href')

	# Information
	pracURLSouped = scrapers.openAndSoup(url)
	takingPatients = pracURLSouped.find('div', {'class': 'box-rgt text'}).find('p').get_text()
	if "is taking new patients" not in takingPatients:
		error_list.append(url + ": Is not taking patients.")
		continue
	info_lines1 = pracURLSouped.find('div', {'class': 'box-lft text'}).find('p').get_text().splitlines()
	address = ' '.join(info_lines1[0:2])
	phone = ' '.join(info_lines1[2].split()[1:])

	# Fees
	try:
		if (clinic_data.get_text() != 'Bader Drive Healthcare Manurewa'):
			info_lines2 = pracURLSouped.find('div', {'class' : 'info'}).find('ul').find_all('li')
		else: 
			info_lines2 = pracURLSouped.find('div', {'class' : 'info'}).find_all('ul')[1].find_all('li')

		count = 0

		print(clinic_data.get_text() + ": ")
		for line in info_lines2:
			fees = line.get_text(strip=True).split(':')
			print(fees)
			if len(fees) == 2:
				# Dealing with the left hand side
				if (count == 0):
					fees[0] = 0;
				else:
					fees[0] = fees[0].replace('-', ' ')
					strip_numbers = [int(s) for s in fees[0].split() if s.isdigit()]
					if len(strip_numbers) > 0:
						fees[0] = strip_numbers[0]

				# Dealing with the right hand side
				fees[1] = fees[1].replace('\xa0', '').replace('&nbsp;', '').replace(' ', '')
				if (fees[1]) == 'Free':
					fees[1] = 0;
				else:
					fees[1] = fees[1].split('(')[0]

				if (isinstance(fees[1], int) is not True):
					fees[1] = float(fees[1].replace("$", ""))

				prices_list.append({"age" : fees[0], "price": fees[1]})
				count += 1

	except AttributeError:
		error_list.append(url + ": Couldn't get fees.")

	practice = {
		'name': clinic_data.get_text(),
		'url': url,
		'address': address,
		'phone': phone,
		'pho': 'Alliance Health Plus',
		'coordinates': coord,
		'prices': prices_list
	}
	practices_list.append(practice)

with open(current_dir + '\\data.json', 'w') as outFile:
	json.dump(practices_list, outFile, ensure_ascii=False, sort_keys=True, indent=4)

scrapers.dealWithFailure(error_list, warning_list, current_dir)