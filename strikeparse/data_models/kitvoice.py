from strikeparse import constants
from strikeparse import helpers

class StrikeKitVoice(object):
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
        self._trigger_spec = StrikeKitVoiceTriggerSpec(raw_header[8:11])
        raw_layers = data[constants.INSTRUMENT_HEADER_SIZE:constants.INSTRUMENT_HEADER_SIZE+(constants.INSTRUMENT_LAYER_SIZE*2)]
        assert len(raw_layers) == constants.INSTRUMENT_LAYER_SIZE*2

        self._layer_a = StrikeKitVoiceLayer(raw_data=raw_layers[0:constants.INSTRUMENT_LAYER_SIZE], samples=samples)
        self._layer_b = StrikeKitVoiceLayer(raw_data=raw_layers[constants.INSTRUMENT_LAYER_SIZE:], samples=samples)
        raw_voice = data[constants.INSTRUMENT_HEADER_SIZE+(2*constants.INSTRUMENT_LAYER_SIZE):]
        assert len(raw_voice) == constants.INSTRUMENT_VOICE_SIZE
        self.instrument_settings = StrikeKitVoiceSettings(raw_data=raw_voice)


class StrikeKitVoiceTriggerSpec(object):
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

class StrikeKitVoiceLayer(object):
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
            self._sample_name = samples.get_instrument_by_index(self._sample_index)
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
    

class StrikeKitVoiceSettings(object):
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
