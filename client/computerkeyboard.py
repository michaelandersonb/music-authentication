from __future__ import division, print_function

import pygame
import threading
import time

from Tkinter import *

lastkey = None
playsounds = False
highlightkeys = False

class Key(object):
    def __init__(self, xleft, ytop, xright, ybottom, name, canvas,
                 outlinecolor="black"):
        self.xleft = xleft
        self.ytop = ytop
        self.xright = xright
        self.ybottom = ybottom
        self.name = name
        self.outlinecolor = outlinecolor
        self.itemid = None
        self.textid = None
        self.width = 1.0
        self.pitch = None
        #self.tags = [tags] if isinstance(tags, str) else list(tags)
        #self.tags.append("_DELETABLE")
        #self.mouseuphandler = mouseuphandler
        self.fill = "#ccccccccc"
        self.canvas = canvas
        self.sound = None
        self._ispressed = False
        #self.keynum = None
    
    def keydown(self):
        global lastkey
        if lastkey:
            lastkey.draw()
        #print("Keydown", self.pitch)
        pygame.mixer.stop()
        if highlightkeys:
            self._ispressed = True
        if playsounds and self.sound:
            self.sound.play()
        self.draw()
    
    def keyup(self):
        global lastkey
        #print("Keyup", self.pitch)
        self._ispressed = False
        if self.sound:
            #self.sound.stop()
            pass
        lastkey = self
        def thread():
            time.sleep(1.0)
            self.draw()
        t = threading.Thread(target=thread)
        t.daemon = True
        t.start()
        #self.draw()
    
    def draw(self):
        fill = "#000fff000" if self._ispressed else self.fill
        if self.itemid == None:
            self.itemid = self.canvas.create_rectangle(self.xleft,
                                                       self.ytop,
                                                       self.xright,
                                                       self.ybottom,
                                                       outline="black",
                                                       width=self.width,
                                                       fill=fill,
                                                       tags=(self.name,))
        else:
            self.canvas.itemconfig(self.itemid, fill=fill)
        
        textfill = "white" if self.fill == "black" else "black"
        if self.pitch and not self.textid:
            posX = self.xleft + (self.xright - self.xleft) / 2
            posY = self.ytop + (self.ybottom - self.ytop) / 2
            self.textid = self.canvas.create_text((posX, posY), 
                                                  text=self.pitch,
                                                  fill=textfill)
        elif self.pitch:
            self.canvas.itemconfig(self.textid, fill=textfill)
        #if self.mouseuphandler:
        #    canvas.tag_bind(itemid, "<Button-1>", self.mouseuphandler)


