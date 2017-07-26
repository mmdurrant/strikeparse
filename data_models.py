from strikeparse import constants
from strikeparse import helpers


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
    0c byte                 - kit fx. FX type + values. Some values stored as 2 byte little endian
                              1 byte fx type
                              1 byte fx level
                              2 byte delay l
                              2 byte delay r
                              1 byte feedback l
                              1 byte feedback r
                              1 byte depth
                              1 byte rate
                              1 byte signed damping
                              1 byte terminator?
    
    Example:
                              04 63 1e 00 23 00 43 00 3a 24 00 00
                              04 = kitfx type = mono chorus 2
                              63 = fx level
                              1e 00 = 30 = delay l
                              23 00 = 35 = delay r
                              43  = 67 = feedback  (not used)
                              00  = 0 = feedback right
                              3a = 58 = depth
                              24 = 36 = rate
                              00 = damping (not used - signed)
                              00 = ??
    
    Example:
                              0f 63 a4 01 44 02 45 47 00 00 2a 00 
                              0f - FX type - xover delay
                              99 - FX level
                              a4 01 = 256 + 164 = 420 delay left
                              44 02 = 512 + 68 = 580 delay right
                              45 = 69 = feedback l
                              57 = 71 = feedback r
                              00 00 = who knows
                              2a = 42 = damping
                              00 = who knows

                              0e 64 20 03 2c 01 37 4e 00 00 1f 00 
                              0e - FX type - stereo delay
                              99 - fx level
                              20 03 = 768 + 32 = 800 = delay l
                              2c 01 = 256 + 44 = 300 = delay r
                              37 = 55 = feedback left
                              4e = 78 = feedback right
                              00 00 = who knows
                              2a = 42 = damping
                              00 = who knows

                              03 5c 17 00 17 00 2b 00 3a 24 00 00
                              03 5c 17 00 17 00 2b 00 3a 24 00 00
                              03 - FX type - mono chorus 1
                              5c - = 92 = fx level
                              17 00 = 23 + 0 = ??
                              17 00 = 23 + 0 = ??
                              2b 00 = 43 = feedback
                              3a = 58 = chorus depth
                              24 = 36 = chorus rate
                              00 = ??
                              00 = who knows

                              04 63 1e 00 23 00 43 00 3a 24 00 00
                              03 - FX type - mono chorus 2
                              63 = 99 = fx level
                              1e 00 = 30 + 0 = ??
                              2e 00 = 35 + 0 = ??
                              43 00 = 67 = feedback
                              3a = 58 = chorus depth
                              24 = 36 = chorus rate
                              00 = ??
                              00 = who knows

                              0d 57 a3 00 2c 01 37 37 00 00 2d 00
                              0d - fx type - mono delay
                              57 - fx level - 87
                              a3 00 = 163 = delay
                              2c 01 = 300 ???
                              37 = 55 = feedback
                              37 = 55 again?
                              00 = ??
                              00 = ??
                              2d = 45 = damp
                              00

                              0e 63 20 03 2c 01 37 4e 00 00 d9 00
                              0e - fx type - delay
                              63 = fx level = 99
                              20 03 = 800 = delay l
                              2c 01 = 300 = delay r
                              37 = 55 = feedback l
                              4e = 78 = feedback r
                              00 = ??
                              00 = ??
                              d9 = 217 = (217 - 256) = -39
                              00 = ??

                              0f 63 2c 01 58 02 47 47 00 00 bd 00
                              0f = fx type = xover dly
                              63 - level
                              2c 01 = 300 = delay l
                              58 02 = 600 = delay r
                              47 = feedback
                              47 = feedback
                              00 = ??
                              00 = ??
                              bd = 189 = (189 - 256) = -67
                              00 = ??

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

    def __str__(self):
        return "\n".join(map(str, self.instruments))

    def csv(self):
        return "\n".join(map(str, map(StrikeInstrument.csv, self.instruments)))

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
        self._parse_header(raw_header)
        inst_begin = constants.KIT_HEADER_SIZE
        inst_end = constants.KIT_HEADER_SIZE + (constants.INSTRUMENT_COUNT * constants.INSTRUMENT_SIZE)
        raw_instruments = data[inst_begin:inst_end]
        raw_sampledata = data[inst_end:]

        # Samples have to be parsed before instruments so we know who uses what.
        self._parse_samples(raw_sampledata)
        self._parse_instruments(raw_instruments)

    def _parse_header(self, data):
        """
            Header is 52 bytes
            KIT followed by SPC terminator
            4 byte little endian integer declaring header length? 0x2c/44 in every file we've found.
            What follows isn't much.
        """
        pass

    def _parse_samples(self, data):
        self._samples = StrikeSamples(data)

    def _parse_instruments(self, data):
        result = []
        
        for x in range(0, constants.INSTRUMENT_COUNT):
            start_index = x * constants.INSTRUMENT_SIZE
            end_index = start_index + constants.INSTRUMENT_SIZE
            raw_instrument = data[start_index:end_index]
            instrument = StrikeInstrument(raw_instrument, samples=self.samples)
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
    def __init__(self, raw_data=None, samples=[]):
        if raw_data:
            self._parse(raw_data, samples)

    def __str__(self):
        return """{0}
        Layer A: {1}
        Layer B: {2}
        """.format(self.trigger_spec, self.layer_a, self.layer_b)

    def csv(self):
        return ",".join([self.trigger_spec.csv(), self.layer_a.csv(), self.layer_b.csv()])

    @property
    def trigger_spec(self):
        return self._trigger_spec

    @property
    def layer_a(self):
        return self._layer_a

    @property
    def layer_b(self):
        return self._layer_b

    def _parse(self, data, samples=[]):
        raw_header = data[0:constants.INSTRUMENT_HEADER_SIZE]
        # throwaway data.
        inst_header = raw_header[0:8]
        # but make sure it's the right throwaway data.
        assert inst_header == constants.SENTINEL_INSTRUMENT_HEADER
        self._trigger_spec = StrikeInstrumentTriggerSpec(raw_header[8:11])
        raw_layers = data[constants.INSTRUMENT_HEADER_SIZE:constants.INSTRUMENT_HEADER_SIZE+(constants.INSTRUMENT_LAYER_SIZE*2)]
        assert len(raw_layers) == constants.INSTRUMENT_LAYER_SIZE*2

        self._layer_a = StrikeInstrumentLayer(raw_data=raw_layers[0:constants.INSTRUMENT_LAYER_SIZE], samples=samples)
        self._layer_b = StrikeInstrumentLayer(raw_data=raw_layers[constants.INSTRUMENT_LAYER_SIZE:], samples=samples)
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
    
    def csv(self):
        return str(self)

