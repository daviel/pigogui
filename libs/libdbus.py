import ffi
import uctypes

libdbus = None
try:
    libdbus = ffi.open("libdbus-1.so")
except:
    print("libwpa could not be found")


if libdbus:
    dbus_bus_get = libdbus.func("i", "dbus_bus_get", "pp")
