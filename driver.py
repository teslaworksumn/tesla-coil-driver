import atexit
import sys
import mido
from teslamidi import TeslaCoilMidi
from midi_song import MidiSong as MS


if len(sys.argv) != 3:
    sys.stderr.write("You must specify an input and output device\n")
    sys.stderr.write(" Usage: {0} [input] [output]\n".format(sys.argv[0]))
    sys.stderr.write("  where [input] is the name of the midi port you\n")
    sys.stderr.write("  would like to use as an input and [output] is \n")
    sys.stderr.write("  the name of the midi port you would like to use\n")
    sys.stderr.write("  as an output")
    sys.stderr.write("To list input and output devices, use `{0} list`\n")
    sys.stderr.write(" to list all, and `{0} list inputs` and\n")
    sys.stderr.write("  `{0} list outputs` to list inputs and outputs\n")
    sys.stderr.write("  respectively\n")
else:
    tcm = TeslaCoilMidi(sys.argv[1],sys.argv[2])

def allstop():
    if tcm is not None:
        tcm.stop()
atexit.register(allstop)