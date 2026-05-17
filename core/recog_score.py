# https://inglow.jp/techblog/python-image-score/ よりコピー、必要そうなら手を加えて組み込みたい
import os

import cv2
import numpy

from settings import DEBUG_BASE_PATH, RECOG_SCORE_IMG

DS = os.sep
BASE_PATH = DEBUG_BASE_PATH

scor_img = RECOG_SCORE_IMG

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
	cv2.imwrite(BASE_PATH + imgname, img)

result_img = cv2.imread(scor_img, cv2.IMREAD_COLOR)

scr = cv2.imread(scor_img)
scr_gray = cv2.cvtColor(scr, cv2.COLOR_RGB2GRAY)

lines = cv2.HoughLinesP(scr_gray, rho=1, theta=numpy.pi/360, threshold=600, minLineLength=800, maxLineGap=600)

for line in lines:
	x1, y1, x2, y2 = line[0]
	result_img = cv2.line(result_img, (x1, y1), (x2, y2), (0,0,255), 1)

debug_image(result_img, 'result2.png')
