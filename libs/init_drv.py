import lvgl as lv
from lv_utils import event_loop

event_loop = event_loop()
mouse = lv.sdl_mouse_create()
indev1 = lv.sdl_keyboard_create()
