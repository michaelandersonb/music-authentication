from __future__ import division, print_function

from Tkinter import *
#from mbauth.pitch import iterpitches
from pitch import iterpitches


playsounds = False
highlightkeys = False


class IRange(object):
    """
    IRange(endinclsv) -> obj starting at 1
    IRange(start, endinclsv) -> obj starting at start
    IRange(start=<val1>, count=<val2>) 
        -> obj starting at start with next count numbers (count must be >= 1)
    
    start, count, endinclsv: (int)
    
    IRange for INCLUSIVE range
    
    Instance attributes:
    
    start: (int) the start of the range
    endinclsv: (int) the last number in the range
    """

    __slots__ = ["start", "endinclsv", "_range"]
    
    def __init__(self, *args, **kwargs):
        if len(args) == 0:
            if "start" in kwargs and "count" in kwargs:
                self.start = kwargs["start"]
                assert kwargs["count"] >= 1
                self.endinclsv = self.start + kwargs["count"] - 1
            else:
                raise TypeError("IRange expected at least 1 argument, got 0")
        elif len(args) == 1:
                self.start = 1
                self.endinclsv = args[0]
        elif len(args) == 2:
            self.start, self.endinclsv = args
        elif len(args) > 2:
            raise TypeError("IRange expected at most 2 arguments, got " + 
                            repr(len(args)))
        else:
            raise AssertionError("not reached")
        self._range = xrange(self.start, self.endinclsv + 1)
    
    def __len__(self):
        return len(self._range)
    
    def __iter__(self):
        return iter(self._range)
    
    def __contains__(self, x):
        return x in self._range
    
    def __repr__(self):
        return "IRange({!r}, {!r})".format(self.start, self.endinclsv)
    
    def __getitem__(self, thing):
        return self._range.__getitem__(thing)
    
    def indexby1(self, i, j=None):
        """
        obj.indexby1(number) -> ith number
        obj.indexby1(first, last) -> new IRange
        """
        if j == None:
            return self._range[i - 1]
        else:
            return IRange(self.start + i - 1, self.start + j - 1)


def indexby1(sequence, itemnum, last=None):
    """
    indexby1(sequence, i) -> ith item in sequence
    indexby1(sequence, i, last) -> items i through last (inclusive)
    """
    if last is None:
        return sequence[itemnum - 1]
    else:
        return sequence[itemnum - 1:last]


class IndexBy1List(object):
    """
    IndexBy1List(iterable) -> new IndexBy1 object
    
    This class provides methods for accesing an iterable or sequence by
    1-based indexing.
    """
    def __init__(self, iterable):
        self._list = list(iterable)
    
    def __repr__(self):
        return "IndexBy1List(" + repr(self._list) + ")"

    def __getitem__(self, item):
        if not isinstance(item, int):
            raise TypeError("indexes must be integers (no slices)")
        return self.getitem(item)
        
    def __setitem__(self, item, newvalue):
        if not isinstance(item, int):
            raise TypeError("indexes must be integers (no slices)")
        self._list[item - 1] = newvalue
    
    def __iter__(self):
        return iter(self._list)
    
    def __len__(self):
        return len(self._list)
        
    def sort(self, key=None):
        """
        obj.sort([key=function]) 
        
        sort the list, optionally calling the function in key on each item to
        extract something from each item to use for the comparison
        """
        self._list.sort(key=key)
    
    def remove(self, obj):
        """
        obj.remove(object) 
        
        remove object from the list
        """
        self._list.remove(obj)
    
    def insert(self, itemnum, obj):
        """
        obj.insert(itemnum, object)
        
        insert object before item number itemnum (the first item is itemnum 1)
        """
        self._list.insert(itemnum - 1, obj)

    def getitem(self, index):
        """
        access item number index where the index of the first item is 1
        """
        if not (1 <= index <= len(self._list)):
            raise IndexError("list index out of range")
        return self._list[index - 1]
    
    def setitem(self, index, value):
        """
        set item number index where the index of the first item is 1
        """
        assert index >= 1
        self._list[index - 1] = value
    
    def getitems(self, beginning, endinclusive):
        """
        retrieve several seccessive items
        """
        beginning_0based = beginning - 1
        end_exclusive_0based = endinclusive
        return self._list.__getitem__(slice(beginning_0based,
                                             end_exclusive_0based))
    
    def setitems(self, beginning, endinclusive, values):
        """
        set a range of items
        """
        beginning_0based = beginning - 1
        end_exclusive_0based = endinclusive
        return self._list.__setitem__(slice(beginning_0based,
                                             end_exclusive_0based),
                                      values)


