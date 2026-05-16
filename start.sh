#!/bin/bash
PIGO_PATH="$(dirname -- "${BASH_SOURCE[0]}")"
cd $PIGO_PATH
SDL_VIDEODRIVER=wayland SDL_APP_ID=pigogui micropython -X heapsize=4M $PIGO_PATH/main.py
