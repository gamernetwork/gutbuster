from defaults import *

OUTPUT_MODE="1080p60"
CARD_MODE="1080p30"

INPUTS=[
	{
		"name": "0",
		"title": "0",
		"src": {
			"type": "decklinkvideosrc",
			"connection": "sdi",
			"device": "0",
			"mode": CARD_MODE,
		},
	},
	{
		"name": "1",
		"title": "1",
		"src": {
			"type": "decklinkvideosrc",
			"connection": "sdi",
			"device": "1",
			"mode": CARD_MODE,
		},
	},
	{
		"name": "2",
		"title": "2",
		"src": {
			"type": "decklinkvideosrc",
			"connection": "sdi",
			"device": "2",
			"mode": CARD_MODE,
		},
	},
	{
		"name": "3",
		"title": "3",
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
			"mode": "1080p60",
		},
	},
	{
		"name": "mixaudio",
		"title": "BROADCAST",
		"src": {
			"type": "decklinkaudiosrc",
			"connection": "embedded",
			"device": "7",
			"mode": "1080p60",
		},
	},
#	{
#		"name": "test",
#		"title": "TEST",
#		"src": {
#			"type": "test",
#			"mode": "1080p60",
#		},
#	},
	{
		"name": "roomaudio",
		"title": "ROOM",
		"src": {
			"type": "alsa",
			"device": "hw:CARD=USB",
			"mode": "1080p60",
		},
	},
]

RECORDINGS=[
    { "input": "mix", },
    { "input": "0", },
    { "input": "1", },
    { "input": "2", },
    { "input": "3", },
]


LAYOUT=[
	{ "input": "mix", "w": 1440, "h": 810, "x": 0, "y": 0 },
	{ "input": "0", "w": 480, "h": 270, "x": 0, "y": 810 },
	{ "input": "1", "w": 480, "h": 270 },
	{ "input": "2", "w": 480, "h": 270 },
	{ "input": "3", "w": 480, "h": 270 },
	{ "input": "roomaudio", "w": 480, "h": 405, "x": 1440, "y": 405 },
	{ "input": "mixaudio", "w": 480, "h": 405, "x": 1440, "y": 0 },
]
