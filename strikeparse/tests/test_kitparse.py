import unittest
import os
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
        assert self.kit.instruments is not None
        
    def test_instruments_have_trigger_specs(self):
        assert not any(x for x in self.kit.instruments if x.trigger_spec is None)

    def test_trigger_specs_print(self):
        kick = list(filter(lambda x: x.input_type == "Kick", [x.trigger_spec for x in self.kit.instruments]))[0]
        assert str(kick) == "Kick1 Head"

    def test_samples_not_none(self):
        assert self.kit.samples

    def test_samples_sample_table_length_nonzero(self):
        assert len(self.kit.samples.sample_table) > 0
