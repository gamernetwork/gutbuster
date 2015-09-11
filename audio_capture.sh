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

gst-launch-1.0 alsasrc device="hw:CARD=USB,DEV=0" \
    ! tee name=t \
    t. ! queue ! audioconvert \
        ! wavescope shader=0 style=color-lines ! video/x-raw,format=BGRx,width=640,height=480,framerate=30 \
        ! videoscale ! ximagesink \
    t. ! queue ! audioconvert \
        ! lamemp3enc quality=$QUALITY target=quality encoding-engine-quality=standard perfect-timestamp=true ! id3v2mux ! filesink location=$FILENAME \
    t. ! queue ! pulsesink

        # ! volume volume=4 \
