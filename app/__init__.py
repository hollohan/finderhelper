from flask import Flask, render_template
import pymysql.cursors
import json

app = Flask(__name__)
	
@app.route('/')
def mapss():
	return render_template('map.html')
	
@app.route('/addMarker/<lat>/<lon>/<tablename>')
@app.route('/addMarker/<lat>/<lon>/<tablename>/<printer>')
def add_marker(lat, lon, tablename, printer=0):

	lat = float(lat)
	lon = float(lon)
	
	q_string = 'INSERT INTO %s (lat, lon) values (%s, %s)' % (tablename, lat, lon)
	if printer != 0: q_string = 'INSERT INTO %s (lat, lon,printer) values (%s, %s, %s)' % (tablename, lat, lon, printer)
	conn = pymysql.connect(
        host = 'localhost',
        user = 'root',
        password = 'toor',
        db = 'finderhelper')        
	cursor = conn.cursor()
	cursor.execute(q_string)
	results = cursor.fetchall()
	conn.commit()
	conn.close()
	return json.dumps({'status':'OK'})

@app.route('/getAllMarkers/<tablename>')
def get_all_markers(tablename):
	q_string = 'SELECT * from ' + tablename
	conn = pymysql.connect(
        host = 'localhost',
        user = 'root',
        password = 'toor',
        db = 'finderhelper')        
	cursor = conn.cursor()
	cursor.execute(q_string)
	results = cursor.fetchall()
	conn.commit()
	conn.close()
	
	r = {}
	for thing in results:
		marker_id = thing[0]
		latitude = thing[1]
		longitude = thing[2]
		printer = thing[3]
		r[marker_id] = [longitude, latitude, printer]
		
	return json.dumps(r)

@app.route('/lookupIP/<string:ip>')
def lookupIP(ip):
	q_string = 'SELECT * from printers where addy like "%' + ip + '%"'
	
	conn = pymysql.connect(
        host = 'localhost',
        user = 'root',
        password = 'toor',
        db = 'finderhelper')        
	cursor = conn.cursor()
	cursor.execute(q_string)
	results = cursor.fetchall()
	conn.commit()
	conn.close()
	
	r = {}
	for thing in results:
		marker_id = thing[0]
		addy = thing[1]
		path = thing[2]
		found = thing[3]
		loc = thing[4]
		r[marker_id] = {'addy':addy, 'path':path, 'found':found, 'loc':loc}
		
	if len(r) == 0: # no results return button
		r['noneFound'] = {'addy':'<button onclick="showNewIP()">add new IP</button>', 'path':'', 'found':'', 'loc':''}	
		
	return json.dumps(r)
	
@app.route('/edit/<int:i>/<string:field>/<string:new_value>')
def edit(i, field, new_value):
	q_string = 'update printers set %s="%s" where id=%s'
	if field=='found': q_string = 'update printers set %s=%s where id=%s'
	q_string = q_string % (field, new_value, i)
	print q_string
	conn = pymysql.connect(
        host = 'localhost',
        user = 'root',
        password = 'toor',
        db = 'finderhelper')        
	cursor = conn.cursor()
	cursor.execute(q_string)
	results = cursor.fetchall()
	conn.commit()
	conn.close()
	
	return json.dumps({'status': 'OK'});
	
@app.route('/getMaps')
def get_maps():
	from os import listdir
	
	a = listdir('./app/static')
	a = [x for x in a if '.jpg' in x]
	a = sorted(a)
	
	return json.dumps(a)
	
@app.route('/addIP/<addy>')
def addIP(addy):
	q_string = 'insert into printers (addy) values ("%s")' % (addy)
	print q_string
	conn = pymysql.connect(
        host = 'localhost',
        user = 'root',
        password = 'toor',
        db = 'finderhelper')        
	cursor = conn.cursor()
	cursor.execute(q_string)
	
	results = cursor.fetchall()
	
	conn.commit()
	conn.close()
	
	return json.dumps({'status': 'OK'});
	
	
	
	

