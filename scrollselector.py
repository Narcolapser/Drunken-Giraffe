from kivy.uix.scrollview import ScrollView
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ListProperty, StringProperty, NumericProperty, ObjectProperty
from kivy.clock import Clock

from kivy.animation import Animation


class ScrollSelector(BoxLayout):
	text = StringProperty("hi")
	val = NumericProperty(0.0)
	sv = ObjectProperty(None)
	
	offset = 0.0025
	
	def __init__(self,**kwargs):
		super(ScrollSelector,self).__init__(**kwargs)
		Clock.schedule_interval(self.inform, 1)

	def set_val(self,val):
		sval = (100 - val) / 100.0
		self.sv.scroll_y = sval + self.offset

	def inform(self,foo):
		if self.sv:
			val = 100 - round(self.sv.scroll_y * 100)
			scroll_val =  round(self.sv.scroll_y*100.0)/100.0
			self.sv.scroll_y = scroll_val + self.offset
	
	def major_update(self):
		self.val = 100 - round(self.sv.scroll_y * 100)
		
	def do_layout(self, *largs):
		print("pre Height:",self.height)
		for l in self.sv.children[0].children:
			l.height = self.height
		super(ScrollSelector,self).do_layout(*largs)
		print("post Height:",self.height)
