import pygame.midi
import threading
import time
import atexit

midi = pygame.midi
midi.init()
mixer = pygame.mixer
mixer.init()

i = midi.Input(1)
o = midi.Output(2)

def passthrough():
	while True:
		b = i.read(50)
		o.write(b)
		time.sleep(0.01)

def allstop():
	midi.quit()
	mixer.quit()
atexit.register(allstop)