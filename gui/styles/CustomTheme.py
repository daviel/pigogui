import lvgl as lv

class CustomTheme(lv.theme_t):
    def __init__(self, primary_color, secondary_color, darkorlight):
        super().__init__()

        # button
        self.style_btn = lv.style_t()
        self.style_btn.init()
        self.style_btn.set_bg_color(lv.palette_main(primary_color))
        self.style_btn.set_border_color(lv.palette_darken(primary_color, 3))
        self.style_btn.set_border_width(3)
        self.style_btn.set_text_color(lv.palette_darken(secondary_color, 3))

        # containers (obj)
        self.style_obj = lv.style_t()
        self.style_obj.init()
        self.style_obj.set_bg_color(lv.palette_main(primary_color))
        self.style_obj.set_border_color(lv.palette_darken(primary_color, 3))
        self.style_obj.set_border_width(3)

        # dropdown
        self.style_dd = lv.style_t()
        self.style_dd.init()
        self.style_dd.set_bg_color(lv.palette_main(primary_color))
        self.style_dd.set_border_color(lv.palette_darken(primary_color, 3))
        self.style_dd.set_border_width(3)

        th_act = lv.theme_get_from_obj(lv.scr_act())
        self.set_parent(th_act)
