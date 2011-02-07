import sqlite3, time

db = 'loc.db'

class locDb():

    
    def __init__(self):
        try:
            self.conn = sqlite3.connect(db)
        except sqlite3.OperationalError: # Can't locate database file
            exit(1)
        self.cursor = self.conn.cursor()
    
    def execute(self, sql):
        self.cursor.execute(sql)
        self.conn.commit()
        results = self.cursor.fetchall()
        return results
    
    def close(self):
        self.conn.commit()
        self.conn.close()
	
	def createTable(self):
		sql = '''create table location (id integer primary key autoincrement, date text, loc text, ip text)'''
		self.execute(sql)
		
if __name__ == "__main__":
    db = locDb()

    db.execute(sql)
    db.close()
