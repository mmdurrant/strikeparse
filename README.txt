
kit_file = "SingleLayer.skt"

header_size = 52
instrument_size = 80
instrument_count = 24



# This function exists purely because VS Code can't collapse comment blocks.
# Ignore freely.

def doc_func():
    print("This function should never get called.")
    return 0
  
    """
    Instrument section
    80 bytes

    13 (that's weird) byte header
    ------------------
    4 byte 0x696e7374       - Begin "inst" header
    1 byte 0x48             - "H" ???
    3 byte 0x00             - Padding
    3 byte trigger spec     - (K|S|T|H|C|R)([1-4])(H|R|F|B|E|D)
                                Kick/Snare/Tom/Hat/Crash/Ride
                                1-4 for Toms, 1-3 Crash, 1 everything else
                                Head/Rim for pads
                                Foot/Edge/Bow for Hat
                                Edge/Bow for Crashes
                                D/B/E for Rides, not sure which is bow and bell
    1 byte                  - 0x20 (SPC) terminator ?
    1 byte sample ref       - offset of sample as listed in sample section?
    1 byte                  - 0x00 padding?
    1 byte level            - 0x00 to 0x63
    1 byte pan              - this is fun. Values > 128 are panned left. 255 - pan. Values < 128 are panned right.
    1 byte decay            - 0x00 to 0x63
    2 byte pad?             - 0x00
    1 byte Tune             - 0-12 = +, 243-255 = -
    1 byte fine             - 0-127 positive, 255-* negative
    1 byte cutoff           - 0-127 positive, 255-* negative
    1 byte ?                - 
    1 byte ?                - 
    1 byte vel decay        -
    1 byte vel filter       -
    1 byte vel level        - 
    1 byte vel pitch        - 



    Samples section
    4 byte 'str '            - marks beginning of record
    2 byte str length        - bytes are swapped (c802 == 02c8 == 712)
    2 byte pad               - might be part of string length?
    """

def print_field(descriptor, data):
    print("{0}\t:{1}\tLength:{2}".format(descriptor, data, len(data)))

def parse_file(filepath):
    with open(kit_file, "rb") as f:
        header = f.read(header_size)
        instruments = f.read(instrument_count * instrument_size)
        samples = f.read()
        parse_instruments(instruments)
        print_kit_header(header)
        print_field("Sample data", samples)


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
    for x in range(0, instrument_count):
        start_index = x * instrument_size
        end_index = start_index + instrument_size
        instrument = data[start_index:end_index]
        result.append(instrument)
    return instrument

parse_file(kit_file)

class StrikeKit(object):
    pass

class StrikeInstrument(object):
    pass

class StrikeSamples(object):
    pass
    
0           4 byte 0x696e7374       - Begin "inst" header
4           1 byte 0x48             - "H" ???
5           3 byte 0x00             - Padding
8           3 byte trigger spec     - (K|S|T|H|C|R)([1-4])(H|R|F|B|E|D)
                                        Kick/Snare/Tom/Hat/Crash/Ride
                                        1-4 for Toms, 1-3 Crash, 1 everything else
                                        Head/Rim for pads
                                        Foot/Edge/Bow for Hat
                                        Edge/Bow for Crashes
                                        D/B/E for Rides, not sure which is bow and bell    
11          1 byte                  - 0x20 (SPC) terminator ?     FF if not set    
    
-- LAYER A DATA
12          1 byte sample ref       - offset of sample as listed in sample section? FF if not set
13          1 byte                  - 0x00 padding?
14          1 byte level            - 0x00 to 0x63
15          1 byte pan              - this is fun. Values > 128 are panned left. 255 - pan. Values < 128 are panned right.
16          1 byte decay            - 0x00 to 0x63
17          2 byte pad?             - 0x002
19          1 byte Tune             - 0-12 = +, 243-255 = -
20          1 byte fine             - 0-127 positive, 255-* negative
21          1 byte cutoff           - 0-127 positive, 255-* negative
22          1 byte vel filtertype   - 0 lo, 1 hi
23          1 byte vel decay        - 
24          1 byte vel pitch        - 
25          1 byte vel filter       -
26          1 byte vel level        - 
27          1 byte 0 pad
28          1 byte 7f terminator?
29          3 byte 0 pad
-- LAYER B DATA
32          1 byte sample ref       - offset of sample as listed in sample section? FF if not set
33          1 byte                  - 0x00 padding?
34          1 byte level            - 0x00 to 0x63
34          1 byte pan              - this is fun. Values > 128 are panned left. 255 - pan. Values < 128 are panned right.
35          1 byte decay            - 0x00 to 0x63
36          2 byte pad?             - 0x00
38          1 byte Tune             - 0-12 = +, 243-255 = -
39          1 byte fine             - 0-127 positive, 255-* negative
40          1 byte cutoff           - 0-127 positive, 255-* negative
41          1 byte vel filtertype   - 0 lo, 1 hi
42          1 byte vel decay        - 
43          1 byte vel pitch        - 
44          1 byte vel filter       -
45          1 byte vel level        - 
46          1 byte 0 pad
47          1 byte 7f terminator?
48          3 byte 0 pad


-- VOICE DATA (MIDI, sends, etc)
51          1 byte reverb send
52          1 byte FX send
53          2 byte 0 pad? 
55          1 byte (Note off or Priority? need to investigate)
56          1 byte mute group
57          1 byte playback?
58          1 byte MIDI chan
59          1 byte MIDI note
60          1 byte gate time
61          1 byte note off?
62          1 byte 0 pad?
63          5 byte FF terminator
68         11 byte zero pad?