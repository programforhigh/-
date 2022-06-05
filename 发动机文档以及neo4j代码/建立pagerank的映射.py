import json
f = open('records.json',encoding='utf-8-sig')
s = json.load(f)
hashtable = {}
for item in s:
    hashtable[item['name']] = item['score']
print(hashtable)