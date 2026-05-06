import cv2
from loguru import logger

_MAX_DISPLAY_WIDTH = 1280
_WINDOW_TITLE = "Frame Selector"


def _resize_for_display(frame):
    h, w = frame.shape[:2]
    if w > _MAX_DISPLAY_WIDTH:
        scale = _MAX_DISPLAY_WIDTH / w
        return cv2.resize(frame, (_MAX_DISPLAY_WIDTH, int(h * scale)))
    return frame


def _overlay_info(frame, frame_info: str, instructions: str):
    """フレーム上部に操作説明を描画する"""
    display = frame.copy()
    w = display.shape[1]
    cv2.rectangle(display, (0, 0), (w, 52), (0, 0, 0), -1)
    cv2.putText(display, frame_info,   (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)
    cv2.putText(display, instructions, (10, 44), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (180, 180, 180), 1)
    return display


def select_frames(peak_frames: list, all_frames: list) -> list:
    """フレームを1枚ずつ表示してユーザーに取捨選択させる

    最初はピーク候補フレームを表示する。
    A キーを押すと全フレーム表示に切り替わる（選択はリセット）。

    Parameters
    ----------
    peak_frames : list[ndarray]
        類似度ピークの候補フレーム
    all_frames : list[ndarray]
        インターバルで抽出した全フレーム

    Returns
    -------
    list[ndarray]
        ユーザーが選択したフレームのリスト
    """
    frames = peak_frames
    mode = "peak"
    logger.info(
        f"フレーム選択開始: ピーク候補 {len(peak_frames)} 枚"
        f" (Enter: 追加 / Space: スキップ / A: 全 {len(all_frames)} 枚表示 / Esc: 完了)"
    )

    confirmed = []
    i = 0

    while i < len(frames):
        display = _overlay_info(
            _resize_for_display(frames[i]),
            f"[{'peak' if mode == 'peak' else 'all'}]  {i + 1} / {len(frames)}",
            "Enter:add  Space:skip  A:show-all  Esc:done",
        )
        cv2.imshow(_WINDOW_TITLE, display)
        key = cv2.waitKey(0) & 0xFF

        if key in (13, ord('y')):  # Enter / Y → 追加
            confirmed.append(frames[i])
            logger.debug(f"フレーム {i + 1} を追加")
            i += 1
        elif key in (32, ord('n')):  # Space / N → スキップ
            logger.debug(f"フレーム {i + 1} をスキップ")
            i += 1
        elif key == ord('a') and mode == "peak":  # A → 全フレームに切り替え
            logger.info("全フレーム表示に切り替えます")
            frames = all_frames
            mode = "all"
            confirmed = []
            i = 0
        elif key == 27:  # Esc → 終了
            break

    cv2.destroyAllWindows()
    logger.info(f"{len(confirmed)} 枚のフレームを選択しました")
    return confirmed
