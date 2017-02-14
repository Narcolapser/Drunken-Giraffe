from kivy.properties import ListProperty, StringProperty, NumericProperty, ObjectProperty
from kivy.adapters.listadapter import ListAdapter
from kivy.animation import Animation

from kivy.uix.listview import ListView, ListItemButton
from kivy.uix.selectableview import SelectableView
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.uix.carousel import Carousel

from kivy.lang import Builder
from kivy.app import App
from kivy.clock import Clock

from Carousel_Selector import Carousel_Selector

import time

class DrunkenGiraffe(FloatLayout):
	drinks = []
	drinks_up = True
	
	pending_drink_quantity = NumericProperty(12)
	pending_drink_ABV = NumericProperty(8)
	gender = StringProperty('Male')
	mass_units = StringProperty('lb')
	mass = NumericProperty(200)
	dname = StringProperty("Brewtacular!")
	
	drink_list = ObjectProperty(None)
	mass_ins = ObjectProperty(None)
	safety_switch = ObjectProperty(None)
	abv_selector = ObjectProperty(None)
	oz_selector = ObjectProperty(None)
	drinks_pane = ObjectProperty(None)
	
	session_start_time = time.localtime()
	session_start_time_str = StringProperty(time.strftime("%H:%M:%S",time.localtime()))
	BAC = NumericProperty(0)
	

	def addItem(self):
		if self.mass_units == 'lb':
			mass = self.mass / 2.2 * 1000
		else:
			mass = self.mass * 1000

		self.abv_selector.major_update()
		self.oz_selector.major_update()
		self.pending_drink_ABV = self.abv_selector.val
		self.pending_drink_quantity = self.oz_selector.val
		name = str(self.dname)

		drink = Drink(mass,
				self.gender,
				self.pending_drink_quantity,
				self.pending_drink_ABV,
				time.localtime(),
				name)
		self.drinks.append(drink)
		self.drink_list.append(drink)

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

	def name_update(self):
		try:
			self.dname = self.drink_name.text
		except:
			pass

	def start_new_session(self):
		self.session_start_time = time.localtime()
		self.session_start_time_str = time.strftime("%H:%M:%S",self.session_start_time)
		while len(self.drinks):
			self.drinks.pop()
		self.drink_list.clear()

	def update(self,*args):
		total = 0
		for drink in self.drinks:
			if not drink.removed:
				total += drink.getCurrent()

		self.BAC = total
	
	def toggle_drinks(self):
		if self.drinks_up:
			self.drinks_up = False
			anim = Animation(y = 150, t='out_elastic')
			anim.start(self.drinks_pane)
		else:
			anim = Animation(y = self.height - 50, t='out_elastic')
			anim.start(self.drinks_pane)
			self.drinks_up = True
		

class Drink():
	def __init__(self,mass,gender,quantity,ABV,at_time,name):
		self.name = name
		self.mass = mass
		self.gender = gender
		self.quantity = quantity
		self.ABV = ABV
		self.grams_alcohol = (quantity * (ABV/100.0)) * 23.35
		self.at_time = at_time
		self.removed = False

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
		try:
			val = float(val[:7])
		except:
			val = 0
		if val < 0:
			return 0
		return val
	
	def __str__(self):
		return "{0} oz. of \"{3}\" at {1}% ABV added {2} to your BAC.".format(
			self.quantity,
			self.ABV,
			self.getCurrent(),
			self.name)

class DrinkLabel(BoxLayout):
	label_text = StringProperty("loading...")
	def __init__(self,drink, dlist, **kwargs):
		super(DrinkLabel,self).__init__(**kwargs)
		self.drink = drink
		self.dlist = dlist
		self.label_text = str(drink)
		
	def edit_drink(self):
		print("editing!")
	
	def delete_drink(self):
		print("deleting!")
		self.dlist.drink_grid.remove_widget(self)
		self.drink.removed = True
		

class DrinkList(ScrollView):
	drinks = []
	drink_grid = ObjectProperty(None)
	
	def append(self,val):
		self.drinks.append(val)
		try:
			self.drink_grid.add_widget(DrinkLabel(val,self))
		except Exception as e:
			print(e)

	def clear(self):
		self.drink_grid.clear_widgets()
		drinks = []


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
