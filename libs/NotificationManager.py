import collections

from gui.components.Generic.Notification import Notification
from libs.GenericManager import GenericManager
# usage: notificationManager.add(lv.SYMBOL.OK, "message")

class NotificationManager(GenericManager):
	notifications = collections.deque((), 10)
	_notificationIsShown = False

	def __init__(self, singletons):
		self.setSingletons(singletons)
		pass

	def add(self, symbol, text, duration=5000):
		notification = Notification(symbol, text, duration, self._done)
		self.notifications.append(
			notification
		)
		if self._notificationIsShown == False:
			self.notifications.popleft().show()
			self._notificationIsShown = True

	def _done(self, notification):
		self._notificationIsShown = False
		if len(self.notifications) > 0:
			self.notifications.popleft().show()
			self._notificationIsShown = True