class StrikeInstrumentLayer(object):
    def __init__(self, raw_data=None, samples=None, *args, **kwargs):
        if raw_data:
            self._parse(raw_data, samples)

    @property
    def sample_name(self):
        return self._sample_name

    @property
    def settings_str(self):
        return """
LEVEL:
    Level:  {0}
    Pan:    {1}
    Decay:  {2}

TONE:
    Tune:   {3}
    Fine:   {4}
    Cutoff: {5}

FILTER:
    Type:   {6}
    Decay:  {7}
    Pitch:  {8}
    Filter: {9}
    Level:  {10}
        """.format(self.lvl_level, helpers.pretty_pan(self.lvl_pan), self.lvl_decay,
                   self.tone_tune, self.tone_fine, self.tone_cutoff,
                   helpers.pretty_filter_type(self.vel_filtertype),
                   self.vel_decay, self.vel_pitch, self.vel_filter, self.vel_level)

    def __str__(self):
        return "Sample {0}: {1}".format(self._sample_index, self.sample_name)
    
    def csv(self):
        return "{0}".format(self.sample_name)

    def _parse(self, data, samples=None):
        # 0-47 if there's a sample. FF if not
        self._sample_index = helpers.parse_signed_byte(data[0])
        if self._sample_index >= 0 and self._sample_index != 255:
            self._sample_name = samples.get_sample_by_index(self._sample_index)
        else:
            self._sample_name = ""
        # mystery pad byte.
        byte2 = data[1]
        self.lvl_level = helpers.parse_signed_byte(data[2])
        self.lvl_pan = helpers.parse_signed_byte(data[3])
        self.lvl_decay = helpers.parse_signed_byte(data[4])
        pad0 = data[5:8]
        self.tone_tune = helpers.parse_signed_byte(data[8])
        self.tone_fine = helpers.parse_signed_byte(data[9])
        self.tone_cutoff = helpers.parse_signed_byte(data[10])
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

    def __str__(self):
        return """
Reverb Send:    {0}
FX Send:        {1}

Priority:       {2}
Mute Group:     {3}
Playback:       {4}

MIDI Channel:   {5}
MIDI Note:      {6}
MIDI Gate Time: {7}
MIDI Note Off:  {8}
        """.format(self.send_reverb, self.send_fx, helpers.pretty_priority(self.priority),
                   helpers.pretty_mute_group(self.mutegroup),
                   helpers.pretty_priority(self.priority),
                   helpers.pretty_playback(self.playback),
                   self.midi_channel, self.midi_note, self.midi_gate,
                   helpers.pretty_note_off(self.midi_noteoff))

    def _parse(self, data):
        self.send_reverb = helpers.parse_signed_byte(data[0])
        self.send_fx =  helpers.parse_signed_byte(data[1])
        pad0 = data[2:4]
        self.priority =  helpers.parse_signed_byte(data[4])
        self.mutegroup =  helpers.parse_signed_byte(data[5])
        self.playback =  helpers.parse_signed_byte(data[6])
        self.midi_channel = helpers.parse_signed_byte(data[7])
        self.midi_note =  helpers.parse_signed_byte(data[8])
        self.midi_gate = helpers.parse_signed_byte(data[7])
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
        size_bytes = data[4:8]
        # Hey one of our more complicated functions, we only get to use it once

        table_size = helpers.parse_dword(size_bytes)
        raw_samples = data[8:]
        split_samples = map(lambda x:x.decode("utf-8"), raw_samples.split(b"\0"))
        self._sample_table = list([str(x) for x in split_samples if x != ""])


