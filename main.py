import kivy
kivy.require('1.9.1')
from kivy.core.window import Window
Window.softinput_mode = 'pan'

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
from kivy.uix.modalview import ModalView

from kivy.lang import Builder
from kivy.app import App
from kivy.clock import Clock

from Carousel_Selector import Carousel_Selector
from scrollselector import ScrollSelector
from Model import Drink
import Model

import time

class FlightNight(FloatLayout):
	drinks = []
	drinks_up = True
	dirty_records = False
	
	pending_drink_quantity = NumericProperty(12)
	pending_drink_ABV = NumericProperty(8)
	gender = StringProperty('Male')
	mass_units = StringProperty('lb')
	mass = NumericProperty(200)
	dname = StringProperty("Sunny Honey Pale Ale!")
	
	drink_list = ObjectProperty(None)
	mass_ins = ObjectProperty(None)
	safety_switch = ObjectProperty(None)
	abv_selector = ObjectProperty(None)
	oz_selector = ObjectProperty(None)
	drinks_pane = ObjectProperty(None)
	
	session_start_time = time.localtime()
	session_start_time_str = StringProperty(time.strftime("%H:%M:%S",time.localtime()))
	last_drink = time.strftime("%H:%M:%S",time.localtime())
	BAC = NumericProperty(0)

	def __init__(self,data_dir,**kwargs):
		self.data_dir = data_dir
		super(FlightNight,self).__init__(**kwargs)
		print("Constructed!")

	def addItem(self):
		if self.last_drink == time.strftime("%H:%M:%S",time.localtime()):
			print("double tap. skipping")
			return None
		self.last_drink = time.strftime("%H:%M:%S",time.localtime())
		
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
		self.dirty_records = True

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
		self.dirty_records = True

	def update(self,*args):
		total = 0
		for drink in self.drinks:
			if not drink.removed:
				total += drink.getCurrent()

		self.BAC = total
		
		if self.dirty_records:
			self.save()
			self.dirty_records = False
	
	def toggle_drinks(self):
		if self.drinks_up:
			self.drinks_up = False
			anim = Animation(y = 150, t='out_elastic')
			anim.start(self.drinks_pane)
		else:
			anim = Animation(y = self.height - 50, t='out_elastic')
			anim.start(self.drinks_pane)
			self.drinks_up = True
	
	def save(self):
		#call to db with self.session_start_time and self.drinks
		Model.save(self.session_start_time,self.drinks,self.data_dir)
	
	def load_last(self):
		sid,self.drinks = Model.load_last(self.data_dir)
		if sid:
			self.session_start_time = time.strptime(str(sid),"%Y%m%d%H%M%S")
			self.session_start_time_str = time.strftime("%H:%M:%S",self.session_start_time)
			for drink in self.drinks:
				self.drink_list.append(drink)
		


class DrinkLabel(BoxLayout):
	name = StringProperty("")
	abv = StringProperty("")
	oz = StringProperty("")
	date = StringProperty("")
	bac = StringProperty("")

	def __init__(self,drink, dlist, **kwargs):
		super(DrinkLabel,self).__init__(**kwargs)
		self.drink = drink
		self.dlist = dlist
		self.label_text = str(drink)
		self.update()
		
	def edit_drink(self):
		de = DrinkEditor(self.drink,self)
		de.open()
	
	def delete_drink(self):
		self.dlist.drink_grid.remove_widget(self)
		self.drink.removed = True
	
	def update(self):
		self.name = str(self.drink.name)
#		self.name = str(self.drink)
		self.abv = str(self.drink.ABV)
		self.oz = str(self.drink.quantity)
		self.date = str(self.drink.at_time)
		self.bac = str(self.drink.getInitial())


class DrinkEditor(ModalView):
	name = StringProperty("loading")
	abv = StringProperty("loading")
	oz = StringProperty("loading")
	at_time = StringProperty("loading")
	name_box = ObjectProperty(None)
	abv_box = ObjectProperty(None)
	oz_box = ObjectProperty(None)
	at_box = ObjectProperty(None)
	def __init__(self,drink,drink_label,**kwargs):
		super(DrinkEditor,self).__init__(**kwargs)
		self.drink = drink
		self.drink_label = drink_label
		self.name = str(drink.name)
		self.oz = str(drink.quantity)
		self.abv = str(drink.ABV)
		self.at_time = time.strftime("%Y/%m/%d %H:%M:%S",drink.at_time)
	
	def save(self):
		try:
			self.drink.name = self.name_box.text
		except:
			print("Error updating name")
		
		try:
			self.drink.ABV = float(self.abv_box.text)
		except:
			print("Error updating ABV")
		
		try:
			self.drink.quantity = float(self.oz_box.text)
		except:
			print("Error updating OZ")
		
		try:
			self.drink.at_time = time.strptime(self.at_box.text,"%Y/%m/%d %H:%M:%S")
		except Exception as e:
			print("Error updating time:", e)
		
		try:
			self.drink_label.update()
		except:
			pass
		self.dismiss()

class DrinkList(ScrollView):
	drinks = []
	drink_grid = ObjectProperty(None)
	
	def append(self,val):
		print("Appending:",val)
		self.drinks.append(val)
		try:
			self.drink_grid.add_widget(DrinkLabel(val,self))
		except Exception as e:
			print(e)

	def clear(self):
		self.drink_grid.clear_widgets()
		drinks = []



class FlightNightApp(App):
	def build(self):
		data_dir = getattr(self, 'user_data_dir')
		print(data_dir)
		self.FlightNight = FlightNight(data_dir)
		Clock.schedule_interval(self.FlightNight.update,1)
		self.FlightNight.load_last()
		return self.FlightNight

	def on_pause(self):
		return True

	def on_resume(self):
		pass

FlightNightApp().run()
