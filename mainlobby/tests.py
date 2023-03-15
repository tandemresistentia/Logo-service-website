import json

scones = {
    'value1' :0,
    'value2' :0,
}
scones['value1'] = 'Fuck you'
scones['value2'] = 'No!'
# .dumps() as a string
json_string = json.dumps(scones)

with open('json_data.json', 'w') as outfile:
    outfile.write(json_string)

