import psycopg2
import sys
import json

#Define our connection string
conn_string = "host='localhost' dbname='find-us-db' user='postgres' password='secret'"

# print the connection string we will use to connect
print "Connecting to database\n	->%s" % (conn_string)

# get a connection, if a connect cannot be made an exception will be raised here
conn = psycopg2.connect(conn_string)
print "Connected!\n"
# conn.cursor will return a cursor object, you can use this cursor to perform queries
cur = conn.cursor()


cur.execute("CREATE TABLE persons(" + 
	"ncmec_number varchar (500)," +
	"namus_number varchar (500)," +
	"org_name varchar (500)," +
	"org varchar (20)," +
	"org_contact varchar (500)," +
	"agency_name varchar (500)," +
	"agency_contact varchar (500)," +
	"date varchar (500)," +
	"city varchar (500)," +
	"state varchar (500)," +
	"county varchar (500)," +
	"country varchar (500)," +
	"circumstance varchar (5000)," +
	"first_name varchar (500)," +
	"middle_name varchar (500)," +
	"last_name varchar (500)," +
	"age varchar (20)," +
	"sex varchar (20)," +
	"race varchar (500)," +
	"eye_color varchar (500)," + 
	"hair_color varchar (500)," +
	"weight varchar (20)," +
	"height varchar (20)," +
	"photo varchar (500)," +
	"aged_photo varchar (500)"
");")

# Pass data to fill a query placeholders and let Psycopg perform
# the correct conversion (no more SQL injections!)
f = open('data/merged_ca.json', 'r')
missing_persons = json.loads(f.read())
f.close()
print missing_persons["NAMUS_17802"]["namus_number"]

for key, value in missing_persons.items():
	cur.execute("INSERT INTO persons (ncmec_number, namus_number, org_name, org, " +
		"org_contact, agency_name, agency_contact, date, city, state, county, country, " + 
		"circumstance, first_name, middle_name, last_name, age, sex, race, eye_color, " +
		"hair_color, weight, height, photo, aged_photo) VALUES (%(ncmec_number)s, " + 
		"%(namus_number)s, %(org_name)s, %(org)s, %(org_contact)s, %(agency_name)s," + 
		"%(agency_contact)s, %(date)s, %(city)s, %(state)s, %(county)s, %(country)s, " + 
		"%(circumstance)s, %(first_name)s, %(middle_name)s, %(last_name)s, %(age)s, " + 
		"%(sex)s, %(race)s, %(eye_color)s, %(hair_color)s, %(weight)s, %(height)s, " + 
		"%(photo)s, %(aged_photo)s)", value)

cur.execute("SELECT * FROM persons;")
print cur.fetchone()
#print cur.fetchall()
conn.commit()
