import sys, codecs, os
import json, io
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '\\..\\')
import scrapers

#stupid shit because the windows console can't print stuff properly
sys.stdout = codecs.getwriter('cp850')(sys.stdout.buffer, 'xmlcharrefreplace')
sys.stderr = codecs.getwriter('cp850')(sys.stderr.buffer, 'xmlcharrefreplace')
url = 'http://www.haurakipho.org.nz/medical-centres/our-medical-centres'
listUrlSouped = scrapers.openAndSoup(url)

practices_list = []
error_list = []
warning_list = []
current_dir = os.path.dirname(os.path.abspath(sys.argv[0]))

for i in range(0, 25):
	address = ''
	phone = ''
	practice = listUrlSouped.find('div', {'class': 'items-row cols-1 row-'+str(i)}).find('div', {'class': 'item column-1'});
	name = practice.find('h2').get_text(strip='true');
	lines = practice.find_all('p');

	if '-' in lines[0].get_text():
		address = ', '.join(lines[0].strings).split('-')[1].strip()

	for line in lines:
		if 'Location:' in line.get_text(strip='true'):
			address = ', '.join(line.strings).split('Location:')[1].replace(',,', ',').strip()
		if 'Contact details:' in line.get_text(strip='true'):
			phone = line.get_text(strip='true').split('Contact details:')[1].split('     ')[0].strip()
		if 'Contact Details:' in line.get_text(strip='true'):
			phone = line.get_text(strip='true').split('Contact Details:')[1].split('     ')[0].strip()
		if 'Contact:' in line.get_text(strip='true'):
			phone = line.get_text(strip='true').split('Contact:')[1].split('     ')[0].strip()

	if address == '':
		error_list.append(name + ": Cannot find address.")
		continue
	if phone == '':
		warning_list.append(name + ": Cannot find phone.")

	if ' - ' in phone:
		phone = phone.split(' - ')[1]

	coord = scrapers.geolocate(address)
	if (coord[0] == 0):
		error_list.append(name + ": Cannot geolocate address: " + address)
		continue

	# Make the dictionary object
	practice = {
		'name': name,
		'url': url,
		'address': address,
		'phone': phone,
		'pho': 'Hauraki PHO',
		'coordinates': coord,
		'prices': [] 
	}

	practices_list.append(practice)

with io.open(current_dir + '\\data.json', 'w', encoding='utf8') as outFile:
	json.dump(practices_list, outFile, ensure_ascii=False, sort_keys=True, indent=4)

scrapers.dealWithFailure(error_list, warning_list, current_dir)