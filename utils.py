
class VideoController:

    def __init__(self, clip):
        self.video = clip
        self._calibration_frame = None
        self._uniformized_frame = None
        self.areas = []

    def calibrate(self):
        self._calibration_frame = self.video.get_frame(0)
        self._uniformized_frame = self._uniformize_keys_color(self._calibration_frame)
        self._identify_areas(self._uniformized_frame)

    def _uniformize_keys_color(self, frame, tolerance=80):
        new_frame = frame.copy()
        for i, px in enumerate(frame[0]):  # working on 1 px height frames
            if(px.mean() >= (255 - tolerance)):
                new_frame[0][i] = [255, 255, 255]
            elif(px.mean() <= tolerance):
                new_frame[0][i] = [0, 0, 0]

        return new_frame

    def _identify_areas(self, frame, min_length=5):
        tmp_area = {
            "id": 1,
            "color": None,
            "px_indexes": []
        }

        for i, px in enumerate(frame[0]):
            m = px.mean()

            if tmp_area["color"] != m and len(tmp_area["px_indexes"]) >= min_length:
                area_start = min(tmp_area["px_indexes"])
                area_end = max(tmp_area["px_indexes"]) + 1
                self.areas.append(
                    {
                        "id": tmp_area["id"],
                        "color": tmp_area["color"],
                        "start": area_start,
                        "end": area_end,
                        "length": area_end - area_start,
                        "px_mean": self._calibration_frame[0][area_start:area_end].mean(axis=0)
                    }
                )
                tmp_area["id"] += 1
                tmp_area["px_indexes"] = []
            if m == 255 or m == 0:
                tmp_area["color"] = m
                tmp_area["px_indexes"].append(i)

    def changes(self, color_diff_treshold=100):
        for i, frame in enumerate(self.video.iter_frames()):
            changes = {
                "frame": i,
                "areas": []
            }
            for area in self.areas:
                
                px_mean = frame[0][area["start"]:area["end"]].mean(axis=0)
                r = abs(px_mean[0] - area["px_mean"][0])
                g = abs(px_mean[1] - area["px_mean"][1])
                b = abs(px_mean[2] - area["px_mean"][2])
                if r > color_diff_treshold or g > color_diff_treshold or b > color_diff_treshold:
                    changes["areas"].append(area["id"])
            
            yield changes