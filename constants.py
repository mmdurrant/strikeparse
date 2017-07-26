KIT_HEADER_SIZE = 52
INSTRUMENT_SIZE = 80
INSTRUMENT_COUNT = 24
INSTRUMENT_HEADER_SIZE = 12
INSTRUMENT_LAYER_SIZE = 20
INSTRUMENT_VOICE_SIZE = 28

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

REVERB_TYPE = [
    "OFF",
    "AmbBrite",
    "BdSpring",
    "BigGate",
    "CloseMic",
    "FxGate",
    "HugeSpace",
    "LgSpacy",
    "Md80sRm",
    "MdHrdRm",
    "MdSoftRm",
    "MetalCav",
    "RmSmlDrk",
    "RoomGate",
    "SeaWolf",
    "Slapper",
    "SmBathRm",
    "SmPlate",
    "SmlBrite",
    "Studio",
    "Warehouse",
    "WoodRm",
    "WrmStudio"
]

SENTINEL_INSTRUMENT_HEADER = b"instH\x00\x00\x00"