import lvgl as lv

class SubPage(lv.obj):
	singletons = None

	def __init__(self, container, singletons):
		super().__init__(container)
		self.setSingletons(singletons)
		
	def loadSubPage(self, event):
		pass

	def setSingletons(self, singletons):
		self.singletons = singletons
