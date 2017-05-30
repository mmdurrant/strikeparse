from . import constants
from . import helpers

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
        raw_header = data[0:constants.KIT_HEADER_SIZE]
        inst_begin = constants.KIT_HEADER_SIZE
        inst_end = constants.KIT_HEADER_SIZE + (constants.INSTRUMENT_COUNT * constants.INSTRUMENT_SIZE)
        raw_instruments = data[inst_begin:inst_end]
        raw_sampledata = data[inst_end:]

        # Samples have to be parsed before instruments so we know who uses what.
        self._parse_samples(raw_sampledata)
        self._parse_instruments(raw_instruments)
        


    def _parse_samples(self, data):
        self._samples = StrikeSamples(data)

    def _parse_instruments(self, data):
        result = []
        
        for x in range(0, constants.INSTRUMENT_COUNT):
            start_index = x * constants.INSTRUMENT_SIZE
            end_index = start_index + constants.INSTRUMENT_SIZE
            raw_instrument = data[start_index:end_index]
            instrument = StrikeInstrument(raw_data=raw_instrument, samples=self.samples)
            result.append(instrument)
        self._instruments = result

class StrikeInstrument(object):
    """
        Instrument section
        80 bytes

        offset      12 (that's weird) byte header
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
        11          1 byte                  - 0x20 (SPC) terminator ?     FF if not set    
            
        -- LAYER A DATA
        12          1 byte sample ref       - offset of sample as listed in sample section? FF if not set
        13          1 byte                  - 0x00 padding?
        14          1 byte level            - 0x00 to 0x63
        15          1 byte pan              - this is fun. Values > 128 are panned left. 255 - pan. Values < 128 are panned right.
        16          1 byte decay            - 0x00 to 0x63
        17          2 byte pad?             - 0x002
        19          1 byte Tune             - 0-12 = +, 243-255 = -
        20          1 byte fine             - 0-127 positive, 255-* negative
        21          1 byte cutoff           - 0-127 positive, 255-* negative
        22          1 byte vel filtertype   - 0 lo, 1 hi
        23          1 byte vel decay        - 
        24          1 byte vel pitch        - 
        25          1 byte vel filter       -
        26          1 byte vel level        - 
        27          1 byte 0 pad
        28          1 byte 7f terminator?
        29          3 byte 0 pad
        -- LAYER B DATA
        32          1 byte sample ref       - offset of sample as listed in sample section? FF if not set
        33          1 byte                  - 0x00 padding?
        34          1 byte level            - 0x00 to 0x63
        34          1 byte pan              - this is fun. Values > 128 are panned left. 255 - pan. Values < 128 are panned right.
        35          1 byte decay            - 0x00 to 0x63
        36          2 byte pad?             - 0x00
        38          1 byte Tune             - 0-12 = +, 243-255 = -
        39          1 byte fine             - 0-127 positive, 255-* negative
        40          1 byte cutoff           - 0-127 positive, 255-* negative
        41          1 byte vel filtertype   - 0 lo, 1 hi
        42          1 byte vel decay        - 
        43          1 byte vel pitch        - 
        44          1 byte vel filter       -
        45          1 byte vel level        - 
        46          1 byte 0 pad
        47          1 byte 7f terminator?
        48          3 byte 0 pad


        -- VOICE DATA (MIDI, sends, etc)
        51          1 byte reverb send
        52          1 byte FX send
        53          2 byte 0 pad? 
        55          1 byte (Note off or Priority? need to investigate)
        56          1 byte mute group
        57          1 byte playback?
        58          1 byte MIDI chan
        59          1 byte MIDI note
        60          1 byte gate time
        61          1 byte note off?
        62          1 byte 0 pad?
        63          5 byte FF terminator
        68         11 byte zero pad?
        """

    
    
    
    #
    def __init__(self, raw_data=None, *args, **kwargs):
        if raw_data:
            self._parse(raw_data)

    @property
    def trigger_spec(self):
        return self._trigger_spec

    def _parse(self, data):
        raw_header = data[0:constants.INSTRUMENT_HEADER_SIZE]
        # throwaway data.
        inst_header = raw_header[0:8]
        # but make sure it's the right throwaway data.
        assert inst_header == constants.SENTINEL_INSTRUMENT_HEADER
        self._trigger_spec = StrikeInstrumentTriggerSpec(raw_header[8:11])
        raw_layers = data[constants.INSTRUMENT_HEADER_SIZE:constants.INSTRUMENT_HEADER_SIZE+constants.INSTRUMENT_LAYER_SIZE*2]
        assert len(raw_layers) == constants.INSTRUMENT_LAYER_SIZE*2
        self.layer_a = StrikeInstrumentLayer(raw_data=raw_layers[0:constants.INSTRUMENT_LAYER_SIZE])
        self.layer_b = StrikeInstrumentLayer(raw_data=raw_layers[constants.INSTRUMENT_LAYER_SIZE:])
        raw_voice = data[constants.INSTRUMENT_HEADER_SIZE+(2*constants.INSTRUMENT_LAYER_SIZE):]
        assert len(raw_voice) == constants.INSTRUMENT_VOICE_SIZE
        self.instrument_settings = StrikeInstrumentSettings(raw_data=raw_voice)


class StrikeInstrumentTriggerSpec(object):
    def __init__(self, raw_data=None, *args, **kwargs):
        if raw_data:
            self._parse(raw_data)

    def _parse(self, data):
        self.input_type = constants.INPUT_TYPES.get(chr(data[0]))
        self.input_index = chr(data[1])
        self.input_pin = constants.INPUT_PINS.get(chr(data[2]))

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
        self._sample_index = helpers.parse_signed_byte(data[0])
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

    def get_sample_by_index(self, index):
        return self._sample_table[index]

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


class StrikeKitSettings(object):
    def __init__(self, *args, **kwargs):
        # TODO(future) - Enum-type thing for reverb_type, map values to names
        pass
        self._reverb_type = kwargs.get("reverb_type")
        self._reverb_size = kwargs.get("reverb_size")
        self._reverb_level = kwargs.get("reverb_level")

        
    def parse(self, data):
        # Parse method is responsible for populating private vars.
        raise NotImplementedError("Abstract class method requires implementation")
