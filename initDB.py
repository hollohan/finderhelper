import pymysql.cursors
from os import listdir

def initDB():
	ls = listdir('./app/static')
	ls = [x[:-4] for x in ls if '.jpg' in x]
	
	q_string = 'CREATE TABLE %s (id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,lat DOUBLE NOT NULL,lon DOUBLE NOT NULL,printer TEXT)'

	conn = pymysql.connect(
        host = 'localhost',
        user = 'root',
        password = 'toor',
        db = 'finderhelper')        
	cursor = conn.cursor()
	
	for thing in ls:
		cursor.execute(q_string % (thing))
		results = cursor.fetchall()
		conn.commit()
	
	
	conn.close()

	
if __name__=='__main__':
	initDB()
	
