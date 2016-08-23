import gi
gi.require_version('Gtk', '3.0')
gi.require_version('Gst', '1.0')
gi.require_version('GstVideo', '1.0')
from gi.repository import GObject, Gst

# Needed for window.get_xid(), xvimagesink.set_window_handle(), respectively:
from gi.repository import GstVideo

GObject.threads_init()
Gst.init(None)

ml = GObject.MainLoop()

class Capture:
    def __init__(self):
        # decklinkvideosrc mode=auto connection=hdmi device-number=$DEVICE ! \
        self.pipeline = Gst.parse_launch( "\
          videotestsrc name=webcam \
          ! video/x-raw, width=640, height=360 \
          ! tee name=t \
          ! queue \
          ! videoconvert \
          ! videoscale \
          ! video/x-raw, width=320, height=180 \
          ! textoverlay name=overlay font-desc=\"Sans Bold 24\" text=\"0\" color=0xffff3000 \
          ! xvimagesink \
        ")
        self.bus = self.pipeline.get_bus()
        self.bus.add_signal_watch()

        # Start playing
        self.pipeline.set_state(Gst.State.PLAYING)
        self.bus.connect('message', self.pmsg)

    def stats(self, msg_bus):
        pad = self.pipeline.get_by_name("webcam").get_static_pad('src')
        caps = pad.get_current_caps()
        if caps:
            s = caps.get_size()
            #print("Size %i" % s)
            st = caps.get_structure(0)
            v = st.get_fraction('framerate')
            fps = v.value_numerator/v.value_denominator
            self.pipeline.get_by_name("overlay").set_property('text', '%i' % fps)

    def addPreview(self):
        print("Add preview")
        queue = Gst.ElementFactory.make('queue', 'pq')
        sink = Gst.ElementFactory.make('xvimagesink', 'ps')
        self.pipeline.add(queue)
        self.pipeline.add(sink)
        queue.set_state(Gst.State.PLAYING)
        sink.set_state(Gst.State.PLAYING)
        tee = self.pipeline.get_by_name('t')
        tee.link(queue)
        queue.link(sink)

    def addScaler(self):
        print("Add scaler")
        scale = Gst.ElementFactory.make('videoscale')
        self.pipeline.add(scale)
        #scale.set_state(Gst.State.PAUSED)

        queue = self.pipeline.get_by_name('pq')
        preview = self.pipeline.get_by_name('ps')
        src = queue.get_static_pad('src')

        preview_caps = Gst.caps_from_string('video/x-raw, width=160, height=90');

        def block(pad, info, user_data):
            return Gst.PadProbeReturn.OK

        self.pipeline.set_state(Gst.State.PAUSED)
        #prid = src.add_probe(Gst.PadProbeType.BLOCK, block, None)
        queue.unlink(preview)
        scale.set_state(Gst.State.PLAYING)
        queue.link(scale)
        scale.link_filtered(preview, preview_caps)
        #src.remove_probe(prid)
        self.pipeline.set_state(Gst.State.PLAYING)

    def pmsg(self, msg_bus, msg):
        if msg.type == Gst.MessageType.ERROR or msg.type == Gst.MessageType.EOS:
            ml.quit()       
        if msg.type == Gst.MessageType.STATE_CHANGED:
            #print pipeline.get_state(Gst.CLOCK_TIME_NONE).state
            self.stats(msg_bus)

c1 = Capture()
c2 = Capture()

GObject.timeout_add(1000, c1.addPreview)
GObject.timeout_add(1000, c2.addPreview)

GObject.timeout_add(2000, c1.addScaler)

try:
    ml.run()
finally:
    # Free resources when mainloop terminates
    c1.pipeline.set_state(Gst.State.NULL)
    c2.pipeline.set_state(Gst.State.NULL)
