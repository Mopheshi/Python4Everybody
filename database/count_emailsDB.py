import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('../files/emaildb.sqlite')
cur = conn.cursor()

# Drop the table if it already exists
cur.execute('DROP TABLE IF EXISTS Counts')

# Create a new table called Counts
cur.execute('CREATE TABLE Counts (org TEXT, count INTEGER)')

# Prompt the user to input the file name
fname = input('Enter file name: ')
if len(fname) < 1: fname = '../files/mbox.txt'

# Open the file
fh = open(fname, 'r')

# Iterate through each line in the file
for line in fh:
    # Check if the line starts with 'From: '
    if not line.startswith('From: '): continue
    # Split the line by '@' to extract the organization domain
    pieces = line.split('@')
    org = pieces[1].strip()  # Extract the organization domain
    # Execute a SELECT statement to retrieve the count for the current organization
    cur.execute('SELECT count FROM Counts WHERE org = ? ', (org,))
    row = cur.fetchone()
    # If the organization is not found, insert a new record with count 1
    if row is None:
        cur.execute('INSERT INTO Counts (org, count) VALUES (?, 1)', (org,))
    # If the organization is found, increment the count by 1
    else:
        cur.execute('UPDATE Counts SET count = count + 1 WHERE org = ?', (org,))

# Commit the changes to the database
conn.commit()

# Select the top 10 organizations with the highest counts and print them
sqlstr = 'SELECT org, count FROM Counts ORDER BY count DESC LIMIT 10'
for row in cur.execute(sqlstr):
    print(str(row[0]), row[1])

# Close the cursor and connection
cur.close()
