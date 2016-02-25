#!/usr/bin/env python3
import argparse
import atexit
import code
import mido
import sys

from teslamidi import TeslaCoilMidi
from midi_song import MidiSong as MS

parser = argparse.ArgumentParser()
parser.add_argument("-i", "--input", help="set the input MIDI port")
parser.add_argument("-o", "--output", help="set the output MIDI port")
parser.add_argument("-l", "--list", help="list the available MIDI ports", action='store_true')
args = parser.parse_args()

if args.list:
    sys.stdout.write("Available inputs:\n")
    for i in mido.get_input_names():
        sys.stdout.write(" {0}\n".format(i))
    sys.stdout.write("Available outputs:\n")
    for i in mido.get_input_names():
        sys.stdout.write(" {0}\n".format(i))

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
    print("This program currently does not support running in script mode")
    sys.exit(1)

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
