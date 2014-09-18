UDP streaming decklink stuff




To get a GStreamer version of the capture
=========================================

Preview:

'''
gst-launch decklinksrc mode=11 connection=hdmi subdevice=0 ! video/x-raw-yuv ! ffmpegcolorspace ! deinterlace ! xvimagesink sync=false
'''

To encode the video to x264 in realtime:

'''
gst-launch decklinksrc mode=11 connection=hdmi ! queue ! autoconvert ! video/x-raw-yuv,framerate=30000/1001 ! x264enc tune=zerolatency speed-preset=ultrafast bitrate=8000 interlaced=true ! mpegtsmux ! filesink location=/tmp/vidtest/test.ts
'''

To tee it into capture and preview:

'''
gst-launch \
	decklinksrc mode=11 connection=hdmi ! autoconvert ! video/x-raw-yuv,framerate=30000/1001,width=1920,height=1080 ! \
	tee name=t \
		t. ! queue ! \
			x264enc tune=zerolatency speed-preset=ultrafast bitrate=8000 ! \
			mpegtsmux ! filesink location=/home/storage/mark/test.ts \
		t. ! queue ! \
			videoscale ! video/x-raw-yuv,framerate=30000/1001,width=320,height=180 ! \
			xvimagesink sync=false
'''

This uses about 180% CPU on my tri-core phenom, which is about 1/6 as powerful as an i7.

Sources
=======

IP streaming stuff:

http://stackoverflow.com/questions/19107301/gstreamer-pipeline-for-decklinksrc-video-capture-card-with-udpsrc-and-udpsink-us

GST encoding:

http://wiki.oz9aec.net/index.php/Gstreamer_cheat_sheet#Encoding_and_Muxing
