import cv2


def select_region(cap) -> tuple[tuple, tuple]:
    """動画の代表フレームを表示し、マウスで楽譜範囲を選択して座標を返す

    Parameters
    ----------
    cap : cv2.VideoCapture
        読み込み済みの動画オブジェクト

    Returns
    -------
    tuple[tuple[int, int], tuple[int, int]]
        (pos1, pos2) = ((x1, y1), (x2, y2)) 左上・右下のピクセル座標
    """
    fps = cap.get(cv2.CAP_PROP_FPS)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    target_frame = min(int(fps * 30), total_frames - 1)

    cap.set(cv2.CAP_PROP_POS_FRAMES, target_frame)
    ret, frame = cap.read()
    if not ret:
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
        ret, frame = cap.read()

    roi = cv2.selectROI(
        "楽譜範囲を選択 (Enter: 確定 / Esc: キャンセル)",
        frame,
        fromCenter=False,
        showCrosshair=True,
    )
    cv2.destroyAllWindows()

    x, y, w, h = roi
    return (x, y), (x + w, y + h)
