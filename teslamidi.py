import atexit
import os
import time
import sys

import mido
#from mido import Message

import midi_song as ms

class TeslaCoilMidi:
    def __init__(self,inport_name,outport_name):
        self.inport = mido.open_input(inport_name)
        self.outport = mido.open_output(outport_name)
        self.outport.reset()
    def passthrough(self):
        while True:
            m = self.inport.receive()
            self.outport.send(m)
    def stop(self):
        self.inport.close()
        self.outport.reset()
        self.outport.close()

if len(sys.argv) != 3:
    sys.stderr.write("You must specify an inport and outport device\n")
    sys.stderr.write(" Usage: {0} [inport] [outport]\n".format(sys.argv[0]))
    sys.stderr.write(" where [inport] is one of the following:\n")
    for i in mido.get_input_names():
        sys.stderr.write(" {0}\n".format(i))
    sys.stderr.write(" and [outport] is one of the following:\n")
    for i in mido.get_input_names():
        sys.stderr.write(" {0}\n".format(i))
else:
    tcm = TeslaCoilMidi(sys.argv[1],sys.argv[2])

def allstop():
    if tcm is not None:
        tcm.stop()
atexit.register(allstop)