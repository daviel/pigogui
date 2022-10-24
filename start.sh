#!/bin/bash
SDL_RPI_VIDEO_LAYER=999999 micropython -X heapsize=4M -i ./main.py
