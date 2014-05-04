Working with Missing Persons Data
=====

There are a number of public databases that store missing persons data, but there exists two major problems: 

- The databases do not provide public API access and
- There is no common data standard for a missing persons case between databases. 

I want to collect all of the missing persons data into one common database to provide easy access to researchers and students.

First I chose to focus on merging [National Missing and Unidentified Persons System (NamUs)](www.findthemissing.org) and [National Center for Missing & Exploited Children (NCMEC)](www.missingkids.com). I crawled through the NCMEC database utilizing [Requests](http://docs.python-requests.org/en/latest/) and its underlying JSON API, while I used [Selenium](http://docs.seleniumhq.org/) to crawl NamUs. Data from both sources were cleaned, standardized and linked if duplicated. 

Crawling can be time consuming and hard to understand. I have created some iPython notebooks tutorials that walk through some of the basic building blocks of the code repository:

- [Extracting Data from NCMEC](http://nbviewer.ipython.org/gist/anonymous/4357ae2ea7bd1ffb3894)
- [Introduction to Selenium](http://nbviewer.ipython.org/gist/jcmack/e328b6a7add74ed75f80)
- [Extracting Data from NamUs](http://nbviewer.ipython.org/gist/anonymous/8de2535ea80dfc35c228)

Find Us API
=====

After all of the data was collected and merged into a single JSON file, I wanted to host the information. I used [PostgreSQL](http://www.postgresql.org/) to build a database, [Flask](http://flask.pocoo.org/) to handle the API requests and [Heroku](www.heroku.com) to host everything. For proof of concept, I decided to only host a snapshot of the missing persons data for California collected April 20, 2014. 

<code>find-us.herokuapp.com</code> - dumps all missing persons cases

<code>find-us.herokuapp.com/{country_abbrev}</code> - dumps all missing persons cases in country
<code>find-us.herokuapp.com/us</code>

<code>find-us.herokuapp.com/{country_abbrev}/{state}</code> - dumps all missing persons cases in country and state
<code>find-us.herokuapp.com/us</California<code>

<code>find-us.herokuapp.com/{country_abbrev}/{state}/{county}</code> - dumps all missing persons cases in country, state and county
<code>find-us.herokuapp.com/us/California/Los Angeles</code>

<code>find-us.herokuapp.com/{country_abbrev}/{state}/{county}/{city}</code> - dumps all missing persons cases in country, state, county and city
<code>find-us.herokuapp.com/us/California/Los Angeles/Los Angeles</code>

<code>find-us.herokuapp.com/search?{param=val}</code> - dumps all missing persons cases matching that criteria
<code>find-us.herokuapp.com/search?{param=val}&{param2=val2}</code>
<code>find-us.herokuapp.com/search?age_start={age}&age_end={age}</code>


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