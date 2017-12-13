OUTPUT_MODE="1080p30"
CARD_MODE="1080p30"

DEBUG=True

USE_VAAPI=True
FILE_PREFIX="/media/mark/capture002/EGX/EGX2016/capture_"

INPUTS=[
	{ "name": "0", "title": "0", "src": { "type": "decklinkvideosrc", "connection": "sdi", "device": "0", "mode": CARD_MODE, }, },
	{ "name": "1", "title": "1", "src": { "type": "decklinkvideosrc", "connection": "sdi", "device": "1", "mode": CARD_MODE, }, },
	{ "name": "2", "title": "2", "src": { "type": "decklinkvideosrc", "connection": "sdi", "device": "2", "mode": CARD_MODE, }, },
	{ "name": "3", "title": "3", "src": { "type": "decklinkvideosrc", "connection": "sdi", "device": "3", "mode": CARD_MODE, }, },
	{ "name": "4", "title": "4", "src": { "type": "decklinkvideosrc", "connection": "sdi", "device": "4", "mode": CARD_MODE, }, },
	{ "name": "5", "title": "5", "src": { "type": "decklinkvideosrc", "connection": "sdi", "device": "5", "mode": CARD_MODE, }, },
	{ "name": "6", "title": "6", "src": { "type": "decklinkvideosrc", "connection": "sdi", "device": "6", "mode": CARD_MODE, }, },
	{ "name": "7", "title": "7", "src": { "type": "decklinkvideosrc", "connection": "sdi", "device": "7", "mode": CARD_MODE, }, },
]

RECORDINGS=[
]

LAYOUT=[
	{ "input": "0", "w": 320, "h": 180, "x": 0, "y": 180 },
	{ "input": "1", "w": 320, "h": 180, },
	{ "input": "2", "w": 320, "h": 180,},
	{ "input": "3", "w": 320, "h": 180,},
	{ "input": "4", "w": 320, "h": 180, "x": 0, "y": 360},
	{ "input": "5", "w": 320, "h": 180,},
	{ "input": "6", "w": 320, "h": 180,},
	{ "input": "7", "w": 320, "h": 180,},
]
