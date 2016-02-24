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
    def open(self):
        self.midifile = MidiFile(self.filename)
        self.server_thread = threading.Thread(target=self.run)
        self.server_thread.setName("Midi song: {0}".format(self.filename))
    def play(self):
        self.break_flag = False
        self.thread = threading.Thread(target=self.thread)
    def stop(self):
        self.break_flag = True
        self.thread.join()
    def thread():
        for message in self.midifile.play():
            self.output.send(message)
            if self.break_flag:
                break;
        self.output.reset()
