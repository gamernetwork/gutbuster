OUTPUT_MODE="1080p60"
CARD_MODE="720p60"

DEBUG=True

USE_VAAPI=True
FILE_PREFIX="/media/mark/capture002/EGX/EGX2018/capture_"

AUDIO_MONITOR_DEVICE="plughw:CARD=USB,DEV=0"

INPUTS=[
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
        "monitor": True,
        "src": {
            "type": "decklinkaudiosrc",
            "connection": "embedded",
            "device": "3",
            "mode": CARD_MODE,
        },
    },
]

RECORDINGS=[
]

LAYOUT=[
    { "input": "mix", "w": 1280, "h": 720, "x": 0, "y": 0 },
    { "input": "mixaudio", "w": 480, "h": 405, "x": 1440, "y": 405 },
]
