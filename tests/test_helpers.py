
import unittest

from strikeparse import constants
from strikeparse import helpers as target


class TestHelpers(unittest.TestCase):
    def test_parse_dword_invalid_returns_zero(self):
        expected = 0
        # h isn't a valid hex character.
        actual = target.parse_dword("habcd")
        self.assertEqual(expected, actual)

    def test_parse_dword_reverses_bytepairs(self):
        # 4096  + 2 = 4098
        value = b"\x02\x00\x00\x01"
        expected = 4098
        actual = target.parse_dword(value)
        self.assertEqual(expected, actual)

    def test_parse_dword_2_bytes(self):
        # a4 01 = 420
        value = b"\xa4\x01"
        expected = 420
        actual = target.parse_dword(value, 2)
        self.assertEqual(expected, actual)

    def test_parse_dword_3_bytes_pads(self):
        # a4 1 03 00 = 420
        value = b"\xa4\x01\x03"
        expected = 12708
        actual = target.parse_dword(value)
        self.assertEqual(expected, actual)

    def test_signed_byte_int(self):
        expected = 7
        actual = target.parse_signed_byte(expected)
        self.assertEqual(expected, actual)

    def test_parse_signed_byte_zero(self):
        value = b"00"
        expected = 0
        actual = target.parse_signed_byte(value)
        self.assertEqual(expected, actual)

    def test_parse_signed_byte_positive_one(self):
        value = b"01"
        expected = 1
        actual = target.parse_signed_byte(value)
        self.assertEqual(expected, actual)

    # It is so strange I'm _forced_ to write this test.
    def test_parse_signed_byte_positive_seven(self):
        value = b'7'
        expected = 7
        actual = target.parse_signed_byte(value)
        self.assertEqual(expected, actual)


    def test_parse_signed_byte_positive_upperbound(self):
        value = b"7f"
        expected = 127
        actual = target.parse_signed_byte(value)
        self.assertEqual(expected, actual)

    def test_parse_signed_byte_negative_lowerbound(self):
        value = b"80"
        expected = -128
        actual = target.parse_signed_byte(value)
        self.assertEqual(expected, actual)

    def test_parse_signed_byte_negative_one(self):
        value = b"FF"
        expected = -1
        actual = target.parse_signed_byte(value)
        self.assertEqual(expected, actual)

    def test_parse_signed_byte_negative_two(self):
        value = b"FE"
        expected = -2
        actual = target.parse_signed_byte(value)
        self.assertEqual(expected, actual)

    def test_parse_signed_byte_invalid_exception(self):
        self.assertRaises(TypeError, target.parse_signed_byte, ["H"])

    def test_pretty_pan_center(self):
        value = 0
        expected = "0"
        actual = target.pretty_pan(value)
        self.assertEqual(expected, actual)

    def test_pretty_pan_left_hard(self):
        value = -127
        expected = "L%s" % abs(value)
        actual = target.pretty_pan(value)
        self.assertEqual(expected, actual)

    def test_pretty_pan_right_hard(self):
        value = 127
        expected = "R%s" % abs(value)
        actual = target.pretty_pan(value)
        self.assertEqual(expected, actual)

    def test_pretty_pan_left(self):
        value = -1
        expected = "L%s" % abs(value)
        actual = target.pretty_pan(value)
        self.assertEqual(expected, actual)

    def test_pretty_pan_right(self):
        value = 1
        expected = "R%s" % abs(value)
        actual = target.pretty_pan(value)
        self.assertEqual(expected, actual)

    def test_pretty_filter_type_lo(self):
        value = 0
        expected = "LO"
        actual = target.pretty_filter_type(value)
        self.assertEqual(expected, actual)

    def test_pretty_filter_type_hi(self):
        value = 1
        expected = "HI"
        actual = target.pretty_filter_type(value)
        self.assertEqual(expected, actual)

    def test_pretty_mute_group_off(self):
        value = 0
        expected = "OFF"
        actual = target.pretty_mute_group(value)
        self.assertEqual(expected, actual)

    def test_pretty_mute_group_9(self):
        value = 9
        expected = 9
        actual = target.pretty_mute_group(value)
        self.assertEqual(expected, actual)

    def test_pretty_note_off_not(self):
        value = 0
        expected = constants.NOTE_OFF[value]
        actual = target.pretty_note_off(value)
        self.assertEqual(expected, actual)

    def test_pretty_note_off_sent(self):
        value = 1
        expected = constants.NOTE_OFF[value]
        actual = target.pretty_note_off(value)
        self.assertEqual(expected, actual)

    def test_pretty_note_off_alt(self):
        value = 2
        expected = constants.NOTE_OFF[value]
        actual = target.pretty_note_off(value)
        self.assertEqual(expected, actual)

    def test_prettY_priority_low(self):
        value = 0
        expected = constants.PRIORITY[value]
        actual = target.pretty_priority(value)
        self.assertEqual(expected, actual)

    def test_prettY_priority_med(self):
        value = 1
        expected = constants.PRIORITY[value]
        actual = target.pretty_priority(value)
        self.assertEqual(expected, actual)

    def test_prettY_priority_high(self):
        value = 2
        expected = constants.PRIORITY[value]
        actual = target.pretty_priority(value)
        self.assertEqual(expected, actual)

    def test_prettY_playback_poly(self):
        value = 0
        expected = constants.PLAYBACK[value]
        actual = target.pretty_playback(value)
        self.assertEqual(expected, actual)

    def test_prettY_playback_mono(self):
        value = 1
        expected = constants.PLAYBACK[value]
        actual = target.pretty_playback(value)
        self.assertEqual(expected, actual)

    def test_pretty_fx_type_vibrato(self):
        value = 9
        expected = constants.FX_TYPE[value]
        actual = target.pretty_fx_type(value)
        self.assertEqual(expected, actual)

        