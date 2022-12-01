import json
import unittest
import os
import requests
import csv
import re
import sqlite3
query = "https://collectionapi.metmuseum.org/public/collection/v1/objects"

def create_limited(query):
    limited_id = []
    resp = requests.get(query)
    museum_info = json.loads(resp.text)
    museum_id = museum_info['objectIDs']
    i = 0
    for x in range(len(museum_id)):
        if x == i:
            limited_id.append(museum_id[x])
            i += 300
        if i >= 30000:
            break
    return limited_id

def find_origin(limited_id):
    fst_lst = []
    for id in limited_id:
        new_query_string = "https://collectionapi.metmuseum.org/public/collection/v1/objects/"+str(id)
        resp = requests.get(new_query_string)
        object_info = json.loads(resp.text)
        fst_lst.append(object_info['country'])
    origin = []
    for item in fst_lst:
        if item == "":
            origin.append("unknown")
        else:
            origin.append(item)
    return origin
def convert_set(info):
    set_info = set(info)
    info_lst = list(set_info)
    return info_lst
def find_materials(limited_id):
    og_materials = []  
    for id in limited_id:
        new_query_string = "https://collectionapi.metmuseum.org/public/collection/v1/objects/"+str(id)
        resp = requests.get(new_query_string)
        object_info = json.loads(resp.text)      
        og_materials.append(object_info['medium'])
    materials =[]
    for x in og_materials:
        x = x.split(",")
        if x == ['']:
            materials.append("unknown")
        else:
            materials.append(x)
    return materials

def find_date(limited_id):
    created = []
    for id in limited_id:
        new_query_string = "https://collectionapi.metmuseum.org/public/collection/v1/objects/"+str(id)
        resp = requests.get(new_query_string)
        object_info = json.loads(resp.text)
        created.append(object_info['objectDate'])
    new_dates = []
    dates = []
    final_dates = []
    for date in created:
        if date == "":
            date = "unknown"
        search = re.findall('^(\d{4})|(^[u]{1}[a-z]{6})|^[a-z]{2}.\s(\d{4})|(^\d{2}[a-z]{2}\s[a-z]{7})|[a-z]{4}\s\d{2}[a-z]{2}–([a-z]{5}\s\d{2}[a-z]{2}\s[a-z]{7})|^[a-z]{5}\s(\d{4})|\d{2}[a-z]{2}–(\d{2}[a-z]{2}\s[a-z]{7})|[A-Z]{1}[a-z]{3}\s\d{2}[a-z]{2}–\s([a-z]{5}\s\d{2}[a-z]{2}\s[a-z]{7})|^([a-z]{4}\s\d{2}[a-z]{2}\s[a-z]{7})|^[a-z]{5},\s(\d{2}[a-z]{2}\s[a-z]{7})|\d{1}[a-z]{2}–(\d{1}[a-z]{2}\s[a-z]{7})|^[a-z]{5}\s(\d{2}[a-z]{2}\s[a-z]{7})|^[a-z]{8}\s\d{2}[a-z]{2}–(\d{2}[a-z]{2}\s[a-z]{7})', date)
        new_dates.append(search)
    for lst in new_dates:
        if lst != []:
            for tup in lst:
                for date in tup:
                    if date != '':
                        dates.append(date)
        else:
            dates.append("unknown")
    for x in dates:
        if "th century" in x:
            if "2" in x:
                x = "150"
            if "3" in x:
                x = "250"
            if "4" in x:
                x = "350"
            if "5" in x:
                x = "450"
            if "6" in x:
                x = "550"
            if "7" in x:
                x = "650"
            if "8" in x:
                x = "750"
            if "9" in x:
                x = "850"
            if "10" in x:
                x = "950"
            if "11" in x:
                x = "1050"
            if "12" in x:
                x = "1150"
            if "13" in x:
                x = "1250"
            if "14" in x:
                x = "1350"
            if "15" in x:
                x = "1450"
            if "16" in x:
                x = "1550"
            if "17" in x:
                x = "1650"
            if "18" in x:
                x = "1750"
            if "19" in x:
                x = "1850"
            if "20" in x:
                x = "1950"
        if x == "unknown":
            x = 0
        x = int(x)
        final_dates.append(x)
    return final_dates

