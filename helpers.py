import struct

from strikeparse import constants

def parse_dword(raw, wordsize=4):
    """Return unsigned integer from <param:wordsize> byte word

    :param raw: Raw 4 byte string

    :type bytestring: Accepts string of bytes

    :return: Unsigned value of reversed bytes

    :rtype: signed int
    """
    """
    The one place we have variable length data requiring a length is the string of samples.
    Bytes are stored right to left.

    Example:
    c8 02 00 00
    ... is read as 00 00 02 c8

    0200 = 512
    00c8 = 200
    02c8 = 712

    """

    rv = 0
    try:
        unpck_fmt = '<%sB' % len(raw)
        hexv = struct.unpack(unpck_fmt, raw)
        hexv = [x for x in reversed(hexv)]
        rv = int(''.join("%01x" % i for i in hexv), 16)
    except TypeError:
        print("Error - could not parse %s " % raw)
    except struct.error:
        rv = 0
    
    

    # #hexv = bytes([hex(c) for t in zip(raw[1::2], raw[::2]) for c in t])
    
    # print(hexv)
    # # we expect we don't have the necessary 0x prefix.
    # rv = int("0x%s" % hexv, 16)

    # reverse the bytes, make life easy
    return rv


def parse_signed_byte(raw):
    """Returns signed integer from byte

        :param raw: Raw byte value read from file

        :type bytestring: Accepts string of bytes

        :return: Signed value of byte

        :rtype: signed int
    """
    """
    Signed integers are stored in an interesting manner.

    Values over 127 are negative.
    255 = -1
    254 = -2

    value = x - 256
    

    """
    # if type(raw) is int:

    retval = 0
    if isinstance(raw, int):
        retval = raw
        return retval
    try:
        retval = int(raw, 16)
    except TypeError as typeex:
        raise
    
    if retval > 127:
        retval = retval - 256
    return retval


def pretty_pan(pan_data):
    """
    Prints [LR]{value} for left/right panning and returns 0 if center.
    """
    prefix = "" if pan_data == 0 else "L" if pan_data < 0 else "R"

    return "{0}{1}".format(prefix, abs(pan_data))

def pretty_filter_type(filter_type):
    return constants.FILTER_TYPE[filter_type]

def pretty_mute_group(mute_group):
    return "OFF" if mute_group == 0 else mute_group

def pretty_note_off(note_off):
    return constants.NOTE_OFF[note_off]

def pretty_priority(priority):
    return constants.PRIORITY[priority]

def pretty_playback(playback):
    return constants.PLAYBACK[playback]

def pretty_reverb_type(reverb_type):
    return constants.REVERB_TYPE[reverb_type]

def pretty_fx_type(fx_type):
    return constants.FX_TYPE[fx_type]