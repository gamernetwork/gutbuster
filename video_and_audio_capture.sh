#!/bin/bash

DIR=`pwd`
DEVICE=0
CONNECTION=sdi
SHOT="Mix"
QUALITY=" pass=4 quantizer=23 "
AUDIO_QUALITY=1 # audio quality, 1 is good 10 is bad
MODE=1080p2997

usage()
{
cat << EOF
usage: $0 options

Capture video from decklink device to 'fragmented' mp4 file, encoded h264 (ultrafast).
Now with preview!

OPTIONS:
   -h       Show this message
   -d       Device ID to capture (0-3 on a 4 card machine, default=0)
   -c       Connection type: 'hdmi' or 'sdi' (default sdi)
   -f       Filename stem
   -n       Name of this shot (default 'Unnamed')
   -l       Folder to save vids into (default pwd)
   -q       Use constant quantizer targeted encoding (default), using this factor (0=lossless, 23=default, 63=max)
   -b       Use bitrate targeted encoding, using this bitrate in Kbit/s (12000 = 12Mbit)
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

FILENAME_STEM=EGX_mix_`date +%Y`_`date +%a_%T`

while getopts “hl:d:m:f:c:q:n:b:” OPTION
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
         q)
             QP=$OPTARG
             QUALITY=" pass=4 quantizer=$QP "
             ;;
         b)
             BITRATE=$OPTARG
             QUALITY=" pass=17 bitrate=$BITRATE "
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

# mode 8 is 1080p29.97 - to find other modes run:
# gst-inspect-1.0 decklinksrc

gst-launch-1.0 \
  decklinkvideosrc mode=$MODE connection=$CONNECTION device-number=$DEVICE do-timestamp=true \
  ! videoconvert \
  ! tee name=t \
  t. \
    ! x264enc speed-preset=ultrafast $QUALITY \
    ! queue \
    ! mux. \
  t. \
    ! videoscale \
    ! video/x-raw, width=320, height=180 \
    ! textoverlay font-desc="Sans Bold 18" text="$DEVICE: $SHOT Video" color=0xff90ff00 \
    ! queue \
    ! xvimagesink sync=false \
  decklinkaudiosrc connection=embedded device-number=$DEVICE do-timestamp=true \
    ! tee name=at \
    at. ! queue \
      ! audioconvert \
      ! lamemp3enc quality=$AUDIO_QUALITY target=quality encoding-engine-quality=standard \
      ! queue \
      ! mux. \
    at. ! queue \
      ! wavescope shader=0 style=color-lines \
      ! video/x-raw,format=BGRx,width=160,height=90,framerate=30000/1001 \
      ! textoverlay font-desc="Sans Bold 18" text="$DEVICE: $SHOT Audio" color=0xff90ff00 \
      ! videoconvert \
      ! xvimagesink sync=false \
  mp4mux name=mux fragment-duration=1000 \
    ! filesink location=$DIR/$FILENAME


