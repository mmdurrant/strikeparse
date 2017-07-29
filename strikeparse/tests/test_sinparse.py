import unittest
import os

from strikeparse import constants
from strikeparse import helpers

from strikeparse.data_models import StrikeInstrument
from strikeparse.data_models import StrikeInstrumentSettings

class TestStrikeInstrument(unittest.TestCase):
    def setUp(self):
        single_file = "%s\\%s" % (os.path.dirname(os.path.realpath(__file__)), "single.sin")
        self.settings_data = b'\x00\x03\x01\x00\x00\x00\x1d\xf3\x0a\x00\x00\x0c\xe8\x2a\x00\xe0\xe0\xed\x41\x00\x7f\x00\x00\x00'
        self.sample_record = b'\x00\x00\x63\x79\x7f\x3c\x3c\x06\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x40\x00\x00\x00\x00\x00\x3c\x00\x00\x00'

        with open(single_file, "rb") as f:
            raw_data = f.read()
            self.instrument = StrikeInstrument(raw_data=raw_data)
            

    def test_not_none(self):
        assert self.instrument is not None

    def test_has_settings(self):
        assert self.instrument.settings is not None

    def test_settings_parse(self):
        actual = StrikeInstrumentSettings(raw_data=self.settings_data)
        self.assertIsNotNone(actual)
        self.assertEqual(29, actual.level)
        self.assertEqual(-13, actual.pan)
        self.assertEqual(10, actual.decay)
        self.assertEqual(42, actual.cutoff)
        self.assertEqual(12, actual.tune_semitones)
        self.assertEqual(-24, actual.tune_fine)
        self.assertEqual(0, actual.filter_type)
        self.assertEqual(65, actual.velocity_volume)
        self.assertEqual(-19, actual.velocity_filter)
        self.assertEqual(-32, actual.velocity_decay)
        self.assertEqual(-32, actual.velocity_tune)

