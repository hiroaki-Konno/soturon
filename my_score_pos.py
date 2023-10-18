# recognite music score position in video
class ScorePosition:
    def __init__(self, pos1=(0,0), pos2=(0,0)) -> None:
        self.pos1 = pos1
        self.pos2 = pos2
        # 1080pの場合
        # self.pos1 = (0, 849) # 楽譜左上
        # self.pos2 = (1920, 1080) # 楽譜右下

        # 480pの場合
        # self.pos1 = (0, 378) # 楽譜左上
        # self.pos2 = (854, 480) # 楽譜右下
    
    def mock_get_pos(self):
        """ 又三郎1620フレームの(0, 378)と(854, 480)を返す """
        return ((0, 378), (854, 480))
    
        # 又三郎1620フレームの(0, 849)と(1920, 1080)を返す
        # return ((0, 849), (1920, 1080))
    
    def mock_takane(self):
        """高嶺の花子さんで1620フレームの(0, 378)と(802, 480)を返す"""
        return ((0, 378), (802, 480))