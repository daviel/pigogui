import lvgl as lv
import os

from gui.pages.GenericPage import GenericPage
from gui.components.Generic.IconButton import IconButton
from gui.styles.PageStyle import SETUP_PAGE_STYLE
from libs.init_drv import indev1
from libs.Helper import loadImageAndConvert


class GameDetailsPage(GenericPage):
	animIn = lv.SCR_LOAD_ANIM.FADE_IN
	animOut = lv.SCR_LOAD_ANIM.FADE_OUT
	_confirmDelete = False

	def __init__(self, singletons):
		super().__init__(singletons)
		self.animIn = lv.SCR_LOAD_ANIM.FADE_IN
		self.animOut = lv.SCR_LOAD_ANIM.FADE_OUT
		self._screenshotImages = []
		self._overlay = None

		self.add_style(SETUP_PAGE_STYLE, 0)
		self.set_flex_flow(lv.FLEX_FLOW.ROW)
		self.set_style_pad_all(0, 0)
		self.set_style_pad_column(0, 0)
		self.set_style_pad_row(0, 0)

		# ── Linke Spalte: Cover + Buttons (100 px) ───────────────────────────
		lc = lv.obj(self)
		lc.set_size(100, 240)
		lc.set_flex_flow(lv.FLEX_FLOW.COLUMN)
		lc.set_flex_align(lv.FLEX_ALIGN.START, lv.FLEX_ALIGN.CENTER, lv.FLEX_ALIGN.CENTER)
		lc.set_style_pad_all(4, 0)
		lc.set_style_pad_row(6, 0)
		lc.set_scrollbar_mode(lv.SCROLLBAR_MODE.OFF)
		self.leftContainer = lc

		self.coverImage = lv.image(lc)
		self.coverImage.set_size(88, 88)
		self.coverImage.set_style_radius(6, 0)
		self.coverImage.set_style_clip_corner(6, 0)

		self.playButton = IconButton(lc, lv.SYMBOL.PLAY, "Play")
		self.playButton.set_size(88, 26)
		self.playButton.add_event_cb(self._onPlay, lv.EVENT.PRESSED, None)

		self.deleteButton = IconButton(lc, lv.SYMBOL.TRASH, "Delete")
		self.deleteButton.set_size(88, 26)
		self.deleteButton.add_event_cb(self._onDelete, lv.EVENT.PRESSED, None)

		self.backButton = IconButton(lc, lv.SYMBOL.LEFT, "Back")
		self.backButton.set_size(88, 26)
		self.backButton.add_event_cb(self._onBack, lv.EVENT.PRESSED, None)

		# ── Rechte Spalte: Metadaten + Screenshots (220 px) ──────────────────
		rc = lv.obj(self)
		rc.set_size(220, 240)
		rc.set_flex_flow(lv.FLEX_FLOW.COLUMN)
		rc.set_flex_align(lv.FLEX_ALIGN.START, lv.FLEX_ALIGN.START, lv.FLEX_ALIGN.START)
		rc.set_style_pad_all(4, 0)
		rc.set_style_pad_row(4, 0)
		rc.set_scrollbar_mode(lv.SCROLLBAR_MODE.OFF)
		self.rightContainer = rc

		# Titel (1 Zeile, scrollend)
		self.gameTitle = lv.label(rc)
		self.gameTitle.set_size(212, 18)
		self.gameTitle.set_long_mode(lv.label.LONG_MODE.SCROLL_CIRCULAR)

		# Größe + Genre (1 Zeile, scrollend)
		self.infoLine = lv.label(rc)
		self.infoLine.set_size(212, 16)
		self.infoLine.set_long_mode(lv.label.LONG_MODE.SCROLL_CIRCULAR)

		# Beschreibung (2 Zeilen, abgeschnitten mit „…")
		self.description = lv.label(rc)
		self.description.set_size(212, 34)
		self.description.set_long_mode(lv.label.LONG_MODE.DOTS)

		# Screenshot-Streifen
		# Höhe: 240 - 2×4pad - 3×4gap - 18 - 16 - 34 = 152 px → 144 mit Abstand
		ic = lv.obj(rc)
		ic.set_size(212, 144)
		ic.set_flex_flow(lv.FLEX_FLOW.ROW)
		ic.set_flex_align(lv.FLEX_ALIGN.START, lv.FLEX_ALIGN.CENTER, lv.FLEX_ALIGN.CENTER)
		ic.set_style_pad_column(4, 0)
		ic.set_style_pad_all(4, 0)
		ic.set_style_border_width(0, 0)
		ic.set_scrollbar_mode(lv.SCROLLBAR_MODE.AUTO)
		self.imageContainer = ic

		# ── Navigation ────────────────────────────────────────────────────────
		self.group = lv.group_create()
		self.group.add_obj(lc)
		self.group.add_obj(ic)
		indev1.set_group(self.group)

		lv.gridnav_add(lc, lv.GRIDNAV_CTRL.NONE)
		lv.gridnav_add(ic, lv.GRIDNAV_CTRL.NONE)

	# ── Lifecycle ─────────────────────────────────────────────────────────────

	def pageOpened(self):
		game = self.data
		self._confirmDelete = False
		self.deleteButton.get_child(1).set_text("Delete")

		installed_dirnames = {g["dirname"] for g in self.singletons["DATA_MANAGER"].get("games")}
		is_installed = game.get("dirname", "") in installed_dirnames
		show_delete = game.get('deletable', True) and is_installed
		if not show_delete:
			self.deleteButton.add_flag(lv.obj.FLAG.HIDDEN)
		else:
			self.deleteButton.remove_flag(lv.obj.FLAG.HIDDEN)

		self.gameTitle.set_text(game['title'])

		tags = ' · '.join(game.get('tags', []))
		size = str(game.get('size', ''))
		self.infoLine.set_text(lv.SYMBOL.SD_CARD + " " + size + " MB   " + lv.SYMBOL.LIST + " " + tags)

		self.description.set_text(game.get('description', ''))

		try:
			self.coverImage.set_src(loadImageAndConvert(game['main_image']))
		except Exception:
			pass

		for src in game.get('screenshots', []):
			self._addScreenshot(src)

	def pageClosed(self):
		self._confirmDelete = False
		self._closeOverlay(None)
		self._screenshotImages.clear()
		for i in range(self.imageContainer.get_child_count()):
			self.imageContainer.get_child(i).delete_delayed(1000)

	# ── Screenshots ───────────────────────────────────────────────────────────

	def _addScreenshot(self, src):
		img_dsc = loadImageAndConvert(src)
		if img_dsc is None:
			return
		self._screenshotImages.append(img_dsc)

		size = 130
		btn = lv.button(self.imageContainer)
		btn.set_size(size, size)
		btn.set_style_pad_all(3, 0)

		img = lv.image(btn)
		img.set_size(size - 6, size - 6)
		img.set_src(img_dsc)
		try:
			img.set_inner_align(lv.IMAGE_ALIGN.STRETCH)
		except Exception:
			pass
		img.set_style_radius(4, 0)
		img.set_style_clip_corner(4, 0)
		img.align(lv.ALIGN.CENTER, 0, 0)

		btn.add_event_cb(self._makeClickHandler(img_dsc), lv.EVENT.CLICKED, None)

	def _makeClickHandler(self, img_dsc):
		def handler(e):
			self._showScreenshotOverlay(img_dsc)
		return handler

	def _showScreenshotOverlay(self, img_dsc):
		if self._overlay:
			return

		overlay = lv.obj(lv.layer_top())
		overlay.set_size(320, 240)
		overlay.set_pos(0, 0)
		overlay.set_style_bg_color(lv.color_hex(0x000000), 0)
		overlay.set_style_bg_opa(lv.OPA.COVER, 0)
		overlay.set_style_border_width(0, 0)
		overlay.set_style_pad_all(0, 0)
		overlay.add_flag(lv.obj.FLAG.CLICKABLE)

		img = lv.image(overlay)
		img.set_size(320, 240)
		img.set_src(img_dsc)
		try:
			img.set_inner_align(lv.IMAGE_ALIGN.STRETCH)
		except Exception:
			pass
		img.align(lv.ALIGN.CENTER, 0, 0)

		self._overlay = overlay

		overlay_group = lv.group_create()
		overlay_group.add_obj(overlay)
		indev1.set_group(overlay_group)

		overlay.add_event_cb(self._closeOverlay, lv.EVENT.CLICKED, None)
		overlay.add_event_cb(self._closeOverlay, lv.EVENT.KEY, None)

	def _closeOverlay(self, e):
		if self._overlay:
			self._overlay.delete()
			self._overlay = None
			indev1.set_group(self.group)

	# ── Helpers ───────────────────────────────────────────────────────────────

	def _deleteDir(self, path):
		for entry in os.ilistdir(path):
			name, ftype = entry[0], entry[1]
			full = path + "/" + name
			if ftype == 0x4000:
				self._deleteDir(full)
			else:
				os.remove(full)
		os.rmdir(path)

	# ── Event-Handler ────────────────────────────────────────────────────────

	def _onPlay(self, e):
		game = self.data
		if not game.get('executable'):
			return
		config = self.singletons["DATA_MANAGER"].get("configuration")
		path = config["gamesdir"] + game["dirname"] + "/" + game["executable"]
		self.singletons["APPLICATION_MANAGER"].startApp(path, game.get("keymap", ""))

	def _onDelete(self, e):
		if not self.data.get('deletable', True):
			return
		if not self._confirmDelete:
			self._confirmDelete = True
			self.deleteButton.get_child(1).set_text("Sure?")
			return

		game = self.data
		config = self.singletons["DATA_MANAGER"].get("configuration")
		try:
			self._deleteDir(config["gamesdir"] + game["dirname"])
		except OSError as err:
			print("delete error:", err)
		self.singletons["DATA_MANAGER"].findGames(config["gamesdir"])
		self.singletons["PAGE_MANAGER"].pagePrev()

	def _onBack(self, e):
		self.singletons["PAGE_MANAGER"].pagePrev()
