#!/bin/bash

# identify alsa devices with
#   aplay -L
# (look for something starting 'plughw')

ALSA_DEVICE="hw:CARD=USB"
DIR=`pwd`
# can be fast or slow (varies quality)
SPEED=standard
QUALITY=1 # is best - 10 is worst
SHOT="mixdown"
DEBUG=""

usage()
{
cat << EOF
usage: $0 options

Capture video from decklink device to mpegts file, encoded h264 (ultrafast).
Now with preview!

OPTIONS:
   -h       Show this message
   -v       Debug on
   -d       ALSA device name, find using: aplay -L (default 'hw:CARD=USB,DEV=0')
   -l       Folder to save mp3s into (default pwd)
   -q       MP3 quality, 0 (best) -> 9 (worst) (default 1)
EOF
}

while getopts “hvd:l:q:” OPTION
do
     case $OPTION in
         h)
             usage
             exit 1
             ;;
         d)
             ALSA_DEVICE=$OPTARG
             ;;
         v)
             GST_DEBUG=1
             ;;
         l)
             DIR=$OPTARG
             ;;
         q)
             QUALITY=$OPTARG
             ;;
         ?)
             usage
             exit
             ;;
     esac
done

FILENAME=$DIR/EGX`date +%Y`_`date +%a_%T`_$SHOT.mp3

echo "Capturing audio to $FILENAME"
echo "Stop by CTRL-C'ing THIS window, not the waveform thing."

# using ximagesink (not xVimagesink, i.e. no 'v') to avoid colorspace conversion
# and just suggesting which caps to use so it's all RGB and low framerate

gst-launch-1.0 alsasrc device="$ALSA_DEVICE" do-timestamp=true \
    ! tee name=t \
    t. ! queue ! audioconvert \
        ! wavescope shader=0 style=color-lines \
        ! video/x-raw,format=BGRx,width=640,height=480,framerate=30/1 \
        ! textoverlay font-desc="Sans Bold 24" text="$SHOT" color=0xff90ff00 \
        ! ximagesink \
    t. ! queue ! audioconvert \
        ! lamemp3enc quality=$QUALITY target=quality encoding-engine-quality=$SPEED ! id3v2mux ! filesink location=$FILENAME \
    t. ! queue ! pulsesink

