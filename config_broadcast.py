OUTPUT_MODE="1080p2997"
CARD_MODE="1080p2997"

USE_VAAPI=True
FILE_PREFIX="/media/mark/capture002/EGX/EGX2016/capture_"

INPUTS=[
	{
		"name": "mix",
		"title": "BROADCAST",
		"src": {
			"type": "decklinkvideosrc",
			"connection": "sdi",
			"device": "7",
			"mode": "1080p2997",
		},
	},
	{
		"name": "mixaudio",
		"title": "BROADCAST",
		"src": {
			"type": "decklinkaudiosrc",
			"connection": "embedded",
			"device": "7",
			"mode": "1080p2997",
		},
	},
	{
		"name": "roomaudio",
		"title": "ROOM",
		"src": {
			"type": "alsa",
			"device": "plughw:CARD=USB",
			"mode": "1080p2997",
		},
	},
]

RECORDINGS=[
]

LAYOUT=[
	{ "input": "mix", "w": 1440, "h": 810, "x": 0, "y": 0 },
	{ "input": "mixaudio", "w": 480, "h": 405, "x": 1440, "y": 0 },
	{ "input": "roomaudio", "w": 480, "h": 405, "x": 1440, "y": 405 },
]
