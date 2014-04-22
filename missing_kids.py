import requests
import json
import common

session = requests.Session()
uri = "http://www.missingkids.com"
json_srv_uri = uri + "/missingkids/servlet/JSONDataServlet"
search_uri = "?action=publicSearch"
child_detail_uri = "?action=childDetail"
session.get(json_srv_uri + search_uri + "&searchLang=en_US&search=new&subjToSearch=child&missState=CA&missCountry=US")

response = session.get(json_srv_uri + search_uri + "&searchLang=en_US&goToPage=1")
dct = json.loads(response.text)
pgs = int(dct["totalPages"])
print "found {} pages".format(pgs)
missing_persons = []

for pg in range(1, pgs + 1):
    print "on page {}".format(pg)
    response = session.get(json_srv_uri + search_uri + "&searchLang=en_US&goToPage=" + str(pg))
    dct = json.loads(response.text)
    print "found {} people".format(len(dct["persons"]))
    #print json.dumps(dct, sort_keys=True, indent=4, separators=(',', ': '))
    for person in dct["persons"]:
        new_person = common.create_new_record()
        #print json.dumps(person, sort_keys=True, indent=4, separators=(',', ': '))
        print json_srv_uri + child_detail_uri + "&caseNum={}&orgPrefix={}".format(person["caseNumber"], person["orgPrefix"])
        detailed_response = session.get(json_srv_uri + child_detail_uri + "&caseNum={}&orgPrefix={}".format(person["caseNumber"], person["orgPrefix"]))
        detailed_person = json.loads(detailed_response.text)["childBean"]
        #print json.dumps(detailed_person, sort_keys=True, indent=4, separators=(',', ': '))
        
        #organization
        new_person["ncmec_number"] = person["caseNumber"]
        new_person["org_name"] = person["orgName"]
        new_person["org"] = person["orgPrefix"]
        new_person["org_contact"] = detailed_person["orgContactInfo"]

        #skip unidentified remains cases
        if  new_person["org_name"] == "NCMEC-Unidentified":
            continue

        if detailed_person["altContact"]:
            (agency_name, agency_phone) = common.extract_agency_info(detailed_person["altContact"])
            new_person["agency_name"] = agency_name.replace("  ", " ")
            new_person["agency_contact"] = agency_phone

        #circumstance
        if "missingDate" in person.keys():
            new_person["date"] = common.clean_date(person["missingDate"])
        new_person["circumstance"] = detailed_person["circumstance"]
        new_person["city"] = common.capitalize(person["missingCity"])
        new_person["county"] = common.capitalize(person["missingCounty"])

        #skip US terrorities
        try:
            new_person["state"] = common.convert_state_abbrev(person["missingState"])
        except KeyError:
            continue
        new_person["country"] = person["missingCountry"]

        #personal characteristics
        new_person["first_name"] = common.capitalize(person["firstName"])
        middle_name = common.capitalize(person["middleName"])
        if len(middle_name) == 1:
            middle_name += "."
        new_person["middle_name"] = middle_name
        new_person["last_name"] = common.capitalize(person["lastName"])
        new_person["age"] = float(person["age"])
        if new_person["age"] < 0:
            try:
                new_person["age"] = float(person["approxAge"])
            except ValueError:
                if "months" in person["approxAge"].lower():
                    new_person["age"] = float(person["approxAge"].lower().replace("months", "").strip())/12.0 
                elif "-" in person["approxAge"]:
                    new_person["age"] = float(person["approxAge"].split("-")[1])
        new_person["sex"] = common.capitalize(detailed_person["sex"])
        new_person["race"] = common.clean_race(detailed_person["race"])
        new_person["eye_color"] = common.clean_eye_color(detailed_person["eyeColor"])
        new_person["hair_color"] = common.clean_hair_color(detailed_person["hairColor"])

        if detailed_person["weightInPound"]:
            new_person["weight"] = float(detailed_person["weight"])
        else: #convert to lb
            new_person["weight"] = float(detailed_person["weight"]) * 2.20462
        if detailed_person["heightInInch"]:
            new_person["height"] = float(detailed_person["height"])
        else: #convert to in
            new_person["height"] = float(detailed_person["height"]) * 0.393701 

        #images
        new_person["photo"] = uri + person["thumbnailUrl"]
        if detailed_person["hasAgedPhoto"]:
            new_person["aged_photo"] = uri + "/photographs/" + person["orgPrefix"] + str(person["caseNumber"]) + "e" + str(person["seqNumber"]) + ".jpg"
        
        missing_persons.append(new_person)
        #print json.dumps(new_person, sort_keys=True, indent=4, separators=(',', ': '))

f = open('ncmc_ca.json', 'w')
f.write(json.dumps(missing_persons, sort_keys=False, indent=4, separators=(',', ': ')))