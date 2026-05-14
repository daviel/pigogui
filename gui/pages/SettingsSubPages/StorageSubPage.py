import lvgl as lv

from gui.components.Generic.SubPage import SubPage
from gui.components.Generic.Button import Button

from libs.ffishell import runShellCommand


def _parse_df(output):
	lines = output.strip().splitlines()
	if len(lines) < 2:
		return None
	parts = lines[-1].split()
	if len(parts) >= 5:
		return {"size": parts[1], "used": parts[2], "avail": parts[3], "pct": parts[4]}
	return None


def _parse_du(output):
	parts = output.strip().split()
	return parts[0] if parts else "?"


def _sh_quote(s):
	return "'" + s.replace("'", "'\\''") + "'"


class StorageSubPage(SubPage):
	def __init__(self, container, singletons):
		super().__init__(container, singletons)
		self.set_width(240)
		self.set_style_pad_column(8, 0)
		self.set_style_pad_row(6, 0)
		self.set_flex_flow(lv.FLEX_FLOW.ROW_WRAP)
		self.set_style_pad_hor(8, 0)
		self.set_style_pad_ver(6, 0)

		lv.label(self).set_text("Root filesystem")
		self._rootLabel = lv.label(self)
		self._rootLabel.set_text("...")
		self._rootLabel.set_width(220)

		lv.label(self).set_text("Games folder")
		self._gamesLabel = lv.label(self)
		self._gamesLabel.set_text("...")
		self._gamesLabel.set_width(220)

		lv.label(self).set_text("Download path")
		self._dlLabel = lv.label(self)
		self._dlLabel.set_text("...")
		self._dlLabel.set_width(220)

		refreshBtn = Button(self, lv.SYMBOL.REFRESH + " Refresh")
		refreshBtn.set_size(110, 28)
		refreshBtn.label.center()
		refreshBtn.add_event_cb(self._onRefresh, lv.EVENT.PRESSED, None)

	def loadSubPage(self, event):
		self._refresh()

	def _refresh(self):
		config = self.singletons["DATA_MANAGER"].get("configuration")
		gamesdir = config["gamesdir"]
		dlpath = config["user"]["store"]["downloadpath"]

		root_info = _parse_df(runShellCommand("df -h /"))
		if root_info:
			self._rootLabel.set_text(
				root_info["used"] + " / " + root_info["size"] + "  (" + root_info["avail"] + " free)"
			)
		else:
			self._rootLabel.set_text("?")

		games_size = _parse_du(runShellCommand("du -sh " + _sh_quote(gamesdir)))
		self._gamesLabel.set_text(games_size + "  " + gamesdir)

		dl_info = _parse_df(runShellCommand("df -h " + _sh_quote(dlpath)))
		if dl_info:
			self._dlLabel.set_text(dlpath + "  " + dl_info["avail"] + " free")
		else:
			self._dlLabel.set_text(dlpath)

	def _onRefresh(self, e):
		self._refresh()
