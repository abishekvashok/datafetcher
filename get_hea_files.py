from bs4 import BeautifulSoup
import requests
import wget
import progressbar

# Avoid warnings: export PYTHONWARNINGS="ignore:Unverified HTTPS request"

ext = 'hea'

def listFD(url, ext=''):
	page = requests.get(url, verify=False).text
	soup = BeautifulSoup(page, 'html.parser')
	return [url + node.get('href') for node in soup.find_all('a') if node.get('href').endswith(ext)]

widgets = [
	' [', progressbar.Timer(format= 'elapsed time: %(elapsed)s'), '] ', 
	progressbar.Bar('*'),
	' [', progressbar.ETA(), ']',
]
bar = progressbar.ProgressBar(max_value=10282, widgets=widgets).start()

with open("RECORDS", 'r') as records:
	f = open("last_record", "r")
	last_id = int(f.read())
	f.close()
	i = 0
	for record in records:
		i = i + 1
		record = record.split('\n')[0]
		rid = int(record.split("/")[1][1:])
		if(rid <= last_id):
			bar.update(i)
			continue
		if(rid == upid):
			break
		url = 'http://physionet.org/files/mimic3wdb-matched/1.0/'+record
		best_hea = ""
		best_hea_link = ""
		diff = 1440 # 24 * 60
		for hea_link in listFD(url, ext):
			if(record.split("/")[1]+"-" in hea_link):
				continue
			if("_layout" in hea_link):
				continue
			hea_contents = requests.get(hea_link, verify=False).text
			if("I" in hea_contents or "II" in hea_contents or "III" in hea_contents or "IV" in hea_contents or "V" in hea_contents):
				print(str(rid))
				ar = hea_contents.split('\n')[0].split(' ')[-1].split('.')[0].split(":")
				hea_hour, hea_minute = ar[0], ar[1]
				hea_diff = abs(420 - (int(hea_hour) * 60) - int(hea_minute)) # 420 = 7 * 60
				if(hea_diff < diff):
					diff = hea_diff
					best_hea = hea_contents
					best_hea_link = hea_link
		if(best_hea != ""):
			rid = str(rid)
			wget.download(best_hea_link.split(".hea")[0]+".dat", rid+".dat")
			with open(rid+".hea", "w") as record_header:
				best_hea = best_hea.replace(best_hea.split(' ')[0], rid)
				print(best_hea, file=record_header, end="")
		with open("last_record", "w") as last_update:
			last_update.write(str(rid))
		bar.update(i)
