#!/usr/bin/python

import bottle
bottle.debug(True)

from bottle import route, run, response, request
import locDb, time




@route('/found/:loc')
def found(loc):
    if(isAuthorized()):
        return updateLoc(loc)
    else:
        return "NOT AUTHORIZED"

@route('/where')
def where():
	if (isAuthorized()):
		return getLastKnownLoc()
	else:
		return "NOT AUTHORIZED"
    
    
    

def getLastKnownLoc():
    resultsPage = ""
    sql = """select * from location order by id desc limit 1"""
    db = locDb.locDb()
    results = db.execute(sql)
    
    for result in results:
        id, timestamp, loc, ip, agent = result[:]
        resultsPage += time.strftime("%a, %b %d %I:%M%p",time.localtime(float(timestamp))) + ": " + loc + " (" + ip + "/" + agent + ") <br>"
    return resultsPage

def updateLoc(loc):
    ip = bottle.request.environ.get('REMOTE_ADDR')
    agent = request.GET.get('agent')
    sql = """insert into location values (null, "%s", "%s", "%s", "%s")""" % (time.time(), loc, ip, agent)
    db = locDb.locDb()
    db.execute(sql)
    return "SUCCESS"

def isAuthorized():
    agent = request.GET.get('agent')
    passw = request.GET.get('pass')
    
    db = locDb.locDb()
    sql = '''select agent from users where agent="%s" and password="%s"'''%(agent, passw)
    result = db.execute(sql)
    if len(result) > 0:
        return True
    else:
        return False

@route('/createDb')
def create():
    db = locDb.locDb()
    db.createTables()
    

bottle.run(host='localhost', port=8080)