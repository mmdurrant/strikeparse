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
        if raw[0:2] == "0x":
            raw = raw[2:]
        hexv = str.join("", [x for x in reversed(str(raw))])
        # we expect we don't have the necessary 0x prefix.
        rv = int("0x%s" % hexv, 16)
    except ValueError as vex:
        rv = 0

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
    reval = 0
    if type(raw) is int:
        retval = 0
        return reval
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

