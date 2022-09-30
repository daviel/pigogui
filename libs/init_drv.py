import lvgl as lv
import SDL


globalKeyCallbacks = []

def global_key_callback(drv, data):
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

# Register SDL display driver.
draw_buf = lv.disp_draw_buf_t()
buf1_1 = bytearray(480*10)
draw_buf.init(buf1_1, None, len(buf1_1)//4)
disp_drv = lv.disp_drv_t()
disp_drv.init()
disp_drv.draw_buf = draw_buf
disp_drv.flush_cb = SDL.monitor_flush
disp_drv.hor_res = 320
disp_drv.ver_res = 240
disp_drv.screen_transp = True
disp_drv.register()

# register SDL mouse driver
indev_drv = lv.indev_drv_t()
indev_drv.init()
indev_drv.type = lv.INDEV_TYPE.POINTER
indev_drv.read_cb = SDL.mouse_read
indev = indev_drv.register()

indev_drv1 = lv.indev_drv_t()
indev_drv1.init()
indev_drv1.type = lv.INDEV_TYPE.KEYPAD
indev_drv1.read_cb = SDL.keyboard_read
indev_drv1.feedback_cb = global_key_callback
indev1 = indev_drv1.register()
