import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('../files/tracksdb.sqlite')
cur = conn.cursor()

# Drop existing tables if they exist
cur.executescript('''
DROP TABLE IF EXISTS Artist;
DROP TABLE IF EXISTS Genre;
DROP TABLE IF EXISTS Album;
DROP TABLE IF EXISTS Track;

CREATE TABLE Artist (
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    name TEXT UNIQUE
);

CREATE TABLE Genre (
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    name TEXT UNIQUE
);

CREATE TABLE Album (
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    artist_id INTEGER,
    title TEXT UNIQUE
);

CREATE TABLE Track (
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    title TEXT UNIQUE,
    album_id INTEGER,
    genre_id INTEGER,
    len INTEGER,
    rating INTEGER,
    count INTEGER
);
''')

# Open the CSV file containing track information
handle = open('../files/tracks.csv')

# Iterate over each line in the CSV file
for line in handle:
    line = line.strip()  # Remove leading/trailing whitespaces
    pieces = line.split(',')  # Split the line by comma

    # Skip lines with incomplete data
    if len(pieces) < 7:
        continue

    # Extract data from each column in the CSV
    name = pieces[0]
    artist = pieces[1]
    album = pieces[2]
    count = pieces[3]
    rating = pieces[4]
    length = pieces[5]
    genre = pieces[6]

    # Print track information
    print(name, artist, album, count, rating, length, genre)

    # Insert or ignore the artist into the Artist table
    cur.execute('INSERT OR IGNORE INTO Artist (name) VALUES (?)', (artist,))
    # Retrieve the artist's ID
    cur.execute('SELECT id FROM Artist WHERE name = ?', (artist,))
    artist_id = cur.fetchone()[0]

    # Insert or ignore the genre into the Genre table
    cur.execute('INSERT OR IGNORE INTO Genre (name) VALUES (?)', (genre,))
    # Retrieve the genre's ID
    cur.execute('SELECT id FROM Genre WHERE name = ?', (genre,))
    genre_id = cur.fetchone()[0]

    # Insert or ignore the album into the Album table
    cur.execute('INSERT OR IGNORE INTO Album (title, artist_id) VALUES (?, ?)', (album, artist_id,))
    # Retrieve the album's ID
    cur.execute('SELECT id FROM Album WHERE title = ?', (album,))
    album_id = cur.fetchone()[0]

    # Insert or replace the track into the Track table
    cur.execute(
        'INSERT OR REPLACE INTO Track (title, album_id, genre_id, len, rating, count) VALUES (?, ?, ?, ?, ?, ?)',
        (name, album_id, genre_id, length, rating, count))

    # Commit the changes to the database
    conn.commit()

# Close the database connection
conn.close()
