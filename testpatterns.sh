
gst-launch-1.0 \
videotestsrc pattern=smpte100 is-live=true ! video/x-raw, width=1920, height=1080 ! decklinkvideosink mode=9 device-number=0 \
videotestsrc pattern=zone-plate kx2=20 ky2=20 kt=1 is-live=true ! video/x-raw, width=1920, height=1080 ! decklinkvideosink mode=9 device-number=1 \
videotestsrc pattern=gamut is-live=true ! video/x-raw, width=1920, height=1080 ! decklinkvideosink mode=9 device-number=2 \
videotestsrc pattern=ball is-live=true ! video/x-raw, width=1920, height=1080 ! decklinkvideosink mode=9 device-number=3

