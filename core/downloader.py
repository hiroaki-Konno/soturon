import os
import yt_dlp
from loguru import logger
from settings import VIDEO_FOLDER_PATH, FFMPEG_DIR


def download(url: str) -> tuple:
    """YouTube URLから動画をダウンロードして保存する

    Parameters
    ----------
    url : str
        YouTube動画のURL

    Returns
    -------
    tuple[str, str]
        (動画ファイルパス, 動画タイトル)
    """
    ydl_opts = {
        'outtmpl': os.path.join(VIDEO_FOLDER_PATH, '%(title)s.%(ext)s'),
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
        'ffmpeg_location': FFMPEG_DIR or None,
    }

    logger.info(f"ダウンロード開始: {url}")
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        title = info['title']
        filepath = info['requested_downloads'][0]['filepath']

    logger.info(f"ダウンロード完了: {filepath}")
    return filepath, title
