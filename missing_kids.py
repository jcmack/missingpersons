import requests
import json

session = requests.Session()
uri = "http://www.missingkids.com/missingkids/servlet/JSONDataServlet"
search_uri = "?action=publicSearch"
child_detail_uri = "?action=childDetail"
session.get(uri + search_uri + "&searchLang=en_US&search=new&subjToSearch=child&missState=All&missCountry=US")

response = session.get(uri + search_uri + "&searchLang=en_US&goToPage=1")
dct = json.loads(response.text)
print response.text
pgs = int(dct["totalPages"])
print "found {} pages".format(pgs)
for pg in range(1, pgs + 1):
	print "on page {}".format(pg)
	response = session.get(uri + search_uri + "&searchLang=en_US&goToPage=" + str(pg))
	dct = json.loads(response.text)
	print "found {} people".format(len(dct["persons"]))
	for person in dct["persons"]:
		print json.dumps(person, sort_keys=True, indent=4, separators=(',', ': '))
