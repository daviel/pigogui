import lvgl as lv

from gui.components.Generic.SubPage import SubPage
from gui.components.Generic.Button import Button
from gui.components.Generic.Loader import Loader
from gui.components.Generic.Switch import Switch

from libs.ffishell import runShellCommand
from libs.threading import runShellCommand_bg


def _parse_bt_devices(output):
	devices = []
	for line in output.splitlines():
		parts = line.strip().split(" ", 2)
		if len(parts) >= 3 and parts[0] == "Device":
			devices.append({"mac": parts[1], "name": parts[2]})
	return devices


class BluetoothSubPage(SubPage):
	def __init__(self, container, singletons):
		super().__init__(container, singletons)
		self.set_width(240)
		self.set_style_pad_column(8, 0)
		self.set_style_pad_row(8, 0)
		self.set_flex_flow(lv.FLEX_FLOW.ROW_WRAP)
		self.set_style_pad_hor(4, 0)
		self.set_style_pad_ver(4, 0)

		# Row 1: power toggle — label + switch as direct children (gridnav-reachable)
		powerLabel = lv.label(self)
		powerLabel.set_text("Bluetooth")
		powerLabel.set_width(148)

		self._powerSwitch = Switch(self)
		self._powerSwitch.add_event_cb(self._onPowerToggle, lv.EVENT.ALL, None)

		# Row 2: scan button + loader as direct children (button is gridnav-reachable)
		self._scanBtn = Button(self, lv.SYMBOL.REFRESH + " Scan")
		self._scanBtn.set_size(100, 28)
		self._scanBtn.label.center()
		self._scanBtn.add_event_cb(self._onScan, lv.EVENT.PRESSED, None)

		self._loader = Loader(self)
		self._loader.set_size(24, 24)
		self._loader.add_flag(self._loader.FLAG.HIDDEN)

		# Row 3: device list — clickable container with its own inner gridnav
		self.deviceContainer = lv.obj(self)
		self.deviceContainer.set_size(224, 156)
		self.deviceContainer.set_flex_flow(lv.FLEX_FLOW.COLUMN)
		self.deviceContainer.set_style_pad_row(2, 0)
		self.deviceContainer.set_style_pad_hor(0, 0)
		self.deviceContainer.set_style_border_width(1, 0)
		self.deviceContainer.add_flag(lv.obj.FLAG.CLICKABLE)
		lv.gridnav_add(self.deviceContainer, lv.GRIDNAV_CTRL.NONE)

		self._scanTimer = lv.timer_create(self._onScanDone, 8000, None)
		self._scanTimer.pause()

	def loadSubPage(self, event):
		self._updatePowerState()
		self._refreshDeviceList()

	def _updatePowerState(self):
		output = runShellCommand("bluetoothctl show")
		if "Powered: yes" in output:
			self._powerSwitch.add_state(lv.STATE.CHECKED)
		else:
			self._powerSwitch.remove_state(lv.STATE.CHECKED)

	def _refreshDeviceList(self):
		self.deviceContainer.clean()
		all_devices = _parse_bt_devices(runShellCommand("bluetoothctl devices"))
		connected_macs = {d["mac"] for d in _parse_bt_devices(runShellCommand("bluetoothctl devices Connected"))}

		for device in all_devices:
			mac = device["mac"]
			name = device["name"]
			is_connected = mac in connected_macs

			prefix = lv.SYMBOL.OK + " " if is_connected else "  "
			btn = Button(self.deviceContainer, prefix + name)
			btn.set_width(210)
			btn.set_height(24)
			btn.set_style_pad_hor(4, 0)
			btn.set_style_pad_ver(2, 0)
			btn.label.align(lv.ALIGN.LEFT_MID, 4, 0)
			btn.label.set_width(155)
			btn.label.set_long_mode(lv.label.LONG_MODE.CLIP)

			actionLabel = lv.label(btn)
			actionLabel.set_text("Disc." if is_connected else "Conn.")
			actionLabel.align(lv.ALIGN.RIGHT_MID, -4, 0)

			def make_cb(m, connected):
				def cb(obj, e):
					if connected:
						runShellCommand_bg("bluetoothctl disconnect " + m)
					else:
						runShellCommand_bg("bluetoothctl connect " + m)
				return cb
			btn.pressCallback = make_cb(mac, is_connected)

	def _onPowerToggle(self, e):
		if e.get_code() == lv.EVENT.VALUE_CHANGED:
			if self._powerSwitch.has_state(lv.STATE.CHECKED):
				runShellCommand_bg("bluetoothctl power on")
			else:
				runShellCommand_bg("bluetoothctl power off")

	def _onScan(self, e):
		self._loader.remove_flag(self._loader.FLAG.HIDDEN)
		runShellCommand_bg("bluetoothctl --timeout 8 scan on")
		self._scanTimer.reset()
		self._scanTimer.resume()

	def _onScanDone(self, timer):
		timer.pause()
		self._loader.add_flag(self._loader.FLAG.HIDDEN)
		self._refreshDeviceList()
