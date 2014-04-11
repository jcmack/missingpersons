import us
import time
import json
import browsers
from selenium.webdriver.common.by import By

class NamUsPerson(object):
	def __init__(self, case_num, name, date_last_seen, loc, sex, race, age):
		self.case_num = case_num
		self.name = name
		self.date_last_seen = date_last_seen
		self.loc = loc
		self.sex = sex
		self.race = race
		self.age = age

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

def parse_results(table, timeout=10):
    rows = table.find_elements_by_tag_name("tr")
    headers = ["mp", "name", "date_last_seen", "location", "sex", "race", "age"]
    tbl = []
    for (row_num, row) in enumerate(rows[1:]):
        cols = row.find_elements_by_tag_name("td")
        dct = {}
        for (col_num, col) in enumerate(cols):
            dct[headers[col_num]] = col.text
        tbl.append(dct)
    return tbl

def parse_state(browser, state):
	browser.get("https://www.findthemissing.org/en")
	#search by state
	select_state(browser, state)
	browser.find_element_by_name("commit").click()

	#select to show 100 entries per page
	elem = browser.wait_until_clickable("select.selbox", by=By.CSS_SELECTOR, timeout=120)
	browser.select_option(elem, str(100))

	#wait for new entries to show up
	table = browser.wait_until_visible("list")
	wait_for_table_to_load(table, 100, timeout=30)

	num_cases = int(browser.wait_until_visible("search_cases_found_count").text)
	curr_pg = 1
	total_pgs = num_cases / 100
	last_pg_num_cases = 0
	if num_cases % 100 > 0:
		total_pgs += 1
		last_pg_num_cases = num_cases % 100
	all_cases = []
	#loop through the pages
	while curr_pg <= total_pgs:
		if curr_pg == total_pgs:
			wait_for_table_to_load(table, last_pg_num_cases, timeout=30)
		else:
			wait_for_table_to_load(table, 100, timeout=30)
		cases = parse_results(table)
		print cases
		print len(cases)
		all_cases += cases
		browser.find_element_by_id("next").click()
		time.sleep(10)
		curr_pg += 1
	return all_cases

browser = browsers.Firefox()
state = "alabama"
cases = parse_state(browser, state)
f = open(state + ".json", "w")
f.write(json.dumps(cases, sort_keys=True, indent=4, separators=(',', ': ')))
f.close()
browser.close