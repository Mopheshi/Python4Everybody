import urllib.request, urllib.parse, urllib.error
import json
import ssl

api_key = False

if api_key is False:
    api_key = 42
    serviceurl = 'http://py4e-data.dr-chuck.net/json?'
else:
    serviceurl = 'https://maps.googleapis.com/maps/api/geocode/json?'

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

while True:
    address = input('Enter location: ')
    if len(address) < 1:
        break

    parms = dict()
    parms['address'] = address

    if api_key is not False:
        parms['key'] = api_key

    url = serviceurl + urllib.parse.urlencode(parms)
    print('Retrieving', url)

    uh = urllib.request.urlopen(url, context=ctx)
    data = uh.read().decode()

    try:
        jason = json.loads(data)
    except:
        jason = None

    if not jason or 'status' not in jason or jason['status'] != 'OK':
        print('===== FAILURE TO RETRIEVE ADDRESS =====')
        print(data)
        continue

    # print(json.dumps(jason, indent=4))

    formatted_address = jason['results'][0]['formatted_address']
    place_id = jason['results'][0]['place_id']
    print(f'Formatted address: {formatted_address}\nPlace ID: {place_id}')
