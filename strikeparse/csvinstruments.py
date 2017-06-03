import os
import sys

PARSE_DIR = None
DEBUG = True

def print_help():
    print("""
-----------------
csvinstruments.py
-----------------

Usage:

python csvinstruments.py {PARSEDIR}

Args:

    {PARSEDIR} - Directory to walk for .SIN files.  The root Instruments folder of the SD card is ideal.

    """)

def main(*args):
    if DEBUG:
        if len(args) == 1:
            PARSE_DIR = "D:\\Projects\\Music\\StrikePro\\internalSD\\Instruments"
    # print help and bail
    if len(args) == 1 and not PARSE_DIR:
        print_help()
        return
    else:
        PARSE_DIR = PARSE_DIR or args[1]

    for inst_group in os.listdir(PARSE_DIR):
        # dirs are Instrument groups.
        group_path = os.path.join(PARSE_DIR, inst_group)

        if os.path.isdir(group_path):
            # import pdb; pdb.set_trace()
            for name in filter(lambda x: str(x).endswith("sin"), os.listdir(group_path)):
                # All files in an instrument group are SIN files.
                print("{0},{1}".format(inst_group,
                                       name[0:-4]))

                




if __name__ == "__main__":
    main(*sys.argv)
