#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  sprint2.py
#  
#  Copyright 2020 Yan <yan@yan-Inspiron-5558>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#  

#pandas
import requests
import json
import csv

token = input("Informe seu token do github: ");

headers = {
    'Content-Type': 'application/json',
    'Authorization': 'bearer '+token,
}

data_file = open('output.csv', 'w') 

csv_writer = csv.writer(data_file) 
        
endCursor = "null"

count = 0

isHeader = 1

while(count < 20):
	data = '{"query": "{ search(query:\\"stars:>100\\", type:REPOSITORY, first:50, after:'+endCursor+'){ pageInfo {hasNextPage endCursor} nodes { ... on Repository {nameWithOwner url primaryLanguage{ name } all_issues: issues{ totalCount } closed_issues: issues(states:CLOSED){ totalCount } } } } rateLimit {remaining resetAt}} "}'
	response = requests.post('https://api.github.com/graphql', headers=headers, data=data)

	if response.status_code != 200:
		print ("ERRO - cheque o codigo")
	
	json_data = json.loads(response.text)

	for repos in json_data['data']['search']['nodes']:
		
		if isHeader:
			header = repos.keys()
			csv_writer.writerow(header)
			isHeader = 0
			
		csv_writer.writerow(repos.values()) 
	
	endCursor = '\\"'+json_data['data']['search']['pageInfo']['endCursor']+'\\"'	
	
	count = count + 1
	
data_file.close() 
	
	
	
