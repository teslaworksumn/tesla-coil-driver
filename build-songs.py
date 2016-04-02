import os

basepath = "../tesla-coil-midi/Tesla Coil Music 1.8/MIDI/"
songs = os.path.join(basepath,"Songs")
themes = os.path.join(basepath,"Themes")

def get_songs(path):
	db = []
	for f in os.listdir(path):
		if f[0] == '.':
			break
		else:
			filename = os.path.join(path,f)
			cname = f.split(".")
			ss = cname[0].split(" - ")
			if len(ss) > 1:
				title = ss[1]
				artist = ss[0]
			else:
				title = ss[0]
				artist = ""
			db.append({"path":filename, "artist":artist, "title":title})
	return db

def print_songs(path):
	for s in get_songs(path):
		print("{0},".format(s))