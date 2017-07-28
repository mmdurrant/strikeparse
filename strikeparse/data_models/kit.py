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
        self._voices = None
        self._samples = None

        raw_data = kwargs.get("raw_data") or args[0]
        # parse raw data if it's there
        if raw_data:
            # Yea assignment by side effect
            self._parse_raw_kit(raw_data)

    def __str__(self):
        return "\n".join(map(str, self.voices))

    def csv(self):
        return "\n".join(map(str, map(StrikeKitVoice.csv, self.voices)))

    @property
    def kit_settings(self):
        return self._kit_settings

    @property
    def voices(self):
        return self._voices

    @property
    def samples(self):
        return self._samples

    def _parse_raw_kit(self, data):
        raw_header = data[0:constants.KIT_HEADER_SIZE]
        self._parse_header(raw_header)
        inst_begin = constants.KIT_HEADER_SIZE
        inst_end = constants.KIT_HEADER_SIZE + (constants.KITVOICE_COUNT * constants.KITVOICE_SIZE)
        raw_voices = data[inst_begin:inst_end]
        raw_sampledata = data[inst_end:]

        # Samples have to be parsed before instruments so we know who uses what.
        self._parse_samples(raw_sampledata)
        self._parse_kitvoices(raw_voices)

    def _parse_header(self, data):
        """
            Header is 52 bytes
            KIT followed by SPC terminator
            4 byte little endian integer declaring header length? 0x2c/44 in every file we've found.
            What follows isn't much.
        """
        kit_header = data[0:4]
        header_length = helpers.parse_dword(data[4:8])
        raw_header = data[8:8+header_length]
        raw_settings = raw_header[8:24]
        self._kit_settings = StrikeKitSettings(raw_settings)

    def _parse_samples(self, data):
        self._samples = StrikeKitVoiceInstruments(data)

    def _parse_kitvoices(self, data):
        result = []
        
        for x in range(0, constants.KITVOICE_COUNT):
            start_index = x * constants.KITVOICE_SIZE
            end_index = start_index + constants.KITVOICE_SIZE
            raw_instrument = data[start_index:end_index]
            instrument = StrikeKitVoice(raw_instrument, samples=self.samples)
            result.append(instrument)
        self._voices = result




class StrikeKitVoiceInstruments(object):
    def __init__(self, raw_data=None, *args, **kwargs):
        if raw_data:
            self._parse(raw_data)

    @property
    def instrument_table(self):
        return self._instrument_table

    def get_instrument_by_index(self, index):

        return self._instrument_table[index]

    def _parse(self, data):
        """
        Instrument table is at the end of file. This makes things a little easier
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
        self._instrument_table = list([str(x) for x in split_samples if x != ""])


class StrikeKitSettings(object):
    def __init__(self, raw_data=None, *args, **kwargs):
        # TODO(future) - Enum-type thing for reverb_type, map values to names
        if raw_data:
            self._parse(raw_data)

        
    def _parse(self, data):
            self._reverb = StrikeReverbSettings(raw_data=data[0:4])
            self._fx = StrikeFxSettings(raw_data=data[4:16])

    @property
    def reverb(self):
        return self._reverb

    @property
    def fx(self):
        return self._fx

class StrikeReverbSettings(object):
    def __init__(self, raw_data=None, *args, **kwargs):
        # TODO(future) - Enum-type thing for reverb_type, map values to names
        if raw_data:
            self._parse(raw_data)
        else:
            self._reverb_type = kwargs.get("reverb_type")
            self._reverb_size = kwargs.get("reverb_size")
            self._reverb_level = kwargs.get("reverb_level")
            self._reverb_color = kwargs.get("reverb_color")

    @property
    def reverb_type(self):
        return self._reverb_type

    @property
    def size(self):
        return self._reverb_size

    @property
    def level(self):
        return self._reverb_level

    @property
    def color(self):
        return self._reverb_color

    def _parse(self, data):
        self._reverb_type_val = data[0]
        self._reverb_type = helpers.pretty_reverb_type(self._reverb_type_val)
        self._reverb_size = data[1]
        self._reverb_color = data[2]
        self._reverb_level = data[3]

class StrikeFxSettings(object):
    def __init__(self, raw_data=None, *args, **kwargs):
        if raw_data:
            self._parse(raw_data)
        else:
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
        self._fx_type_val = data[0]
        self._fx_type = helpers.pretty_fx_type(self._fx_type_val)
        self._fx_level = data[1]
        self._delay_left = helpers.parse_dword(data[2:4])
        self._delay_right = helpers.parse_dword(data[4:6])
        self._feedback_left = data[6]
        self._feedback_right = data[7]
        self._depth = data[8]
        self._rate = data[9]
        self._damping = helpers.parse_signed_byte(data[10])
        mystery_byte = data[11]


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
        return self._fx_type

    @property
    def level(self):
        return self._fx_level

    @property
    def delay_left(self):
        return self._delay_left

    @property
    def delay_right(self):
        return self._delay_right

    @property
    def feedback_left(self):
        return self._feedback_left

    @property
    def feedback_right(self):
        return self._feedback_right

    @property
    def depth(self):
        return self._depth

    @property
    def rate(self):
        return self._rate

    @property
    def damping(self):
        return self._damping