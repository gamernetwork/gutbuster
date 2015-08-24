# Notes

## To get a GStreamer version of the capture

Preview:

```
gst-launch -e \
	decklinksrc mode=11 connection=hdmi subdevice=0 \
	! video/x-raw-yuv \
	! ffmpegcolorspace \
	! deinterlace \
	! xvimagesink sync=false
```

To encode the video to x264 in realtime:

```
gst-launch -e \
	decklinksrc mode=11 connection=hdmi \
	! queue \
	! autoconvert \
	! video/x-raw-yuv,framerate=30000/1001 \
	! x264enc tune=zerolatency speed-preset=ultrafast bitrate=8000 \
	! mpegtsmux \
	! filesink location=/tmp/vidtest/test.ts
```

To tee it into capture and preview:

```
gst-launch -e \
	decklinksrc mode=11 connection=hdmi ! \
	autoconvert ! \
	video/x-raw-yuv,framerate=30000/1001,width=1920,height=1080 ! \
	tee name=t \
		t. ! queue ! \
			x264enc tune=zerolatency speed-preset=ultrafast bitrate=8000 ! \
			mpegtsmux ! filesink location=/home/storage/mark/test.ts \
		t. ! queue ! \
			videoscale ! video/x-raw-yuv,framerate=30000/1001,width=320,height=180 ! \
			xvimagesink sync=false
```

This uses about 180% CPU on my tri-core phenom, which is about 1/6 as powerful as an i7.

Add a label and make sure frames are padded out when dropped:

```
gst-launch -e \
	decklinksrc mode=8 connection=hdmi subdevice=0 ! \
  video/x-raw-yuv,framerate=30000/1001,width=1920,height=1080 ! \
	ffmpegcolorspace ! \
  videorate drop-only=true ! \
	tee name=t \
		t. ! queue ! \
			x264enc tune=zerolatency speed-preset=ultrafast bitrate=8000 ! \
			mpegtsmux ! filesink location=/home/storage/mark/test.ts \
		t. ! queue ! \
			videoscale ! video/x-raw-yuv,framerate=30000/1001,width=320,height=180 ! \
			textoverlay font-desc="Sans Bold 28" text="Head shot" ! \
			xvimagesink sync=false
```

Notes:

  - mode 8 is 1080p29.97 or rather 1080p30000/1001 with square pixels
	- decklink src is UYVY which is a 'packed' format
	- x264enc operates in YV12 which is a 'planar' format 

```
gst-launch-1.0 -e \
	decklinksrc mode=8 connection=hdmi device-number=0 \
	! video/x-raw,format=UYVY,framerate=30000/1001,width=1920,height=1080,interlaced=false \
	! videoconvert \
	! videorate drop-only=true \
	! tee name=t t. \
		! queue \
		! videoconvert \
		! video/x-raw,format=YV12,framerate=30000/1001,width=1920,height=1080,profile=high-4:2:2 \
		! x264enc tune=zerolatency speed-preset=ultrafast bitrate=8000 \
		! mpegtsmux \
		! filesink location=/home/storage/mark/test.ts \
	t. \
		! queue \
		! videoconvert \
		! videoscale \
		! video/x-raw,format=UYVY,framerate=30000/1001,width=320,height=180 \
		! textoverlay font-desc="Sans Bold 28" text="Head shot" \
		! xvimagesink sync=false
```

```
gst-launch -e \
	decklinksrc mode=8 connection=hdmi subdevice=0 \
	! video/x-raw-yuv,framerate=30000/1001,width=1920,height=1080,interlaced=false \
	! ffmpegcolorspace \
	! videorate drop-only=true \
	! tee name=t t. \
		! queue \
		! x264enc tune=zerolatency speed-preset=ultrafast bitrate=8000 \
		! mpegtsmux \
		! filesink location=/home/storage/mark/test.ts \
	t. \
		! queue \
		! videoscale \
		! video/x-raw-yuv,framerate=30000/1001,width=320,height=180 \
		! textoverlay font-desc="Sans Bold 28" text="Head shot" \
		! xvimagesink sync=false
```

## Gstreamer 1.0 versions

Using Gstreamer-1.0 opens up possibility of using x264enc with 4:2:2 sampling (rather than 4:2:0).  Camera provides this so may as well keep it!

### 4:2:0

```
gst-launch-1.0 -e \
	decklinksrc mode=8 connection=hdmi device-number=0 \
	! videoconvert \
	! 'video/x-raw,format=YV12,framerate=30000/1001,width=1920,height=1080' \
	! x264enc speed-preset=ultrafast bitrate=8000 \
	! mpegtsmux \
	! filesink location=/home/storage/mark/test.ts
```

### 4:2:2 (uses slightly more CPU due to splitting packed channels to planar)

```
gst-launch-1.0 -e \
	decklinksrc mode=8 connection=hdmi device-number=0 ! \
	videoconvert ! \
	tee name=t \
		! \
			queue ! \
			videoconvert ! \
			'video/x-raw,format=Y42B,framerate=30000/1001,width=1920,height=1080' ! \
			x264enc speed-preset=ultrafast bitrate=8000 ! \
			mpegtsmux ! \
			filesink location=/home/storage/mark/test.ts \
		t. ! \
			queue ! \
			videoscale ! \
			videoconvert ! \
			video/x-raw, width=320, height=180 ! \
			textoverlay font-desc="Sans Bold 28" text="Head shot" ! \
			xvimagesink sync=false \
```

## Putting it all together

```
gst-launch-1.0 -e \
	decklinksrc mode=8 connection=hdmi device-number=0 \
	! videoconvert \
	! 'video/x-raw,format=Y42B,framerate=30000/1001,width=1920,height=1080' \
	! x264enc speed-preset=ultrafast bitrate=8000 \
	! mpegtsmux \
	! filesink location=/home/storage/mark/test.ts
```

## Sources

### IP streaming stuff:

http://stackoverflow.com/questions/19107301/gstreamer-pipeline-for-decklinksrc-video-capture-card-with-udpsrc-and-udpsink-us

### GST encoding:

http://wiki.oz9aec.net/index.php/Gstreamer_cheat_sheet#Encoding_and_Muxing

### Python GST:

http://www.jonobacon.org/2006/08/28/getting-started-with-gstreamer-with-python/

### Debugging:

http://docs.gstreamer.com/display/GstSDK/Basic+tutorial+11%3A+Debugging+tools

### Porting to gst1

https://wiki.ubuntu.com/Novacut/GStreamer1.0

### THIS PPA

https://launchpad.net/~ricotz/+archive/ubuntu/experimental

### Decklink GST patch (should be in 1.3.2+ anyway)

https://bugzilla.gnome.org/show_bug.cgi?id=727306

### Some streaming notes:

https://github.com/matthiasbock/gstreamer-phone/wiki/Streaming-H.264-via-RTP

### Caps syntax:

http://stackoverflow.com/questions/2380575/what-is-the-gstreamer-caps-syntax

### Lossless x264:

 - https://bugzilla.gnome.org/show_bug.cgi?id=725051
 - http://stackoverflow.com/questions/6701805/h264-lossless-coding
 - https://trac.ffmpeg.org/wiki/Encode/H.264#LosslessH.264

### Something about tees:

http://gstreamer-devel.966125.n4.nabble.com/Problem-with-multiple-tees-in-pipeline-td4667937.html
