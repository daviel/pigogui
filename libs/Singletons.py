from libs.PageManager import PageManager
from libs.NotificationManager import NotificationManager
from libs.DataManager import DataManager
from libs.SoundDisplayBarManager import SoundDisplayBarManager
from libs.ApplicationManager import ApplicationManager
from libs.DownloadManager import DownloadManager
from libs.BatteryManager import BatteryManager




class SingletonsClass():
    singletons = {}

    def __init__(self):
        self.singletons["DATA_MANAGER"] = DataManager(self.singletons)
        self.singletons["NOTIFICATION_MANAGER"] = NotificationManager(self.singletons)
        self.singletons["SOUNDDISPLAYBAR_MANAGER"] = SoundDisplayBarManager(self.singletons)
        self.singletons["DOWNLOAD_MANAGER"] = DownloadManager(self.singletons)
        self.singletons["BATTERY_MANAGER"] = BatteryManager(self.singletons)
        self.singletons["PAGE_MANAGER"] = PageManager(self.singletons)
        self.singletons["APPLICATION_MANAGER"] = ApplicationManager(self.singletons)
