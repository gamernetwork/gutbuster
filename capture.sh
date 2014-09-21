#!/bin/bash

DIR=`pwd`
DEVICE=0 # 0-3
CONNECTION=sdi # or hdmi
SHOT="Unnamed"
BITRATE=8000
FILENAME=EGX`date +%Y`_`date +%a_%T`_$SHOT.ts

usage()
{
cat << EOF
usage: $0 options

Capture video from decklink device to mpegts file, encoded h264 (ultrafast).
Now with preview!

OPTIONS:
   -h      Show this message
   -d      Device ID to capture (0-3 on a 4 card machine, default=0)
   -c      Connection type: 'hdmi' or 'sdi' (default sdi)
   -n      Name of this shot (default 'Unnamed')
   -l      Folder to save vids into (default pwd)
   -b      Bitrate in Kbit/s (default 8000 = 8Mbit)
EOF
}

while getopts “hl:d:c:n:b:” OPTION
do
     case $OPTION in
         h)
             usage
             exit 1
             ;;
         d)
             DEVICE=$OPTARG
             ;;
         l)
             DIR=$OPTARG
             ;;
         c)
             CONNECTION=$OPTARG
             ;;
         n)
             SHOT=$OPTARG
             ;;
         b)
             BITRATE=$OPTARG
             ;;
         ?)
             usage
             exit
             ;;
     esac
done

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
      textoverlay font-desc="Sans Bold 24" text="$DEVICE: $SHOT" color=0xff90ff00 ! \
      xvimagesink sync=false 

# note color is big endian, so 0xaaRRGGBB