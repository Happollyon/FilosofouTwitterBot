import json

with open('test.json','r+') as file:
    data = json.load(file)
    print(data['last_mention'])
    data['last_mention'] = '88'
    file.seek(0)
    file.write(json.dumps(data))
    file.truncate()
