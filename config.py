WEBCAM_ID = 1
RESOLUTION = 24
ALGORITHM = 'LINEAR_REGRESSION' # 'LINEAR_REGRESSION' or 'CNN'
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