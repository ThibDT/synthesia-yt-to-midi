

class PianoKeyboard:
    def __init__(self):
        pattern = ["A", ["A#", "Bb"], "B", "C", ["C#", "Db"],
                   "D", ["D#", "Eb"], "E", "F", ["F#", "Gb"], "G", ["G#", "Ab"]]

        modes = {
            "major": {
                "pattern": [2,2,1,2,2,2,1],
                "scales": ["major", "dorian", "phrygian", "lydian", "mixolydian", "minor", "locrian"]
            },
            "harmonic major": {
                "pattern": [],
                "scales": ["major", "dorian", "phrygian", "lydian", "mixolydian", "minor", "locrian"]
            },
            "melodic minor": {
                "pattern": [],
                "scales": ["major", "dorian", "phrygian", "lydian", "mixolydian", "minor", "locrian"]
            },
            "harmonic minor": {
                "pattern": [],
                "scales": ["major", "dorian", "phrygian", "lydian", "mixolydian", "minor", "locrian"]
            }
        }

        self.keys = [
            {
                "id": i,
                "midi": 21 + i,
                "note": pattern[i % len(pattern)],
                "state": False,
                "key_color": "black" if type(pattern[i % len(pattern)]) == list else "white"
            } for i in range(88)
        ]

    