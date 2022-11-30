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
    return dates

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


def combine(origin_lst, date_lst, credit_lst, materials_lst):
    all_info = []
    for i in range(len(origin)):
        if len(all_info) < 100:    
            all_info.append([origin_lst[i], date_lst[i], credit_lst[i], materials_lst[i]])
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
            f.write(x + ", ")
        f.write(list[-1][0])
        f.write("\n")
    f.close()
    return None

def setupDataBase(db_name):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_name)
    cur = conn.cursor()
    return cur, conn

def createtable(cur, conn):
    cur.execute('CREATE TABLE IF NOT EXISTS met (origin TEXT, date TEXT, credit TEXT, materials TEXT)')
    conn.commit()

def add_info(all_info, cur, conn):
    for list in all_info:
        cur.execute('INSERT OR IGNORE INTO met (origin, date, credit, materials) VALUES (?, ?, ?, ?)', (list[0], list[1], list[2], str(list[3])))
    conn.commit()

test = create_limited(query)
origin = find_origin(test)
date = find_date(test)
credit = find_credit(test)
materials = find_materials(test)
all = combine(origin, date, credit, materials)
# write_csv(all, "new_sample.csv")

cur, conn = setupDataBase("met.db")
createtable(cur, conn)
add_info(all, cur, conn)







