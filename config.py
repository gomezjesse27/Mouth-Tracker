from enum import Enum

class Algorithms(Enum):
    LINEAR_REGRESSION = 1
    CNN = 2

WEBCAM_ID = 0
RESOLUTION = 24
ALGORITHM = Algorithms.LINEAR_REGRESSION
TARGET_COUNT = 3
TARGET_NAMES = ['smile', 'mouth_open', 'puff', 'frown']

def print_config():
    print('--- Configuration ----')
    print('Webcam ID:', WEBCAM_ID)
    print('Resolution:', RESOLUTION)
    print('Algorithm:', ALGORITHM)
    print('Target Count:', TARGET_COUNT)
    print('Target Names:', TARGET_NAMES)
    print('----------------------')