class Coordinate:
    """楽譜座標を保持するクラス。直接ピクセル値または比率+解像度の2方式に対応。"""

    def __init__(self, x: int = None, y: int = None,
                 ratio_x: float = None, ratio_y: float = None):
        self._x = x
        self._y = y
        self._ratio_x = ratio_x
        self._ratio_y = ratio_y

    @classmethod
    def from_pixels(cls, x: int, y: int) -> 'Coordinate':
        """ピクセル値から座標を生成する"""
        return cls(x=x, y=y)

    @classmethod
    def from_ratio(cls, ratio_x: float, ratio_y: float) -> 'Coordinate':
        """解像度に対する比率（0.0〜1.0）から座標を生成する。resolve()時に実ピクセル値へ変換。"""
        return cls(ratio_x=ratio_x, ratio_y=ratio_y)

    def resolve(self, width: int = None, height: int = None) -> tuple:
        """実ピクセル座標 (x, y) を返す。

        Parameters
        ----------
        width : int, optional
            動画の横解像度。比率方式の場合に必須。
        height : int, optional
            動画の縦解像度。比率方式の場合に必須。

        Returns
        -------
        tuple(int, int)
            ピクセル座標 (x, y)
        """
        if self._x is not None and self._y is not None:
            return self._x, self._y
        if self._ratio_x is not None and self._ratio_y is not None:
            if width is None or height is None:
                raise ValueError("比率方式の座標を解決するには width と height が必要です")
            return round(self._ratio_x * width), round(self._ratio_y * height)
        raise ValueError("座標を解決できません: from_pixels() か from_ratio() で生成してください")

    @property
    def x(self) -> int:
        """直接ピクセル値が設定されている場合に x を返す。比率方式の場合は resolve() を使用。"""
        if self._x is not None:
            return self._x
        raise AttributeError("x は直接設定されていません。resolve(width, height) を使用してください")

    @property
    def y(self) -> int:
        """直接ピクセル値が設定されている場合に y を返す。比率方式の場合は resolve() を使用。"""
        if self._y is not None:
            return self._y
        raise AttributeError("y は直接設定されていません。resolve(width, height) を使用してください")

    def __repr__(self):
        if self._x is not None:
            return f"Coordinate(x={self._x}, y={self._y})"
        return f"Coordinate(ratio_x={self._ratio_x}, ratio_y={self._ratio_y})"


class ScorePosition:
    mock_pos_dict = {
        "サマータイムレコード": (
            Coordinate.from_pixels(169, 372),
            Coordinate.from_pixels(854, 480),
        ),
        "できっこないをやらなくちゃ": (
            Coordinate.from_pixels(0, 386),
            Coordinate.from_pixels(854, 480),
        ),
        "快晴": (
            Coordinate.from_pixels(0, 383),
            Coordinate.from_pixels(854, 480),
        ),
        "紅": (
            Coordinate.from_pixels(181, 419),
            Coordinate.from_pixels(854, 480),
        ),
        "高嶺の花子さん": (
            Coordinate.from_pixels(0, 378),
            Coordinate.from_pixels(802, 480),
        ),
        "脱法ロック": (
            Coordinate.from_pixels(0, 378),
            Coordinate.from_pixels(793, 480),
        ),
        "天体観測": (
            Coordinate.from_pixels(0, 384),
            Coordinate.from_pixels(854, 480),
        ),
        "又三郎": (
            Coordinate.from_pixels(0, 378),
            Coordinate.from_pixels(854, 480),
        ),
        "踊り子": (
            Coordinate.from_pixels(95, 400),
            Coordinate.from_pixels(757, 466),
        ),
        "ギターと孤独と蒼い惑星／吉他與孤獨的藍色星球│DRUM COVER": (
            Coordinate.from_pixels(0, 412),
            Coordinate.from_pixels(854, 480),
        ),
    }

    def __init__(self, pos1: Coordinate = None, pos2: Coordinate = None) -> None:
        self.pos1 = pos1 if pos1 is not None else Coordinate.from_pixels(0, 0)
        self.pos2 = pos2 if pos2 is not None else Coordinate.from_pixels(0, 0)

    @classmethod
    def mock_get_pos(cls, video_name) -> 'ScorePosition':
        """mock_pos_dictから該当動画の楽譜座標を ScorePosition インスタンスで返す"""
        coord1, coord2 = cls.mock_pos_dict[video_name]
        return cls(pos1=coord1, pos2=coord2)

    def mock_takane(self) -> 'ScorePosition':
        """高嶺の花子さん用の座標を返す"""
        return ScorePosition(
            pos1=Coordinate.from_pixels(0, 378),
            pos2=Coordinate.from_pixels(802, 480),
        )
