# https://inglow.jp/techblog/python-image-score/ よりコピー、必要そうなら手を加えて組み込みたい
import numpy
import cv2
import os
import sys
from settings import DEBUG_BASE_PATH, RECOG_SCORE_IMG

#パスのベースを作成
DS = os.sep
BASE_PATH = DEBUG_BASE_PATH

#楽譜画像のパスを生成
scor_img = RECOG_SCORE_IMG

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

result_img = cv2.imread(scor_img, cv2.IMREAD_COLOR)


#五線を認識する
scr = cv2.imread(scor_img)
scr_gray = cv2.cvtColor(scr, cv2.COLOR_RGB2GRAY)

#線を検出
lines = cv2.HoughLinesP(scr_gray, rho=1, theta=numpy.pi/360, threshold=600, minLineLength=800, maxLineGap=600)


for line in lines:
	x1, y1, x2, y2 = line[0]

	#赤線
	result_img = cv2.line(result_img, (x1, y1), (x2, y2), (0,0,255), 1)


#検出結果を表示
debug_image(result_img, 'result2.png')
