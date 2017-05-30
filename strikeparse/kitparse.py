from . import helpers

kit_file = "layerb.skt"

kit_header_size = 52
instrument_size = 80
instrument_count = 24
instrument_header_size = 12
instrument_layer_size = 20
instrument_voice_size = 28

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

    @property
    def instruments(self):
        return self._instruments

    @property
    def samples(self):
        return self._samples

    def _parse_raw_kit(self, data):
        raw_header = data[0:kit_header_size]
        inst_begin = kit_header_size
        inst_end = kit_header_size + (instrument_count * instrument_size)
        raw_instruments = data[inst_begin:inst_end]
        raw_sampledata = data[inst_end:]

        self._parse_instruments(raw_instruments)
        self._parse_samples(raw_sampledata)


    def _parse_samples(self, data):
        self._samples = StrikeSamples(data)

    def _parse_instruments(self, data):
        result = []
        
        for x in range(0, instrument_count):
            start_index = x * instrument_size
            end_index = start_index + instrument_size
            raw_instrument = data[start_index:end_index]
            instrument = StrikeInstrument(raw_data=raw_instrument)
            result.append(instrument)
        self._instruments = result

class StrikeInstrument(object):
    def __init__(self, *args, **kwargs):
        raw_data = kwargs.get("raw_data")

        if raw_data:
            self._parse(raw_data)

    @property
    def trigger_spec(self):
        return self._trigger_spec

    def _parse(self, data):
        raw_header = data[0:instrument_header_size]
        # throwaway data.
        inst_header = raw_header[0:8]
        # but make sure it's the right throwaway data.
        assert inst_header == b"instH\x00\x00\x00"
        self._trigger_spec = StrikeInstrumentTriggerSpec(raw_header[8:11])
        raw_layers = data[instrument_header_size:instrument_header_size+instrument_layer_size*2]
        len(raw_layers)
        assert len(raw_layers) == instrument_layer_size*2
        self.layer_a = StrikeInstrumentLayer(raw_data=raw_layers[0:instrument_layer_size])
        self.layer_b = StrikeInstrumentLayer(raw_data=raw_layers[instrument_layer_size:])
        raw_voice = data[instrument_header_size+(2*instrument_layer_size):]
        assert len(raw_voice) == instrument_voice_size
        self.instrument_settings = StrikeInstrumentSettings(raw_data=raw_voice)

class StrikeInstrumentTriggerSpec(object):
    def __init__(self, raw_data=None, *args, **kwargs):
        if raw_data:
            self._parse(raw_data)

    def _parse(self, data):
        self.input_type = INPUT_TYPES.get(chr(data[0]))
        self.input_index = chr(data[1])
        self.input_pin = INPUT_PINS.get(chr(data[2]))

    def __str__(self):
        return "{0}{1} {2}".format(self.input_type, self.input_index, self.input_pin)


class StrikeInstrumentLayer(object):
    def __init__(self, *args, **kwargs):
        raw_data = kwargs.get("raw_data")

        if raw_data:
            self._parse(raw_data)

    def _parse(self, data):
        # 0-47 if there's a sample. FF if not
        # import pdb; pdb.set_trace()
        self.sample_index = helpers.parse_signed_byte(data[0])
        # mystery pad byte.
        byte2 = data[1]
        self.lvl_level = helpers.parse_signed_byte(data[2])
        self.lvl_pan = helpers.parse_signed_byte(data[3])
        self.lvl_decay = helpers.parse_signed_byte(data[4])
        pad0 = data[5:8]
        self.tone_tune = helpers.parse_signed_byte(data[8])
        self.tone_fine = helpers.parse_signed_byte(data[9])
        self.tone_cutoff = helpers.parse_signed_byte(data[10])
        # TODO(future)  - parse filtertype
        self.vel_filtertype = helpers.parse_signed_byte(data[11])
        self.vel_decay = helpers.parse_signed_byte(data[12])
        self.vel_pitch = helpers.parse_signed_byte(data[13])
        self.vel_filter = helpers.parse_signed_byte(data[14])
        self.vel_level = helpers.parse_signed_byte(data[15])
        self.pad1 = data[16]
        self.term_pad = data[17:20]

class StrikeInstrumentSettings(object):
    def __init__(self, *args, **kwargs):
        raw_data = kwargs.get("raw_data")

        if raw_data:
            self._parse(raw_data)

    def _parse(self, data):
        self.send_reverb = helpers.parse_signed_byte(data[0])
        self.send_fx =  helpers.parse_signed_byte(data[1])
        pad0 = data[2:4]
        self.priority =  helpers.parse_signed_byte(data[4])
        # TODO(parse mutegroup)
        self.mutegroup =  helpers.parse_signed_byte(data[5])
        # TODO(parse playback)
        self.playback =  helpers.parse_signed_byte(data[6])
        self.midi_channel = helpers.parse_signed_byte(data[7])
        self.midi_note =  helpers.parse_signed_byte(data[8])
        self.midi_gate = helpers.parse_signed_byte(data[7])
        # TODO(parse note off)
        self.midi_noteoff = helpers.parse_signed_byte(data[8])
        pad1 = data[9]
        ffterminator = data[10:15]
        pad2 = data[15:]

