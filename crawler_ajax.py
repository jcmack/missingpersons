import us
import time
import json
import browsers
import common
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

def select_state(browser, state):
	elem = browser.wait_until_clickable("search_Circumstances.StateLKA", timeout=30)
	browser.select_option(elem, state)

def wait_for_table_to_load(table, rows, timeout=10):
	index = 0
	while index != timeout:
		if len(table.find_elements_by_tag_name("tr")) == rows + 1:
			break
		time.sleep(1)
		index += 1

def parse_state(browser, state):
	browser.get("https://www.findthemissing.org/en")
	#search by state
	select_state(browser, state)
	browser.find_element_by_name("commit").click()

	#select to show 100 entries per page
	#elem = browser.wait_until_clickable("select.selbox", by=By.CSS_SELECTOR, timeout=120)
	#browser.select_option(elem, str(100))

	#wait for new entries to show up
	table = browser.wait_until_visible("list")
	#wait_for_table_to_load(table, 10, timeout=30)

	browser.get("https://www.findthemissing.org/en/ajax/search_results?page=1&rows=100&sidx=DateLKA&sord=desc&_search=false")
	dct = json.loads(browser.find_element_by_css_selector("body").text)
	pgs = int(dct["total"])
	print "found {} pages".format(pgs)
	missing_persons = []

	person = dct["rows"][5]
	for person in dct["rows"]:
		new_person = common.create_new_record()
		#organization
		new_person["namus_number"] =  person["cell"][0]
		new_person["org_name"] =  "National Missing and Unidentified Persons System"
		new_person["org"] =  "NAMUS"
		new_person["org_contact"] = "1-855-626-7600"

		#personal characteristics
		new_person["sex"] =  person["cell"][4].lower()
		new_person["race"] =  person["cell"][5].lower()
		new_person["age"] =  person["cell"][6]

		arr = person["id"].split("_")
		browser.get("https://www.findthemissing.org/en/cases/" + arr[0] + "/" + arr[1])
		time.sleep(10)
		if browser.find_element_by_xpath("//div[@id='case_information']/div/table/tbody/tr[6]/td/label").text == "NCMEC number":
			print "**********MERGE"
			continue

		#case info
		new_person["photo"] = browser.find_element_by_css_selector("dt.photo > img").get_attribute("src")
		new_person["first_name"] = browser.find_element_by_xpath("//div[@id='case_information']/div/table/tbody/tr[2]/td[2]").text.upper()
		new_person["middle_name"] = browser.find_element_by_xpath("//div[@id='case_information']/div/table/tbody/tr[3]/td[2]").text.upper()
		new_person["last_name"] = browser.find_element_by_xpath("//div[@id='case_information']/div/table/tbody/tr[4]/td[2]").text.upper()
		date = browser.find_element_by_xpath("//div[@id='case_information']/div/table/tbody/tr[6]/td[2]").text
		new_person["date"] = common.convert_date(date)

		height = browser.find_element_by_xpath("//div[@id='case_information']/div[2]/table/tbody/tr[6]/td[2]").text
		if "to" in height:
			arr = height.split("to")
			height = arr[1].strip()
		new_person["height"] = float(height)
		weight = browser.find_element_by_xpath("//div[@id='case_information']/div[2]/table/tbody/tr[7]/td[2]").text
		if "to" in weight:
			arr = weight.split("to")
			weight = arr[1].strip()
		new_person["weight"] = float(weight)

		browser.find_element_by_link_text("Circumstances").click()
		time.sleep(3)

		#circumstance
		new_person["city"] = browser.find_element_by_css_selector("div.column1-unit > table > tbody > tr > td.view_field").text.upper()
		new_person["state"] = browser.find_element_by_xpath("//div[@id='circumstances']/div/table/tbody/tr[2]/td[2]").text.upper()
		new_person["country"] = "US"
		try:
			new_person["circumstance"] = browser.find_element_by_id("case_Circumstances").text
		except NoSuchElementException:
			new_person["circumstance"] = ""

		browser.find_element_by_link_text("Physical / Medical").click()
		time.sleep(3)

		#physical
		new_person["hair_color"] = browser.find_element_by_xpath("//div[@id='physical_characteristics']/div/table/tbody/tr/td[3]").text.lower()
		new_person["eye_color"] = browser.find_element_by_xpath("//div[@id='physical_characteristics']/div/table/tbody/tr[5]/td[3]").text.lower()

		browser.find_element_by_link_text("Investigating Agency").click()
		time.sleep(3)

		new_person["agency_name"] = browser.find_element_by_xpath("//div[@id='police_information']/div[2]/table/tbody/tr[2]/td[2]").text + " (" + browser.find_element_by_xpath("//div[@id='police_information']/div[2]/table/tbody/tr[6]/td[2]").text + ")"
		new_person["agency_contact"] = browser.find_element_by_xpath("//div[@id='police_information']/div/table/tbody/tr[4]/td[2]").text
		
		print new_person
		missing_persons.append(new_person)

	return missing_persons

browser = browsers.Firefox()
state = "alabama"
cases = parse_state(browser, state)
f = open(state + ".json", "w")
f.write(json.dumps(cases, sort_keys=True, indent=4, separators=(',', ': ')))
f.close()
browser.close