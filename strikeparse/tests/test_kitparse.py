import unittest
import os

from strikeparse import constants
from strikeparse import helpers

from strikeparse.data_models import StrikeKit


class TestStrikeKit(unittest.TestCase):
    def setUp(self):
        test_file = "%s\\%s" % (os.path.dirname(os.path.realpath(__file__)), "testdata.skt")
        with open(test_file, "rb") as f:
            raw_data = f.read()
            self.kit = StrikeKit(raw_data)
            # header = f.read(header_size)
            # instruments = f.read(instrument_count * instrument_size)
            # samples = f.read()

            # parse_instruments(instruments)
            # print_kit_header(header)
            # print_field("Sample data", samples)

    def test_not_none(self):
        assert self.kit is not None

    def test_instruments_not_none(self):
        assert self.kit.voices is not None
        
    def test_instruments_have_trigger_specs(self):
        assert not any(x for x in self.kit.voices if x.trigger_spec is None)

    def test_trigger_specs_print(self):
        kick = list(filter(lambda x: x.input_type == "Kick", [x.trigger_spec for x in self.kit.voices]))[0]
        # we know this because of the dataset/filter above.
        assert str(kick) == "Kick1 Head"

    def test_instruments_not_none(self):
        assert self.kit.instruments

    def test_instruments_table_length_nonzero(self):
        assert len(self.kit.instruments.instrument_table) > 0

    def test_instruments_have_layers(self):
        assert not any(x for x in self.kit.voices if x.layer_a is None)

    def test_kit_str(self):
        assert str(self.kit)

    def test_kit_csv(self):
        assert self.kit.csv()

    def test_instrument_setting_str(self):
        for x in self.kit.voices:
            print("%s\n\t%s\t%s" % (x.trigger_spec, x.layer_a.sample_name, x.layer_a.settings_str))

    def test_kit_settings_not_none(self):
        ks = self.kit.kit_settings
        assert ks
        assert ks.reverb
        assert ks.fx
    
    def test_kit_settings_reverb(self):
        ks = self.kit.kit_settings
        assert ks.reverb
        assert ks.reverb.reverb_type == "BigGate"
        self.assertEqual(ks.reverb.color, 50)
        self.assertEqual(ks.reverb.size, 75)
        self.assertEqual(ks.reverb.level, 32)
        
    def test_kit_settings_fx(self):
        fx = self.kit.kit_settings.fx
        assert fx
        self.assertEqual(fx.delay_left, 800)
        self.assertEqual(fx.delay_right, 300)
        self.assertEqual(fx.feedback_left, 55)
        self.assertEqual(fx.feedback_right, 78)
        self.assertEqual(fx.damping, 00)
        self.assertEqual(fx.level, 99)