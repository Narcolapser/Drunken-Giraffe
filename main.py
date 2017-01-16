from kivy.properties import ListProperty, StringProperty, NumericProperty, ObjectProperty
from kivy.adapters.listadapter import ListAdapter
from kivy.uix.listview import ListView, ListItemButton
from kivy.uix.selectableview import SelectableView
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.lang import Builder
from kivy.app import App
from kivy.clock import Clock

import time

class DrunkenGiraffe(BoxLayout):
	drink_list = ListProperty([])
	drinks = []
	pending_drink_quantity = NumericProperty(12)
	pending_drink_ABV = NumericProperty(8)
	gender = StringProperty('Male')
	mass_units = StringProperty('lb')
	mass = NumericProperty(200)
	mass_ins = ObjectProperty(None)
	safety_switch = ObjectProperty(None)
	session_start_time = time.localtime()
	session_start_time_str = StringProperty(time.strftime("%H:%M:%S",time.localtime()))
	BAC = NumericProperty(0)
	

	def addItem(self):
		if self.mass_units == 'lb':
			mass = self.mass / 2.2 * 1000
		else:
			mass = self.mass * 1000
		#print('Mass: {0}, ABV: {1}, oz: {2}'.format(mass,self.pending_drink_ABV,self.pending_drink_quantity))
		drink = Drink(mass,
							self.gender,
							self.pending_drink_quantity,
							self.pending_drink_ABV,
							time.localtime())
		self.drinks.append(drink)

		self.drink_list.append("{0} oz. at {1}% added {2} to your BAC.".format(
			self.pending_drink_quantity,
			self.pending_drink_ABV,
			drink.getCurrent()))

	def ABVUp(self):
		self.pending_drink_ABV+=1

	def ABVDown(self):
		self.pending_drink_ABV-=1

	def QuantityUp(self):
		self.pending_drink_quantity+=0.5

	def QuantityDown(self):
		self.pending_drink_quantity-=0.5

	def gender_swap(self):
		if self.gender == 'Male':
			self.gender = 'Female'
		else:
			self.gender = 'Male'

	def mass_swap(self):
		if self.mass_units == 'lb':
			self.mass_units = 'kg'
		else:
			self.mass_units = 'lb'

	def mass_update(self):
		try:
			self.mass = int(self.mass_ins.text)
		except:
			pass

	def start_new_session(self):
		if self.safety_switch.active:
			self.safety_switch.active = False
			self.session_start_time = time.localtime()
			self.session_start_time_str = time.strftime("%H:%M:%S",self.session_start_time)
			while len(self.drinks):
				self.drinks.pop()
			while len(self.drink_list):
				self.drink_list.pop()

	def update(self,*args):
		total = 0
		for drink in self.drinks:
			total += drink.getCurrent()

		self.BAC = total

class Drink():
	def __init__(self,mass,gender,quantity,ABV,at_time):
		self.mass = mass
		self.gender = gender
		self.quantity = quantity
		self.ABV = ABV
		self.grams_alcohol = (quantity * (ABV/100.0)) * 23.35
		self.at_time = at_time

	def getCurrent(self):
		A = self.grams_alcohol
		W = self.mass
		if self.gender == 'Female':
			R = 0.55
		else:
			R = 0.68
		H = (time.mktime(time.localtime()) - time.mktime(self.at_time)) / 3600
		BAC = (((A)/(W*R))*100)-(H*.015)
		val = str(BAC)
		val = float(val[:7])
		return val
	

class DrunkenGiraffeApp(App):
	def build(self):
		self.DrunkenGiraffe = DrunkenGiraffe()
		Clock.schedule_interval(self.DrunkenGiraffe.update,1)
		return self.DrunkenGiraffe

	def on_pause(self):
		return True

	def on_resume(self):
		pass

DrunkenGiraffeApp().run()
