KIT_HEADER_SIZE = 52
INSTRUMENT_SIZE = 80
INSTRUMENT_COUNT = 24
INSTRUMENT_HEADER_SIZE = 12
INSTRUMENT_LAYER_SIZE = 20
INSTRUMENT_VOICE_SIZE = 28

SWAP_KV = lambda x: dict([(v, k) for k, v in x.items()])
TUPLE_SWAP = lambda x: (x[1], x[0])

INPUT_TYPES = {
    "K": "Kick",
    "S": "Snare",
    "T": "Tom",
    "C": "Crash",
    "R": "Ride",
    "H": "HiHat"
}

INPUT_PINS = {
    "H": "Head",
    "R": "Rim",
    "F": "Foot Splash",
    "B": "Bow",
    "E": "Edge",
    "D": "Bell"
}

NOTE_OFF = [
    "NOT SENT",
    "SENT",
    "ALT"
]

PRIORITY = [
    "LOW",
    "MED",
    "HI"
]

FILTER_TYPE = [
    "LO",
    "HI"
]

PLAYBACK = [
    "POLY",
    "MONO"
]

REVERB_TYPE_PAIRS = [("OFF", 255),
    ("AmbBrite", 0),
    ("BdSpring", 1),
    ("BigGate", 2),
    ("CloseMic", 3),
    ("FxGate", 4),
    ("HugeSpace", 5),
    ("LgSpacy", 6),
    ("Md80sRm", 7),
    ("MdHrdRm", 8),
    ("MdSoftRm", 9),
    ("MetalCav", 10),
    ("RmSmlDrk", 11),
    ("RoomGate", 12),
    ("SeaWolf", 13),
    ("Slapper", 14),
    ("SmBathRm", 15),
    ("SmPlate", 16),
    ("SmlBrite", 17),
    ("Studio", 18),
    ("Warehouse", 19),
    ("WoodRm", 20),
    ("WrmStudio", 21),]


REVERB_TYPE = dict(list(map(TUPLE_SWAP, REVERB_TYPE_PAIRS)))
REVERB_TYPE_VALUES = dict(REVERB_TYPE_PAIRS)

FX_TYPE_PAIRS = [
        ("OFF", -1),
        ("Mono Flanger", 0),
        ("Stereo Flanger", 1),
        ("Xover Flanger", 2),
        ("Mono Chorus 1", 3),
        ("Mono Chorus 2", 4),
        ("Stereo Chorus", 5),
        ("XOver Chorus", 6),
        ("Mono Vibrato", 7),
        ("Vibrato", 8),
        ("Mono Doubler", 9),
        ("Mono Slapback", 10),
        ("Slapback", 11),
        ("Mono Delay", 12),
        ("Delay", 13),
        ("XOver Delay", 14),
        ("Ping Pong", 15),
]

FX_TYPE = dict(list(map(TUPLE_SWAP, FX_TYPE_PAIRS)))
FX_TYPE_VALUES = dict(FX_TYPE_PAIRS)

FX_GROUP = [
    None,
    "Flanger",
    "Chorus",
    "Vibrato",
    "Doubler",
    "Slapback",
    "MonoDelay",
    "StereoDelay",
    "XOverDelay",
    "PingPong"


]
SENTINEL_INSTRUMENT_HEADER = b"instH\x00\x00\x00"