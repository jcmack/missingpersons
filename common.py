import re
import datetime

def create_new_record():
	return dict({
		"ncmec_number" : "",
		"namus_number" : "",
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
		"aged_photo" : ""
	})

def convert_date(d):
	try:
		date = str(datetime.datetime.strptime(d, "%b %d, %Y %I:%M:%S %p"))
	except ValueError:
		date = str(datetime.datetime.strptime(d, "%B %d, %Y %H:%M"))
	return date

def extract_agency_info(contact):
	match = re.search("[\d-]*\d{3}[ |]*-\d{3}[ |]*-\d{4}", contact)
	agency_phone = ""
	if match: 
		agency_phone = match.group(0)
	agency_name = contact.replace(agency_phone, "").strip()
	return (agency_name, agency_phone)

def is_std_eye_color(eye_color):
	print "bunies"

def convert_state_abbrev(state_abbrev):
	states = {
		"AL" : "Alabama",
		"AK" : "Alaska",
		"AZ" : "Arizonia", 
		"AR" : "Arkansas", 
		"CA" : "California", 
		"CO" : "Colorado", 
		"CT" : "Connecticut", 
		"DE" : "Delaware", 
		"FL" : "Florida", 
		"GA" : "Georgia",
		"HI" : "Hawaii", 
		"ID" : "Idaho", 
		"IL" : "Illinois", 
		"IN" : "Indiana", 
		"IA" : "Iowa", 
		"KS" : "Kansas",
		"KY" : "Kentucky",
		"LA" : "Louisiana",
		"ME" : "Maine",
		"MT" : "Montana",
		"NE" : "Nebraska",
		"NV" : "Nevada",
		"NH" : "New Hampshire",
		"NJ" : "New Jersey",
		"NM" : "New Mexico",
		"NY" : "New York",
		"NC" : "North Carolina",
		"ND" : "North Dakota",
		"OH" : "Ohio",
		"OK" : "Oklahoma", 
		"OR" : "Oregon",
		"MD" : "Maryland",
		"MA" : "Massachusetts",
		"MI" : "Michigan",
		"MN" : "Minnesota",
		"MS" : "Mississippi",
		"MO" : "Missouri",
		"PA" : "Pennsylvania",
		"RI" : "Rhode Island",
		"SC" : "South Carolina",
		"SD" : "South Dakota",
		"TN" : 'Tennessee',
		"TX" : "Texas",
		"UT" : "Utah",
		"VT" : "Vermont",
		"VA" : "Virginia",
		"WA" : "Washington",
		"WV" : "West Virginia",
		"WI" : "Wisconsin",
		"WY" : "Wyoming"
	}
	return states[state_abbrev]
