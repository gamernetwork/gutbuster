gst-launch-1.0 -e \
    decklinkvideosrc mode=1080p30 connection=sdi device-number=4 \
    ! video/x-raw, width=1920, height=1080 \
    ! videoconvert \
    ! videoscale \
    ! video/x-raw, width=1920, height=1080 \
    ! x264enc key-int-max=60 tune=zerolatency pass=cbr bitrate=4000 speed-preset=ultrafast \
    ! tee name=t \
    ! queue \
    ! flvmux streamable=true name=mux \
    ! rtmpsink location="rtmp://live-lhr.twitch.tv/app/live_49236445_gfLQWmuxEpuo7pWgJlokyBInEB12tJ" \
    decklinkaudiosrc connection=embedded device-number=4 \
    ! audioconvert \
    ! avenc_aac bitrate=160000 \
    ! mux. \
#    t. \
#    ! queue \
#    ! avdec_h264 \
#    ! videoconvert \
#    ! xvimagesink

                  #! filesink location=test.flv

                  
                  #! tee name=t \
                  #! queue \
                  #! flvdemux \
                  #! avdec_h264 \
                  #! xvimagesink
#

#                  ! vaapipostproc scale-method=hq,
#                  ! video/x-raw, width=1920, height=1080
#                  ! vaapih264enc init-qp=23 keyframe-period=120
    #! rtmpsink location="rtmp://live-lhr.twitch.tv/app/live_49382179_Zrbr9wIynJZrp7BOt7HzQPtX4XcqaQ?bandwidthtest=true" \
    #REAL ONE ! rtmpsink location="rtmp://live-lhr.twitch.tv/app/live_49382179_Zrbr9wIynJZrp7BOt7HzQPtX4XcqaQ" \
