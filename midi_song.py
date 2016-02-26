import mido
from mido import MidiFile
import threading

class MidiSong:
    def __init__(self,filename,output):
        self.filename = filename
        self.output = output
        self.midifile = None
        self.midifile = MidiFile(self.filename)
        self.break_flag = False
        self.paused = False
    def open(self):
        self.midifile = MidiFile(self.filename)
        self.server_thread = threading.Thread(target=self.run)
        self.server_thread.setName("Midi song: {0}".format(self.filename))
    def play(self):
        if self.paused:
            self.pause()
        else:
            self.break_flag = False
            self.paused = False
            self.thread = threading.Thread(target=self.runnable)
            self.thread.setName("MIDI file {0}".format(self.filename))
            self.thread.start()
    def pause(self):
        self.paused = not self.paused
        self.output.reset()
    def stop(self):
        self.break_flag = True
        self.paused = False
        self.thread.join()
        self.output.reset()
    def close(self):
        self.stop()
        self.midifile.close()
    def runnable(self):
        for message in self.midifile.play():
            self.output.send(message)
            if self.break_flag:
                break;
        self.output.reset()
