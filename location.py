#!/usr/bin/python
import bottle
import locDb, time

bottle.debug(True)

@bottle.route('/found/:loc')
def found(loc):
	ip = bottle.request.environ.get('REMOTE_ADDR')
	
	sql = """insert into location values (null, "%s", "%s", "%s")""" % (time.time(), loc, ip)
	db = locDb.locDb()
	db.execute(sql)
	return "SUCCESS"

@bottle.route('/where')
def where():
	resultsPage = ""
	sql = """select * from location order by id desc"""
	
	db = locDb.locDb()
	results = db.execute(sql)
	
	for result in results:
		id, timestamp, loc, ip, agent = result[:]
		resultsPage += time.strftime("%a, %b %d %I:%M%p",time.localtime(float(timestamp))) + ": " + loc + " (" + ip + "/" + agent + ") <br>"
	return resultsPage

	
bottle.run(host='localhost', port=8080)