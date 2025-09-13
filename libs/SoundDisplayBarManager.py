import collections
from gui.components.SoundBar import SoundBar
from gui.components.DisplayBar import DisplayBar
from libs.GenericManager import GenericManager


class SoundDisplayBarManager(GenericManager):
	soundbar = ""
	displaybar = ""

	def __init__(self, singletons):
		self.setSingletons(singletons)
		self.soundbar = SoundBar(singletons)
		self.displaybar = DisplayBar(singletons)
		pass

	