import os
import os

ABS_PATH = os.path.abspath(__file__)
BASE_DIR = os.path.dirname(ABS_PATH)
DATA_DIR = os.path.join(BASE_DIR, "data")
SAMPLES_DIR = os.path.join(BASE_DIR, "samples")
SAMPLE_INPUTS = os.path.join(SAMPLES_DIR, "inputs")
SAMPLE_OUTPUTS = os.path.join(SAMPLES_DIR, "outputs")
