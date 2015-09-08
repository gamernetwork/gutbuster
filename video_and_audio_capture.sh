#!/bin/bash

DIR=`pwd`
DEVICE=0 # 0-3
CONNECTION=sdi # or hdmi
SHOT="Unnamed"
BITRATE=8000
MODE=8

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
   -f      Filename stem
   -n      Name of this shot (default 'Unnamed')
   -l      Folder to save vids into (default pwd)
   -m      Mode
   -b      Bitrate in Kbit/s (default 8000 = 8Mbit)
EOF
}

FILENAME_STEM=EGX_mix_`date +%Y`_`date +%a_%T`

while getopts “hl:d:m:f:c:n:b:” OPTION
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
         m)
             MODE=$OPTARG
             ;;
         b)
             BITRATE=$OPTARG
             ;;
         f)
             FILENAME_STEM=$OPTARG
             ;;
         ?)
             usage
             exit
             ;;
     esac
done

FILENAME=${FILENAME_STEM}_${SHOT}.mp4

echo "Capturing device $DEVICE to $FILENAME"
echo "To stop, CTRL-C in THIS WINDOW - do not just close the display"

# mode 8 is 1080p29.97 - to find other modes run:
# gst-inspect-1.0 decklinksrc

gst-launch-1.0 -vvvv \
  decklinkvideosrc mode=$MODE connection=$CONNECTION device-number=$DEVICE \
  ! videoconvert \
  ! tee name=t \
  t. \
    ! x264enc speed-preset=ultrafast bitrate=8000 \
    ! queue \
    ! mux. \
  t. \
    ! videoscale \
    ! video/x-raw, width=320, height=180 \
    ! textoverlay font-desc="Sans Bold 24" text="$DEVICE: $SHOT" color=0xff90ff00 \
    ! queue \
    ! xvimagesink sync=false \
  decklinkaudiosrc connection=embedded device-number=$DEVICE \
    ! audioconvert \
    ! lamemp3enc \
    ! queue \
    ! mux. \
  mp4mux name=mux fragment-duration=1000 \
    ! filesink location=$DIR/$FILENAME


    #! queue \
    #! streamable=true

#  tee name=t \
#    t. ! \
#      videoscale ! \
#      video/x-raw, width=320, height=180 ! \
#      textoverlay font-desc="Sans Bold 24" text="$DEVICE: $SHOT" color=0xff90ff00 ! \
#      queue ! \
#      xvimagesink sync=false \
#    t. ! \
      #'video/x-raw,format=YV12,framerate=30000/1001,width=1920,height=1080' ! \
# note color is big endian, so 0xaaRRGGBB
