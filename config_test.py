from defaults import *

OUTPUT_MODE="1080p30"
CARD_MODE="1080p30"

USE_VAAPI=True

INPUTS=[
    {
        "name": "0",
        "title": "0",
        "src": {
            "type": "test",
            "mode": CARD_MODE,
        },
    },
    {
        "name": "1",
        "title": "1",
        "src": {
            "type": "test",
            "mode": CARD_MODE,
        },
    },
    {
        "name": "2",
        "title": "2",
        "src": {
            "type": "test",
            "mode": CARD_MODE,
        },
    },
    {
        "name": "3",
        "title": "3",
        "src": {
            "type": "test",
            "mode": CARD_MODE,
        },
    },
    {
        "name": "mix",
        "title": "BROADCAST",
        "src": {
            "type": "test",
            "mode": CARD_MODE,
        },
    },
]

LAYOUT=[
    { "input": "mix", "w": 1440, "h": 810, "x": 0, "y": 0 },
    { "input": "0", "w": 480, "h": 270, "x": 0, "y": 810 },
    { "input": "1", "w": 480, "h": 270 },
    { "input": "2", "w": 480, "h": 270 },
    { "input": "3", "w": 480, "h": 270 },
]
RECORDINGS=[
    { "input": "mix", },
    { "input": "0", },
    { "input": "1", },
    { "input": "2", },
    { "input": "3", },
]
