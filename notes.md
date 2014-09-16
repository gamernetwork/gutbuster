UDP streaming decklink stuff




To get a GStreamer version of the capture
=========================================

Preview:

'''
gst-launch decklinksrc mode=11 connection=hdmi subdevice=0 ! video/x-raw-yuv ! ffmpegcolorspace ! deinterlace ! xvimagesink sync=false
'''



Sources
=======

IP streaming stuff:

http://stackoverflow.com/questions/19107301/gstreamer-pipeline-for-decklinksrc-video-capture-card-with-udpsrc-and-udpsink-us

GST encoding:

http://wiki.oz9aec.net/index.php/Gstreamer_cheat_sheet#Encoding_and_Muxing