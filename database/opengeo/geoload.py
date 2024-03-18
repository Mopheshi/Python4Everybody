"""
This Python script retrieves geolocation data for addresses from a file (where.data) using a geocoding API. It
stores the data in a SQLite database (opengeo.sqlite). The script limits the number of requests to 100 to avoid
overwhelming the server, and it pauses every 10 requests to comply with API usage limits. If an address is not found,
it prints a message indicating that the object was not found. After running the script, the user can visualize the
data on a map using geodump.py.
"""

import urllib.request, urllib.parse, urllib.error
import http
import sqlite3
import json
import time
import ssl
import sys

# Service URL for geocoding API
serviceurl = 'https://py4e-data.dr-chuck.net/opengeo?'

# Connect to SQLite database or create if it doesn't exist
conn = sqlite3.connect('opengeo.sqlite')
cur = conn.cursor()

# Create Locations table if it doesn't exist
cur.execute('''
CREATE TABLE IF NOT EXISTS Locations (address TEXT, geodata TEXT)''')

# Ignore SSL certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

# Open the file containing addresses
fh = open("where.data")
count = 0
nofound = 0

# Loop through each address in the file
for line in fh:
    # Stop after retrieving 100 locations
    if count > 100:
        print('Retrieved 100 locations, restart to retrieve more')
        break

    # Get the address from the file
    address = line.strip()
    print('')

    # Check if the address is already in the database
    cur.execute("SELECT geodata FROM Locations WHERE address= ?", (memoryview(address.encode()),))

    try:
        # Retrieve geodata if address is found in the database
        data = cur.fetchone()[0]
        print("Found in database", address)
        continue
    except:
        pass

    # Prepare parameters for the API request
    parms = dict()
    parms['q'] = address

    # Construct the URL for the API request
    url = serviceurl + urllib.parse.urlencode(parms)

    print('Retrieving', url)

    # Open the URL and retrieve data
    uh = urllib.request.urlopen(url, context=ctx)
    data = uh.read().decode()
    print('Retrieved', len(data), 'characters', data[:20].replace('\n', ' '))
    count = count + 1

    try:
        # Parse the JSON data
        js = json.loads(data)
    except:
        print(data)  # Print in case Unicode causes an error
        continue

    # Check if features key exists in the JSON data
    if not js or 'features' not in js:
        print('==== Download error ===')
        print(data)
        break

    # Check if any features were found
    if len(js['features']) == 0:
        print('==== Object not found ====')
        nofound = nofound + 1

    # Insert the address and geodata into the database
    cur.execute('''INSERT INTO Locations (address, geodata)
        VALUES ( ?, ? )''',
                (memoryview(address.encode()), memoryview(data.encode())))

    # Commit the transaction
    conn.commit()

    # Pause every 10 requests to avoid overwhelming the server
    if count % 10 == 0:
        print('Pausing for a bit...')
        time.sleep(5)

# Print the number of features for which the location could not be found
if nofound > 0:
    print('Number of features for which the location could not be found:', nofound)

# Inform the user how to visualize the data on a map
print("Run geodump.py to read the data from the database so you can visualize it on a map.")
