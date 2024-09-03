import os
import sqlite3

# EDITABLE
path = '/Users/joaquinsepulvedariquelme/Downloads/'
extension = 'mp4'
limit = 5
threshold = 1e6 # In bytes

# Get the list of files in the specified path
files = os.listdir(path)

# SQLITE WILL BE USED TO MAKE THE QUERIES
connection = sqlite3.connect(':memory:')
cursor = connection.cursor()

# CREATE TABLE
create_table_query = 'CREATE TABLE files (id INTEGER PRIMARY KEY, file_name TEXT, size INTEGER)'
cursor.execute(create_table_query)
connection.commit()

insert_query = 'INSERT INTO files(file_name, size) VALUES(?, ?)'

# Insert files into the database
for file in files:
    size = os.path.getsize(os.path.join(path, file))
    cursor.execute(insert_query, (file, size))

connection.commit()

# SELECT query
select_query = f'SELECT * FROM files WHERE file_name LIKE "%.{extension}" AND size > {threshold} ORDER BY size DESC LIMIT {limit}'
print(select_query)

# Execute and display the results
for i in cursor.execute(select_query):
    print(f'File: {i[1]}, Size: {int(i[2]) / 1e6} MB')

# Close the connection
cursor.close()
connection.close()