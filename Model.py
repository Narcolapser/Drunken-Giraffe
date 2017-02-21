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
		return BAC
	
	
	def __str__(self):
		return "{0} oz. of \"{3}\" at {1}% ABV added {2} to your BAC.".format(
			self.quantity,
			self.ABV,
			self.getInitial(),
			self.name)

create_drink_table = """
CREATE TABLE IF NOT EXISTS drinks(
	drink_id INT PRIMARY KEY,
	session_id INT,
	drinker_gender INT,
	drinker_mass INT,
	drink_quantity REAL,
	drink_ABV REAL,
	drink_name TEXT);"""

insert_drink = """INSERT INTO drinks VALUES(?,?,?,?,?,?,?)"""

get_drink = """SELECT * FROM drinks WHERE drink_id=?"""

update_drink = """UPDATE drinks SET
	drinker_gender=?,
	drinker_mass=?,
	drink_quantity=?,
	drink_ABV=?,
	drink_name=?
	WHERE drink_id=?"""

get_sessions = "SELECT DISTINCT session_id FROM drinks"

get_session = "SELECT * FROM drinks WHERE session_id=?"

def Build_DB(location):
	con = sqlite3.connect(location)
	c = con.cursor()
	c.execute(create_drink_table)
	con.commit()
	c.close()
	con.close()

def save(session_start,drink_list,location):
	con = sqlite3.connect(location)
	c = con.cursor()
	drinks = {}
	for drink in drink_list:
		#drinks[time.strftime("%Y%m%d%H%M%S",drink.at_time)] = drink
		if drink.removed:
			continue
		if drink.gender == 'Male':
			gender = 0
		else:
			gender = 1
		
		mass = drink.mass
		oz = drink.quantity
		abv = drink.abv
		name = drink.name
		drink_id = time.strftime("%Y%m%d%H%M%S",drink.at_time)

		c.execute(get_drink,drink_id)
		if c.rowcount > 0:
			c.execute(update_drink,
				gender,
				mass,
				oz,
				abv,
				name,
				drink_id)
		else:
			c.execute(insert_drink,
				drink_id,
				time.strftime("%Y%m%d%H%M%S",session_start),
				gender,
				mass,
				oz,
				abv,
				name)
		con.commit()

def load(location,session_id=None):
	pass
	
def get_Sessions(location):
	pass
