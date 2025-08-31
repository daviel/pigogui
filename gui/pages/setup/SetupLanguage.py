import lvgl as lv

from gui.pages.GenericPage import GenericPage
from gui.components.Generic.Button import Button
from libs.init_drv import indev1
from libs.Helper import loadImage, KEYBOARD_LETTERS_ONLY, KEYBOARD_ALL_SYMBOLS, COUNTRY_LIST, add_or_replace
from gui.styles.CustomTheme import CustomTheme

from gui.components.Generic.ActiveSlider import ActiveSlider
from gui.components.Generic.ActiveRoller import ActiveRoller

from gui.styles.PageStyle import SETUP_PAGE_STYLE

from libs.ffishell import runShellCommand


class SetupLanguage(GenericPage):
	errLabel = ""
	nametextarea = ""
	nextbutton = ""
	keyboard = False
	group = ""
	language_list = COUNTRY_LIST
	language_list_parsed = []

	def __init__(self, container):
		super().__init__(container)

		for country in self.language_list:
			self.language_list_parsed.append(self.language_list[country])

		# Create sub pages
		self.set_width(240)
		self.set_style_pad_column(8, 0)
		self.set_style_pad_row(8, 0)
		self.set_flex_flow(lv.FLEX_FLOW.ROW_WRAP)
		# content
		label = lv.label(self)
		label.set_text("Country")
		label.set_width(100)

		self.countryRoller = ActiveRoller(self)
		self.countryRoller.set_options("\n".join(self.language_list_parsed), lv.roller.MODE.NORMAL)
		self.countryRoller.set_visible_row_count(2)
		self.countryRoller.set_width(180)
		self.countryRoller.add_event_cb(self.changeCountryHandler, lv.EVENT.ALL, None)

		label = lv.label(self)
		label.set_text("Language")
		label.set_width(100)

		self.languageRoller = ActiveRoller(self)
		self.languageRoller.set_options("\n".join(self.language_list_parsed), lv.roller.MODE.NORMAL)
		self.languageRoller.set_visible_row_count(2)
		self.languageRoller.set_width(180)
		self.languageRoller.add_event_cb(self.changeLanguageHandler, lv.EVENT.ALL, None)

		self.nextbutton = Button(self, lv.SYMBOL.RIGHT)
		self.nextbutton.set_size(50, 30)
		self.nextbutton.label.center()
		self.nextbutton.add_event_cb(self.pageNext, lv.EVENT.PRESSED, None)

		self.group = lv.group_create()
		self.group.add_obj(self)
		indev1.set_group(self.group)

		lv.gridnav_add(self, lv.GRIDNAV_CTRL.NONE)
		lv.gridnav_set_focused(self, self.countryRoller, False)


	def changeCountryHandler(self, e):
		code = e.get_code()
		obj = e.get_target_obj()
		if code == lv.EVENT.KEY:
			key = e.get_key()
			if key == lv.KEY.UP or key == lv.KEY.DOWN:
				option = " " * 20
				obj.get_selected_str(option, len(option))
				selection = option.strip()[:-1]
				country_code = ""
				for country in self.language_list:
					if(self.language_list[country] == selection):
						country_code = country
						break

				config = self.singletons["DATA_MANAGER"].get("configuration")
				if config["debug"] == False:
					configline = "cfg80211.ieee80211_regdom={}".format(country_code)
					# add cfg80211.ieee80211_regdom=DE to /boot/firmware/cmdline.txt
					ret = runShellCommand('cp "/boot/firmware/cmdline.txt" "/boot/firmware/cmdline.txt.old"')
					add_or_replace_in_file("/boot/firmware/cmdline.txt", "configline", identifier="cfg80211.ieee80211_regdom=")

				config = self.singletons["DATA_MANAGER"].get("configuration")
				config["user"]["system"]["country"] = selection
				config["user"]["system"]["country_code"] = country_code
				self.singletons["DATA_MANAGER"].saveAll()

	def changeLanguageHandler(self, e):
		code = e.get_code()
		obj = e.get_target_obj()
		if code == lv.EVENT.KEY:
			key = e.get_key()
			if key == lv.KEY.UP or key == lv.KEY.DOWN:
				option = " " * 20
				obj.get_selected_str(option, len(option))
				selection = option.strip()[:-1]

				config = self.singletons["DATA_MANAGER"].get("configuration")
				config["user"]["system"]["language"] = selection
				self.singletons["DATA_MANAGER"].saveAll()

	def pageNext(self, e):
		self.singletons["PAGE_MANAGER"].setCurrentPage("setuppage", True)
	
	