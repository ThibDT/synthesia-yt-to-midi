#!/usr/bin/env python3

if __name__ == "__main__":
    import os
    from conf import SAMPLE_INPUTS, SAMPLE_OUTPUTS
    from moviepy.editor import VideoFileClip
    from moviepy.video.fx.all import crop
    from piano import PianoKeyboard
    from utils import VideoController
    from mido import Message, MidiFile, MidiTrack

    start_time = 0
    piano = PianoKeyboard()
    
    source = os.path.join(SAMPLE_INPUTS, "synthesia.mp4")
    clip = VideoFileClip(source)
    clip = clip.subclip(t_start=start_time)
    clip = crop(clip, x1=0, y1=600, x2=clip.w, y2=601)
    video_controller = VideoController(clip)
    video_controller.calibrate()

    mid = MidiFile()
    track = MidiTrack()
    mid.tracks.append(track)
    # track.append(Message('program_change', program=12, time=0))

    active_changes = set()

    last_msg_time = 0

    for frame_diff in video_controller.changes():
        current_time = int((frame_diff["frame"] / video_controller.video.fps) * 1000)
        changes = set(frame_diff["areas"])

        notes_on = changes.difference(active_changes)
        notes_off = active_changes.difference(changes)

        for note in notes_on:
            track.append(Message('note_on', note= 21 + 12 + note, velocity=127, time=int((current_time - last_msg_time))))
            last_msg_time = current_time
        for note in notes_off:
            track.append(Message('note_off', note= 21 + 12 + note, velocity=127, time=int((current_time - last_msg_time))))
            last_msg_time = current_time

        active_changes = changes
    
    mid.save(f'{SAMPLE_OUTPUTS}/a heart made of yarn.mid')


# clip = clip.fl_image()


# clip.save_frame("frame_processed.png")

# clip.write_videofile("cropped2.mp4")
