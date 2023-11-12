# https://inglow.jp/techblog/python-image-score/
# https://qiita.com/tifa2chan/items/d2b6c476d9f527785414
# https://note.nkmk.me/python-numpy-opencv-image-binarization/

import numpy
import cv2
import os
import sys

#パスのベースを作成
DS = os.sep
# BASE_PATH = os.path.dirname(__file__) + DS
BASE_PATH = "./pics/test_ahodri/"

#楽譜画像のパスを生成
# scor_img = BASE_PATH + 'score' + DS + 'score.jpg'
scor_img = "./pics/loc_score/480p_samareko_loc_score_1620.jpg"

#指定したデータを指定したファイル名で出力
def debug_image(img, imgname = 'result.png'):
	global BASE_PATH
	#画像を出力
	cv2.imwrite(BASE_PATH + imgname, img)

#楽譜データを読み込む
scr = cv2.imread(scor_img, cv2.IMREAD_COLOR)

# #画像のサイズを取得 pg=02
# height, width, channels = scr.shape
# image_size = height * width

#グレースケール化 ①
dst = cv2.cvtColor(scr, cv2.COLOR_RGB2GRAY)
# cv2.imwrite("./imgname.png", scr_filled)
# debug_image(dst, 'note_01.png')

def gazo_shori(scr_filled, debug=False):
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
# sys.exit()

# 使用する画像を選択(閾値の選択方法)
# dst = im_gray_th_tri

#輪郭を抽出 pg=02
cnt, hierarchy = cv2.findContours(dst, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

# #抽出した領域を出力 抽出した領域に境界線を引いた画像を出力　pg=02
# # dst = cv2.imread(scor_img, cv2.IMREAD_COLOR)
# im_clr_th_tri = cv2.cvtColor(im_gray_th_tri, cv2.COLOR_GRAY2RGB)
# dst = cv2.drawContours(im_clr_th_tri, cnt, -1, (0, 0, 255, 255), 2, cv2.LINE_AA)
# cv2.imwrite(BASE_PATH + 'rinkaku_tri.png', dst)

im_clr_th_tri = cv2.cvtColor(im_gray_th_tri, cv2.COLOR_GRAY2RGB)
result_img = im_clr_th_tri

# processed_gray = gazo_shori(im_gray_th_tri)
# lines = cv2.HoughLinesP(processed_gray, rho=1, theta=numpy.pi/360, threshold=780, minLineLength=800, maxLineGap=600)
lines = cv2.HoughLinesP(im_gray_th_tri, rho=1, theta=numpy.pi/360, threshold=780, minLineLength=800, maxLineGap=600)

for line in lines:
	x1, y1, x2, y2 = line[0]
	
	#赤線
	result_img = cv2.line(result_img, (x1, y1), (x2, y2), (0,0,255), 1)
debug_image(result_img, 'line_with_tri_samareko.png')
