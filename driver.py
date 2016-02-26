#!/usr/bin/env python3
import argparse
import atexit
import code
import json
import mido
import sys

from teslamidi import TeslaCoilMidi
from midi_song import MidiSong as MS
from playlist import Playlist as Pl

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
    sys.exit(1)

tcm = TeslaCoilMidi()

if args.input is None:
    sys.stderr.write("An input port is required to use passthrough mode\n")
    tcm.set_output(args.output)
else:
    tcm.set_input(args.input)
    tcm.set_output(args.output)

songfilename = "./songs.json"
pl = Pl(songfilename, tcm.outport)

if sys.flags.interactive:
    print("Type `coilhelp()` to list commands.")
    print(" Type `coilhelp(command)` for help on a specific command")
else:
    print("This program currently does not support running in script mode")
    sys.exit(1)

def coilhelp(command=None):
    try:
        if command is None:
            print("Available commands:")
            print("  passthrough()      Passes the input midi directly to the output")
            print("  list_songs()       Lists the files that have been automatically loaded")
            print("  reload_songs()     Reloads the files containing the list of songs")
            print("  play(song_name)    Plays the preloaded song indicated by string song_name")
            print("  pause()            Pauses the currently playing song. If a song is already paused, it will resume playback")
            print("  stop()             Stops the currently playing song and resets the position to the beginning")
            print("If you get an error like \"NameError: Name 'command' is not defined\", that is not a valid command here")
        elif command is passthrough or command == "passthrough":
            print("passthrough()")
            print("  Passes the input midi directly to the output, effectively creating a software pipe between them")
            print("  This is useful for attaching a keyboard to the comptuer; allowing the computer to interrput the signal.")
        elif command is list_songs or command == "list_songs":
            print("list_songs()")
            print("  Lists the files that have been automatically loaded.")
            print("  See README for file format")
        elif command is reload_songs or command == "reload_songs":
            print("reload_songs()")
            print("  Reloads the songs defined in ./songs.json")
            print("  See README for file format")
        elif command is play or command == "play":
            print("play([song_name])")
            print("  Plays the preloaded song indicated by string song_name")
            print("  Control playback with pause() and stop().")
            print("  If a song is already playing when play() is called with a title (even if it's the same song!), it will reset to the beginning of the song.")
            print("  Executing play() while a song is paused will unpause the song.")
        elif command is pause or command == "pause":
            print("pause()")
            print("  Pauses the currently playing song. If a song is already paused, it will resume playback")
        elif command is stop or command == "stop":
            print("stop()")
            print("  Stops the currently playing song and resets the position to the beginning")
        else:
            print("Command not recognized, or I don't have any info on that command")
    except NameError:
        print("Command not recognized, or I don't have any info on that command")
def passthrough():
    tcm.passthrough()

def list_songs():
    pl.list()
def reload_songs():
    pl.reload()
current_song = None
def play(song_name):
    if current_song is not None:
        pl.stop(current_song)
        current_song = song_name
        pl.play(song_name)
    else:
        current_song = song_name
        pl.play(song_name)
def pause():
    if current_song is None:
        print("No song is playing")
    else:
        pl.pause(current_song)
def stop():
    if current_song is None:
        print("No song is playing")
    else:
        pl.stop(current_song)


def allstop():
    if tcm is not None:
        tcm.stop()
atexit.register(allstop)
