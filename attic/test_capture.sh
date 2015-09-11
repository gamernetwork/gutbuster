#!/bin/bash

DIR=`pwd`
SHOT="Test-encode"
FILENAME=EGX`date +%Y`_`date +%a_%T`_$SHOT.ts
echo "Capturing device $DEVICE to $FILENAME"
echo "To stop, CTRL-C in THIS WINDOW - do not just close the display"

# mode 8 is 1080p29.97 - to find other modes run:
# gst-inspect-1.0 decklinksrc

gst-launch-1.0 -e \
  videotestsrc is-live=true ! \
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
      textoverlay font-desc="Sans Bold 24" text="$DEVICE: $SHOT" color=0xffffff00 ! \
      xvimagesink sync=false 

# note color is big endian, so 0xaaRRGGBB
