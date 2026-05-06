import contextlib
import os
import cv2
from loguru import logger


_MAX_DISPLAY_WIDTH = 1280


@contextlib.contextmanager
def _suppress_c_output():
    """cv2.selectROI が stdout/stderr に出力する案内メッセージを抑制する"""
    devnull_fd = os.open(os.devnull, os.O_WRONLY)
    saved_stdout = os.dup(1)
    saved_stderr = os.dup(2)
    try:
        os.dup2(devnull_fd, 1)
        os.dup2(devnull_fd, 2)
        yield
    finally:
        os.dup2(saved_stdout, 1)
        os.dup2(saved_stderr, 2)
        os.close(saved_stdout)
        os.close(saved_stderr)
        os.close(devnull_fd)


def select_region(cap) -> tuple[tuple, tuple]:
    """動画の代表フレームを表示し、マウスで楽譜範囲を選択して座標を返す

    Parameters
    ----------
    cap : cv2.VideoCapture
        読み込み済みの動画オブジェクト

    Returns
    -------
    tuple[tuple[int, int], tuple[int, int]]
        (pos1, pos2) = ((x1, y1), (x2, y2)) 元解像度でのピクセル座標
    """
    fps = cap.get(cv2.CAP_PROP_FPS)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    target_frame = min(int(fps * 30), total_frames - 1)

    cap.set(cv2.CAP_PROP_POS_FRAMES, target_frame)
    ret, frame = cap.read()
    if not ret:
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
        ret, frame = cap.read()

    orig_h, orig_w = frame.shape[:2]
    if orig_w > _MAX_DISPLAY_WIDTH:
        scale = _MAX_DISPLAY_WIDTH / orig_w
        display_frame = cv2.resize(frame, (_MAX_DISPLAY_WIDTH, int(orig_h * scale)))
    else:
        scale = 1.0
        display_frame = frame

    logger.info("ROI選択: ドラッグで楽譜範囲を囲み Enter で確定、Esc でキャンセル")
    with _suppress_c_output():
        roi = cv2.selectROI("Score Region Selector", display_frame, fromCenter=False, showCrosshair=True)
    cv2.destroyAllWindows()

    x, y, w, h = roi
    if scale != 1.0:
        inv = 1.0 / scale
        x, y, w, h = int(x * inv), int(y * inv), int(w * inv), int(h * inv)

    return (x, y), (x + w, y + h)
