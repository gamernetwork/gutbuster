#!/bin/bash

# identify alsa devices with
#   aplay -L
# (look for something starting 'plughw')

ALSA_DEVICE="hw:CARD=USB,DEV=0"
# can be fast or slow (varies quality)
SHOT="mixdown"

usage()
{
cat << EOF
usage: $0 options

Preview audio on capture device.

OPTIONS:
   -h       Show this message
   -d       ALSA device name, find using: aplay -L (default 'hw:CARD=USB,DEV=0')
EOF
}

while getopts “hd:” OPTION
do
     case $OPTION in
         h)
             usage
             exit 1
             ;;
         d)
             ALSA_DEVICE=$OPTARG
             ;;
         ?)
             usage
             exit
             ;;
     esac
done

echo "Stop by CTRL-C'ing THIS window, not the waveform thing."

gst-launch-1.0 alsasrc device="$ALSA_DEVICE" \
    ! tee name=t \
    t. ! queue ! audioconvert \
        ! wavescope shader=0 style=color-lines \
        ! video/x-raw,format=BGRx,width=640,height=480,framerate=30000/1001 \
        ! textoverlay font-desc="Sans Bold 24" text="$SHOT" color=0xff90ff00 \
        ! ximagesink \
    t. ! queue ! pulsesink

