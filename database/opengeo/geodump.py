"""
This script retrieves data from the Locations table in the SQLite database opengeo.sqlite, parses the JSON data
stored in it, and writes the latitude, longitude, and location name to a JavaScript file where.js. The JavaScript
data is structured as an array of arrays. Finally, it prints the number of records written and instructs the user to
open where.html to view the data in a browser.
"""

import sqlite3
import json
import codecs

# Connect to SQLite database
conn = sqlite3.connect('opengeo.sqlite')
cur = conn.cursor()

# Select all rows from the Locations table
cur.execute('SELECT * FROM Locations')

# Open a file for writing JavaScript data
fhand = codecs.open('where.js', 'w', "utf-8")
fhand.write("myData = [\n")

count = 0
# Iterate over each row in the query result
for row in cur:
    # Extract geodata from the row
    data = str(row[1].decode())
    try:
        # Parse the JSON data
        js = json.loads(str(data))
    except:
        continue

    # Skip if no features are found
    if len(js['features']) == 0: continue

    try:
        # Extract latitude, longitude, and location name from JSON
        lat = js['features'][0]['geometry']['coordinates'][1]
        lng = js['features'][0]['geometry']['coordinates'][0]
        where = js['features'][0]['properties']['display_name']
        where = where.replace("'", "")  # Remove single quotes from location name
    except:
        print('Unexpected format')
        print(js)

    try:
        # Print and write latitude, longitude, and location name to the file
        print(where, lat, lng)

        count = count + 1
        if count > 1: fhand.write(",\n")  # Add comma separator after the first record
        output = "[" + str(lat) + "," + str(lng) + ", '" + where + "']"
        fhand.write(output)
    except:
        continue

# Close the JavaScript file and database cursor
fhand.write("\n];\n")
cur.close()
fhand.close()

# Print the number of records written and instruct to view the data in a browser
print(count, "records written to where.js")
print("Open where.html to view the data in a browser")
