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
		"county" : "",
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
		"height" : "",
		"photo" : "",
		"aged_photo" : ""
	})

def clean_date(d):
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

def capitalize(s):
	if s:
		arr = s.strip().split(" ")
		rets = ""
		for subs in arr:
			rets += subs[0].upper() + subs[1:].lower() + " "
		return rets.strip()
	return ""

def clean_race(race):
	races = ["White", "Black/African American", "Asian or Pacific Islander", "Native American", "Non-White Hispanic/Latino", "White Hispanic/Latino", "Other", "Unknown"]
	if race in races:
		return race
	elif race.lower() == "white":
		return "White"
	elif race.lower() == "black":
		return "Black/African American"
	elif race.lower() == "whitehisp":
		return "White Hispanic/Latino"
	elif race.lower() == "biracial":
		return "Other"
	elif race.lower() == "pacific" or race.lower() == "asian":
		return "Asian or Pacific Islander"
	elif race.lower() == "hispanic":
		return "Non-White Hispanic/Latino"
	elif race.lower() == "amind":
		return "Native American"
	elif race.lower() == "white":
		return "White"
	return "Unknown"

def clean_eye_color(eye_color):
	eye_colors = ["Blue", "Brown", "Hazel", "Gray", "Green", "Pink", "Maroon", "Black", "Multicolor"]
	if eye_color in eye_colors:
		return eye_color
	if capitalize(eye_color) in eye_colors:
		return capitalize(eye_color)
	return "Unknown"

def clean_hair_color(hair_color):
	hair_colors = ["Brown", "Sandy", "Black", "Gray", "White", "Blonde", "Red/Auburn"]
	if hair_color in hair_colors:
		return hair_color
	elif capitalize(hair_color) in hair_colors:
		return capitalize(hair_color)
	elif hair_color.lower() == "gray or partially gray" or hair_color.lower() == "grey":
		return "Gray"
	elif hair_color.lower() == "red" or hair_color.lower() == "auburn":
		return "Red/Auburn"
	elif hair_color.lower() == "ltbrown":
		return "Brown"
	elif hair_color.lower() == "blond/strawberry":
		return "Blonde"
	return "Unknown"

