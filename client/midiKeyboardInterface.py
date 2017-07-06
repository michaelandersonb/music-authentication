'''
Run: python midiKeyboardInterface.py

You must have a connected midi keyboard for this program to work. I'll potentially improve error handling.
When you call the function 'startMidiKeyboard()', a loop is started that accepts input from keyboard.
Every keystroke of the keyboard will cause a note to be played, and for a variable named: 'note_played' to 
be set. 

@author: Daryl
'''
import pygame
import pygame.midi
from time import sleep
import threading

#map notes to string value
#First value F#3 has a number value of 42
#Last value G4 has a number value of 79
#The numbers increment by a value of 1 for each half step.
def number_to_note(number):
    notes = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
    return notes[number%12] + `number/12`

#prints a list of all the attached devices
def print_devices():
    pygame.midi.init()
    for n in range(pygame.midi.get_count()):
        print (n,pygame.midi.get_device_info(n))
        
going = False


#begins the midi keyboard interface        
def startMidiKeyboard(keycallback):
    pygame.midi.init()  
    
    going = [True]
    
    def stop():
        going[0] = False # this would be cleaner in Python 3 with nonlocal
    
    def midiloop():
        #setup output port, this hooks-up to your computer's default midi synth
        port = pygame.midi.get_default_output_id()
        midi_out = pygame.midi.Output(port, 0)
        try:
            #set keyboard to piano sound
            midi_out.set_instrument(0);
        
            #setup input port, usually the keyboard will be on port 1
            input_device = pygame.midi.Input(1)
            print "Program Starting, accepting input." #for debugging
            while going[0]:
                #await input from keyboard
                if input_device.poll():
                    #parse the data in the piano keystroke
                    event = input_device.read(1)[0]      
                    data = event[0]
                    timestamp = event[1]
                    note_number = data[1]
                    velocity = data[2]
                
                    # If velocity is 0, that means that the key has been
                    # released and we need to turn the note off.
                    # else, we need play the note.
                    if velocity == 0:    
                        midi_out.note_off(note_number,velocity)
                    else:
                        midi_out.note_on(note_number,velocity)   
                        note_played = number_to_note(note_number)
                        keycallback(note_played)
                        #print 'Note: ' + note_played
        finally:
            del midi_out
            del input_device
            pygame.midi.quit()
    
    t = threading.Thread(target=midiloop)
    t.daemon = True
    t.start()
    return stop
    
 
#run the midi keyboard    
#startMidiKeyboard()  
#print_devices()