#!/usr/bin/micropython -i
import lvgl as lv
lv.init()

import SDL
SDL.init(w=320,h=240)

from gui.components.button import Button
from gui.components.topbar import TopBar
from gui.components.bottombar import BottomBar
from gui.components.games import Games

from imagetools import get_png_info, open_png

# Register PNG image decoder
decoder = lv.img.decoder_create()
decoder.info_cb = get_png_info
decoder.open_cb = open_png

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
disp_drv.screen_transp = 1
disp_drv.register()

# Regsiter SDL mouse driver

indev_drv = lv.indev_drv_t()
indev_drv.init()
indev_drv.type = lv.INDEV_TYPE.POINTER
indev_drv.read_cb = SDL.mouse_read
indev = indev_drv.register()


indev_drv1 = lv.indev_drv_t()
indev_drv1.init()
indev_drv1.type = lv.INDEV_TYPE.KEYPAD
indev_drv1.read_cb = SDL.keyboard_read
indev1 = indev_drv1.register()


scr = lv.obj()
lv.scr_load(scr)



col_dsc = [320, lv.GRID_TEMPLATE_LAST]
row_dsc = [40, 160, 40, lv.GRID_TEMPLATE_LAST]

container = lv.obj(lv.scr_act())
container.set_style_grid_column_dsc_array(col_dsc, 0)
container.set_style_grid_row_dsc_array(row_dsc, 0)
container.set_size(320, 240)
container.set_layout(lv.LAYOUT_GRID.value)
container.set_style_pad_all(0, 0)
container.set_scrollbar_mode(lv.SCROLLBAR_MODE.OFF)


tobpar1 = TopBar(container)
tobpar1.set_grid_cell(lv.GRID_ALIGN.STRETCH, 0, 1,
                     lv.GRID_ALIGN.STRETCH, 0, 1)

games1 = Games(container)
games1.set_grid_cell(lv.GRID_ALIGN.STRETCH, 0, 1,
                     lv.GRID_ALIGN.STRETCH, 1, 1)


bottombar1 = BottomBar(container)
bottombar1.set_grid_cell(lv.GRID_ALIGN.STRETCH, 0, 1,
                     lv.GRID_ALIGN.STRETCH, 2, 1)