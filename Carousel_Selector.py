from kivy.properties import ListProperty, StringProperty, NumericProperty, ObjectProperty
from kivy.adapters.listadapter import ListAdapter
from kivy.uix.listview import ListView, ListItemButton
from kivy.uix.selectableview import SelectableView
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.pagelayout import PageLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.uix.carousel import Carousel
from kivy.lang import Builder
from kivy.app import App
from kivy.clock import Clock

import time

class Carousel_Selector(BoxLayout):
	majc = ObjectProperty(None)
	minc = ObjectProperty(None)
	text = StringProperty("hi")
	val = NumericProperty(0.0)

	def major_update(self):
		self.val = self.majc.index + 1 + (self.minc.index * 0.1)
	
	def minor_update(self):
		self.val = self.majc.index + 1 + (self.minc.index * 0.1)

