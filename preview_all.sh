#!/bin/bash

DIR=`pwd`
DEVICES="0 1 2 3" # 0 -> (devices - 1)
CONNECTION=sdi # or hdmi
MODE=1080p2997
ALSA_DEVICE="hw:CARD=USB"
SHOTHEIGHT=180
SHOTWIDTH=320

usage()
{
cat << EOF
usage: $0 options device [device ...]

Preview all inputs and audio

OPTIONS:
   -h       Show this message
   -d       ALSA device to preview audio, find using: aplay -L (default 'hw:CARD=USB,DEV=0')
   -c       Connection type: 'hdmi' or 'sdi' (default sdi)
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

while getopts “hd:m:c:” OPTION
do
     case $OPTION in
         h)
             usage
             exit 1
             ;;
         d)
             ALSA_DEVICE=$OPTARG
             ;;
         c)
             CONNECTION=$OPTARG
             ;;
         m)
             MODE=$OPTARG
             ;;
         ?)
             usage
             exit
             ;;
     esac
done

DEVICES=${@:$OPTIND}

mixercmd=""
gstcmd=""
dc=0
for device in $DEVICES;
  do
    gstcmd="$gstcmd \
  decklinkvideosrc mode=$MODE connection=$CONNECTION device-number=$device \
    ! videoconvert \
    ! videoscale \
    ! video/x-raw, width=$SHOTWIDTH, height=$SHOTHEIGHT \
    ! textoverlay font-desc=\"Sans Bold 24\" text=\"$device\" color=0xff90ff00 \
    ! queue \
    ! mix.sink_$dc \
"
    mixy=`echo "scale=0;$dc/2*$SHOTHEIGHT" | bc`
    mixx=`echo "($dc%2)*$SHOTWIDTH" | bc`
    mixercmd="$mixercmd \
      sink_$dc::xpos=$mixx sink_$dc::ypos=$mixy sink_0::alpha=1 sink_0::zorder=1 \
"
    let dc+=1
  done

gstcmd="gst-launch-1.0 \
  $gstcmd \
  videomixer name=mix \
    $mixercmd \
    ! xvimagesink sync=false
"

# run it!
$gstcmd

