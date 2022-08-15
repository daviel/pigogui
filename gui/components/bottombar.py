import lvgl as lv
from gui.components.button import Button


class BottomBar(lv.obj):
	clock = ""
	buttons = [
		{
			'button_text': "A",
			'text': "Start",
			'color': lv.PALETTE.BLUE
		},
		{
			'button_text': "B",
			'text': "Back",
			'color': lv.PALETTE.RED
		},
		{
			'button_text': "X",
			'text': "Info",
			'color': lv.PALETTE.YELLOW
		},
		{
			'button_text': "Y",
			'text': "Options",
			'color': lv.PALETTE.GREEN
		}
	]


	def __init__(self, container):
		super().__init__(container)

		self.set_size(320, 240)
		self.align(lv.ALIGN.CENTER, 0, 0)
		self.set_flex_flow(lv.FLEX_FLOW.ROW)
		self.clear_flag(self.FLAG.SCROLLABLE)

		for button in self.buttons:
			button1 = Button(self, button['button_text'])
			button1.set_size(20, 20)
			button1.label.center()
			button1.set_style_bg_color(lv.palette_main(button['color']), 0)

			label = lv.label(self)
			label.set_text(button['text'])
