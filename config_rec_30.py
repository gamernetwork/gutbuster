OUTPUT_MODE="1080p30"
CARD_MODE="1080p30"

DEBUG=True

USE_VAAPI=True
FILE_PREFIX="/media/mark/CAPTURE001/EGX/REZZED2017/capture_"

INPUTS=[
	{
		"name": "wide",
		"title": "WIDE",
		"src": {
			"type": "decklinkvideosrc",
			"connection": "sdi",
			"device": "0",
			"mode": CARD_MODE,
		},
	},
	{
		"name": "audience",
		"title": "AUDIENCE",
		"src": {
			"type": "decklinkvideosrc",
			"connection": "sdi",
			"device": "1",
			"mode": CARD_MODE,
		},
	},
	{
		"name": "head",
		"title": "HEAD",
		"src": {
			"type": "decklinkvideosrc",
			"connection": "sdi",
			"device": "2",
			"mode": CARD_MODE,
		},
	},
	{
		"name": "playout",
		"title": "PLAYOUT",
		"src": {
			"type": "decklinkvideosrc",
			"connection": "sdi",
			"device": "3",
			"mode": "1080p30",
		},
	},
	{
		"name": "mix",
		"title": "BROADCAST",
		"src": {
			"type": "decklinkvideosrc",
			"connection": "sdi",
			"device": "7",
			"mode": "1080p30",
		},
	},
	{
		"name": "mixaudio",
		"title": "BROADCAST",
		"src": {
			"type": "decklinkaudiosrc",
			"connection": "embedded",
			"device": "7",
			"mode": "1080p30",
		},
	},
#	{
#		"name": "test",
#		"title": "TEST",
#		"src": {
#			"type": "test",
#			"mode": "1080p30",
#		},
#	},
	{
		"name": "roomaudio",
		"title": "ROOM",
		"src": {
			"type": "alsa",
			"device": "hw:CARD=USB",
			"mode": "1080p30",
		},
	},
]

RECORDINGS=[
    { "input": "mix", },
    { "input": "wide", },
    { "input": "head", },
    { "input": "playout", },
    { "input": "roomaudio", },
]

LAYOUT=[
	{ "input": "mix", "w": 1440, "h": 810, "x": 0, "y": 0 },
	{ "input": "audience", "w": 480, "h": 270, "x": 0, "y": 810 },
	{ "input": "head", "w": 480, "h": 270 },
	{ "input": "wide", "w": 480, "h": 270 },
	{ "input": "playout", "w": 480, "h": 270 },
	{ "input": "roomaudio", "w": 480, "h": 405, "x": 1440, "y": 405 },
	{ "input": "mixaudio", "w": 480, "h": 405, "x": 1440, "y": 0 },
]
