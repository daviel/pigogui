import collections

from gui.components.Notification import Notification



class NotificationManager():
	notifications = collections.deque((), 10)
	_notificationIsShown = False

	def __init__(self):
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
		


notificationManager = NotificationManager()