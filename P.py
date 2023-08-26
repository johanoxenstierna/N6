import P

POST = 1
MAP_DIMS = (1280, 720)  #(233, 141)small  # NEEDED FOR ASSERTIONS

FRAMES_START = 0
FRAMES_STOP = 2600

FRAMES_TOT = FRAMES_STOP - FRAMES_START

# A (what to animate) ========
A_SPS = 1  # sparks  MUST BE 1 (being fixed though)
A_FS = 1
ARS = 0

NUM_SPS_SH = None  # a
NUM_SPS_F = 10  # used by 0, 5, 6  can be reduced for big bug
NUM_FS = 50 # NEED AT LEAST 2

# NUM_FIRE = 1

SHS_TO_SHOW = ['6']
