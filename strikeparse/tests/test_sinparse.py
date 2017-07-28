import unittest
import os

from strikeparse import constants
from strikeparse import helpers

from strikeparse.data_models import StrikeInstrument


class TestStrikeInstrument(unittest.TestCase):
    def setUp(self):
        single_file = "%s\\%s" % (os.path.dirname(os.path.realpath(__file__)), "single.sin")
        with open(single_file, "rb") as f:
            raw_data = f.read()
            self.instrument = StrikeInstrument(raw_data)
            

    def test_not_none(self):
        assert self.instrument is not None

    def test_has_settings(self):
        assert self.instrument