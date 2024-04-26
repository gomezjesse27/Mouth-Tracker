from enum import Enum

class Algorithms(Enum):
    LINEAR_REGRESSION = 1
    CNN = 2

WEBCAM_ID = 0
RESOLUTION = 64
ALGORITHM = Algorithms.CNN
TARGET_COUNT = 3
TARGET_NAMES = ['smile', 'mouth_open', 'puff', 'frown']
FEATURE_COUNT = RESOLUTION * RESOLUTION  # Assuming grayscale images
BATCH_SIZE = 32  # Batch size for model training

# Assuming that the label columns are always the last two columns
FEATURE_COLUMNS = slice(0, FEATURE_COUNT)
LABEL_COLUMNS = slice(-2, None)

def print_config():
    print('--- Configuration ----')
    print('Webcam ID:', WEBCAM_ID)
    print('Resolution:', RESOLUTION)
    print('Algorithm:', ALGORITHM)
    print('Target Count:', TARGET_COUNT)
    print('Target Names:', TARGET_NAMES)
    print('Feature Columns:', FEATURE_COLUMNS)
    print('Label Columns:', LABEL_COLUMNS)
    print('----------------------')