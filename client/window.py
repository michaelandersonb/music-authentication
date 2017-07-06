from __future__ import division, print_function

from Tkinter import *
from authenticate import *
from musickeyboard import PianoKeyboard
import computerkeyboard as compkey
import musickeyboard as musickb
from midiKeyboardInterface import startMidiKeyboard
import tkMessageBox
import os
import pygame
import threading
#import time
#from mbauth.pitch import iterpitches

from sound import pitch2sound

pitches_seen = []
stopmidi = None

def keycallback(pitch):
    print("adding pitch " + pitch + " to pitches_seen")
    pitches_seen.append(pitch)

def start():
    del pitches_seen[:]
    musickb.playsounds = compkey.playsounds = use_sound_var.get()
    musickb.highlightkeys = compkey.highlightkeys = highlight_key_var.get()
    computerkeyboard.getkeypresses()
    start_button.config(text="Start Over")
    done_button.config(state=NORMAL)
    global stopmidi
    try:
        stopmidi = startMidiKeyboard(keycallback)
    except ImportError as e:
        print("MIDI seems to be broken")

def done():
    global stopmidi
    start_button.config(text="Start")
    done_button.config(state=DISABLED)
    computerkeyboard.stopkeypresses()
    if stopmidi:
        stopmidi()
        stopmidi = None
    #print("pitches_seen is", pitches_seen)
    # now authenticate the password
    # tkMessageBox.showinfo("Authentication", authenticate(pitches_seen))
    try:
        tkMessageBox.showinfo("Authentication", authenticate(pitches_seen))
    except:
        tkMessageBox.showerror("Error", "An error occured while authenticating")


root = Tk()
root.title("Music-based Authentication Client")

kfbg = "#ccccccccc"

keyboardframe = Frame(root, bd=5, bg=kfbg, relief=GROOVE)
keyboardframe.pack(padx=20, pady=20, expand=True)

pianokeyboard = PianoKeyboard(keyboardframe, pitch2sound)
pianokeyboard.pack()

Frame(keyboardframe, height=20, width=20, bg=kfbg, bd=0).pack()

computerkeyboard = compkey.ComputerKeyboard(keyboardframe, 
                                            pitch2sound, 
                                            keycallback,
                                            done)
computerkeyboard.pack()

Frame(root, height=20, width=20, bd=0).pack()

lowerframe = Frame(root)
lowerframe.pack(expand=True, fill=Y)

use_sound_var = BooleanVar()
use_sound_var.set(True)
use_sound = Checkbutton(lowerframe, 
                        text="Play Notes", 
                        variable=use_sound_var)
use_sound.pack(side=LEFT, padx=20)

highlight_key_var = BooleanVar()
highlight_key_var.set(True)
highlight_key = Checkbutton(lowerframe,
                            text="Highlight Keys",
                            variable=highlight_key_var)
highlight_key.pack(side=LEFT, padx=20)

start_button = Button(lowerframe, text="Start", command=start)
start_button.pack(side=LEFT, padx=20)

done_button = Button(lowerframe, text="Done", state=DISABLED, command=done)
done_button.pack(side=LEFT, padx=20)
