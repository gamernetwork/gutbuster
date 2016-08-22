import gi
gi.require_version('Gtk', '3.0')
gi.require_version('Gst', '1.0')
gi.require_version('GstVideo', '1.0')
from gi.repository import GObject, Gst

# Needed for window.get_xid(), xvimagesink.set_window_handle(), respectively:
from gi.repository import GstVideo

GObject.threads_init()
Gst.init(None)


# decklinkvideosrc mode=auto connection=hdmi device-number=$DEVICE ! \
# Build the pipeline
pipeline = Gst.parse_launch( "\
  autovideosrc name=webcam \
  ! video/x-raw, width=640, height=360 \
  ! videoconvert \
  ! videoscale \
  ! video/x-raw, width=320, height=180 \
  ! textoverlay name=overlay font-desc=\"Sans Bold 24\" text=\"PREVIEW: $DEVICE: $SHOT\" color=0xffff3000 \
  ! queue \
  ! xvimagesink \
")

# Start playing
pipeline.set_state(Gst.State.PLAYING)

def stats():
    pad = pipeline.get_by_name("webcam").get_static_pad('src')
    caps = pad.get_current_caps()
    if caps:
        s = caps.get_size()
        print("Size %i" % s)
        st = caps.get_structure(0)
        v = st.get_fraction('framerate')
        print(v.value_numerator/v.value_denominator)

# Wait until error or EOS
bus = pipeline.get_bus()
while True:
    msg = bus.timed_pop(Gst.CLOCK_TIME_NONE)
    if msg.type == Gst.MessageType.ERROR or msg.type == Gst.MessageType.EOS:
        break
    if msg.type == Gst.MessageType.STATE_CHANGED:
        print pipeline.get_state(Gst.CLOCK_TIME_NONE).state
        stats()



# Free resources
pipeline.set_state(Gst.State.NULL)
