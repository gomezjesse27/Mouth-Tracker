from enum import IntEnum

class Algorithms(IntEnum):
    LINEAR_REGRESSION = 0
    CNN = 1
    ANN = 2
    ANN_NOPCA = 3
    ALL = 4

WEBCAM_ID = 0
RESOLUTION = 32
ALGORITHM = Algorithms.ALL
TARGET_COUNT = 3
TARGET_NAMES = ['smile', 'mouth_open', 'puff', 'frown']
FEATURE_COUNT = RESOLUTION * RESOLUTION  
BATCH_SIZE = 32  # Batch size for model training


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

def algo_to_string(algo):
    if algo == Algorithms.LINEAR_REGRESSION:
        return "Linear Regression"
    elif algo == Algorithms.CNN:
        return "CNN"
    elif algo == Algorithms.ANN:
        return "ANN"
    elif algo == Algorithms.ANN_NOPCA:
        return "ANN No PCA"
    elif algo == Algorithms.ALL:
        return "ALL"
    return "Unknown"