def find_credit(limited_id):
    old_credit = []
    for id in limited_id:
        new_query_string = "https://collectionapi.metmuseum.org/public/collection/v1/objects/"+str(id)
        resp = requests.get(new_query_string)
        object_info = json.loads(resp.text)
        old_credit.append(object_info['creditLine'])
    new_credit = []
    credit_line = []
    credit = []
    for line in old_credit:
        line = line.lower()
        searching = re.findall('^([g]{1}[i]{1}[a-z]{2})|\s([f]{1}[u]{1}[n]{1}[d]{1})|^([bequest]{7})|[anonymous]{9}\s([gift]{4})|^([purchase]{8}),\s[gift]{4}\s[o]{1}|^([purchase]{8}),\s[jose]{4}|^([purchase]{8}),\s[arth]{4}|,\s([bequest]{7})|([giovanni]{8})|,\s([gift]{4})\s[of]{2}\s[howard]{6}|,\s([gift]{4})\s[of]{2}\s[edward]{6}|^([fund]{4})|^([purchase]{8}),\s[b]{1}|([purchase]{8}),\s[so]{2}', line)
        new_credit.append(searching)
    for lst in new_credit:
        if lst != []:
            for tup in lst:
                for c in tup:
                    if c != '':
                        credit_line.append(c)
        else:
            credit_line.append("unknown")

    for z in credit_line:
        if z == "bequest":
            credit.append("donation")
        elif z == "giovanni":
            credit.append("gift")
        else:
            credit.append(z)
    return credit


def combine(origin_lst, date_lst, credit_lst):
    all_info = []
    for i in range(len(origin_lst)):
        if len(all_info) < 100:    
            all_info.append([origin_lst[i], date_lst[i], credit_lst[i]])
        else:
            break
    return all_info


def write_csv(data, filename):
    f = open(filename, "w")
    header = ["Place of Origin", "Date", "Credit", "Materials"]
    for x in header[0:-1]:
        f.write(x + ", ")
    f.write(header[-1])
    f.write("\n")
    for list in data:
        for x in list[0:-1]:
            f.write(str(x) + ", ")
        f.write(str(list[-1][0]))
        f.write("\n")
    f.close()
    return None

def total_countries(met_origin, chicago_origin):
    both_countries = []
    for item in met_origin:
        both_countries.append(item)
    for item in chicago_origin:
        both_countries.append(item)
    return both_countries

def setupDataBase(db_name):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_name)
    cur = conn.cursor()
    return cur, conn

def createtable(cur, conn):
    cur.execute('CREATE TABLE IF NOT EXISTS met (origin TEXT, date INT, credit TEXT)')
    cur.execute('CREATE TABLE IF NOT EXISTS countries (country_id INT, country TEXT)')
    cur.execute('CREATE TABLE IF NOT EXISTS dates (dates_id INT, date INT)')
    cur.execute('CREATE TABLE IF NOT EXISTS credit (credit_id INT, credit TEXT)')
    conn.commit()

def add_info(all_info, unique_origin, unique_credit, cur, conn):
    for list in all_info:
        cur.execute('INSERT OR IGNORE INTO met (origin, date, credit) VALUES (?, ?, ?)', (unique_origin.index(list[0]), list[1], unique_credit.index(list[2])))
    conn.commit()
def add_country(country_lst, cur, conn):  
    for country in country_lst:
        cur.execute('INSERT OR IGNORE INTO countries (country_id, country) VALUES (?, ?)', (country_lst.index(country), country))
    conn.commit()
