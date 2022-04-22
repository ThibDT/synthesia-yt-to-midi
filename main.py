#!/usr/bin/env python3



if __name__ == "__main__":
    import os
    from conf import SAMPLE_INPUTS, SAMPLE_OUTPUTS
    from moviepy.editor import VideoFileClip
    from moviepy.video.fx.all import crop
    from utils import KeyboardVideoController
    from mido import Message, MidiFile, MidiTrack
    from pytube import YouTube
    from pytube.exceptions import RegexMatchError
    import sys
    import ntpath

    
    start_time = 0
    y_pos = 600
    source = None
    base_name = None
    offset = 0
    screenshot = False


    try:
        source_url = sys.argv[1]
        yt = YouTube(source_url)
        stream = yt.streams.filter(file_extension='mp4').order_by('resolution').desc().first()
        print(f"Downloading {stream.default_filename}")
        source = stream.download(output_path=SAMPLE_INPUTS)
    except(IndexError):
        print("You must provide a youtube video url")
        exit(1)
    except RegexMatchError:
        print(f"Invalid url: {sys.argv[1]}")
        exit(1)

    if("-s" in sys.argv or "--start" in sys.argv):
        try:
            start_arg_index = (sys.argv.index("-s") if("-s" in sys.argv) else sys.argv.index("--start")) + 1 
            start_time = sys.argv[start_arg_index]
        except(IndexError):
            print("You must provide a start time when using the start option")
            exit(1)

    if("-y" in sys.argv):
        try:
            y_arg_index = sys.argv.index("-y") + 1 
            y_pos = float(sys.argv[y_arg_index])
        except(IndexError):
            print("You must provide a y position for the row of pixel to be analized when using the y option")
            exit(1)

    if("-o" in sys.argv or "--offset" in sys.argv):
        try:
            o_arg_index = (sys.argv.index("-o") if("-o" in sys.argv) else sys.argv.index("--offset")) + 1
            offset = int(sys.argv[o_arg_index])
        except(IndexError):
            print("You must provide an offset number when using the offset option")
            exit(1)

    if("--screenshot" in sys.argv):
        screenshot = True

    base_name = ntpath.basename(source).replace("mp4", "mid")
    
    clip = VideoFileClip(source)
    clip = clip.subclip(t_start=start_time)
    clip = crop(clip, x1=0, y1=y_pos, x2=clip.w, y2=y_pos+1)
    frames_nb = round(clip.fps * clip.duration)

    video_controller = KeyboardVideoController(clip)
    video_controller.calibrate(screenshot=screenshot)

    mid = MidiFile()
    LHTrack = MidiTrack()
    RHTrack = MidiTrack()
    mid.tracks.append(LHTrack)
    mid.tracks.append(RHTrack)

    active_changes = set()
    last_msg_time = 0

    print("Generating midi...")
    for frame_diff in video_controller.changes():
        current_time = int((frame_diff["frame"] / video_controller.video.fps) * 1000)
        changes = set(frame_diff["areas"])

        notes_on = changes.difference(active_changes)
        notes_off = active_changes.difference(changes)

        for note in notes_on:
            msg_time = current_time - last_msg_time
            msg_note = 21 + offset + note
            RHTrack.append(Message('note_on', note=msg_note, velocity=65, time=msg_time))
            last_msg_time = current_time
        for note in notes_off:
            msg_time = current_time - last_msg_time
            msg_note = 21 + offset + note
            RHTrack.append(Message('note_off', note=msg_note, velocity=0, time=msg_time))
            last_msg_time = current_time

        active_changes = changes



    mid.save(os.path.join(SAMPLE_OUTPUTS, base_name))
    print(f"\r\n{base_name} saved in {SAMPLE_OUTPUTS}")


# clip = clip.fl_image()
# clip.save_frame("frame_processed.png")
# clip.write_videofile("cropped2.mp4")

