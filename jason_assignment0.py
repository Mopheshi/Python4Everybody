import json
import ssl
import urllib.request

url = input('Enter url: ')

print('Retrieving', url)

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

connection = urllib.request.urlopen(url, context=ctx)
data = connection.read().decode()
jason = json.loads(data)

total = 0

for number in jason['comments']:
    total += number['count']

print(total)
