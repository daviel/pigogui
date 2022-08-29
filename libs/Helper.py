def loadImage(src):
	try:
		with open('./imgs/launchscreens/10.png','rb') as f:
			png_data = f.read()
	except:
		print("Could not find img_launchscreen_argb.png")
	return png_data