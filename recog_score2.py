# https://inglow.jp/techblog/python-image-score/
# https://qiita.com/tifa2chan/items/d2b6c476d9f527785414
# https://note.nkmk.me/python-numpy-opencv-image-binarization/

import numpy
import cv2
import os
import sys
from settings import DEBUG_BASE_PATH, RECOG_SCORE2_IMG

#パスのベースを作成
DS = os.sep
BASE_PATH = DEBUG_BASE_PATH

#楽譜画像のパスを生成
scor_img = RECOG_SCORE2_IMG

#指定したデータを指定したファイル名で出力
def debug_image(img, imgname = 'result.png'):
	"""デバッグ用に画像をBASE_PATHへ保存する

	Parameters
	----------
	img: ndarray
		保存したい画像データ
	imgname: str
		保存するファイル名（デフォルトは 'result.png'）
	"""
	global BASE_PATH
	#画像を出力
	cv2.imwrite(BASE_PATH + imgname, img)

#楽譜データを読み込む
scr = cv2.imread(scor_img, cv2.IMREAD_COLOR)

#グレースケール化 ①
dst = cv2.cvtColor(scr, cv2.COLOR_RGB2GRAY)

def gazo_shori(scr_filled, debug=False):
    """グレースケール画像に閾値処理・白黒反転・2値化を順に適用して返す

    Parameters
    ----------
    scr_filled: ndarray
        処理対象のグレースケール画像
    debug: bool
        Trueの場合、各処理段階の画像をファイルに出力する

    Returns
    -------
    ndarray
        2値化処理後の画像
    """
    #閾値指定してフィルタリング　②
    retval, dst = cv2.threshold(scr_filled, 130, 255, cv2.THRESH_TOZERO_INV )

    #白黒反転　③
    dst2 = cv2.bitwise_not(dst)

    #もっかいフィルタリング
    retval, dst3 = cv2.threshold(dst2, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)

    if debug:
        debug_image(dst, 'note_02.png')
        debug_image(dst2, 'note_03.png')
        debug_image(dst3, 'note_04.png')
    return dst3

th, im_gray_th_otsu = cv2.threshold(dst, 128, 255, cv2.THRESH_OTSU)
th, im_gray_th_tri = cv2.threshold(dst, 128, 255, cv2.THRESH_TRIANGLE)
cv2.imwrite(BASE_PATH + 'otsu.png', im_gray_th_otsu)
cv2.imwrite(BASE_PATH + 'tri.png', im_gray_th_tri)

#輪郭を抽出 pg=02
cnt, hierarchy = cv2.findContours(dst, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

im_clr_th_tri = cv2.cvtColor(im_gray_th_tri, cv2.COLOR_GRAY2RGB)
result_img = im_clr_th_tri

lines = cv2.HoughLinesP(im_gray_th_tri, rho=1, theta=numpy.pi/360, threshold=780, minLineLength=800, maxLineGap=600)

for line in lines:
	x1, y1, x2, y2 = line[0]

	#赤線
	result_img = cv2.line(result_img, (x1, y1), (x2, y2), (0,0,255), 1)
debug_image(result_img, 'line_with_tri_samareko.png')
