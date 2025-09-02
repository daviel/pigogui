import lvgl as lv


GENERIC_PAGE_STYLE = lv.style_t()
col_dsc = [320, lv.GRID_TEMPLATE_LAST]
row_dsc = [240, lv.GRID_TEMPLATE_LAST]
GENERIC_PAGE_STYLE.set_grid_column_dsc_array(col_dsc)
GENERIC_PAGE_STYLE.set_grid_row_dsc_array(row_dsc)
GENERIC_PAGE_STYLE.set_layout(lv.LAYOUT.GRID)
GENERIC_PAGE_STYLE.set_pad_all(0)
GENERIC_PAGE_STYLE.set_pad_row(0)
GENERIC_PAGE_STYLE.set_border_width(0)


SETUP_PAGE_STYLE = lv.style_t()
col_dsc = [320, lv.GRID_TEMPLATE_LAST]
row_dsc = [240, lv.GRID_TEMPLATE_LAST]