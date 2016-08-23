# -*- coding: utf-8 -*-
"""
Get document types from pravo.by
"""
import requests
#from pprint import pprint
 
json = '{"GuidControl":2361,"Param1":"","Param2":null,"Param3":null}'
headers = {'content-type': 'application/json; charset=utf-8'}

r = requests.post('http://www.pravo.by/Ajax.asmx/GetExt', headers=headers, data=json)
#print r.status_code 
#pprint(r.headers)
#print r.content
types = r.content

output = open('gettypes.bin', 'wb')
# this writes types as a string like:
# "\u003cdiv onclick=\"RA_Akt_Add(57,this)\"\u003eАкт\u003c...
# which should be parsed/unquoted
output.write(types)
output.write('\n\n')

# this gets back linefeed characters:
types2 = types.decode('string_escape')
output.write(types2)
output.write('\n\n')

# this removes unicode escaping
types3 = types2.replace('\\u003c', '<').replace('\\u003e', '>')
output.write(types3)
output.write('\n\n')

# parse "<div onclick="RA_Akt_Add(43,this)">Правила</div>" and write CSV
# id, doctype
import re
pairs = re.findall("Add\((\d+),this\)\">(.*?)\<", types3)
for typeid, typename in pairs:
  output.write(typeid + ', ' + typename + '\n')
output.write('\n\n')
