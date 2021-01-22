import csv  # library to create csv file
import os  # library to use system commands
import cx_Oracle  # library to connect Oracle Database
import pandas as pd  # library to create dataframe with the results

# Variables to connect oracle's database
host = 'db_address'
user = 'db_user'
pwd = 'db_password'
db = 'db_name'
connector = '{0}/{1}@{2}/{3}'.format(user, pwd, host, db)

# Build the connection
con = cx_Oracle.connect(connector)
cur = con.cursor()

# These two variables will be used at different times,
# one will be used to receive a temporary file (which will be deleted at the end of the process)
# and the other will be used to host the SQL queries in separate files in order to
# keep the code more readable and more easy maintenance.
path = '/home/user/path'  # Example directory

PATH_TO_FILE = '/home/user/path/journal_entry.sql'  # Example of path containing SQL file to run in the database

# The fullLine variable will be used to build the query inside the for in our script by reading the lines of the file
fullLine = ''

# named_params is used to pass some values to the SQL Query, for example: time period or id
named_params = {'variable': 'variable'}

# This is our constructor, responsible for creating an SQL query within our Python script
# when reading a file containing an sql statement.
for line in open(PATH_TO_FILE):
    tempLine = line.strip()

    if len(tempLine) == 0:
        continue

    if tempLine[0] == "#":
        continue

    fullLine += line

    try:
        cur.execute(fullLine, named_params)
    except Exception as e:
        pass

# So we take the result of the query and build the structure of our dataframe
for result in cur:
    try:
        with open(path + 'test.csv', 'a', encoding='utf-8', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(result)
            writer.close()
    except Exception as e:
        pass
# Don't forget to close the connections to the oracle database
cur.close()
con.close()

# Using Pandas to construction dataframe
columns = ['column_name', 'column_name', 'column_name']

df = pd.read_csv('test.csv', delimiter=",", names=[columns])

dataframe = df
writer_excel = pd.ExcelWriter('file.xlsx', engine='xlsxwriter')
dataframe.to_excel(writer_excel, sheet_name="Report", index=False)
writer_excel.save()

# So, in the end, we remove the test file create to generate our dataframe
file = 'test.csv'
directory = os.listdir(path)
if file in directory:
    os.remove('{}/{}'.format(path, file))
else:
    pass
