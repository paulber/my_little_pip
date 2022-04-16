import sqlite3
import os

# Clean old database
if os.path.exists("functions.db"):
    os.remove("functions.db")

# Open Connection to freshly created database
connection_object = sqlite3.connect("functions.db")

# Open and read the file as a single character array
with open('functions_db.sql', 'r') as fd:
    sqlFile = fd.read()

# Split all command based on the symbol ';'
sqlCommands = sqlFile.split(';')

# Execute every command from the input file and raise exception
for command in sqlCommands:
    try:
        connection_object.execute(command)
    except sqlite3.OperationalError as e:
        raise

# Commit changes
connection_object.commit()

# Close connection
connection_object.close()