keyboardwidth = 510


class Key(object):
    def __init__(self, xleft, ytop, xright, ybottom, fill, tags, 
                 mouseuphandler=None):
        self.xleft = xleft
        self.ytop = ytop
        self.xright = xright
        self.ybottom = ybottom
        self.fill = fill
        self.tags = [tags] if isinstance(tags, str) else list(tags)
        self.tags.append("_DELETABLE")
        self.mouseuphandler = mouseuphandler
        self.itemid = None
        self.ispressed = False
        self.keynum = None
        self.sound = None
    
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
        
    def draw(self, canvas):
        #fill = "black" if self.isfillblack ^ self.ispressed else "white"
        fill = "#000fff000" if self.ispressed else self.fill
        if self.itemid == None:
            self.itemid = canvas.create_rectangle(self.xleft,
                                                  self.ytop,
                                                  self.xright,
                                                  self.ybottom,
                                                  # outline="white" if self.isfillblack 
                                                  #                else "black",
                                                  outline="black",
                                                  fill=fill,
                                                  tags=tuple(self.tags))
        else:
            canvas.itemconfig(self.itemid, fill=fill)
        if self.mouseuphandler:
            canvas.tag_unbind(self.itemid, "<Button-1>")
            canvas.tag_bind(self.itemid, "<Button-1>", self.mouseuphandler)
    

