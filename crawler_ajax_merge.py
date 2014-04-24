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

def parse_state(browser, state, missing_persons=None):
	
	if not missing_persons:
		missing_persons = {}

	browser.get("https://www.findthemissing.org/en")
	#search by state
	select_state(browser, state)
	browser.find_element_by_name("commit").click()

	#select to show 100 entries per page
	#elem = browser.wait_until_clickable("select.selbox", by=By.CSS_SELECTOR, timeout=120)
	#browser.select_option(elem, str(100))

	#wait for new entries to show up
	table = browser.wait_until_visible("list", timeout=30)
	#wait_for_table_to_load(table, 10, timeout=30)

	browser.get("https://www.findthemissing.org/en/ajax/search_results?page=1&rows=100&sidx=DateLKA&sord=desc&_search=false")
	dct = json.loads(browser.find_element_by_css_selector("body").text)
	pgs = int(dct["total"])
	print "found {} pages".format(pgs)

	for pg in range(1, pgs + 1):
		browser.get("https://www.findthemissing.org/en/ajax/search_results?page=" + str(pg) + "&rows=100&sidx=DateLKA&sord=desc&_search=false")
		dct = json.loads(browser.find_element_by_css_selector("body").text)
		print "page " + str(pg) + " of " + str(pgs)
		for (num, person) in enumerate(dct["rows"]):
			print "person " + str(num + 1) + " of " + str(len(dct["rows"]))
			new_person = common.create_new_record()
			#organization
			new_person["namus_number"] =  person["cell"][0]
			new_person["org_name"] =  "National Missing and Unidentified Persons System"
			new_person["org"] =  "NAMUS"
			new_person["org_contact"] = "1-855-626-7600"

			#personal characteristics
			new_person["sex"] = common.capitalize(person["cell"][4])
			new_person["race"] = person["cell"][5]
			new_person["age"] = float(person["cell"][6])

			arr = person["id"].split("_")
			browser.get("https://www.findthemissing.org/en/cases/" + arr[0] + "/" + arr[1])
			time.sleep(10)
			has_NCMEC_lbl = False
			if browser.find_element_by_xpath("//div[@id='case_information']/div/table/tbody/tr[6]/td/label").text == "NCMEC number":
				has_NCMEC_lbl = True 
				ncmec_case_number = browser.find_element_by_xpath("//div[@id='case_information']/div/table/tbody/tr[6]/td[2]").text.strip()
				if "NCMEC_" + ncmec_case_number in missing_persons.keys():
					print "found NCMEC_" + ncmec_case_number + " so merging..."
					missing_persons["NCMEC_" + ncmec_case_number]["namus_number"] = new_person["namus_number"]
					continue

			#case info
			photo = browser.find_element_by_css_selector("dt.photo > img").get_attribute("src")
			if "no_photo" not in photo:
				new_person["photo"] = browser.find_element_by_css_selector("dt.photo > img").get_attribute("src")
			new_person["first_name"] = common.capitalize(browser.find_element_by_xpath("//div[@id='case_information']/div/table/tbody/tr[2]/td[2]").text)
			new_person["middle_name"] = common.capitalize(browser.find_element_by_xpath("//div[@id='case_information']/div/table/tbody/tr[3]/td[2]").text.replace("\"", ""))
			new_person["last_name"] = common.capitalize(browser.find_element_by_xpath("//div[@id='case_information']/div/table/tbody/tr[4]/td[2]").text)

			if has_NCMEC_lbl:
				date = browser.find_element_by_xpath("//div[@id='case_information']/div/table/tbody/tr[7]/td[2]").text			
			else:
				date = browser.find_element_by_xpath("//div[@id='case_information']/div/table/tbody/tr[6]/td[2]").text
			new_person["date"] = common.clean_date(date)

			#determining white or non-white hispanic
			if new_person["race"] == "White" or new_person["race"] == "Other":
				ethnicity = browser.find_element_by_xpath("//div[@id='case_information']/div[2]/table/tbody/tr[4]/td[2]").text
				if ethnicity == "Hispanic/Latino" and new_person["race"] == "White":
					new_person["race"] = "White Hispanic/Latino"
				if ethnicity == "Hispanic/Latino" and new_person["race"] == "Other":
					new_person["race"] = "Non-White Hispanic/Latino"
			new_person["race"] = common.clean_race(new_person["race"]) 

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
			new_person["city"] = common.capitalize(browser.find_element_by_css_selector("div.column1-unit > table > tbody > tr > td.view_field").text)
			new_person["state"] = common.capitalize(browser.find_element_by_xpath("//div[@id='circumstances']/div/table/tbody/tr[2]/td[2]").text)
			new_person["county"] = common.capitalize(browser.find_element_by_xpath("//div[@id='circumstances']/div/table/tbody/tr[4]/td[2]").text)
			new_person["country"] = "US"
			try:
				new_person["circumstance"] = browser.find_element_by_id("case_Circumstances").text
			except NoSuchElementException:
				new_person["circumstance"] = ""

			browser.find_element_by_link_text("Physical / Medical").click()
			time.sleep(3)

			#physical
			new_person["hair_color"] = common.clean_hair_color(browser.find_element_by_xpath("//div[@id='physical_characteristics']/div/table/tbody/tr/td[3]").text)
			left_eye_color = browser.find_element_by_xpath("//div[@id='physical_characteristics']/div/table/tbody/tr[5]/td[3]").text		
			right_eye_color = browser.find_element_by_xpath("//div[@id='physical_characteristics']/div/table/tbody/tr[6]/td[3]").text
			if left_eye_color == right_eye_color:
				new_person["eye_color"] = common.clean_eye_color(left_eye_color)
			else:
				new_person["eye_color"] = "Multicolor"
			browser.find_element_by_link_text("Investigating Agency").click()
			time.sleep(3)

			state = browser.find_element_by_xpath("//div[@id='police_information']/div[2]/table/tbody/tr[6]/td[2]").text 
			state_paren = ""
			if state:
				state_paren = " (" + state + ")"
			new_person["agency_name"] = browser.find_element_by_xpath("//div[@id='police_information']/div[2]/table/tbody/tr[2]/td[2]").text + state_paren
			new_person["agency_contact"] = browser.find_element_by_xpath("//div[@id='police_information']/div/table/tbody/tr[4]/td[2]").text
			
			#print new_person
			missing_persons["NAMUS_" + new_person["namus_number"]] = new_person

	return missing_persons

f = open('ncmc_ca1.json', 'r')
missing_persons = json.loads(f.read())
f.close()

browser = browsers.Firefox()
state = "California"
cases = parse_state(browser, state, missing_persons=missing_persons)
f = open(state + ".json", "w")
f.write(json.dumps(cases, sort_keys=True, indent=4, separators=(',', ': ')))
f.close()
browser.close