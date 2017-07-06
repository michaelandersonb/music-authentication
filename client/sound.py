import os
import subprocess
import pygame.mixer

#from mbauth.pitch import iterpitches
from pitch import iterpitches

samples = os.path.join(os.path.dirname(__file__), "samples")

makesamples = os.path.join(os.path.dirname(__file__), "makesamples")

if not os.path.exists(samples):
    assert subprocess.call(["python2.7", makesamples]) == 0

assert os.path.exists(samples)

pygame.mixer.init()

pitch2sound = dict()

def _soundname(pitch):
    return os.path.join(samples, pitch + ".wav")

for pitch in iterpitches():
    pitch2sound[pitch] = pygame.mixer.Sound(_soundname(pitch))

