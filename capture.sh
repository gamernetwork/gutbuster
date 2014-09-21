#!/bin/bash

DIR=/home/storage/mark
DEVICE=0 # 0-3
CONNECTION=hdmi # or sdi
SHOT="Head-shot"
FILENAME=EGX`date +%Y`_`date +%a_%T`_$SHOT.ts
echo "Capturing device $DEVICE to $FILENAME"
echo "To stop, CTRL-C in THIS WINDOW - do not just close the display"

# mode 8 is 1080p29.97 - to find other modes run:
# gst-inspect-1.0 decklinksrc

gst-launch-1.0 -e \
  decklinksrc mode=8 connection=$CONNECTION device-number=$DEVICE ! \
  videoconvert ! \
  tee name=t \
    ! \
      queue ! \
      videoconvert ! \
      'video/x-raw,format=YV12,framerate=30000/1001,width=1920,height=1080' ! \
      x264enc speed-preset=ultrafast bitrate=8000 ! \
      mpegtsmux ! \
      filesink location=$DIR/$FILENAME \
    t. ! \
      queue ! \
      videoscale ! \
      videoconvert ! \
      video/x-raw, width=320, height=180 ! \
      textoverlay font-desc="Sans Bold 28" text="$DEVICE: $SHOT" ! \
      xvimagesink sync=false 

