import sqlite3
import time

class Drink():
	def __init__(self,mass,gender,quantity,ABV,at_time,name):
		self.name = name
		self.mass = mass #in grams
		self.gender = gender
		self.quantity = quantity
		self.ABV = ABV
		self.at_time = at_time
		self.removed = False

	def getCurrent(self):
		#A = self.grams_alcohol
		A = (self.quantity * (self.ABV/100.0)) * 23.35
		W = self.mass
		if self.gender == 'Female':
			R = 0.55
		else:
			R = 0.68
		H = (time.mktime(time.localtime()) - time.mktime(self.at_time)) / 3600
		BAC = (((A)/(W*R))*100)-(H*.015)
		val = str(BAC)
		try:
			val = float(val[:7])
		except:
			val = 0
		if val < 0:
			return 0
		val = round(val*1000)/1000.0
		return val
	
	def getInitial(self):
		#A = self.grams_alcohol
		A = (self.quantity * (self.ABV/100.0)) * 23.35
		W = self.mass
		if self.gender == 'Female':
			R = 0.55
		else:
			R = 0.68
		H = (time.mktime(time.localtime()) - time.mktime(self.at_time)) / 3600
		BAC = (((A)/(W*R))*100)
		BAC = round(BAC*1000)/1000.0
		return BAC
	
	
	def __str__(self):
		return "{4}: {0} oz. of \"{3}\" at {1}% ABV added {2} to your BAC.".format(
			self.quantity,
			self.ABV,
			self.getInitial(),
			self.name,
			time.strftime("%H:%M:%S",self.at_time))

create_drink_table = """
CREATE TABLE IF NOT EXISTS drinks(
	drink_id INT PRIMARY KEY,
	session_id INT,
	drinker_gender INT,
	drinker_mass INT,
	drink_quantity REAL,
	drink_ABV REAL,
	drink_name TEXT,
	drink_removed INT);"""

insert_drink = """INSERT INTO drinks VALUES(?,?,?,?,?,?,?,?)"""

get_drink = """SELECT * FROM drinks WHERE drink_id=?"""

update_drink = """UPDATE drinks SET
	drinker_gender=?,
	drinker_mass=?,
	drink_quantity=?,
	drink_ABV=?,
	drink_name=?,
	drink_removed=?
	WHERE drink_id=?"""

get_sessions = "SELECT DISTINCT session_id FROM drinks"

get_session = "SELECT * FROM drinks WHERE session_id=?"

last_session = "SELECT session_id FROM drinks ORDER BY session_id DESC LIMIT 1"

dbname = '/drinks.db'

def Build_DB(location):
	con = sqlite3.connect(location + dbname)
	c = con.cursor()
	c.execute(create_drink_table)
	con.commit()
	c.close()
	con.close()

def save(session_start,drink_list,location):
	Build_DB(location)
	print("Location:", location)
	con = sqlite3.connect(location+dbname)
	c = con.cursor()
	drinks = {}
	print("saving drinks")
	for drink in drink_list:
		removed = 0
		if drink.removed:
			removed = 1
			
		gender = 1
		if drink.gender == 'Male':
			gender = 0
		
		mass = drink.mass
		oz = drink.quantity
		abv = drink.ABV
		name = drink.name
		drink_id = time.strftime("%Y%m%d%H%M%S",drink.at_time)
		print("Saving drink: ", drink_id)

		c.execute(get_drink,(drink_id,))
		try:
			if len(c.fetchall()) > 0:
				c.execute(update_drink,
					(gender,
					mass,
					oz,
					abv,
					name,
					removed,
					drink_id))
			else:
				c.execute(insert_drink,
					(drink_id,
					time.strftime("%Y%m%d%H%M%S",session_start),
					gender,
					mass,
					oz,
					abv,
					name,
					removed))
			print("saved drink: ", str(drink))
		except sqlite3.IntegrityError as ie:
			print("id collision. probably drink button spam.",ie,drink_id)
		con.commit()
	c.close()

def load(location,session_id=None):
	pass

def load_last(location):
	con = sqlite3.connect(location + dbname)
	c = con.cursor()
	try:
		c.execute(last_session)
	except sqlite3.OperationalError as oe:
		print("No table, must be first run.")
		return (None,[])
	ret = []
	sid = None
	try:
		sid = c.fetchone()[0]
		print("sid: ", sid)
		c.execute(get_session,(sid,))
		for row in c.fetchall():
			drink = Drink(row[3],row[2],row[4],row[5],time.strptime(str(row[0]),"%Y%m%d%H%M%S"),row[6])
			if row[7]:
				drink.removed = True
			if not drink.removed:
				ret.append(drink)
			print(str(drink),drink.removed)
	except Exception as e:
		print("Hit an error: ",e)
	c.close()
	con.close()
	return (sid,ret)

def get_Sessions(location):
	pass
