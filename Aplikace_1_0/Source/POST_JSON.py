# -*- coding: utf-8 -*-
'''
Created on 1.7.2024

@author: Meloun
'''


import requests
import json
import datetime

data1 = [
  {"id": 1025,
   "number": "E68",
   "time1": "5.04",
   "time2": "4.99"
  },
  {"id": 1031,
   "number": "C99",
   "time1": "5.14",
   "time2": "5.21"
  }
]


data2 = {"times":
[
{"id":2031,"season_id":4,"number":"E99","time1":"00:00:05.05"},
{"id":2032,"season_id":4,"number":"E68","time1":"00:00:05.05"}
]
}

data3 = {'times': [
                   {'number': "17", "season_id":4, 'id': 32760, 'time': '00:00:09,69'}, 
                   {'number': "19", "season_id":4, 'id': 16566, 'time': '00:00:10,42'}
                   ]}


data4 = {'times': [
           {u'season_id': 4, u'time1': u'00:02,69', u'id': 2153, u'number': u'17'},
           {u'season_id': 4, u'time1': u'00:03,55', u'id': 2154, u'number': u'19'},
           {u'season_id': 4, u'time1': u'00:09,69', u'id': 2157, u'number': u'17'},
           {u'season_id': 4, u'time1': u'00:10,42', u'id': 2158, u'number': u'19'}
        ]}


data5 = {"times": [
                   {
                    "season_id": "4",
                    u'time1': u'00:5,050',
                    u'lap': u'1',
                    "id": "20211",
                    u'number': "C5"
                    }
                   ]
         }

data6 = {
    "times":[
        {
            "id": "20211",
            "season_id": "4",
            "number": "E53",
            "time1": "00:5,050",
            "lap": "1"
        },
        {
            "id": "20231",
            "season_id": "4",
            "number": "E53",
            "time1": "00:5,150",
            "lap": "2"
        }
    ]
}

         
'''
print "http://httpbin.org/post"
response = requests.post("http://httpbin.org/post", json=data2)

# Check if the request was successful
if response.status_code == 200:
    print("Request was successful.")
else:
    print("Failed with status code:", response.status_code)
    print("Response content:", response.text)
#print(response.ok)


print "\n\nhttps://reqbin.com/echo/post/json"
response = requests.post("https://ptsv3.com/t/123432324/", json=data2)
if response.status_code == 200:
    print("Request was successful.")
else:
    print("Failed with status code:", response.status_code)
    print("Response content:", response.text)
#print(response.ok)
'''

#url = "https://portal.fsczech.cz/api/acceleration"
#url = "https://portal.fsczech.cz/api/skidpad"
#url = "https://portal.fsczech.cz/api/autocross"
#url = "https://portal.fsczech.cz/api/endurance"
url = "https://portal.fsczech.cz/api/trackdrive"

print "\n\n", url
auth_token='1|71j4X5ae7j9kfLkfhJaxMc9neKsgDpw0jVIuYN7Qa689166f'
headers = {'Authorization': 'Bearer '+auth_token}
print headers
print(datetime.datetime.now())
response = requests.post(url, json=data5, headers=headers)
print(datetime.datetime.now())
if response.status_code == 200:
    print("Request successful.")
else:
    print("Failed with status code:", response.status_code)
    print("Response content:", response.text)

print(response.ok)


