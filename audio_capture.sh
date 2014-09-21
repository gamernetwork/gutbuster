#!/bin/bash

# identify alsa devices with
#   aplay -L
# (look for something starting 'plughw')
ALSA_DEVICE="plughw:CARD=CODEC,DEV=0"

DIR=`pwd`
FILENAME=$DIR/EGX`date +%Y`_`date +%a_%T`_audio_mixdown.mp3

# can be fast or slow (varies quality)
SPEED=standard

QUALITY=1 # is best - 10 is worst

echo "Capturing audio to $FILENAME"
echo "Stop by CTRL-C'ing THIS window, not the waveform thing."

gst-launch-1.0 -ve alsasrc device="plughw:CARD=CODEC,DEV=0" ! tee name=t t. ! queue ! audioconvert ! volume volume=4 ! wavescope shader=0 style=2 ! video/x-raw,format=BGRx,width=320,height=180,framerate=30000/1001 ! ximagesink t. ! queue ! audioconvert ! lamemp3enc quality=$QUALITY target=0 encoding-engine-quality=standard perfect-timestamp=true ! id3v2mux ! filesink location=$FILENAME t. ! queue ! pulsesink

