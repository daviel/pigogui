#!/bin/bash
PIGO_PATH="$(dirname -- "${BASH_SOURCE[0]}")"
cd $PIGO_PATH
SDL_RPI_VIDEO_LAYER=999999 micropython -X heapsize=4M -i $PIGO_PATH/main.py
