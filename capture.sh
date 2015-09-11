#!/bin/bash

DIR=`pwd`
DEVICE=0 # 0 ->  (devices - 1)
CONNECTION=sdi # or hdmi
SHOT="Unnamed"
BITRATE=12000
MODE=1080p2997

usage()
{
cat << EOF
usage: $0 options

Capture video from decklink device to mpegts file, encoded h264 (ultrafast).
Now with preview!

OPTIONS:
   -h       Show this message
   -d       Zero indexed device ID to capture (e.g. 0-3 on a 4 card machine, default=0)
   -c       Connection type: 'hdmi' or 'sdi' (default sdi)
   -n       Name of this shot (default 'Unnamed')
   -l       Folder to save vids into (default pwd)
   -b       Bitrate in Kbit/s (default 8000 = 8Mbit)
   -m       Mode (mode # or shotcode should work)
                Mode #  Name             Shortcode
                ------  ---------------  ----------
                0       Auto (dodgy)     auto
                6       HD1080 23.98p    1080p2398
                7       HD1080 24p       1080p24
                8       HD1080 25p       1080p25
                9       HD1080 29.97p    1080p2997
                10      HD1080 30p       1080p30
                11      HD1080 50i       1080i50
                12      HD1080 59.94i    1080i5994
                13      HD1080 60i       1080i60
                14      HD1080 50p       1080p50
                15      HD1080 59.94p    1080p5994
                16      HD1080 60p       1080p60
                17      HD720 50p        720p50
                18      HD720 59.94p     720p5994
                19      HD720 60p        720p60
		
		See 'gst-inspect-1.0 decklinkvideosrc' for more modes
EOF
}

while getopts “hl:d:m:c:n:b:” OPTION
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
         ?)
             usage
             exit
             ;;
     esac
done

FILENAME=EGX`date +%Y`_`date +%a_%T`_$SHOT.ts

echo "Capturing device $DEVICE to $FILENAME"
echo "To stop, CTRL-C in THIS WINDOW - do not just close the display"

gst-launch-1.0 \
  decklinkvideosrc mode=$MODE connection=$CONNECTION device-number=$DEVICE \
  ! videoconvert \
  ! tee name=t \
    t. \
      ! videoscale method=nearest-neighbour \
      ! video/x-raw, width=320, height=180 \
      ! textoverlay font-desc="Sans Bold 24" text="$DEVICE: $SHOT" color=0xff90ff00 \
      ! queue \
      ! xvimagesink sync=false \
    t. \
      ! videoscale \
      ! queue \
      ! x264enc speed-preset=ultrafast bitrate=$BITRATE \
      ! mpegtsmux \
      ! filesink location=$DIR/$FILENAME

# note text color is big endian, so 0xaaRRGGBB