# abstract class
class Keyboard(Frame):
    # abstract class property canvaswidth
    # abstract class property canvasheight
    # abstract class property skipwhitekeys
    # abstract class property whitekeyheight
    # abstract class property numwhitekeys
    # abstract class property totalnumkeys
    
    def __init__(self, parent):
        Frame.__init__(self, parent)   
        self.nodrive = True
        self.canvas = Canvas(self, width=self.canvaswidth, 
                                   height=self.canvasheight)
        self.canvas.pack(side=TOP)

        self.keyispressedlist = IndexBy1List([False] * self.totalnumkeys)
        
        self.whitekeys = None
        self.blackkeys = None
        self.allkeys = None
        
        self.makekeys()
        self.drawkeys()
    
    @staticmethod
    def _find_with_tag(rectlist, tag):
        for rect in rectlist:
            if tag in rect.tags:
                yield rect
    
    def makekeys(self):
        keysleftedge = 5
        keystopedge = 5
        whitekeyheight = self.whitekeyheight
        skipwhitekeys = self.skipwhitekeys
        numwhitekeys = self.numwhitekeys  # ALL white keys
        
        blackkeyfrontedge = keystopedge + whitekeyheight / 2
        
        whitekeywidth = keyboardwidth / numwhitekeys
        
        whitekeycoords = list()
        
        ytop = keystopedge
        ybottom = ytop + whitekeyheight
        xleft = keysleftedge
        
        whitekeys = list()
        
        def loop(whitekeynum):
            if whitekeynum == numwhitekeys:
                xright = keysleftedge + keyboardwidth
            else:
                xright = xleft + whitekeywidth
            
            mouseup = self.mouseup if not self.nodrive else None
            key = Key(xleft, ytop, xright, ybottom,
                      fill="white",
                      tags="whitekey_" + str(whitekeynum),
                      mouseuphandler=mouseup)
            whitekeys.append(key)
            coord = (xleft, ytop, xright, ybottom)
            whitekeycoords.append(coord)
            
        for whitekeynum in IRange(numwhitekeys):
            loop(whitekeynum)
            xleft += whitekeywidth
        
        blackkeys = list()
        keynum = 1
        blackkeynum = 1
        
        # minus one to not add a sharp after the last white key
        for whitekeynum in IRange(numwhitekeys - 1):
            # add 1 to go from index (starts at 0) to num (starts at 1)
            rects = list(Keyboard._find_with_tag(whitekeys, 
                                                 "whitekey_" + 
                                                 str(whitekeynum)))
            assert len(rects) == 1
            rect = rects[0]
            rect.keynum = keynum
            rect.tags.append("key_" + str(keynum))
            keynum += 1
            
            whitekeyindex = whitekeynum - 1
            if (skipwhitekeys + whitekeyindex) % 7 in (0, 1, 3, 4, 5):
                coord = whitekeycoords[whitekeyindex]
                whitekeyleftedge = coord[0]
                whitekeyrightedge = coord[2]
                width = whitekeyrightedge - whitekeyleftedge
                twothirds = width * 2 / 3
                
                xleft = whitekeyleftedge + twothirds
                xright = xleft + twothirds
                ytop = keystopedge
                ybottom = blackkeyfrontedge
                
                tags = ("blackkey_" + str(blackkeynum),
                        "key_" + str(keynum))
                key = Key(xleft, ytop, xright, ybottom,
                          fill="black", tags=tags,
                          mouseuphandler=self.mouseup)
                key.keynum = keynum
                blackkeys.append(key)

                blackkeynum += 1
                keynum += 1
                
        if True:
            whitekeynum += 1
            
            rects = list(Keyboard._find_with_tag(whitekeys, 
                                                 "whitekey_" + 
                                                 str(whitekeynum)))
            if not len(rects) == 1:
                print("len(rects) =>", len(rects))
                raise AssertionError
            rect = rects[0]
            rect.keynum = keynum
            rect.tags.append("key_" + str(keynum))
            keynum += 1
        
        allkeys = IndexBy1List(whitekeys + blackkeys)
        #print("all key rects . :", allkeys)
        allkeys.sort(key=lambda rect: rect.keynum)
    
        self.whitekeys = whitekeys
        self.blackkeys = blackkeys
        self.allkeys = allkeys
        
    def drawkeys(self):
        #self.canvas.delete("_DELETABLE")
        for rect in self.whitekeys:
            #print("ManualKeyboard.drawkeys(): rect has tags:", 
            #      repr(rect.tags))
            rect.draw(self.canvas)

        for rect in self.blackkeys:
            #print("ManualKeyboard.drawkeys(): rect has tags:", 
            #      repr(rect.tags))
            rect.draw(self.canvas)
        
        #print("\nDONE\n")
    
    def mouseup(self, event):
        canvas_x = self.canvas.canvasx(event.x)
        canvas_y = self.canvas.canvasy(event.y)
        
        items = self.canvas.find_closest(canvas_x, canvas_y)
        if len(items) == 0:
            raise Exception("no items found under mouse")
        else:
            pass  # print("ManualKeyboard.mouseup(): items found:", items)
        highestitem = items[-1]  # last item
        
        tags = self.canvas.gettags(highestitem)
        # print("ManualKeyboard.mouseup(): tags of default item:", repr(tags))
        for tag in tags:
            if tag.startswith("key_"):
                keytag = tag
                break
        else:
            raise Exception("couldn't find keynum tag on item clicked")
        
        keynum = int(keytag.replace("key_", ""))
        
        from ._globals import organ
        
        self.keyispressedlist[keynum] = newkeystate = \
            not self.keyispressedlist[keynum]
        
        aggregatekeyboard = \
            organ.organstate.keyboardsstate.keyboardstates[self.keyboardname]
            
        keyboard = aggregatekeyboard.physicalkbstate
        keyboard.keystates[keynum].isdownsig.next = newkeystate
        
        self.allkeys[keynum].ispressed = newkeystate
        
        self.drawkeys()
    
    def release_all_keys(self):
        for r in self.allkeys:
            r.ispressed = False


class OrganKeyboard(Keyboard):
    canvaswidth = 520
    canvasheight = 30
    whitekeyheight = 25
    numwhitekeys = 7 * 5 + 1
    totalnumkeys = 61
    skipwhitekeys = 0
    
    def __init__(self, parent):
        Keyboard.__init__(self, parent)


class PianoKeyboard(Keyboard):
    "PianoKeyboard(parent)"
    canvaswidth = 520
    canvasheight = 30
    whitekeyheight = 25
    numwhitekeys = 52
    totalnumkeys = 88
    skipwhitekeys = 5
    
    def __init__(self, parent, pitch2sound):
        Keyboard.__init__(self, parent)
        for key, pitch in zip(self.allkeys, iterpitches()):
            key.pitch = pitch
            key.sound = pitch2sound[pitch]
