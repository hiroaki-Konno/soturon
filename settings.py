import configparser
from pathlib import Path

_config = configparser.ConfigParser()
_config.read(Path(__file__).parent / 'config.ini', encoding='utf-8')

VIDEO_FOLDER_PATH   = _config['paths']['video_folder_path']
SCORE_FOLDER_PATH   = _config['paths']['score_folder_path']
PIC_DIR_PATH        = _config['paths']['pic_dir_path']
DEBUG_BASE_PATH     = _config['paths']['debug_base_path']

RECOG_SCORE_IMG     = _config['score_images']['recog_score_img']
RECOG_SCORE2_IMG    = _config['score_images']['recog_score2_img']

DEFAULT_INTERVAL_SEC = _config.getint('processing', 'default_interval_sec')
SIMILARITY_THRESHOLD = _config.getfloat('processing', 'similarity_threshold')

FFMPEG_DIR = _config.get('tools', 'ffmpeg_dir', fallback='')

LOG_LEVEL   = _config.get('logging', 'log_level', fallback='INFO')
LOG_DIR     = _config['logging']['log_dir']
