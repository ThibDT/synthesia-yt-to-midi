

class PianoKeyboard:
    def __init__(self):
        pattern = ["A", ["A#", "Bb"], "B", "C", ["C#", "Db"],
                   "D", ["D#", "Eb"], "E", "F", ["F#", "Gb"], "G", ["G#", "Ab"]]

        self.keys = [
            {
                "id": i,
                "midi": 21 + i,
                "note": pattern[i % len(pattern)],
                "state": False,
                "key_color": "black" if type(pattern[i % len(pattern)]) == list else "white"
            } for i in range(88)
        ]

    