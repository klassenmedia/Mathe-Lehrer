#!/bin/sh
# Setzt die Szenen-Clips und die Sprachspur zum fertigen Video zusammen.
set -e
cd "$(dirname "$0")/build"
ls clips/*.mp4 | sort | sed "s|^|file '|; s|\$|'|" > clips.txt
ffmpeg -y -loglevel error -f concat -safe 0 -i clips.txt -i audio_all.wav \
  -c:v copy -c:a aac -b:a 128k -shortest -movflags +faststart "$1"
