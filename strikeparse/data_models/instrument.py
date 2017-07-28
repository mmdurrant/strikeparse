from strikeparse import constants
from strikeparse import helpers

class StrikeInstrument(object):
    def __init__(self, *args, **kwargs):
        #import pdb; pdb.set_trace()
        self._settings = None
        self._instruments = None
        self._samples = None

        raw_data = kwargs.get("raw_data")
        # parse raw data if it's there
        if raw_data:
            # Yea assignment by side effect
            self._parse(raw_data)

    @property
    def voices(self):
        return self._instruments

    @property
    def settings(self):
        return self._settings

    @property
    def samples(self):
        return self._samples

    def __str__(self):
        return "\n".join(map(str, self.instruments))

    def csv(self):
        return "\n".join(map(str, map(StrikeKitVoice.csv, self.instruments)))

    def _parse(self, data):
        offset = 0
        # INST header
        header_marker = data[0:4]
        offset += len(header_marker)
        # size of data that follows (almost always 24)
        header_size = helpers.parse_dword(data[4:8])
        offset += header_size
        # raw header data to pass to parse func
        header_raw = helpers.parse_dword(data[8:8+header_size])
        self._settings = StrikeInstrumentSettings(raw_data=header_raw)

class StrikeInstrumentVelocityRange(object):
    def __init__(self, *args, **kwargs):
        # A velocity range includes min-max pairs and a list of samples.
        self._lbound = 0
        self._ubound = 127


class StrikeHiHatCymbalSettings(object):
    def __init__(self, *args, **kwargs):
        # 0-2
        self._semi_layers = None
        self._open = None
        self._semi3 = None
        self._semi2 = None
        self._semi1 = None
        self._closed = None

        

class StrikeInstrumentSettings(object):
    def __init__(self, *args, **kwargs):
        # main instrument settings
        self._level = 0
        self._pan = 0
        self._decay = 0
        self._tune_semitone = 0
        self._tune_fine = 0
        self._cutoff = 0
        self._tune_semi = 0
        self._tune_fine = 0
        self._vel_decay = 0
        self._vel_tune = 0
        self._vel_filter = 0
        self._vel_volume = 0
        self._filter_type = None

        # auto-saved pieces
        self._instrument_group = None

        data = kwargs.get("raw_data")
        #import pdb; pdb.set_trace()
        if data:
            self._parse(data)
        else:
            # get values from kwargs
            pass


    def _parse(self, data):
        byte1 = data[0]
        self._instrument_group = data[1]
        flag1 = data[2]
        byte2 = data[3]
        bytepair1 = data[4:6]
        level = data[6]
        pan = helpers.parse_signed_byte(data[7])
        decay = data[8]
        byte3 = data[9]
        byte4 = data[10]
        self._tune_semitone = helpers.parse_signed_byte(data[11])
        self._tune_fine = helpers.parse_signed_byte(data[12])
        self._cutoff = data[13]
        self._filter_type = data[14]
        self._vel_decay = helpers.parse_signed_byte(data[15])
        self._vel_tune = helpers.parse_signed_byte(data[16])
        self._vel_filter = helpers.parse_signed_byte(data[17])
        self._vel_volume = helpers.parse_signed_byte(data[18])
        byte5 = data[19]
        terminator = data[20:23]
        assert terminator == constants.SENTINEL_INSTRUMENT_HEADER_TERM

    @property
    def level(self):
        return self._level

    @property
    def pan(self):
        return self._pan

    @property
    def decay(self):
        return self._decay

    @property
    def cutoff(self):
        return self._cutoff

    @property
    def tune_semitones(self):
        return self._tune_semi

    @property
    def tune_fine(self):
        return self._tune_fine

class StrikeInstrumentSampleData(object):
    def __init__(self, *args, **kwargs):
        if "raw_data" in kwargs:
            raw_data = kwargs.get("raw_data")
            self._parse(raw_data)
        else:
            #
            pass

    def _parse(self, data):
        pass

class StrikeInstrumentFile(object):
    """
        offset      12 (that's weird) byte header
                    ------------------
        0           4 byte 0x696e7374       - Begin "INST" header
        4           4 byte 0x18000000       - 24 bytes of header data - dword


        5           3 byte 0x00             - Padding
        8           3 byte trigger spec     - (K|S|T|H|C|R)([1-4])(H|R|F|B|E|D)
                                                Kick/Snare/Tom/Hat/Crash/Ride
                                                1-4 for Toms, 1-3 Crash, 1 everything else
                                                Head/Rim for pads
                                                Foot/Edge/Bow for Hat
                                                Edge/Bow for Crashes
                                                D/B/E for Rides, not sure which is bow and bell    
        11          1 byte                  - 0x20 (SPC) terminator ?     FF if not set    

    """