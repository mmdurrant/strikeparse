
import unittest

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
