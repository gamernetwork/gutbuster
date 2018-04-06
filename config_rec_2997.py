OUTPUT_MODE="1080p2997"
CARD_MODE="1080p2997"

DEBUG=True

USE_VAAPI=True
FILE_PREFIX="/media/mark/CAPTURE002/EGX/EGX2017/capture_"

INPUTS=[
	{
		"name": "wide",
		"title": "WIDE",
		"src": {
			"type": "decklinkvideosrc",
			"connection": "sdi",
			"device": "1",
			"mode": CARD_MODE,
		},
	},
#	{
#		"name": "audience",
#		"title": "AUDIENCE",
#		"src": {
#			"type": "decklinkvideosrc",
#			"connection": "sdi",
#			"device": "2",
#			"mode": CARD_MODE,
#		},
#	},
	{
		"name": "head",
		"title": "HEAD",
		"src": {
			"type": "decklinkvideosrc",
			"connection": "sdi",
			"device": "0",
			"mode": CARD_MODE,
		},
	},
	{
		"name": "proj",
		"title": "PROJ",
		"src": {
			"type": "decklinkvideosrc",
			"connection": "sdi",
			"device": "3",
			"mode": CARD_MODE,
		},
	},
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
        "monitor": True,
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
			"type": "pulse",
			"mode": "1080p2997",
		},
	},
]

RECORDINGS=[
    { "input": "wide", },
    { "input": "head", },
    { "input": "proj", },
    { "input": "mix", },
    { "input": "roomaudio", },
]

LAYOUT=[
	{ "input": "mix", "w": 1440, "h": 810, "x": 0, "y": 0 },
	{ "input": "head", "w": 480, "h": 270,"x": 0, "y": 810  },
	{ "input": "wide", "w": 480, "h": 270 },
#	{ "input": "audience", "w": 480, "h": 270 },
	{ "input": "proj", "w": 480, "h": 270 },
	{ "input": "roomaudio", "w": 480, "h": 405, "x": 1440, "y": 405 },
	{ "input": "mixaudio", "w": 480, "h": 405, "x": 1440, "y": 0 },
]
