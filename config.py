OUTPUT_MODE="1080p30"
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
			"device": "4",
			"mode": CARD_MODE,
		},
	},
]

LAYOUT=[
	{ "device": "mix", "w": 1440, "h": 810, "x": 0, "y", 0 },
	{ "device": "0", "w": 480, "h": 270, "x": 0, "y": 810 },
	{ "device": "1", "w": 480, "h": 270 },
	{ "device": "2", "w": 480, "h": 270 },
	{ "device": "3", "w": 480, "h": 270 },
]
