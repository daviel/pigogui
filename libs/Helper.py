import lvgl as lv

def loadImage(src):
	try:
		with open('./imgs/launchscreens/10.png','rb') as f:
			png_data = f.read()
	except:
		print("Could not find img_launchscreen_argb.png")
	return png_data


KEYBOARD_LETTERS_ONLY_MAP = ["Q", "W", "E", "R", "T", "Z", "U", "I", "O", "P", "\n",
	                        "A", "S", "D", "F", "G", "H", "J", "K", "L", "\n",
	                        "Y", "X", "C", "V", "B", "N", "M", "\n",
	                        lv.SYMBOL.CLOSE, lv.SYMBOL.LEFT, lv.SYMBOL.RIGHT, lv.SYMBOL.BACKSPACE, lv.SYMBOL.OK, ""
	                       ]

KEYBOARD_LETTERS_ONLY_CTRL = [4, 4, 4, 4, 4, 4, 4, 4, 4, 4,
					            4, 4, 4, 4, 4, 4, 4, 4, 4,
					            4, 4, 4, 4, 4, 4, 4,
					            6, 6, 6, 6, 6
							]

def KEYBOARD_LETTERS_ONLY():
	KEYBOARD = lv.keyboard(lv.scr_act())
	KEYBOARD.set_map(KEYBOARD.MODE.USER_2, KEYBOARD_LETTERS_ONLY_MAP, KEYBOARD_LETTERS_ONLY_CTRL)
	KEYBOARD.set_mode(KEYBOARD.MODE.USER_2)
	return KEYBOARD

def KEYBOARD_ALL_SYMBOLS():
	KEYBOARD = lv.keyboard(lv.scr_act())
	KEYBOARD.set_mode(KEYBOARD.MODE.USER_1)
	return KEYBOARD
