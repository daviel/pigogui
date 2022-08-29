import lvgl as lv

import usys as sys
from libs.imagetools2 import get_png_info, open_png


class LaunchScreen():

	def __init__(self):
		try:
			with open('./imgs/launchscreens/10.png','rb') as f:
				png_data = f.read()
		except:
			print("Could not find img_cogwheel_argb.png")
			sys.exit()

		# Register PNG image decoder
		decoder = lv.img.decoder_create()
		decoder.info_cb = get_png_info
		decoder.open_cb = open_png
		
		img_cogwheel_argb = lv.img_dsc_t({
			'data_size': len(png_data),
			'data': png_data
		})

		img1 = lv.img(lv.scr_act())
		img1.set_src(img_cogwheel_argb)
		img1.align(lv.ALIGN.CENTER, 0, 0)
		img1.set_size(320, 240)

		img2 = lv.img(lv.scr_act())
		img2.set_src(lv.SYMBOL.OK + "Accept")
		img2.align_to(img1, lv.ALIGN.OUT_BOTTOM_MID, 0, -20)