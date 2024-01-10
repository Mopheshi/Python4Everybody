import urllib.request, urllib.parse, urllib.error
from twurl import augment
import ssl
import json

TWITTER_URL = 'https://api.twitter.com/1.1/friends/list.json'

# Ignore SSL certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

while True:
    print('')
    acct = input('Enter X account: ')

    if len(acct) < 1:
        break

    url = augment(TWITTER_URL, {'screen_name': acct, 'count': '5'})
    print('Retrieving', url)

    connection = urllib.request.urlopen(url, context=ctx)
    data = connection.read().decode()
    js = json.loads(data)
    print(json.dumps(js, indent=4))

    headers = dict(connection.getheaders())
    print('Remaining', headers['x-rate-limit-remaining'])

    for user in js['users']:
        print(user['screen_name'])

        if 'status' not in user:
            print('    ** No status found...')
            continue

        status = user['status']['text']
        print(' ', status[:50])
