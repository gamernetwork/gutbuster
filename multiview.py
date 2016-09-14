import gi
gi.require_version('Gtk', '3.0')
gi.require_version('Gst', '1.0')
gi.require_version('GstVideo', '1.0')
from gi.repository import GObject, Gst, Gtk

# Needed for window.get_xid(), xvimagesink.set_window_handle(), respectively:
from gi.repository import GstVideo, GdkX11

import re

GObject.threads_init()
Gst.init(None)

ml = GObject.MainLoop()

def caps_from_mode( mode ):
    m = re.match( '(720|1080)(i|p)(2398|24|25|2997|30|50|5994|60)', mode )
    if m:
        height = int(m.group(1))
        width = height/9*16
        if m.group(2) == 'i':
            interlace = 'interleaved'
        else:
            interlace = 'progressive'
        framerate = {
            '2398': '24000/1001',
            '24' : '24/1',
            '25' : '25/1',
            '2997' : '30000/1001',
            '30' : '30/1',
            '50' : '50/1',
            '5994' : '60000/1001',
            '60' : '60/1',
        }[m.group(3)]

        return {
            'filter': 'video/x-raw, width=%i, height=%i, interlace-mode=%s, framerate=%s' % (width, height, interlace, framerate),
            'width': width,
            'height': height,
            'interlace-mode': interlace,
            'framerate': framerate
        }

    else:
        raise Exception('Mode "' + mode + '" is not valid.')

def lookup_layout(layout, inp):
    x = 0
    y = 0
    prev_w = 0
    prev_h = 0
    for l in layout:
        if l.has_key('x'):
            x = l['x']
            y = l['y']
        else:
            x += prev_w
            # y stays the same

        if l['input'] == inp['name']:
            return {
                'x': x,
                'y': y,
                'w': l['w'],
                'h': l['h']
            }
        prev_w = l['w']
        prev_h = l['h']

class SimpleGSTGTKApp:

    def __init__(self):
        self.build_gui('main.ui')
        self.pipeline = False
        self.setup_messaging()

    def build_gui(self, interface_def):
        self.builder = Gtk.Builder()
        self.builder.add_from_file(interface_def)
        self.window = self.builder.get_object("main")
        self.window.connect('destroy', self.quit)
        self.window.set_default_size(960, 540)
        self.view = self.builder.get_object("view")
        self.window.show_all()
        # You need to get the XID after window.show_all().  You shouldn't get it
        # in the on_sync_message() handler because threading issues will cause
        # segfaults there.
        self.view_xid = self.view.get_property('window').get_xid()

    def quit(self, window):
        self.pipeline.set_state(Gst.State.NULL)
        Gtk.main_quit()

    def setup_messaging(self):
        self.bus = self.pipeline.get_bus()
        #self.bus.connect('message', self.pmsg)
        self.bus.add_signal_watch()
        self.bus.connect('message::error', self.on_error)

        # This is needed to make the video output in our DrawingArea:
        self.bus.enable_sync_message_emission()
        self.bus.connect('sync-message::element', self.on_sync_message)

    def run(self):
        # Start playing
        self.pipeline.set_state(Gst.State.PLAYING)

    def on_sync_message(self, bus, msg):
        if msg.get_structure().get_name() == 'prepare-window-handle':
            #print(msg.src.name);
            if msg.src.name == "view_sink":
                #print('live prepare-window-handle')
                msg.src.set_property('force-aspect-ratio', True)
                msg.src.set_window_handle(self.view_xid)
    def on_error(self, bus, msg):
        print('on_error():', msg.parse_error())

class Capture(SimpleGSTGTKApp):

    def build_pipeline(self, inputs, output_mode, layout):
        # decklinkvideosrc mode=auto connection=hdmi device-number=$DEVICE ! \
        input_pipelines = []
        mixer_spec = [
            "videomixer name=mix",
        ]
        for inp in inputs:
            inp_layout = lookup_layout(layout, inp)
            input_pipelines += self.make_src_branch_spec(inp, inp_layout)
            mixer_spec += self.make_mixer_pad_spec(inp, inp_layout)
            
        pipeline_spec = input_pipelines + mixer_spec + [
            "! xvimagesink name=view_sink sync=false"
        ]

        pipeline_spec = " ".join(pipeline_spec)

        self.pipeline = Gst.parse_launch( pipeline_spec )

    def __init__(self, inputs, output_mode, layout):
        self.build_gui('multiview.ui')
        self.build_pipeline(inputs, output_mode, layout)
        self.setup_messaging()

    def make_mixer_pad_spec(self, device, layout):
        device['x'] = layout['x']
        device['y'] = layout['y']
        spec = [
            "sink_{index}::xpos={x} sink_{index}::ypos={y} sink_{index}::alpha=1 sink_{index}::zorder=1"
        ]
        spec = [l.format(**device) for l in spec]
        return spec

    def make_src_branch_spec(self, device, layout):
        device['w'] = layout['w']
        device['h'] = layout['h']
        if device['src']['type'] == 'decklinkvideosrc':
            spec = [
              "decklinkvideosrc mode={src[mode]} connection={src[connection]} device-number={src[device]}",
                "! videoconvert",
                "! videoscale",
                "! video/x-raw, width={w}, height={h}",
                "! textoverlay font-desc=\"Sans Bold 24\" text=\"{title}\" color=0xff90ff00",
                "! queue",
                "! mix.sink_{index}",
            ]
        elif device['src']['type'] == 'test':
            spec = [
              "videotestsrc is-live=true",
                "! videoconvert",
                "! videoscale",
                "! video/x-raw, width={w}, height={h}",
                "! textoverlay font-desc=\"Sans Bold 24\" text=\"{title}\" color=0xff90ff00",
                "! queue",
                "! mix.sink_{index}"
            ]
        else:
            raise Exception('Unknown device type ' + device['src']['type'])
        spec = [l.format(**device) for l in spec]
        return spec

    # TODO plug in this stats stuff, perhaps into status bar?
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

#    def pmsg(self, msg_bus, msg):
#        if msg.type == Gst.MessageType.ERROR or msg.type == Gst.MessageType.EOS:
#            ml.quit()       
#        if msg.type == Gst.MessageType.STATE_CHANGED:
#            #print pipeline.get_state(Gst.CLOCK_TIME_NONE).state
#            self.stats(msg_bus)


def get_args():
    import argparse

    parser = argparse.ArgumentParser(description='')
    parser.add_argument('devices', metavar='DEV', type=str, nargs='*',
        help='which devices to preview (default: all defined in config)')
    parser.add_argument('--config',
        default='config',
        help='config module (default: config i.e. config.py)')

    args = parser.parse_args()
    # people might accidentally supply a module filename, which we'll forgive them for
    args.config=re.sub('.py$', '', args.config)
    return args

if __name__=="__main__":

    args = get_args()
    config = __import__(args.config, fromlist=['*'])

    # filter devices if some were supplied on cmdline
    inps=[]
    index = 0
    for inp in config.INPUTS:
        if len(args.devices) == 0 or inp['name'] in args.devices:
            inp['src']['caps'] = caps_from_mode(inp['src']['mode'])
            inp['index'] = index
            index += 1
            inps.append(inp)

    output_mode = caps_from_mode(config.OUTPUT_MODE)

    try:
        c1 = Capture(inps, output_mode, config.LAYOUT)
        c1.run()
        Gtk.main()
    finally:
        # Free resources if mainloop dies
        c1.pipeline.set_state(Gst.State.NULL)

