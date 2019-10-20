OUTPUT_MODE="1080p5994"
CARD_MODE="720p5994"

DEBUG=True

USE_VAAPI=True
FILE_PREFIX="/media/egx/CAPTURE002/EGX/egx19_capture_"

AUDIO_MONITOR_DEVICE="hw:CARD=USB,DEV=0"

INPUTS=[
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
                "denoise": 0.1,
		"src": {
			"type": "decklinkvideosrc",
			"connection": "sdi",
			"device": "6",
			"mode": CARD_MODE,
		},
	},
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
		"name": "proj",
		"title": "PROJ",
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
                "monitor": True,
		"src": {
			"type": "decklinkaudiosrc",
			"connection": "embedded",
			"device": "3",
			"mode": CARD_MODE,
		},
	},
#	{
#		"name": "roomaudio",
#		"title": "ROOM",
#                "monitor": False,
#		"src": {
#			"type": "alsa",
#                        "device": "hw:CARD=USB,DEV=0",
#			"mode": CARD_MODE,
#		},
#	},
]

RECORDINGS=[
    { "input": "wide", },
    { "input": "head", },
    { "input": "proj", },
    { "input": "mix", },
    { "input": "audience", },
    { "input": "mixaudio", },
#    { "input": "roomaudio", },
]

LAYOUT=[
	{ "input": "mix", "w": 1440, "h": 810, "x": 0, "y": 0 },
	{ "input": "head", "w": 480, "h": 270,"x": 0, "y": 810  },
	{ "input": "wide", "w": 480, "h": 270 },
	{ "input": "audience", "w": 480, "h": 270 },
	{ "input": "proj", "w": 480, "h": 270 },
#	{ "input": "roomaudio", "w": 480, "h": 405, "x": 1440, "y": 405 },
	{ "input": "mixaudio", "w": 480, "h": 405, "x": 1440, "y": 0 },
]
