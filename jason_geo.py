import urllib.request, urllib.parse, urllib.error
import json

serviceUrl = 'http://maps.googleapis.com/maps/api/geocode/json?'

while True:
    address = input('Enter address: ')

    if len(address) < 1:
        break

    url = serviceUrl + urllib.parse.urlencode({'address': address})
    print('Retrieved', url)
    uh = urllib.request.urlopen(url)  # URL handle
    data = uh.read().decode()
    print('Retrieved', len(data), 'characters...')

    try:
        js = json.loads(data)
    except:
        js = None

    if not js or 'status' not in js or js['status'] != 'OK':
        print('==== FAILURE TO RETRIEVE ADDRESS ====')
        print(data)
        continue

    print(json.dumps(js, indent=4))

    latitude = js['results'][0]['geometry']['location']['lat']
    longitude = js['results'][0]['geometry']['location']['lng']
    print(f'Latitude: {latitude} \n Longitude: {longitude}')

    location = js['results'][0]['formatted_address']
    print(location)
