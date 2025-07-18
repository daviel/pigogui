import lvgl as lv
from gui.anims.GenericAnim import GenericAnim


def anim_func(obj, anim, val):
	obj.target.set_pos(val, 0)
	pass

def ANIM_EXAMPLE():
	ANIM_EXAMPLE = GenericAnim()
	ANIM_EXAMPLE.set_values(0, 320)
	ANIM_EXAMPLE.set_duration(1000)
	ANIM_EXAMPLE.set_path_cb(lv.anim_t.path_ease_in)
	ANIM_EXAMPLE.anim_cb = anim_func
	return ANIM_EXAMPLE
