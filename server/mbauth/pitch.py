__all__ = ["iterpitches", "frequencies", "note_names"]


def iterpitches():
    nextnotemap = {
        "C": "C#",
        "C#": "D",
        "D": "D#",
        "D#": "E",
        "E": "F",
        "F": "F#",
        "F#": "G",
        "G": "G#",
        "G#": "A",
        "A": "A#",
        "A#": "B",
        "B": "C"
    }
    note, octave = "A", 0
    while True:
        pitch = note + str(octave)
        yield pitch
        if pitch == "C8":
            break
        octave = octave + 1 if note == "B" else octave
        note = nextnotemap[note]


frequencies = {
    "C4": 261.63,
    "C#4": 277.18, 
    "D4": 293.66, 
    "D#4": 311.13, 
    "E4": 329.63, 
    "F4": 349.23,
    "F#4": 369.99,
    "G4": 392.00,
    "G#4": 415.30,
    "A4": 440.00,
    "A#4": 466.16,
    "B4": 493.88,
}


note_names = "C C# D D# E F F# G G# A A# B".split()


def _extendfrequencies():
    frequencies["A0"] = frequencies["A4"] / 16
    frequencies["A#0"] = frequencies["A#4"] / 16
    frequencies["B0"] = frequencies["B4"] / 16
    for octave in range(1, 4):
        denominator = 2 ** (4 - octave)
        for note in note_names:
            frequencies[note + str(octave)] = \
                frequencies[note + "4"] / denominator
    for octave in range(5, 8):
        multiplier = 2 ** (octave - 4)
        for note in note_names:
            frequencies[note + str(octave)] = \
                frequencies[note + "4"] * multiplier
    frequencies["C8"] = frequencies["C4"] * 16

_extendfrequencies()