class StrikeKitSettings(object):
    def __init__(self, *args, **kwargs):
        # TODO(future) - Enum-type thing for reverb_type, map values to names
        pass
        self._reverb_type = kwargs.get("reverb_type")
        self._reverb_size = kwargs.get("reverb_size")
        self._reverb_level = kwargs.get("reverb_level")

        
    def _parse(self, data):
        
        raise NotImplementedError("Abstract class method requires implementation")


class StrikeReverbSettings(object):
    def __init__(self, *args, **kwargs):
        # TODO(future) - Enum-type thing for reverb_type, map values to names
        self._reverb_type = kwargs.get("reverb_type")
        self._reverb_size = kwargs.get("reverb_size")
        self._reverb_level = kwargs.get("reverb_level")

    @property
    def reverb_type(self):
        return self._reverb_type

    @property
    def reverb_size(self):
        return self._reverb_size

    def reverb_level(self):
        return self._reverb_level


class StrikeFxSettings(object):
    def __init__(self, *args, **kwargs):
        # TODO(future) - Enum-type thing for reverb_type, map values to names

        self._fx_type = kwargs.get("fx_type")
        self._fx_level = kwargs.get("fx_level")
        self._delay_left = kwargs.get("delay_left")
        self._delay_right = kwargs.get("delay_right")
        self._feedback_left = kwargs.get("feedback_left")
        self._feedback_right = kwargs.get("feedback_right")
        self._depth = kwargs.get("depth")
        self._rate = kwargs.get("rate")
        self._damping = kwargs.get("damp")

        def _parse(self, data):
                    """
        0c byte                 - kit fx. FX type + values. Some values stored as 2 byte little endian
                              1 byte fx type
                              1 byte fx level
                              2 byte delay l
                              2 byte delay r
                              1 byte feedback l
                              1 byte feedback r
                              1 byte depth
                              1 byte rate
                              1 byte signed damping
                              1 byte terminator?    
        """

        @property
        def fx_type(self):
            return _fx_type

        @property
        def fx_level(self):
            return _fx_level

        @property
        def delay_left(self):
            return _delay_left

        @property
        def delay_right(self):
            return _delay_right

        @property
        def feedback_left(self):
            return _feedback_left

        @property
        def feedback_right(self):
            return _feedback_right

        @property
        def depth(self):
            return _depth

        @property
        def rate(self):
            return _rate

        @property
        def damping(self):
            return _damping



