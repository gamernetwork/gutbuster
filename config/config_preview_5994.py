OUTPUT_MODE="1080p5994"
CARD_MODE="1080p5994"

DEBUG=True

USE_VAAPI=True
FILE_PREFIX="/media/mark/capture002/EGX/EGX2018/capture_"

AUDIO_MONITOR_DEVICE="plughw:CARD=USB,DEV=0"

INPUTS=[
    {
        "name": "head",
        "title": "HEAD",
        "src": {
            "type": "decklinkvideosrc",
            "connection": "sdi",
            "device": "4",
            "mode": CARD_MODE,
        },
    },
    {
        "name": "wide",
        "title": "WIDE",
        "src": {
            "type": "decklinkvideosrc",
            "connection": "sdi",
            "device": "5",
            "mode": CARD_MODE,
        },
    },
    {
        "name": "audience",
        "title": "AUDIENCE",
        "src": {
            "type": "decklinkvideosrc",
            "connection": "sdi",
            "device": "6",
            "mode": CARD_MODE,
        },
    },
    {
        "name": "playout",
        "title": "PLAYOUT",
        "src": {
            "type": "decklinkvideosrc",
            "connection": "sdi",
            "device": "7",
            "mode": CARD_MODE,
        },
    },
    {
        "name": "mix",
        "title": "BROADCAST",
        "src": {
            "type": "decklinkvideosrc",
            "connection": "sdi",
            "device": "3",
            "mode": CARD_MODE,
        },
    },
    {
        "name": "mixaudio",
        "title": "BROADCAST",
        "monitor": False,
        "src": {
            "type": "decklinkaudiosrc",
            "connection": "embedded",
            "device": "3",
            "mode": CARD_MODE,
        },
    },
#    {
#        "name": "test",
#        "title": "TEST",
#        "src": {
#            "type": "test",
#            "mode": "1080p30",
#        },
#    },
    {
        "name": "roomaudio",
        "monitor": True,
        "title": "ROOM",
        "src": {
            "type": "alsa",
            "device": "plughw:CARD=USB,DEV=0",
            "mode": CARD_MODE,
        },
    },
]

RECORDINGS=[
]

LAYOUT=[
    { "input": "mix", "w": 1440, "h": 810, "x": 0, "y": 0 },
    { "input": "head", "w": 480, "h": 270, "x": 0, "y": 810 },
    { "input": "wide", "w": 480, "h": 270 },
    { "input": "audience", "w": 480, "h": 270 },
    #{ "input": "foo", "w": 480, "h": 270 },
    { "input": "playout", "w": 480, "h": 270 },
    { "input": "mixaudio", "w": 480, "h": 405, "x": 1440, "y": 405 },
    { "input": "roomaudio", "w": 480, "h": 405, "x": 1440, "y": 0 },
]
