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


# def gene_html(song_folder_name, song_name):
def gene_html(song_folder_name : str = "test_ahodri2", song_name : str = "曲名：テスト、アホウドリ"):
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

    # body1の生成
    body1 = ""
    for img in os.listdir(song_dir_path):
        body1 += """<img src="{}">\n\t""".format(os.path.join(song_dir_path, img))
    
    body1 = body1[:-2]
    # print(body1)

    kw_dict = {
        "title1" : song_name,
        "body1" : body1
    }

    # 置換に{}を用いるが、sytleの定義でも中括弧を使っているので
    # それをエスケープするために二つ重ねる -> {{}}
    ret_html = BASE_HTML.format(**kw_dict)

    print(ret_html) 

    path1 = os.path.dirname(__file__) + "/" 
    file1 = path1 + "html1.html" 
    write1(file1, ret_html) 

gene_html("tmp_kodoku", "孤独")