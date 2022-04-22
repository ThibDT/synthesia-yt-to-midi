from pickle import TRUE
from colormath.color_objects import sRGBColor, LabColor
from colormath.color_conversions import convert_color
from colormath.color_diff import delta_e_cie2000
from piano import PianoKeyboard, pattern
import numpy as np
    
class KeyboardVideoController:

    def __init__(self, clip):
        self.video = clip
        self._calibration_frame = None
        self._uniformized_frame = None
        self.areas = []
        self.piano = PianoKeyboard()
        self.colors = set()
        self.channels = set()

    def calibrate(self, screenshot=False):
        self._calibration_frame = self.video.get_frame(0)
        self._uniformized_frame = self._uniformize_keys_color(self._calibration_frame)
        self._identify_areas(self._uniformized_frame)
        self._bind_areas_key()

        if screenshot:
            from moviepy.editor import ImageClip
            ImageClip(self._uniformized_frame).save_frame("frame_processed.png")

    def _uniformize_keys_color(self, frame, tolerance=100):
        new_frame = frame.copy()
        for i, px in enumerate(frame[0]):  # working on 1 px height frames => only frame[0]
            if(px.mean() >= (255 - tolerance)):
                new_frame[0][i] = [255, 255, 255]
            elif(px.mean() <= tolerance):
                new_frame[0][i] = [0, 0, 0]

        return new_frame

    def _identify_areas(self, frame, min_length=6):
        print("Identifying keys...")
        tmp_area = {
            "id": 0,
            "color": None,
            "px_indexes": []
        }

        for i, px in enumerate(frame[0]):
            m = px.mean()

            if tmp_area["color"] != m and len(tmp_area["px_indexes"]) >= min_length:
                area_start = min(tmp_area["px_indexes"])
                area_end = max(tmp_area["px_indexes"])
                self.areas.append(
                    {
                        "id": tmp_area["id"],
                        "start": area_start,
                        "end": area_end,
                        "length": area_end - area_start,
                        "color": sRGBColor(*self._calibration_frame[0][area_start:area_end].mean(axis=0).astype(int), is_upscaled=True)
                    }
                )
                tmp_area["id"] += 1
                tmp_area["px_indexes"] = []
            if m == 255 or m == 0:
                tmp_area["color"] = m
                tmp_area["px_indexes"].append(i)

        print(f"{len(self.areas)} keys identified")

    def _bind_areas_key(self, color_diff_treshold=20):
        print("Identifying position on keyboard...")
        b_found = False
        b_index = 0

        while not b_found:
            expected_b_area = self.areas[b_index]
            expected_c_area = self.areas[b_index+1]
            expected_e_area = self.areas[b_index+5]
            expected_f_area = self.areas[b_index+6]

            b_lab = convert_color(expected_b_area['color'], LabColor)
            delta_c = delta_e_cie2000(b_lab, convert_color(expected_c_area['color'], LabColor))
            delta_e = delta_e_cie2000(b_lab, convert_color(expected_e_area['color'], LabColor))
            delta_f = delta_e_cie2000(b_lab, convert_color(expected_f_area['color'], LabColor))

            if delta_c < color_diff_treshold and delta_e < color_diff_treshold and delta_f < color_diff_treshold:
                b_found = True
            else:
                b_index += 1
        
        for i, area in enumerate(self.areas):
            area["note"] = pattern[(len(pattern) + i - b_index + 2) % len(pattern)] # adding len(pattern) to safely remove b_index, +2 because b has index 2 in pattern (A, A#, B)


    def changes(self, color_diff_treshold=30):

        for i, frame in enumerate(self.video.iter_frames()):
            changes = {
                "frame": i,
                "areas": []
            }
            
            for area in self.areas:
                color = frame[0][area["start"]:area["end"]].mean(axis=0)
                frame_rgb = sRGBColor(*color)
                frame_lab = convert_color(frame_rgb, LabColor)
                area_lab = convert_color(area['color'], LabColor)

                delta_e = delta_e_cie2000(area_lab, frame_lab)

                if delta_e > color_diff_treshold:
                    changes["areas"].append(area["id"])

            yield changes
            
        