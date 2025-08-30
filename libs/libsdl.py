import ffi
import time
import uctypes

libsdl = ffi.open("libSDL2-2.0.so.0")

SDL_ShowCursor = libsdl.func("i", "SDL_ShowCursor", "i")
SDL_GL_SetAttribute = libsdl.func("i", "SDL_GL_SetAttribute", "ii")
SDL_SetRenderDrawColor = libsdl.func("i", "SDL_SetRenderDrawColor", "PBBBB")
SDL_RenderClear        = libsdl.func("v", "SDL_RenderClear", "P")
SDL_PollEvent        = libsdl.func("i", "SDL_PollEvent", "P")
SDL_GetKeyboardState = libsdl.func("p", "SDL_GetKeyboardState", "P")


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

# Scancodes
SDL_SCANCODE_A      = 4
SDL_SCANCODE_D      = 7
SDL_SCANCODE_S      = 22
SDL_SCANCODE_W      = 26
SDL_SCANCODE_ESCAPE = 41


# SDL2 Scancodes Mapping
# Quelle: SDL_scancode.h
# Achtung: Dies ist nur ein Mapping Dictionary, keine echte SDL-Bindung.

SCANCODES = {
    "UNKNOWN": 0,
    "A": 4,
    "B": 5,
    "C": 6,
    "D": 7,
    "E": 8,
    "F": 9,
    "G": 10,
    "H": 11,
    "I": 12,
    "J": 13,
    "K": 14,
    "L": 15,
    "M": 16,
    "N": 17,
    "O": 18,
    "P": 19,
    "Q": 20,
    "R": 21,
    "S": 22,
    "T": 23,
    "U": 24,
    "V": 25,
    "W": 26,
    "X": 27,
    "Y": 28,
    "Z": 29,
    "1": 30,
    "2": 31,
    "3": 32,
    "4": 33,
    "5": 34,
    "6": 35,
    "7": 36,
    "8": 37,
    "9": 38,
    "0": 39,
    "RETURN": 40,
    "ESCAPE": 41,
    "BACKSPACE": 42,
    "TAB": 43,
    "SPACE": 44,
    "MINUS": 45,
    "EQUALS": 46,
    "LEFTBRACKET": 47,
    "RIGHTBRACKET": 48,
    "BACKSLASH": 49,
    "NONUSHASH": 50,
    "SEMICOLON": 51,
    "APOSTROPHE": 52,
    "GRAVE": 53,
    "COMMA": 54,
    "PERIOD": 55,
    "SLASH": 56,
    "CAPSLOCK": 57,
    "F1": 58,
    "F2": 59,
    "F3": 60,
    "F4": 61,
    "F5": 62,
    "F6": 63,
    "F7": 64,
    "F8": 65,
    "F9": 66,
    "F10": 67,
    "F11": 68,
    "F12": 69,
    "PRINTSCREEN": 70,
    "SCROLLLOCK": 71,
    "PAUSE": 72,
    "INSERT": 73,
    "HOME": 74,
    "PAGEUP": 75,
    "DELETE": 76,
    "END": 77,
    "PAGEDOWN": 78,
    "RIGHT": 79,
    "LEFT": 80,
    "DOWN": 81,
    "UP": 82,
    "NUMLOCKCLEAR": 83,
    "KP_DIVIDE": 84,
    "KP_MULTIPLY": 85,
    "KP_MINUS": 86,
    "KP_PLUS": 87,
    "KP_ENTER": 88,
    "KP_1": 89,
    "KP_2": 90,
    "KP_3": 91,
    "KP_4": 92,
    "KP_5": 93,
    "KP_6": 94,
    "KP_7": 95,
    "KP_8": 96,
    "KP_9": 97,
    "KP_0": 98,
    "KP_PERIOD": 99,
    "NONUSBACKSLASH": 100,
    "APPLICATION": 101,
    "POWER": 102,
    "KP_EQUALS": 103,
    "F13": 104,
    "F14": 105,
    "F15": 106,
    "F16": 107,
    "F17": 108,
    "F18": 109,
    "F19": 110,
    "F20": 111,
    "F21": 112,
    "F22": 113,
    "F23": 114,
    "F24": 115,
    "EXECUTE": 116,
    "HELP": 117,
    "MENU": 118,
    "SELECT": 119,
    "STOP": 120,
    "AGAIN": 121,
    "UNDO": 122,
    "CUT": 123,
    "COPY": 124,
    "PASTE": 125,
    "FIND": 126,
    "MUTE": 127,
    "VOLUMEUP": 128,
    "VOLUMEDOWN": 129,
}

NAMES = {v: k for k, v in SCANCODES.items()}

SDL_QUIT     = 0x100
SDL_KEYDOWN  = 0x300
SDL_KEYUP    = 0x301


globalKeyCallbacks = {}

def addGlobalKeyCallback(cb, type):
    globalKeyCallbacks[type] = cb

def handleGlobalKeys(type):
    if type in globalKeyCallbacks:
        globalKeyCallbacks[type]()

keystates = {
    "F1": {
        "scancode": SCANCODES["F1"],
        "pressed": 0,
        "pressingHistory": [0, 0]
    },
    "F2": {
        "scancode": SCANCODES["F2"],
        "pressed": 0,
        "pressingHistory": [0, 0]
    },
    "F3": {
        "scancode": SCANCODES["F3"],
        "pressed": 0,
        "pressingHistory": [0, 0]
    },
    "F4": {
        "scancode": SCANCODES["F4"],
        "pressed": 0,
        "pressingHistory": [0, 0]
    },
    "F5": {
        "scancode": SCANCODES["F5"],
        "pressed": 0,
        "pressingHistory": [0, 0]
    },
}

def keyboard_loop():
    # Event-Puffer
    EVENT_SIZE = 56
    evbuf = bytearray(EVENT_SIZE)
    # int numkeys
    numkeys_buf = bytearray(uctypes.sizeof({"v": uctypes.INT32}))
    numkeys = uctypes.struct(uctypes.addressof(numkeys_buf), {"v": uctypes.INT32})
    # Get Pointer
    keystate_ptr = SDL_GetKeyboardState(uctypes.addressof(numkeys_buf))
    # Bytearray cast
    keystate = uctypes.bytearray_at(keystate_ptr, numkeys.v)

    # Events
    while SDL_PollEvent(evbuf):
        pass

    # parallel pressed keys
    pressed = []
    for key in keystates:
        state = keystate[keystates[key]["scancode"]]
        keystate[keystates[key]["pressed"]] = state
        keystates[key]["pressingHistory"].append(state)
        keystates[key]["pressingHistory"] = keystates[key]["pressingHistory"][-2:]
        if state == 1:
            pressed.append(key)

    if pressed:
        combination = "+".join(pressed)
        if combination.find("F1") != -1:
            if combination.find("F2") != -1:
                if keystates["F2"]["pressingHistory"] == [0, 1]:
                    handleGlobalKeys("louder")
            elif combination.find("F3") != -1:
                if keystates["F3"]["pressingHistory"] == [0, 1]:
                    handleGlobalKeys("quieter")
            elif combination.find("F4") != -1:
                if keystates["F4"]["pressingHistory"] == [0, 1]:
                    handleGlobalKeys("lighter")
            elif combination.find("F5") != -1:
                if keystates["F5"]["pressingHistory"] == [0, 1]:
                    handleGlobalKeys("darker")
