# recognite music score position in video
class ScorePosition:
    mock_pos_dict = {
        "サマータイムレコード": ((169, 372), (854, 480)),
        "できっこないをやらなくちゃ": ((0, 386), (854, 480)),
        "快晴": ((0, 383), (854, 480)),
        "紅": ((181, 419), (854, 480)),
        "高嶺の花子さん": ((0, 378), (802, 480)),
        "脱法ロック": ((0, 378), (793, 480)),
        "天体観測": ((0, 384), (854, 480)),
        "又三郎": ((0, 378), (854, 480)),
        "踊り子": ((88, 394), (765, 474)),
    }

    def __init__(self, pos1=(0,0), pos2=(0,0)) -> None:
        self.pos1 = pos1
        self.pos2 = pos2
        # 1080pの場合
        # self.pos1 = (0, 849) # 楽譜左上
        # self.pos2 = (1920, 1080) # 楽譜右下

        # 480pの場合
        # self.pos1 = (0, 378) # 楽譜左上
        # self.pos2 = (854, 480) # 楽譜右下
    
    @classmethod
    def mock_get_pos(cls, video_name):
        """mock_pos_dictから該当動画の楽譜座標を返す
        
        Parameters
        ----------
        video_name: str
            動画の名称、本来なら消したい
            手動で特定した座標をまとめた辞書へのアクセス用
        
        Returns
        -------
        tuple(tuple(int, int)):
            動画内の楽譜の座標2点のタプルを返す
        """
        return cls.mock_pos_dict[video_name]

    # def mock_get_pos(self):
    #     """ 又三郎1620フレームの(0, 378)と(854, 480)を返す """
    #     return ((0, 378), (854, 480))
    
    #     # 又三郎1620フレームの(0, 849)と(1920, 1080)を返す
    #     # return ((0, 849), (1920, 1080))
    
    def mock_takane(self):
        """高嶺の花子さんで1620フレームの(0, 378)と(802, 480)を返す"""
        return ((0, 378), (802, 480))