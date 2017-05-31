File/Kit Header
52 bytes
------------------
3 byte 0x4b4954         - Begin KIT header
2 byte 0x202c           - 32, 44
4 byte 0x00             - Padding?
2 byte 0x0063           - 00, 99
40 byte Kit data?       - Appears to be kit-specific settings, needs decoding.
------------------

Instrument Section    
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
