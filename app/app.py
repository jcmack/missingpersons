import os
import json
import urlparse
from flask import Flask
from flask import request
import psycopg2
from psycopg2.extras import DictCursor

import common

urlparse.uses_netloc.append("postgres")
url = urlparse.urlparse(os.environ["DATABASE_URL"])

conn = psycopg2.connect(
    database=url.path[1:],
    user=url.username,
    password=url.password,
    host=url.hostname,
    port=url.port
)
dict_cur = conn.cursor(cursor_factory=DictCursor)

app = Flask(__name__)


def query(q):
    if "FAVICON.ICO" in q:
        return []
    app.logger.info(q)
    dict_cur.execute(q)
    new_records = []
    for row in dict_cur.fetchall():
        new_record = {}
        for i, value in enumerate(row):
            new_record[dict_cur.description[i][0]] = value
        new_records.append(new_record)
    app.logger.info("found " + str(len(new_records)) + " persons")
    return new_records

@app.route('/')
def index():
    return json.dumps(query("SELECT * FROM persons;"))

@app.route('/<country_abbrev>')
def index_country(country_abbrev):
    return json.dumps(query("SELECT * FROM persons WHERE country = \'" + country_abbrev.upper() + "\';"))

@app.route('/<country_abbrev>/<state>')
def index_state(country_abbrev, state):
    resp = query("SELECT * FROM persons " +
        "WHERE country = \'" + country_abbrev.upper() + "\' " +
            "AND state =\'" + common.capitalize(state) + "\';")
    return json.dumps(resp)

@app.route('/<country_abbrev>/<state>/<county>')
def index_county(country_abbrev, state, county):
    resp = query("SELECT * FROM persons " +
        "WHERE country = \'" + country_abbrev.upper() + "\' " +
            "AND state =\'" + common.capitalize(state) + "\' " +
            "AND county =\'" + common.capitalize(county) + "\';")
    return json.dumps(resp)

@app.route('/<country_abbrev>/<state>/<county>/<city>')
def index_city(country_abbrev, state, county, city):
    resp = query("SELECT * FROM persons " +
        "WHERE country = \'" + country_abbrev.upper() + "\' " +
            "AND state =\'" + common.capitalize(state) + "\' " +
            "AND county =\'" + common.capitalize(county) + "\' " +
            "AND city =\'" + common.capitalize(city) + "\';")
    return json.dumps(resp)

@app.route('/identifiers/race')
def id_race():
    return json.dumps(["Asian or Pacific Islander", "Black/African American", "Native American", "Non-White Hispanic/Latino", "Other", "Unknown", "White", "White Hispanic/Latino"])

@app.route('/identifiers/eye_color')
def id_eye():
    return json.dumps(["Black", "Blue", "Brown", "Gray", "Green", "Hazel", "Maroon", "Multicolor", "Pink", "Unknown"])

@app.route('/identifiers/hair_color')
def id_hair():
    return json.dumps(["Black", "Blonde", "Brown", "Gray", "Red/Auburn", "Sandy", "Unknown", "White"])

@app.route('/identifiers/sex')
def id_sex():
    return json.dumps(["Female", "Male", "Unknown"])

@app.route('/search')
def search(): #search?hair_color=Blonde, #search?age_start=10&age_end=15
    queries = []
    params = ["country", "state", "county", "city", "first_name", "last_name", "sex",
    "race", "eye_color", "hair_color", "age", "age_start", "weight","weight_start",
    "height", "height_start", "date", "date_start"]
    sql = "SELECT * FROM persons WHERE "
    for param in params:
        if request.args.get(param):
            if param == "age_start":
                queries.append("age::numeric BETWEEN " 
                    + request.args.get("age_start") 
                    + " AND "+ request.args.get("age_end"))
            elif param == "weight_start":
                queries.append("weight::numeric BETWEEN " 
                    + request.args.get("weight_start") 
                    + " AND "+ request.args.get("weight_end"))
            elif param == "height_start":
                queries.append("height::numeric BETWEEN " 
                    + request.args.get("height_start") 
                    + " AND "+ request.args.get("height_end"))
            elif param == "date_start":
                app.logger.info("date start is " + request.args.get("date_start") )
                app.logger.info("date end is " + request.args.get("date_end") )
                queries.append("date::timestamp >= '" 
                    + request.args.get("date_start") 
                    + "'::timestamp AND date::timestamp <= '"+ request.args.get("date_end") + "'::timestamp")
            else:
                queries.append(param + " = \'" + request.args.get(param) + "\'")
    for q in queries[:-1]:
        sql += q + " AND "
    sql += queries[-1] + ";"
    resp = query(sql)
    return json.dumps(resp)

if __name__ == '__main__':
    #app.run(debug = True)
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)