class ComputerKeyboard(Frame):
    edgebuffer = 5
    keyheight = 40
    standardwidth = 40
    spacewidth = 8
    spaceheight = 8
    canvasheight = 5 * keyheight + 4 * spaceheight
    canvaswidth = 13 * standardwidth + 12.5 * spacewidth + \
                  standardwidth * 1.5 + spacewidth
    if not canvaswidth.is_integer():
        print("canvaswidth is {} (not integer)".format(canvaswidth))
        raise AssertionError()
    canvaswidth = int(canvaswidth)
    
    def __init__(self, parent, pitch2sound, keycallback, donecallback):
        Frame.__init__(self, parent)
        self.canvas = Canvas(self, width=self.canvaswidth + self.edgebuffer * 2, 
                                   height=self.canvasheight + 
                                       self.edgebuffer * 2,
                                   bg="#eeeeeeeee")
        self.canvas.pack()
        
        self.pitch2sound = pitch2sound
        self.keycallback = keycallback
        self.donecallback = donecallback
        
        self.firstrowkeys = []
        self.secondrowkeys = []
        self.thirdrowkeys = []
        self.fourthrowkeys = []
        self.fifthrowkeys = []
        self.keymap = None # will be dictionary
        self.allkeys = []
        
        self.make_keys()
        self.assignpitches()
        self.draw_keys()
        self.focus_set()
        
        
    def getkeypresses(self):
        self.bind("<KeyPress>", self.keydown)
        self.bind("<KeyRelease>", self.keyup)
    
    def stopkeypresses(self):
        self.unbind("<KeyPress>")
        self.unbind("<KeyRelease>")
        
    
    def keydown(self, event):
        keysym = event.keysym.upper()
        if keysym in self.keymap:
            key = self.keymap[keysym]
            if key.pitch:
                self.keycallback(key.pitch)
                key.keydown()
        else:
            pass
            #print("Keydown: keysym not in keymap:", repr(keysym))
        
    def keyup(self, event):
        keysym = event.keysym.upper()
        if keysym in self.keymap:
            key = self.keymap[keysym]
            if key.pitch:
                key.keyup()
        elif keysym == "RETURN":
            self.donecallback()
        else:
            pass
            print("Keyup: keysym not in keymap:", repr( keysym))
            
    def make_keys(self):
        # top row (numbers)
        xleft = self.edgebuffer
        ytop = self.edgebuffer
        ybottom = ytop + self.keyheight
        for keyname in "QUOTELEFT 1 2 3 4 5 6 7 8 9 0 MINUS EQUAL".split():
            xright = xleft + self.standardwidth
            self.firstrowkeys.append(Key(xleft, 
                                         ytop, 
                                         xright, 
                                         ybottom,
                                         keyname,
                                         self.canvas))
            
            xleft = xright + self.spacewidth
        xright = self.canvaswidth + self.spacewidth / 2
        
        self.firstrowkeys.append(Key(xleft, 
                                     ytop, 
                                     xright, 
                                     ybottom, 
                                     "delete",
                                     self.canvas))
        
        # 2nd from top row
        xleft = self.edgebuffer
        ytop = ybottom + self.spaceheight
        ybottom = ytop + self.keyheight
        xright = self.standardwidth + self.spacewidth + (self.standardwidth) / 2
        TABWIDTH = abs(xright - xleft)
        self.secondrowkeys.append(Key(xleft, 
                                      ytop, 
                                      xright, 
                                      ybottom, 
                                      "tab",
                                      self.canvas))
        for keyname in "Q W E R T Y U I O P BRACKETLEFT BRACKETRIGHT BACKSLASH"\
            .split():
            xleft = xright + self.spacewidth
            xright = xleft + self.standardwidth
            self.secondrowkeys.append(Key(xleft, 
                                          ytop, 
                                          xright, 
                                          ybottom, 
                                          keyname,
                                          self.canvas))
        
        # 3d from top row
        xleft = self.edgebuffer
        ytop = ybottom + self.spaceheight
        ybottom = ytop + self.keyheight
        xright = TABWIDTH + self.standardwidth / 2.0
        CAPSLOCKWIDTH = abs(xright - xleft)
        self.thirdrowkeys.append(Key(xleft, 
                                     ytop, 
                                     xright, 
                                     ybottom, 
                                     "caps lock",
                                     self.canvas))
        for keyname in '''A S D F G H J K L SEMICOLON QUOTERIGHT'''.split():
            xleft = xright + self.spacewidth
            xright = xleft + self.standardwidth
            self.thirdrowkeys.append(Key(xleft, 
                                         ytop, 
                                         xright, 
                                         ybottom, 
                                         keyname,
                                         self.canvas))
        xleft = xright + self.spacewidth
        xright = self.canvaswidth + self.edgebuffer
        self.thirdrowkeys.append(Key(xleft, 
                                     ytop, 
                                     xright, 
                                     ybottom, 
                                     "enter",
                                     self.canvas))
        
        # 4th from top row
        xleft = self.edgebuffer
        ytop = ybottom + self.spaceheight
        ybottom = ytop + self.keyheight
        xright = CAPSLOCKWIDTH + self.spacewidth + (self.standardwidth) / 2
        LEFTSHIFTWIDTH = abs(xright - xleft)
        self.secondrowkeys.append(Key(xleft, 
                                      ytop, 
                                      xright, 
                                      ybottom, 
                                      "left shift",
                                      self.canvas))        
        for keyname in "Z X C V B N M COMMA PERIOD SLASH".split():
            xleft = xright + self.spacewidth
            xright = xleft + self.standardwidth
            self.secondrowkeys.append(Key(xleft, 
                                          ytop, 
                                          xright, 
                                          ybottom, 
                                          keyname,
                                          self.canvas))
            if keyname == "C":
                spaceleft = xleft
            elif keyname == "M":
                spaceright = xright
            
        xleft = xright + self.spacewidth
        xright = self.canvaswidth + self.edgebuffer
        self.thirdrowkeys.append(Key(xleft, 
                                     ytop, 
                                     xright, 
                                     ybottom, 
                                     "right shift",
                                     self.canvas))
        
        ytop = ybottom + self.spaceheight
        ybottom = ytop + self.keyheight
        self.fifthrowkeys.append(Key(spaceleft,
                                     ytop,
                                     spaceright,
                                     ybottom,
                                     "space",
                                     self.canvas))
                                     
        self.allkeys = self.firstrowkeys + self.secondrowkeys + \
                       self.thirdrowkeys + self.fourthrowkeys + \
                       self.fifthrowkeys
        
        self.keymap = {key.name: key for key in self.allkeys}
        self.keymap["F"].width = self.keymap["J"].width = 2.0
        
    def assignpitches(self):
        pitchmap = {
            "A": "F#3",
            "Z": "G3",
            "S": "G#3",
            "X": "A3",
            "D": "A#3",
            "C": "B3",
            "V": "C4",
            "G": "C#4",
            "B": "D4",
            "H": "D#4",
            "N": "E4",
            "M": "F4",
            "K": "F#4",
            "COMMA": "G4",
            "L": "G#4",
            "PERIOD": "A4",
            "SEMICOLON": "A#4",
            "SLASH": "B4",
            "Q": "C5",
            "2": "C#5",
            "W": "D5",
            "3": "D#5",
            "E": "E5",
            "R": "F5",
            "5": "F#5",
            "T": "G5",
            "6": "G#5",
            "Y": "A5",
            "7": "A#5",
            "U": "B5",
            "I": "C6",
            "9": "C#6",
            "O": "D6",
            "0": "D#6",
            "P": "E6",
            "BRACKETLEFT": "F6",
            "EQUAL": "F#6",
            "BRACKETRIGHT": "G6"
        }
        for keyname, pitch in pitchmap.items():
            self.keymap[keyname].pitch = pitch
            self.keymap[keyname].sound = self.pitch2sound[pitch]
            if "#" in pitch:
                self.keymap[keyname].fill = "black"
            else:
                self.keymap[keyname].fill = "white"

        
    def draw_keys(self):
        #self.canvas.delete("_DELETABLE")
        for rect in self.allkeys:
            rect.draw()
