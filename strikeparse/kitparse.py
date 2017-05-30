from . import helpers

kit_file = "layerb.skt"

header_size = 52
instrument_size = 80
instrument_count = 24

class StrikeKit(object):
    """
    File/Kit Header
    52 bytes
    ------------------
    03 byte 0x4b4954        - Begin KIT header
    02 byte 0x202c          - 32, 44
    04 byte 0x00            - Padding?
    02 byte 0x0063          - 00, 99
    04 byte                 - Flag data?
    04 byte                 - kit settings - reverb type, size, color, level
    33 byte Kit data?       - Appears to be kit-specific settings, needs decoding.
    """
    def __init__(self, *args, **kwargs):
        self._kit_settings = None
        self._instruments = None
        self._samples = None

        raw_data = kwargs.get("raw_data") or args[0]
        # parse raw data if it's there
        if raw_data:
            # Yea assignment by side effect
            self._parse_raw_kit(raw_data)
        # else extract kwargs
        else:
            instruments = kwargs.get("instruments")
            samples = kwargs.get("samples")

    @property
    def kit_settings(self):
        return self._kit_settings

    def _parse_raw_kit(self, data):
        self._kit_settings = self._parse_kit_settings(data)
        self._parse_instruments(data)
        pass

    def _parse_kit_settings(self, data):
        # header
        header_data = data[0:52]
        # KIT header
        kit_bytes = header_data[0:3]
        print_field("KIT Header", kit_bytes)
        # No idea. 0x202c (32,44)
        field0 = header_data[3:5]
        print_field("Pad bytes", field0)
        # Zero pad?
        pad0 = header_data[5:9]
        print_field("Zero pad", pad0)
        # 0x0063 - no idea - kit volume?
        field0 = header_data[9:11]
        # kitfx - reverb
        kitfx_reverb = header_data[11:15]
        print_field("Kit reverb", kitfx_reverb)

    def _parse_instruments(self, data):
        result = []
        instraw_length = instrument_size * instrument_count
        # offset the header.
        inst_offset = instraw_length + header_size
        # get the slice header:(instcount * instsize)
        instrument_data = data[header_size:inst_offset]
        for x in range(0, instrument_count):
            start_index = x * instrument_size
            end_index = start_index + instrument_size
            instrument = instrument_data[start_index:end_index]
            result.append(instrument)
        self._instruments = result

class StrikeInstrument(object):
    pass

class StrikeSamples(object):
    pass

class KitSettings(object):
    def __init__(self, *args, **kwargs):
        # TODO(future) - Enum-type thing for reverb_type, map values to names
        self._reverb_type = kwargs.get("reverb_type")
        self._reverb_size = kwargs.get("reverb_size")
        self._reverb_level = kwargs.get("reverb_level")

class Parseable(object):
    def __init__(self, raw):
        self.parse(raw)

    def parse(self, data):
        # Parse method is responsible for populating private vars.
        raise NotImplementedError("Abstract class method requires implementation")

# This function exists purely because VS Code can't collapse comment blocks.
# Ignore freely.

def doc_func():
    print("This function should never get called.")
    assert False
  
"""
    Instrument section
    80 bytes

    offset      13 (that's weird) byte header
            ------------------
            4 byte 0x696e7374       - Begin "inst" header
            1 byte 0x48             - "H" ???
            3 byte 0x00             - Padding
            3 byte trigger spec     - (K|S|T|H|C|R)([1-4])(H|R|F|B|E|D)
                                        Kick/Snare/Tom/Hat/Crash/Ride
                                        1-4 for Toms, 1-3 Crash, 1 everything else
                                        Head/Rim for pads
                                        Foot/Edge/Bow for Hat
                                        Edge/Bow for Crashes
                                        D/B/E for Rides, not sure which is bow and bell
            1 byte                  - 0x20 (SPC) terminator ?
            1 byte sample ref       - offset of sample as listed in sample section?
            1 byte                  - 0x00 padding?
            1 byte level            - 0x00 to 0x63
            1 byte pan              - this is fun. Values > 128 are panned left. 255 - pan. Values < 128 are panned right.
            1 byte decay            - 0x00 to 0x63
            2 byte pad?             - 0x00
            1 byte Tune             - 0-12 = +, 243-255 = -
            1 byte fine             - 0-127 positive, 255-* negative
            1 byte cutoff           - 0-127 positive, 255-* negative
            1 byte ?                - 
            1 byte ?                - 
            1 byte vel decay        -
            1 byte vel filter       -
            1 byte vel level        - 
            1 byte vel pitch        - 



    Samples section
    4 byte 'str '            - marks beginning of record
    2 byte str length        - bytes are swapped (c802 == 02c8 == 712)
    2 byte pad               - might be part of string length?
    """

def print_field(descriptor, data):
    print("{0}\t:{1}\tLength:{2}".format(descriptor, data, len(data)))

def parse_file(filepath):
    with open(kit_file, "rb") as f:
        raw_data = f.read()
        x = StrikeKit(raw_data)
        # header = f.read(header_size)
        # instruments = f.read(instrument_count * instrument_size)
        # samples = f.read()

        # parse_instruments(instruments)
        # print_kit_header(header)
        # print_field("Sample data", samples)




def print_kit_header(data):
    # KIT header
    kit_bytes = data[0:3]
    print_field("KIT Header", kit_bytes)
    # No idea. 0x202c (32,44)
    field0 = data[3:5]
    print_field("Pad bytes", field0)
    # Zero pad?
    pad0 = data[5:9]
    print_field("Zero pad", pad0)
    # 0x0063 - no idea - kit volume?
    field0 = data[9:11]
    # kitfx - reverb
    kitfx_reverb = data[11:15]
    print_field("Kit reverb", kitfx_reverb)


def parse_instruments(data):
    result = []
    for x in range(0, instrument_count):
        start_index = x * instrument_size
        end_index = start_index + instrument_size
        instrument = data[start_index:end_index]
        result.append(instrument)
    return instrument

parse_file(kit_file)

