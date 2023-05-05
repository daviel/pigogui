import lvgl as lv
#import SDL
from lv_utils import event_loop


globalKeyCallbacks = []

def global_key_callback(drv, data):
    if data == lv.EVENT.PRESSED or data == lv.EVENT.RELEASED or data == lv.EVENT.KEY:
        #print(indev1.get_key(), data)
        for func in globalKeyCallbacks:
            func(indev1, drv, data)

def addGlobalKeyCallback(cb):
    globalKeyCallbacks.append(cb)

def removeGlobalKeyCallback(cb):
    for func in globalKeyCallbacks:
        if func.__name__ == cb.__name__:
            globalKeyCallbacks.remove(func)
            break


event_loop = event_loop()
mouse = lv.sdl_mouse_create()
indev1 = lv.sdl_keyboard_create()
