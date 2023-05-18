import ffi

libsdl = ffi.open("libSDL2-2.0.so.0")

SDL_ShowCursor = libsdl.func("i", "SDL_ShowCursor", "i")
