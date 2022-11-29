import json 
import os
import requests
import pprint
import csv
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

material_type={}
for x in data:
    material=x['material_titles']
    for type in material:
        if type not in material_type:
            material_type[type]=1
        else:
            material_type[type]+=1
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
    dates_list.append(years)
# print(len(dates_list))

material_type_list=[]
for x in data:
    material=x['material_titles']
    if material==[]:
        material_type_list.append(['digital'])
    else:
        material_type_list.append(material)
# print(material_type_list)

origin_place_list=[]
for x in data:
    place=x['place_of_origin']
    if place==None:
        origin_place_list.append("Unknown")
    else:
        origin_place_list.append(place)
# print(len(origin_place_list))

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
    elif 'donors' in credit.lower():
        credits_list.append('Donation')
    elif 'trust' in credit.lower():
        credits_list.append("Donation")
    elif 'endowment' in credit.lower():
        credits_list.append("Donation")
    elif 'acquisitions' in credit.lower():
        credits_list.append("Purchased")
    elif 'bequest' in credit.lower():
        credits_list.append("Donation")
# print(len(credits_list))

# Combining the data based on index
lst_combined=[]
for idx in range(len(origin_place_list)):
        lst_combined.append((origin_place_list[idx], dates_list[idx], credits_list[idx], material_type_list[idx]))
# print(lst_combined)


# Making data table
filename=open('/Users/samlawrence/Desktop/Final Project 206/data_chicago.csv', 'w')
writer=csv.writer(filename)    
data=load['data']
header=["Place of Origin","Date","Credit","Materials"]
writer=csv.writer(filename, delimiter=",")
writer.writerow(header)
for x in lst_combined:
    writer.writerow(x)
