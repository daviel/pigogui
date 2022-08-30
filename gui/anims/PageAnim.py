import lvgl as lv
from gui.anims.GenericAnim import GenericAnim


def anim_func(obj, anim, val):
	obj.target.set_pos(val, 0)


ANIM_PAGE_SLIDE_OUT_LEFT = GenericAnim()
ANIM_PAGE_SLIDE_OUT_LEFT.set_values(0, -320)
ANIM_PAGE_SLIDE_OUT_LEFT.set_time(1000)
ANIM_PAGE_SLIDE_OUT_LEFT.set_path_cb(lv.anim_t.path_ease_in)
ANIM_PAGE_SLIDE_OUT_LEFT.anim_cb = anim_func

ANIM_PAGE_SLIDE_OUT_RIGHT = GenericAnim()
ANIM_PAGE_SLIDE_OUT_RIGHT.set_values(0, 320)
ANIM_PAGE_SLIDE_OUT_RIGHT.set_time(1000)
ANIM_PAGE_SLIDE_OUT_RIGHT.set_path_cb(lv.anim_t.path_ease_in)
ANIM_PAGE_SLIDE_OUT_RIGHT.anim_cb = anim_func

ANIM_PAGE_SLIDE_IN_LEFT = GenericAnim()
ANIM_PAGE_SLIDE_IN_LEFT.set_values(-320, 0)
ANIM_PAGE_SLIDE_IN_LEFT.set_time(1000)
ANIM_PAGE_SLIDE_IN_LEFT.set_path_cb(lv.anim_t.path_ease_in)
ANIM_PAGE_SLIDE_IN_LEFT.anim_cb = anim_func

ANIM_PAGE_SLIDE_IN_RIGHT = GenericAnim()
ANIM_PAGE_SLIDE_IN_RIGHT.set_values(320, 0)
ANIM_PAGE_SLIDE_IN_RIGHT.set_time(1000)
ANIM_PAGE_SLIDE_IN_RIGHT.set_path_cb(lv.anim_t.path_ease_in)
ANIM_PAGE_SLIDE_IN_RIGHT.anim_cb = anim_func

