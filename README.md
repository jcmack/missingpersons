Working with Missing Persons Data
=====

While there are a number of public facing databases containing missing persons data, I have chosen to work with 

- National Center for Missing & Exploited Children (NCMEC) www.missingkids.com and 
- National Missing and Unidentified Persons Systems Missing Persons Database www.findthemissing.org. 

Unfortunately both do not have public facing APIs or share a common data standard. 

Data was scraped from NCMEC utilizing Requests and its underlying JSON API, while NamUs data was gathered using Selenium. Data from both sources were cleaned, standardized and linked if duplicated.

Missing Persons Characteristics
=====

1. 	**ncmec_number**: NCMEC case number
2. 	**namus_number**: NamUs case number
3. 	**org_name**: long name of organization storing the information
4. 	**org**: organization abbreviation such as NCMEC and NAMUS
5. 	**org_contact**: contact information for the organization
6. 	**agency_name**: investigating agency usually local police department 
7. 	**agency_contact**: contact information for the agency
8. 	**date** (YYY-MM-DD HH:MM:SS): the date and miltary time when this person went missing
9. 	**city**: city where the person went missing
10. **state**: state where the person went missing
11.	**county**: county where the person went missing
12.	**country**: country where the missing person
13.	**circumstance**: description of the circumstances surrounding this disappearance
14.	**first_name**: first name of the missing person
15.	**middle_name**: middle name of the missing person
16.	**last_name**: last name of the missing person
17.	**age** (years): the current age of the missing person
18.	**sex**: {Female, Male}
19.	**race**: {"White", "Black/African American", "Asian or Pacific Islander", "Native American", "Non-White Hispanic/Latino", "White Hispanic/Latino", "Other", "Unknown"}
20.	**eye_color**: {"Blue", "Brown", "Hazel", "Gray", "Green", "Pink", "Maroon", "Black", "Multicolor", "Unknown"}
21.	**hair_color**: {"Brown", "Sandy", "Black", "Gray", "White", "Blonde", "Red/Auburn", "Unknown"}
22.	**weight** (pounds): the maximum weight of the missing person
23.	**height** (inches): the maximum height of the missing person
24.	**photo**: the url to a photo of the missing person
25.	**aged_photo**: the url to an age-enhanced photo of the missing person