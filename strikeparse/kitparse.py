from . import helpers
from . import constants
from .data_models import StrikeKit

kit_file = "layerb.skt"


# This function exists purely because VS Code can't collapse comment blocks.
# Ignore freely.

def doc_func():
    print("This function should never get called.")
    assert False
    """  
    Samples section
    4 byte 'str '            - marks beginning of record
    2 byte str length        - bytes are swapped (c802 == 02c8 == 712)
    2 byte pad               - might be part of string length?
    """

def print_field(descriptor, data):
    print("{0}\t:{1}\tLength:{2}".format(descriptor, data, len(data)))

def parse_file(filepath):
    with open(kit_file, "rb") as f:
        raw_data = f.read()
        x = StrikeKit(raw_data)
        print(x)
        # header = f.read(header_size)
        # instruments = f.read(instrument_count * instrument_size)
        # samples = f.read()

        # parse_instruments(instruments)
        # print_kit_header(header)
        # print_field("Sample data", samples)




def print_kit_header(data):
    # KIT header
    kit_bytes = data[0:3]
    print_field("KIT Header", kit_bytes)
    # No idea. 0x202c (32,44)
    field0 = data[3:5]
    print_field("Pad bytes", field0)
    # Zero pad?
    pad0 = data[5:9]
    print_field("Zero pad", pad0)
    # 0x0063 - no idea - kit volume?
    field0 = data[9:11]
    # kitfx - reverb
    kitfx_reverb = data[11:15]
    print_field("Kit reverb", kitfx_reverb)


def parse_instruments(data):
    result = []
    for x in range(0, constants.INSTRUMENT_COUNT):
        start_index = x * constants.INSTRUMENT_SIZE
        end_index = start_index + constants.INSTRUMENT_SIZE
        instrument = data[start_index:end_index]
        result.append(instrument)
    return instrument

# parse_file(kit_file)

