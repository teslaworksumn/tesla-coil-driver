import argparse
import atexit
import code
import mido
import sys

from teslamidi import TeslaCoilMidi
from midi_song import MidiSong as MS

parser = argparse.ArgumentParser()
parser.add_argument("-i", "--input", nargs="?", help="set the input MIDI port")
parser.add_argument("-o", "--output", help="set the output MIDI port")
args = parser.parse_args()

tcm = TeslaCoilMidi()

if args.input is None:
    sys.stderr.write("An input port is required to use passthrough mode\n")
    tcm.set_output(args.output)
else:
    tcm.set_input(args.input)
    tcm.set_output(args.output)

if sys.flags.interactive:
    print("Type `help()` to list commands.")
    print(" Type `help(command)` for help on a specific command")
else:
    print("Type `help()` to list commands.")
    print(" Type `help(command)` for help on a specific command")
    code.interact(local=dict(globals(), **locals()))

def help(command):
    if command is None:
        print("Available commands:")
        print("  passthrough()      Passes the input midi directly to the output")
    elif command is passthrough:
        print("passthrough()")
        print("  Passes the input midi directly to the output, effectively creating a software pipe between them")
        print("  This is useful for attaching a keyboard to the comptuer; allowing the computer to interrput the signal.")

def passthrough():
    tcm.passthrough()

def allstop():
    if tcm is not None:
        tcm.stop()
atexit.register(allstop)
