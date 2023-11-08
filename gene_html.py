import os

def write1( file1, str1 ): 
    with open( file1, 'w', encoding='utf-8' ) as f1: 
        f1.write( str1 ) 
    return 0 


PIC_DIR_PATH = "./pics"
BASE_HTML = '''<html>
    <head>
        <style>
            img {{
                width:100%;
                /* border:3px solid blue;  */
                vertical-align:top;
            }}
            body {{
                margin:0;
            }}
            h1 {{
                margin-left: 25px;
                font-size: 40px;
            }}
        </style>
        <meta charset="utf-8">
        <title>{title1}</title>
    </head>
    <body>
        <h1>{title1}</h1>
        {body1}
    </body>
</html>
'''

HTML_DIR_PATH = "./htmls"


# def gene_html(song_folder_name, song_name):
def gene_html(song_folder_name : str = "test_ahodri2", song_name : str = "曲名：テスト、アホウドリ", ideal_score_indexes = []):
    """曲の楽譜のフォルダ名と曲名から楽譜のhtmlを生成する
    
    Parameters
    ----------
    song_folder_name: str
        曲の楽譜画像が格納されているフォルダ名
    song_name: str
        生成する楽譜の曲名、html内のタイトルなどに使用
    """
    # 楽譜画像のパスを生成
    song_dir_path = os.path.join(PIC_DIR_PATH, song_folder_name)
    # print(os.listdir(song_dir_path))

    ls = ideal_score_indexes
    # body1の生成
    body1 = ""
    for i, img in enumerate(os.listdir(song_dir_path)):
        try:
            if ls[0] == i:
                body1 += """<img src="{}">\n\t\t""".format(os.path.join(song_dir_path, img))
                ls = ls[1:]
        except:
            pass
    
    body1 = body1[:-3]
    # print(body1)

    kw_dict = {
        "title1" : song_name,
        "body1" : body1
    }

    # 置換に{}を用いるが、sytleの定義でも中括弧を使っているので
    # それをエスケープするために二つ重ねる -> {{}}
    ret_html = BASE_HTML.format(**kw_dict)

    # print(ret_html) 

    file1 = os.path.join(os.path.dirname(__file__) ,HTML_DIR_PATH , f"{song_name}.html")
    write1(file1, ret_html) 

song_folder_ls = [
    'tmp_dekikko',
    'tmp_samareko',
    'tmp_matasaburo',
    'tmp_tentai',
    'tmp_kaisei',
    'tmp_kurenai',
    'tmp_dappou',
    'tmp_odoriko',
    'tmp_takane',
]
song_name_ls = [
    'できっこないをやらなくちゃ.mp4',
    'サマータイムレコード.mp4',
    '又三郎.mp4',
    '天体 観測.mp4',
    '快晴.mp4',
    '紅.mp4',
    '脱法ロック.mp4',
    '踊り子.mp4',
    '高嶺の花子さん.mp4',
]
indexes_dict ={
    "tmp_dappou":[0, 2, 4, 6, 8, 11, 13, 15, 17, 19, 21, 23, 25, 26, 28, 30, 32, 34, 36, 38, 40, 43, 45, 47, 49, 51, 53, 55, 56, 58, 60],
    "tmp_dekikko":[0, 1, 3, 6, 7, 11, 14, 17, 19, 21, 23, 25, 27, 30, 32, 33, 35, 38, 40, 42, 45, 47, 49, 51, 53, 55, 58, 60, 62, 63, 66],
    "tmp_kaisei":[0, 1, 3, 5, 7, 9, 11, 13, 14, 16, 18, 20, 22, 24, 26, 27, 29, 31, 33, 35, 37, 39, 41, 42, 44, 46, 48, 50, 52, 54, 56, 58, 60, 61, 63, 65, 67, 69, 71, 73, 74, 76, 78, 80, 82],
    "tmp_kurenai":[2, 5, 7, 9, 11, 13, 15, 16, 19, 21, 23, 25, 27, 28, 30, 32, 34, 36, 38, 40, 42, 44, 46, 48, 50, 52, 54, 56, 58, 60, 62, 64, 66, 68, 70, 72, 74, 75, 77, 79, 81, 83],
    "tmp_matasaburo":[0, 2, 3, 5, 6, 8, 10, 11, 13, 14, 16, 18, 19, 21, 22, 25, 26, 28, 30, 31, 33, 34, 36, 37, 39, 41, 42, 44, 45, 47, 49, 50, 52, 54, 55, 57, 58, 60, 61, 63, 65, 66, 69, 70, 72, 73],
    "tmp_odoriko":[0, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24, 28, 32, 34, 36, 38, 40, 42, 45, 49, 54, 56, 58, 60, 62, 64, 66, 68, 70, 72],
    "tmp_samareko":[0, 4, 7, 9, 11, 14, 16, 18, 20, 21, 23, 25, 26, 28, 30, 32, 33, 35, 37, 39, 40, 42, 45, 47, 49, 51, 52, 54, 56, 58, 59, 61, 63, 66, 68, 70, 71, 73, 75, 77, 78, 80, 82],
    "tmp_takane":[8, 11, 13, 15, 18, 20, 22, 25, 26, 28, 33, 35, 37, 40, 42, 44, 47, 49, 51, 54, 55, 57, 62, 64, 66, 71, 73, 76, 78, 80, 85, 87, 90, 92, 94],
    "tmp_tentai":[3, 5, 7, 9, 10, 12, 14, 16, 18, 20, 22, 24, 26, 28, 30, 32, 34, 36, 38, 40, 41, 43, 45, 47, 49, 51, 53, 55, 57, 59, 61, 63, 65, 67, 69, 70, 72, 74, 76, 78, 80, 82, 84],
}

for i in range(len(song_folder_ls)):
    song_folder_name = song_folder_ls[i]
    gene_html(song_folder_name=song_folder_name, song_name=song_name_ls[i][:-4], ideal_score_indexes=indexes_dict[song_folder_name])