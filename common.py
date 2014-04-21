import re
import datetime

def create_new_record():
	return dict({
		"case_number" : "",
		"org_name" : "", 
		"org" : "",
		"org_contact" : "", 
		"agency_name" : "",
		"agency_contact" : "",
		"date" : "", 
		"city" : "",
		"state" : "",
		"country" : "",
		"circumstance" : "",
		"first_name" : "",
		"middle_name" : "",
		"last_name" : "",
		"age" : "",
		"sex" : "",
		"race" : "",
		"eye_color" : "",
		"hair_color" : "",
		"weight" : "",
		"photo" : "",
		"aged_photo" : "",
		"ncmc_profile" : "",
		"namus_profile" : ""
	})

def convert_date(d):
	return str(datetime.datetime.strptime(d, "%b %d, %Y %I:%M:%S %p"))

def extract_agency_info(contact):
	match = re.search("[\d-]*\d{3}[ |]*-\d{3}[ |]*-\d{4}", contact)
	agency_phone = ""
	if match: 
		agency_phone = match.group(0)
	agency_name = contact.replace(agency_phone, "").strip()
	return (agency_name, agency_phone)
