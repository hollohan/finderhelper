import  csv
import pymysql.cursors

conn = pymysql.connect(
    host = 'localhost',
    user = 'root',
    password = 'toor',
    db = 'finderhelper')        
cursor = conn.cursor()


with open('theMaster.csv', 'r') as file:
	csvfile = csv.reader(file)
	record = "INSERT INTO printers (addy, path, loc, found) VALUES ('%s', '%s', '%s', False)"
	for thing in csvfile:
		addy = thing[1]
		path = thing[6]
		loc = thing[2]
		cursor.execute(record % (addy, path, loc))
		conn.commit()
		
conn.close()