class StrikeSamples(object):
    def __init__(self, raw_data=None, *args, **kwargs):
        if raw_data:
            self._parse(raw_data)

    @property
    def sample_table(self):
        return self._sample_table

    def _parse(self, data):
        """
        Sample table is at the end of file. This makes things a little easier
        starts with a "str" type indicator, followed by space.
        
        The following 4 bytes are a 32-bit integer with the bytes stored in reverse order
        Since we get them as whole bytes, we can reverse them and parse the resulting hex.
        This number is our string length.

        Read that size til end of string. Alesis was nice and split them all on NUL boundaries
        """
        str_header = data[0:4]
        size_bytes = data[4:7]
        # Hey one of our more complicated functions, we only get to use it once
        table_size = helpers.parse_dword(size_bytes)
        raw_samples = data[8:]
        split_samples = raw_samples.split(b"\0")
        self._sample_table = [str(x) for x in split_samples if x != ""]
        

class KitSettings(object):
    def __init__(self, *args, **kwargs):
        # TODO(future) - Enum-type thing for reverb_type, map values to names
        pass
        self._reverb_type = kwargs.get("reverb_type")
        self._reverb_size = kwargs.get("reverb_size")
        self._reverb_level = kwargs.get("reverb_level")

        
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
0           4 byte 0x696e7374       - Begin "inst" header
4           1 byte 0x48             - "H" ???
5           3 byte 0x00             - Padding
8           3 byte trigger spec     - (K|S|T|H|C|R)([1-4])(H|R|F|B|E|D)
                                        Kick/Snare/Tom/Hat/Crash/Ride
                                        1-4 for Toms, 1-3 Crash, 1 everything else
                                        Head/Rim for pads
                                        Foot/Edge/Bow for Hat
                                        Edge/Bow for Crashes
                                        D/B/E for Rides, not sure which is bow and bell
-- LAYER A DATA
11          1 byte                  - 0x20 (SPC) terminator ?
12          1 byte sample ref       - offset of sample as listed in sample section?
13          1 byte                  - 0x00 padding?
14          1 byte level            - 0x00 to 0x63
15          1 byte pan              - this is fun. Values > 128 are panned left. 255 - pan. Values < 128 are panned right.
16          1 byte decay            - 0x00 to 0x63
17          2 byte pad?             - 0x00
19          1 byte Tune             - 0-12 = +, 243-255 = -
20          1 byte fine             - 0-127 positive, 255-* negative
21          1 byte cutoff           - 0-127 positive, 255-* negative
22          1 byte ?                - 
23          1 byte ?                - 
24          1 byte vel decay        -
25          1 byte vel filter       -
26          1 byte vel level        - 
27          1 byte vel pitch        -     
28          1 byte vel filtertype   - 0 lo, 1 hi

-- LAYER B DATA
32          1 byte                  - 0x20 (SPC) terminator ?
33         1 byte sample ref       - offset of sample as listed in sample section?
34          1 byte                  - 0x00 padding?
35          1 byte level            - 0x00 to 0x63
36          1 byte pan              - this is fun. Values > 128 are panned left. 255 - pan. Values < 128 are panned right.
37          1 byte decay            - 0x00 to 0x63
38          2 byte pad?             - 0x00
40          1 byte Tune             - 0-12 = +, 243-255 = -
40          1 byte fine             - 0-127 positive, 255-* negative
42          1 byte cutoff           - 0-127 positive, 255-* negative
43          1 byte vel filtertype   - 0 lo, 1 hi
44          1 byte vel decay        - 
45          1 byte vel pitch        - 
46          1 byte vel filter       -
47          1 byte vel level        - 
48          1 byte 0 pad
49          1 byte 7f terminator?
50          3 byte 0 pad

-- VOICE DATA (MIDI, sends, etc)
53          1 byte reverb send
54          1 byte FX send
55          2 byte 0 pad? 
57          1 byte (Note off or Priority? need to investigate)
58          1 byte mute group
59          1 byte playback?
60          1 byte MIDI chan
61          1 byte MIDI note
62          1 byte gate time
63          1 byte note off?
64          1 byte 0 pad?
65          5 byte FF terminator
70          11 byte zero pad?


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
        print(x)
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

# parse_file(kit_file)

