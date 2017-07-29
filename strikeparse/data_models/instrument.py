from strikeparse import constants
from strikeparse import helpers

from sortedcontainers import SortedList

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
        header_raw = data[8:8+header_size]
        self._settings = StrikeInstrumentSettings(raw_data=header_raw)
        # msmp header
        msmp_header = str(data[32:36], "ascii")
        assert msmp_header == constants.SENTINEL_INSTRUMENT_MSMP_HEADER
        # msmp length
        msmp_length = helpers.parse_dword(data[36:40])
        cycle_mode = data[40]
        assert cycle_mode in (0, 1)
        byte0 = data[41]
        sample_count = data[42]
        flag0 = data[43]
        # This changes depending on the type of file we're reading.
        # This should fix that.
        sample_size = int((msmp_length - 4) / sample_count)
        # make sure it's a normal sample size
        assert sample_size in (28, 30)
        range_upper = int(44 + (sample_size * sample_count))
        raw_ranges = data[44:range_upper]
        
        # Parse the sample data out.
        velocity_samples = []
        read_offset = 0
        for i in range(0, sample_count - 1):
            raw_sample = raw_ranges[0:sample_size]
            vel_sample = StrikeInstrumentVelocitySample(raw_sample)



class StrikeInstrumentVelocitySample(object):
    def __init__(self, *args, **kwargs):
        # A velocity range includes min-max pairs and a list of samples.
        self._vel_lbound = 0
        self._vel_ubound = 127
        self._range_samples = []
        self._sample_index = -1
        self._sample_order = -1
        self._volume_pad = 64

        raw_data = kwargs.get("raw_data")
        if raw_data:
            self._parse(raw_data)
        else:
            pass

        def _parse(self, data):
            self._sample_index = helpers.parse_signed_byte(data[0:2])
            byte1 = helpers.parse_signed_byte(data[2])
            self._vel_lbound = data[3]
            self._vel_ubound = data[4]
            weird_bytes = data[5:7]
            self._sample_order = data[7]
            weird_zeroes = data[8:18]
            self._volume_pad = helpers.parse_signed_byte(data[18:22])
            more_zeroes = data[22:24]
            terminator = data[24:28]


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
        self._level = data[6]
        self._pan = helpers.parse_signed_byte(data[7])
        self._decay = data[8]
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
        terminator = data[20:24]
        assert terminator == constants.SENTINEL_INSTRUMENT_HEADER_TERM, "%s was not terminator" % terminator

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
        return self._tune_semitone

    @property
    def tune_fine(self):
        return self._tune_fine

    @property
    def filter_type(self):
        return self._filter_type

    @property
    def velocity_decay(self):
        return self._vel_decay

    @property
    def velocity_tune(self):
        return self._vel_tune

    @property
    def velocity_filter(self):
        return self._vel_filter

    @property
    def velocity_volume(self):
        return self._vel_volume

