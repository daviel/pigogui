import ffi

libsdl = ffi.open("libSDL2-2.0.so.0")

SDL_ShowCursor = libsdl.func("i", "SDL_ShowCursor", "i")
SDL_GL_SetAttribute = libsdl.func("i", "SDL_GL_SetAttribute", "ii")
SDL_SetRenderDrawColor = libsdl.func("i", "SDL_SetRenderDrawColor", "PBBBB")
SDL_RenderClear        = libsdl.func("v", "SDL_RenderClear", "P")



SDL_GL_RED_SIZE              = 0
SDL_GL_GREEN_SIZE            = 1
SDL_GL_BLUE_SIZE             = 2
SDL_GL_ALPHA_SIZE            = 3
SDL_GL_DOUBLEBUFFER          = 5
SDL_GL_DEPTH_SIZE            = 6
SDL_GL_STENCIL_SIZE          = 7
SDL_GL_MULTISAMPLEBUFFERS    = 13
SDL_GL_MULTISAMPLESAMPLES    = 14
SDL_GL_CONTEXT_MAJOR_VERSION = 17
SDL_GL_CONTEXT_MINOR_VERSION = 18
SDL_GL_CONTEXT_PROFILE_MASK  = 21


SDL_GL_SetAttribute(SDL_GL_RED_SIZE, 8)
SDL_GL_SetAttribute(SDL_GL_GREEN_SIZE, 8)
SDL_GL_SetAttribute(SDL_GL_BLUE_SIZE, 8)
SDL_GL_SetAttribute(SDL_GL_ALPHA_SIZE, 8)
