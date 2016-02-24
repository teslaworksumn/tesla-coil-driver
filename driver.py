import argparse
import atexit
import sys
import mido

from teslamidi import TeslaCoilMidi
from midi_song import MidiSong as MS

parser = argparse.ArgumentParser()
parser.add_argument("-i", "--input", nargs="?", help="set the input MIDI port")
parser.add_argument("-o", "--output", help="set the output MIDI port")
args = parser.parse_args()

tcm = TeslaCoilMidi(sys.argv[1],sys.argv[2])

def allstop():
    if tcm is not None:
        tcm.stop()
atexit.register(allstop)
