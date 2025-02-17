import sqlite3

# Connect to SQLite (Creates a file-based database)
mycon = sqlite3.connect("warehouse.db")
mycursor = mycon.cursor()

# Create Table
mycursor.execute('''
CREATE TABLE IF NOT EXISTS studentrecords (
    ccid TEXT PRIMARY KEY,
    lastname TEXT NOT NULL,
    firstname TEXT NOT NULL,
    residence TEXT NOT NULL,
    roomnumber INTEGER NOT NULL
);
''')

print("Database and table created successfully.")

# Read input data from file
with open('data/tableinputs.txt', 'r') as f:
    data = f.readlines()

# Insert data into the table
for i in data:
    mycursor.execute(i.strip())


# Commit changes and close the connection
mycon.commit()
mycon.close()

print("Data inserted to successfully.")

