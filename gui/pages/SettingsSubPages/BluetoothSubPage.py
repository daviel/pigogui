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
		self.set_style_pad_column(4, 0)
		self.set_style_pad_row(6, 0)
		self.set_flex_flow(lv.FLEX_FLOW.COLUMN)
		self.set_style_pad_hor(4, 0)
		self.set_style_pad_ver(4, 0)

		powerRow = lv.obj(self)
		powerRow.set_size(220, 32)
		powerRow.set_flex_flow(lv.FLEX_FLOW.ROW)
		powerRow.set_style_border_width(0, 0)
		powerRow.set_style_bg_opa(lv.OPA.TRANSP, 0)
		powerRow.set_style_pad_column(8, 0)
		powerRow.remove_flag(lv.obj.FLAG.SCROLLABLE)

		powerLabel = lv.label(powerRow)
		powerLabel.set_text("Bluetooth")
		powerLabel.set_width(120)

		self._powerSwitch = Switch(powerRow)
		self._powerSwitch.add_event_cb(self._onPowerToggle, lv.EVENT.ALL, None)

		scanRow = lv.obj(self)
		scanRow.set_size(220, 32)
		scanRow.set_flex_flow(lv.FLEX_FLOW.ROW)
		scanRow.set_style_border_width(0, 0)
		scanRow.set_style_bg_opa(lv.OPA.TRANSP, 0)
		scanRow.set_style_pad_column(8, 0)
		scanRow.remove_flag(lv.obj.FLAG.SCROLLABLE)

		scanBtn = Button(scanRow, lv.SYMBOL.REFRESH + " Scan")
		scanBtn.set_size(100, 28)
		scanBtn.label.center()
		scanBtn.add_event_cb(self._onScan, lv.EVENT.PRESSED, None)

		self._loader = Loader(scanRow)
		self._loader.set_size(24, 24)
		self._loader.add_flag(self._loader.FLAG.HIDDEN)

		self.deviceContainer = lv.obj(self)
		self.deviceContainer.set_size(220, 140)
		self.deviceContainer.set_flex_flow(lv.FLEX_FLOW.COLUMN)
		self.deviceContainer.set_style_pad_row(2, 0)
		self.deviceContainer.set_style_pad_hor(0, 0)
		self.deviceContainer.set_style_border_width(1, 0)

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

			row = lv.obj(self.deviceContainer)
			row.set_size(210, 26)
			row.set_flex_flow(lv.FLEX_FLOW.ROW)
			row.set_style_border_width(0, 0)
			row.set_style_bg_opa(lv.OPA.TRANSP, 0)
			row.set_style_pad_column(4, 0)
			row.remove_flag(lv.obj.FLAG.SCROLLABLE)

			nameLabel = lv.label(row)
			nameLabel.set_text(name)
			nameLabel.set_width(130)
			nameLabel.set_long_mode(lv.label.LONG_MODE.CLIP)

			btn = Button(row, "Disc." if is_connected else "Conn.")
			btn.set_size(64, 22)
			btn.label.center()

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
