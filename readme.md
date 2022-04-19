# Simple synthesia youtube video to midi converter

## Usage
The script basically download the video from youtube, use first frame to try determining zones for each piano key in a 1 pixel height row of the video
then check for color changes in each zone to generate corresponding midi file.

### Basic Usage
```
python main.py (youtube url video)
```

#### Available options
Few options are available, more might be added later.

##### Start
Use --start option or its shorthand -s to determine the start time of the video to be analyzed. The first frame needs to include a piano keyboard with no active key.
This allows to skip fade in effects or video introductions which would prevent the script to get the correct calibration frame.
You then need to provide a starting time in seconds.
```
python main.py (youtube url video) [-s --start] start_time
```

##### y
The script use a one pixel height row, this row should include a keyboard with color changes when notes are supposed to be pressed, this option allows to provide a y position for that row.
```
python main.py (youtube url video) [-y] y_position
```


##### Offset
Use --offset option or its shorthand -o to offset the keyboard starting key. 
Default to 0, first key identified in the video is then supposed to be first key on a full piano keyboard (A)
```
python main.py (youtube url video) [-o --offset] offset
```