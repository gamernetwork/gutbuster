import gi
gi.require_version('Gtk', '3.0')
gi.require_version('Gdk', '3.0')
gi.require_version('Gst', '1.0')
gi.require_version('GstVideo', '1.0')
from gi.repository import GObject, Gst, Gtk, Gdk

# Needed for window.get_xid(), xvimagesink.set_window_handle(), respectively:
from gi.repository import GstVideo, GdkX11

import re, logging

GObject.threads_init()
Gst.init(None)

import datetime

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
 
    def keypress(self, win, event):
        if event.keyval == Gdk.KEY_F11:
            win.is_fullscreen = not getattr(win, 'is_fullscreen', False)
            action = win.fullscreen if win.is_fullscreen else win.unfullscreen
            action()
            self.builder.get_object('statusbar1').set_visible(not win.is_fullscreen)


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

        #self.window.connect("delete-event", gtk.main_quit)
        self.window.connect('key-press-event', self.keypress)

        #self.builder.get_object("tool_recordall").connect("clicked", self.set_rec_test)

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

    def stop_recording(self):
        logging.debug("Stop recording")
        # how to dynamically set a property
        inputname = "0"
        overlay = self.pipeline.get_by_name('%s_textoverlay' % inputname)
        overlay.set_property("color", 0xff80ff00)
        #valve = self.pipeline.get_by_name('%s_rec_valve' % inputname) 
        #valve.set_property('drop', True)

        # send an EOS
        # del( self.bins[inputname] )


    def get_input(self, name):
        for a in self.inputs:
            if a['name'] == name:
                l = self.get_layout_for_input(name)
                a['w'] = l['w']
                a['h'] = l['h']
                return a

    def get_layout_for_input(self, name):
        for a in self.layout:
            if a['input'] == name:
                return a

    def start_recording(self):
        logging.debug("Start recording")
        # how to dynamically set a property
        inputname = "0"
        vals = self.get_input(inputname)
        vals['index'] = datetime.datetime.now().strftime('%a_%H:%M.%S')
        vals['fileprefix'] = 'monk_' + vals['index']
        vid_capture = [
              #"queue",
              #"! valve drop=false name=\"{name}_rec_valve\"",
              #"! vaapipostproc scale-method=hq",
              "videoconvert",
              "! videoscale",
              "! video/x-raw, width={src[caps][width]}, height={src[caps][height]}",
              #"! vaapih264enc init-qp=16 keyframe-period=120",
              "! x264enc speed-preset=ultrafast",
              "! mpegtsmux",
              "! filesink location={fileprefix}_{name}.ts",
        ]
        vid_capture = [l.format(**vals) for l in vid_capture]
        bin_spec = " ".join(vid_capture)
            #"{name}_rec_tee.",
        logging.debug(bin_spec)
        self.bins[inputname] = Gst.parse_bin_from_description(bin_spec, True)

        queue = Gst.ElementFactory.make('queue')
        self.pipeline.add(queue)
        self.pipeline.add(self.bins[inputname])

        tee = self.pipeline.get_by_name('%s_rec_tee' % inputname)
        self.pipeline.set_state(Gst.State.PAUSED)
        tee.link(queue)
        queue.link(self.bins[inputname])
        self.bins[inputname].set_state(Gst.State.PLAYING)
        #self.bins[inputname].sync_state_with_parent()


        overlay = self.pipeline.get_by_name('%s_textoverlay' % inputname)
        overlay.set_property("color", 0xffff8060)
        #valve = self.pipeline.get_by_name('%s_rec_valve' % inputname)
        #valve.set_property('drop', False)

    def build_pipeline(self):
        # decklinkvideosrc mode=auto connection=hdmi device-number=$DEVICE ! \
        input_pipelines = []
        mixer_spec = [
            "videomixer name=mix",
        ]
        for inp in self.inputs:
            inp_layout = lookup_layout(self.layout, inp)
            input_pipelines += self.make_src_branch_spec(inp, inp_layout)
            mixer_spec += self.make_mixer_pad_spec(inp, inp_layout)
            
        pipeline_spec = input_pipelines + mixer_spec + [
            "! %s " % self.output_mode['filter'],
            "! xvimagesink name=view_sink sync=false"
        ]

        pipeline_spec = " ".join(pipeline_spec)
        logging.debug(pipeline_spec)

        self.pipeline = Gst.parse_launch( pipeline_spec )

    def __init__(self, inputs, output_mode, layout):
        self.build_gui('gutbuster.ui')
        self.inputs = inputs
        self.output_mode = output_mode
        self.layout = layout
        self.build_pipeline()
        self.setup_messaging()
        self.bins = {}

    def make_mixer_pad_spec(self, device, layout):
        device['x'] = layout['x']
        device['y'] = layout['y']
        spec = [
            "sink_{index}::xpos={x} sink_{index}::ypos={y} sink_{index}::alpha=1 sink_{index}::zorder=1"
        ]
        spec = [l.format(**device) for l in spec]
        return spec

    def make_src_branch_spec(self, device, layout):
        vals = device
        vals['w'] = layout['w']
        vals['h'] = layout['h']
        textoverlay = "! textoverlay name=\"{name}_textoverlay\" font-desc=\"Sans Bold 24\" text=\"{title}\" color=0xff90ff00 auto-resize=false shaded-background=true x-absolute=20 y-absolute=20"
        tee = "! tee name=\"{name}_rec_tee\" ! queue "
        scope = [
            "! audioconvert",
            "! wavescope shader=0 style=lines",
            "! video/x-raw, format=BGRx, width={w}, height={h}, framerate={src[caps][framerate]}",
            "! videorate",
        ]
        if device['src']['type'] == 'decklinkvideosrc':
            spec = [
              "decklinkvideosrc mode={src[mode]} connection={src[connection]} device-number={src[device]}",
                "! video/x-raw, width={src[caps][width]}, height={src[caps][height]}",
                tee,
                "! queue",
                "! videoconvert",
                "! videoscale",
                "! video/x-raw, width={w}, height={h}",
                textoverlay,
                "! mix.sink_{index}",
            ]
        elif device['src']['type'] == 'decklinkaudiosrc':
            spec = [
              "decklinkaudiosrc connection={src[connection]} device-number={src[device]}",
                tee,
                "! queue",
              ] + scope + [
                textoverlay,
                "! mix.sink_{index}",
            ]
        elif device['src']['type'] == 'test':
            spec = [
              "videotestsrc is-live=true",
                "! video/x-raw, width={src[caps][width]}, height={src[caps][height]}",
                tee,
                "! queue",
                "! videoconvert",
                "! videoscale",
                "! video/x-raw, width={w}, height={h}",
                textoverlay,
                "! mix.sink_{index}"
            ]
        elif device['src']['type'] == 'alsa':
            spec = [
               "alsasrc device=\"{src[device]}\" do-timestamp=true",
                tee,
                "! queue",
              ] + scope + [
                textoverlay,
                "! mix.sink_{index}"
            ]
        else:
            raise Exception('Unknown device type ' + device['src']['type'])
        spec = [l.format(**vals) for l in spec]
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
    parser.add_argument('--debug', '-v',
        default=False, action='store_const', const=True,
        help='debug output')

    args = parser.parse_args()
    # people might accidentally supply a module filename, which we'll forgive them for
    args.config=re.sub('.py$', '', args.config)
    return args

if __name__=="__main__":

    args = get_args()
    config = __import__(args.config, fromlist=['*'])

    if args.debug:
        logging.basicConfig(level=logging.DEBUG)

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
        GObject.timeout_add(3000, c1.start_recording)
        GObject.timeout_add(6000, c1.stop_recording)
        #c1.start_recording()
        c1.run()
        Gtk.main()
    finally:
        # Free resources if mainloop dies
        # c1.pipeline.set_state(Gst.State.NULL)
        pass

