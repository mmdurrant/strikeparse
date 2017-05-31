import struct

def parse_dword(raw):
    """Return unsigned integer from 4 byte word

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
        hexv = struct.unpack('<4B', raw)
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

