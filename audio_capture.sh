#!/bin/bash

# identify alsa devices with
#   aplay -L
# (look for something starting 'plughw')

ALSA_DEVICE="hw:CARD=USB,DEV=0"
DIR=`pwd`
# can be fast or slow (varies quality)
SPEED=standard
QUALITY=1 # is best - 10 is worst
SHOT="mixdown"

usage()
{
cat << EOF
usage: $0 options

Capture video from decklink device to mpegts file, encoded h264 (ultrafast).
Now with preview!

OPTIONS:
   -h       Show this message
   -d       ALSA device name, find using: aplay -L (default 'hw:CARD=USB,DEV=0')
   -l       Folder to save mp3s into (default pwd)
   -q       MP3 quality, 0 (best) -> 9 (worst) (default 1)
EOF
}

while getopts “hd:l:q:” OPTION
do
     case $OPTION in
         h)
             usage
             exit 1
             ;;
         d)
             ALSA_DEVICE=$OPTARG
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

gst-launch-1.0 alsasrc device="$ALSA_DEVICE" \
    ! tee name=t \
    t. ! queue ! audioconvert \
        ! wavescope shader=0 style=color-lines \
        ! video/x-raw,format=BGRx,width=640,height=480,framerate=30000/1001 \
        ! textoverlay font-desc="Sans Bold 24" text="$SHOT" color=0xff90ff00 \
        ! ximagesink \
    t. ! queue ! audioconvert \
        ! lamemp3enc quality=$QUALITY target=quality encoding-engine-quality=$SPEED perfect-timestamp=true ! id3v2mux ! filesink location=$FILENAME \
    t. ! queue ! pulsesink

