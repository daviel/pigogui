import collections
from gui.components.SoundBar import SoundBar
from gui.components.DisplayBar import DisplayBar
from libs.GenericManager import GenericManager


class SoundDisplayBarManager(GenericManager):
	soundbar = SoundBar()
	displaybar = DisplayBar()

	def __init__(self, singletons):
		self.setSingletons(singletons)
		pass

	