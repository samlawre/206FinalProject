import json 
import os
import requests
import pprint
import csv
import sqlite3
p=pprint.PrettyPrinter(indent=3)

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
print(lst_combined)


# Making data table
filename=open('/Users/samlawrence/Desktop/Final Project 206/data_chicago.csv', 'w')
writer=csv.writer(filename)    
data=load['data']
header=["Place of Origin","Date","Credit"]
writer=csv.writer(filename, delimiter=",")
writer.writerow(header)
for x in lst_combined:
    writer.writerow(x)


# -------------------------------------------------------------------------------------------------------------
# Create Database
# def setUpDatabase(db_name):
#     path = os.path.dirname(os.path.abspath(__file__))
#     conn = sqlite3.connect(path+'/'+db_name)
#     cur = conn.cursor()
#     return cur, conn


# Creates list of species ID's and numbers
# def create_species_table(cur, conn):

#     Countries = ["United States",
#     "Netherlands",
#     "Japan",
#     "Dessau",
#     "India",
#     "Cirebon",
#     "Timor",
#     "Java",
#     "Saltillo",
#     "France",
#     "Israel",
#     "Indonesia",
#     ]

    # cur.execute("DROP TABLE IF EXISTS Countries")
    # cur.execute("CREATE TABLE Countries (id INTEGER PRIMARY KEY, Country TEXT)")
    # for i in range(len(Countries)):
    #     cur.execute("INSERT INTO Countries (id,Country) VALUES (?,?)",(i,Countries[i]))
    # conn.commit()

# TASK 1
# CREATE TABLE FOR PATIENTS IN DATABASE
# def create_patients_table(cur, conn):
#     cur.execute('drop table if exists Patients')
#     cur.execute('create table Patients (pet_id INTEGER PRIMARY KEY, name TEXT, species_id NUMBER, age INTEGER, cuteness INTEGER, aggressiveness NUMBER)')
#     conn.commit()


# TASK 2
# CODE TO ADD JSON TO THE TABLE
# ASSUME TABLE ALREADY EXISTS
# def add_pets_from_json(filename, cur, conn):
    
#     # WE GAVE YOU THIS TO READ IN DATA
#     f = open(filename)
#     file_data = f.read()
#     f.close()
#     json_data = json.loads(file_data)

#     # THE REST IS UP TO YOU
#     for data in json_data:
#         cur.execute('SELECT id FROM Species WHERE title=?',(data['species'],))
#     conn.commit()


# TASK 3
# CODE TO OUTPUT NON-AGGRESSIVE PETS
# def non_aggressive_pets(aggressiveness, cur, conn):
#     aggressiveness=[]
#     file=open('pets.json', 'r')
#     f=file.read()
#     file.close()
#     for data in f:
#         ints=data['aggressiveness']
#         if int(ints)<=10:
#             aggressiveness.append(data)
#     print(aggressiveness)



# def main():
#     # SETUP DATABASE AND TABLE
#     cur, conn = setUpDatabase('ChicagoArt.db')
#     create_species_table(cur, conn)

    # create_patients_table(cur, conn)
    # add_fluffle(cur, conn)
    # add_pets_from_json('data_chicago.csv', cur, conn)
    # ls = (non_aggressive_pets(10, cur, conn))
    # print(ls)
    
    
# if __name__ == "__main__":
#     main()
