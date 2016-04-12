#!/usr/bin/env python

import sys
import struct
import binascii
import time

from GoodFETAT91SAM9G20 import *
from intelhex import IntelHex16bit, IntelHex

#######################################
#   GoodFET              AT91r40008  
#     PIN                 PIN
#
#      1 <----- TDO ----> 90
#      3 <----- TDI ----> 89
#      5 <----- TMS ----> 88
#      7 <----- TCK ----> 91
#      9 <----- GND ----> GND
#     11 <----- RST ----> 79
#######################################

FLASH_BASE =    0x100000
EBI_Block  =    0xFFFFFFF
EBI_1_beg  =    0x10000000
EBI_2_beg  =    0x20000000
EBI_3_beg  =    0x30000000
EBI_4_beg  =    0x40000000
EBI_5_beg  =    0x50000000
EBI_6_beg  =    0x60000000
EBI_7_beg  =    0x70000000



def at91sam9g20_syntax():
    print "Usage: %s verb [objects]\n" % sys.argv[0]
    print "%s info" % sys.argv[0]
    print "%s dump $foo.hex [0x$start 0x$stop]" % sys.argv[0]
    print "%s ecdump $foo.hex [0x$start 0x$stop] [$chipselectregnum 0x$chipselectregvalue] - exception-handling dump" % sys.argv[0]
    print "%s erase" % sys.argv[0]
    print "%s eraseinfo" % sys.argv[0]
    print "%s flash $foo.hex [0x$start 0x$stop]" % sys.argv[0]
    print "%s verify $foo.hex [0x$start 0x$stop]" % sys.argv[0]
    print "%s poke 0x$adr 0x$val" % sys.argv[0]
    print "%s peek 0x$start [0x$stop]" % sys.argv[0]
    print "%s stat_watchdog" % sys.argv[0]
    print "%s test_disable_watchdog" % sys.argv[0]
    print "%s reset" % sys.argv[0]
    sys.exit()


def read(start, lenght, fname):
    stop=start+lenght
    f=fname
    print "Dumping from %04x to %04x as %s." % (start,stop,f)
    #h = IntelHex16bit(None)
    # FIXME: get mcu state and return it to that state
    client.halt()

    try:
        h = IntelHex(None)
        i=start
        while i<=stop:
            #data=client.ARMreadMem(i, 48)
            data=client.ARMreadChunk(i, 48, verbose=0)
            print "Dumped %06x."%i
            for dword in data:
                if i<=stop and dword != 0xdeadbeef:
                    h.puts( i, struct.pack("<I", dword) )
                i+=4
        # FIXME: get mcu state and return it to that state
    except:
        print "Unknown error during read. Writing results to output file."
        print "Rename file with last address dumped %06x."%i
        pass

    client.resume()
    h.write_hex_file(f)


client=GoodFETAT91SAM9G20()
client.serInit()
client.setup()
client.start()

read(EBI_1_beg,EBI_Block, "EBI_1.hex")
read(EBI_2_beg,EBI_Block, "EBI_2.hex")
read(EBI_3_beg,EBI_Block, "EBI_3.hex")
read(EBI_4_beg,EBI_Block, "EBI_4.hex")
read(EBI_5_beg,EBI_Block, "EBI_5.hex")
read(EBI_6_beg,EBI_Block, "EBI_6.hex")
read(EBI_7_beg,EBI_Block, "EBI_7.hex")