def add_date(date_lst, cur, conn):
    for date in date_lst:
        cur.execute('INSERT OR IGNORE INTO dates (dates_id, date) VALUES (?, ?)', (date_lst.index(date), date))
    conn.commit()
def add_credit(credit_lst, cur, conn):
    for credit in credit_lst:
        cur.execute('INSERT OR IGNORE INTO credit (credit_id, credit) VALUES (?, ?)', (credit_lst.index(credit), credit))
    conn.commit()  



# european musueum data

#open api
file='https://api.artic.edu/api/v1/artworks?limit=100'
req=requests.get(file).text
# print(type(req))
load=json.loads(req)
# p.pprint(load)

# DICTIONARIES (shows how many of each)
dates={}
data=load['data']
# print(data)

for x in data:
    years=x['date_start']
    if years not in dates:
        dates[years]=1
    else:
        dates[years]+=1
# print(dates)

# material_type={}
# for x in data:
#     material=x['material_titles']
#     for type in material:
#         if type not in material_type:
#             material_type[type]=1
#         else:
#             material_type[type]+=1
# print(material_type)

origin_place={}
for x in data:
    place=x['place_of_origin']
    if place not in origin_place:
        origin_place[place]=1
    else:
        origin_place[place]+=1
# print(origin_place)

# -----------------------------------------------------------------------
# LISTS to make table

dates_list=[]
for x in data:
    years=x['date_start']
    if years== None:
        dates_list.append('Unknown')
    else:
        dates_list.append(years)
# print(len(dates_list))

# material_type_list=[]
# for x in data:
#     material=x['material_titles']
#     if material==[]:
#         material_type_list.append(['digital'])
#     else:
#         material_type_list.append(material)
# print(len(material_type_list))

origin_place_list=[]
for x in data:
    place=x['place_of_origin']
    if place==None:
        origin_place_list.append("Unknown")
    else:
        origin_place_list.append(place)
# print(origin_place_list)

credits_list=[]
for x in data:
    credit=x['credit_line']
    # print(credit)
    if 'purchase' in credit.lower():
        credits_list.append('Purchased')
    elif 'fund' in credit.lower():
        credits_list.append('Fund')
    elif 'gift' in credit.lower():
        credits_list.append('Gift')
    elif 'donors' or "collection" in credit.lower():
        credits_list.append('Donation')
    elif 'trust' in credit.lower():
        credits_list.append("Donation")
    elif 'endowment' in credit.lower():
        credits_list.append("Donation")
    elif 'acquisitions' in credit.lower():
        credits_list.append("Purchased")
    elif 'bequest' in credit.lower():
        credits_list.append("Donation")
    else:
        credits_list.append(credit)
# print(credits_list)

# Combining the data based on index
lst_combined=[]
for idx in range(len(origin_place_list)):
        lst_combined.append((origin_place_list[idx], dates_list[idx], credits_list[idx]))


# Making data table
# filename=open('/Users/samlawrence/Desktop/Final Project 206/data_chicago.csv', 'w')
# writer=csv.writer(filename)    
# data=load['data']
# header=["Place of Origin","Date","Credit"]
# writer=csv.writer(filename, delimiter=",")
# writer.writerow(header)
# for x in lst_combined:
#     writer.writerow(x)

chicago = combine(origin_place_list, dates_list, credits_list)

test = create_limited(query)
origin = find_origin(test)
date = find_date(test)
credit = find_credit(test)

both_countries = total_countries(origin, origin_place_list)
unique_both_countries = convert_set(both_countries)

# materials = find_materials(test)
all = combine(origin, date, credit)

unique_origin = convert_set(origin)
unique_dates = convert_set(date)
unique_credit = convert_set(credit)

# write_csv(all, "new_sample.csv")

cur, conn = setupDataBase("met.db")
createtable(cur, conn)
add_info(all, unique_both_countries, unique_credit, cur, conn)
add_country(unique_both_countries, cur, conn)
add_date(unique_dates, cur, conn)
add_credit(unique_credit, cur, conn)
