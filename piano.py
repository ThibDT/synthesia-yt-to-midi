
pattern = ["A", ["A#", "Bb"], "B", "C", ["C#", "Db"],"D", ["D#", "Eb"], "E", "F", ["F#", "Gb"], "G", ["G#", "Ab"]]

class PianoKeyboard:
    def __init__(self):

        scalesPatterns = { # Unit is half tone
            "major": [2,2,1,2,2,2,1],
            "minor": [2,1,2,2,2,1,2]
        }

        self.keys = [
            {
                "id": i,
                "midi": 21 + i,
                "note": pattern[i % len(pattern)],
                "state": False,
            } for i in range(88)
        ]

    