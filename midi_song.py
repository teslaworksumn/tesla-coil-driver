import mido
from mido import MidiFile
import threading
import traceback

class MidiSong:
    def __init__(self,filename,output):
        self.filename = filename
        self.output = output
        self.midifile = None
        self.midifile = MidiFile(self.filename)
        self.playing = threading.Event()
        self.playing.clear()
        self.stopped = threading.Event()
        self.stopped.set()
        self.thread = None
        self.open()
    def open(self):
        if self.thread is not None:
            self.stop()
        self.midifile = MidiFile(self.filename)
    def play(self):
        #print("1: n:{0},p:{1},s:{2}".format(self.filename,self.playing.is_set(), self.stopped.is_set()))
        if self.playing.is_set():
            self.pause()
        else:
            if not self.stopped.is_set():
                self.stop()
            self.thread = threading.Thread(target=self.runnable)
            self.thread.setName("MIDI song: {0}".format(self.filename))
            self.thread.start()
        #print("2: n:{0},p:{1},s:{2}".format(self.filename,self.playing.is_set(), self.stopped.is_set()))
    def pause(self):
        if self.playing.is_set():
            self.playing.clear()
            self.output.reset()
        else:
            self.playing.set()
    def stop(self):
        #print("1: n:{0},p:{1},s:{2}".format(self.filename,self.playing.is_set(), self.stopped.is_set()))
        self.stopped.set()
        self.playing.set()
        self.thread.join()
        self.playing.clear()
        self.output.reset()
        #print("2: n:{0},p:{1},s:{2}".format(self.filename,self.playing.is_set(), self.stopped.is_set()))
    def wait(self, timeout=None):
        self.stopped.wait(timeout)
    def close(self):
        self.stop()
        self.midifile.close()
    def runnable(self):
        self.stopped.clear()
        self.playing.set()
        for message in self.midifile.play():
            self.playing.wait()
            self.output.send(message)
            if self.stopped.is_set():
                break;
        self.output.reset()
        self.playing.clear()
        self.stopped.set()
