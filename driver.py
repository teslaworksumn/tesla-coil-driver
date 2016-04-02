#!/usr/bin/env python3
import argparse
import atexit
import code
import json
import mido
import random
import sys
import threading

from teslamidi import TeslaCoilMidi
from midi_song import MidiSong as MS
from playlist import Playlist as Pl

parser = argparse.ArgumentParser()
parser.add_argument("-i", "--input", help="set the input MIDI port")
parser.add_argument("-o", "--output", help="set the output MIDI port")
parser.add_argument("-l", "--list", help="list the available MIDI ports", action='store_true')
parser.add_argument("-s", "--songs", help="set the list of songs to use (see README)")
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

if args.songs is None:
    songfilename = "./songs.json"
else:
    songfilename = args.songs
pl = Pl(songfilename, tcm.outport)
current_song = None
randomizing = False
#random_thread = threading.Thread(target=random_thread_runnable)
#random_thread.setName("Random Thread")

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
            print("  passthrough()           Passes the input midi directly to the output")
            print("  panic()                 Stops all playing notes abruptly without regard to decay times")
            print("  reset()                 Sends the \"all notes off\" and \"reset all controllers\" on every channel.")
            print("")
            print("  list_songs()            Lists the files that have been automatically loaded")
            print("  reload_songs()          Reloads the files containing the list of songs")
            print("  find_songs(key, value)  Searches the playlist for the string 'value' in the field 'key', and returns all that contain the match")
            print("  whats_playing()         Prints the known info about the currently playing song")
            print("  play(song_name)         Plays the preloaded song indicated by string song_name")
            print("  pause()                 Pauses the currently playing song. If a song is already paused, it will resume playback")
            print("  stop()                  Stops the currently playing song and resets the position to the beginning")
            print("")
            print("If you get an error like \"NameError: Name 'command' is not defined\", that is not a valid command here")
        elif command is passthrough or command == "passthrough":
            print("passthrough()")
            print("  Passes the input midi directly to the output, effectively creating a software pipe between them")
            print("  This is useful for attaching a keyboard to the comptuer; allowing the computer to interrput the signal.")
            print("  NOTE: This is a blocking command, meaning that you have to press Ctrl+C to exit this mode to send the next command")
        elif command is panic or command == "panic":
            print("panic()")
            print("  Stops all playing notes abruptly without regard to decay times")
            print("  See also reset()")
        elif command is reset or command == "reset":
            print("reset()")
            print("  Sends the \"all notes off\" and \"reset all controllers\" on every channel.")
            print("  This is often used after a song, but we try to do that for you. If it didn't happen automatically, try this.")
            print("  See also panic()")
        elif command is list_songs or command == "list_songs":
            print("list_songs()")
            print("  Lists the files that have been automatically loaded.")
            print("  See README for file format")
        elif command is reload_songs or command == "reload_songs":
            print("reload_songs()")
            print("  Reloads the songs defined in ./songs.json")
            print("  See README for file format")
        elif command is find_songs or command == "find_songs":
            print("find_songs(key, value)")
            print("  Searches the playlist for the string 'value' in the field 'key', and returns all that contain the match")
        elif command is whats_playing or command == "whats_playing":
            print("whats_playing()")
            print("  Prints the known info about the currently playing song")
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
    if current_song is not None:
        pl.stop(current_song)
    tcm.passthrough()
def panic():
    tcm.outport.panic()
def reset():
    tcm.outport.reset()

def list_songs():
    pl.list_songs()
def reload_songs():
    pl.reload()
def find_songs(key, value):
    s_l = pl.find_songs(key, value)
    for s in s_l:
        print(s)
        print("{0}:\t\"{1}\" - \"{2}\"".format(s, s_l[s]["title"], s_l[s]["artist"]))

def whats_playing():
    if current_song is not None:
        pl.print_info(current_song)
    else:
        print("No song is playing")
def play(song_name):
    global current_song
    if song_name not in pl.list.keys():
        print("Error: song not found")
        return
    if current_song is not None:
        pl.stop(current_song)
    current_song = song_name
    pl.play(song_name)
def pause():
    global current_song
    if current_song is None:
        print("No song is playing")
    else:
        pl.pause(current_song)
def stop():
    global current_song
    global randomizing
    if current_song is None:
        print("No song is playing")
    else:
        pl.stop(current_song)
    if randomizing:
        randomizing = False

def randomize():
    global current_song
    global randomizing
    if current_song is not None:
        pl.stop(current_song)
    randomizing = True
    random_thread.start()

def allstop():
    if pl is not None:
        pl.close()
    if tcm is not None:
        tcm.stop()
    #sys.exit(0)
atexit.register(allstop)

class RandomThread():
    def run():
        global current_song
        global randomizing
        while randomizing:
            current_song = None
