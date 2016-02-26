import json
from midi_song import MidiSong as MS

class Playlist:
    def __init__(self, filename, midi_out):
        self.list = []
        self.midi_out = midi_out
        self.reload()
    def reload(self):
        with open(filename) as json_file:
            data = json.load(json_file)
            # Check for the root level 'playlist' element
            if 'songs' not in data:
                sys.stderr.write("Error: Invalid JSON file (missing songs tag)\n")
            else:
                self.list = data['songs']
        for s in self.list:
            s["player"] = MS(s["filename"], self.midi_out)
    def play(self, name):
        s = self.find_song(name)
        if s is None:
            raise PlaylistException("Song {0} not found".format(name))
        s.play()
    def pause(self, name):
        s = self.find_song(name)
        if s is None:
            raise PlaylistException("Song {0} not found".format(name))
        s.pause()
    def stop(self, name):
        s = self.find_song(name)
        if s is None:
            raise PlaylistException("Song {0} not found".format(name))
        s.stop()
    def list(self):
        for s in self.list:
            print("{0}: \"{1}\" - \"{2}\"".format(s["short-name"], s["title"], s["artist"]))
    def find_song(self, name):
        if name is None or name == "":
            return None
        for s in self.list:
            if s["short-name"] == name:
                return s
        return None

class PlaylistException(Exception):
    def __init__(self,*args,**kwargs):
        Exception.__init__(self,*args,**kwargs)