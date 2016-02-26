import json
from midi_song import MidiSong as MS

class Playlist:
    def __init__(self, filename, midi_out):
        self.filename = filename
        self.list = []
        self.midi_out = midi_out
        self.reload()
    def reload(self):
        with open(self.filename) as json_file:
            data = json.load(json_file)
            # Check for the root level 'playlist' element
            if 'songs' not in data:
                sys.stderr.write("Error: Invalid JSON file (missing songs tag)\n")
            else:
                self.list = data['songs']
        for s in self.list:
            self.list[s]["player"] = MS(self.list[s]["path"], self.midi_out)
    def play(self, name):
        s = self.find_song(name)
        if s is None:
            raise PlaylistException("Song {0} not found".format(name))
        s['player'].play()
    def pause(self, name):
        s = self.find_song(name)
        if s is None:
            raise PlaylistException("Song {0} not found".format(name))
        s['player'].pause()
    def stop(self, name):
        s = self.find_song(name)
        if s is None:
            raise PlaylistException("Song {0} not found".format(name))
        s['player'].stop()
    def list_songs(self):
        for s in self.list:
            print("{0}:\t\"{1}\" - \"{2}\"".format(s, s["title"], s["artist"]))
    def find_song(self, name):
        if name is None or name == "":
            return None
        for s in self.list:
            if s == name:
                return self.list[s]
        return None
    def find_songs(self, key, value):
        s_l = []
        for s in self.list:
            try:
                if value in self.list[s][key]:
                    s_l.append(self.list[s])
            except KeyError:
                sys.stderr.write("Key {0} not found".format(key))
        return s_l
    def close(self):
        for s in self.list:
            self.list[s].close()

class PlaylistException(Exception):
    def __init__(self,*args,**kwargs):
        Exception.__init__(self,*args,**kwargs)