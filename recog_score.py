# https://inglow.jp/techblog/python-image-score/ よりコピー、必要そうなら手を加えて組み込みたい
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
scor_img = "./pics/loc_score/480p_takane_loc_score_1620.jpg"

#指定したデータを指定したファイル名で出力
def debug_image(img, imgname = 'result.png'):
	global BASE_PATH
	#画像を出力
	cv2.imwrite(BASE_PATH + imgname, img)

result_img = cv2.imread(scor_img, cv2.IMREAD_COLOR)


#五線を認識する
scr = cv2.imread(scor_img)
scr_gray = cv2.cvtColor(scr, cv2.COLOR_RGB2GRAY)
# print(scr_gray)

# debug_image(scr_gray, "1.png")
# sys.exit()

# #途切れてるところがつながるようにぼかしてみる
# kval = 3
# kernel = numpy.ones((kval,kval),numpy.float32)/(kval*kval)
# scr_gray = cv2.filter2D(scr_gray,-1,kernel)

# #閾値指定してフィルタリング
# line_retval, line_dst = cv2.threshold(scr_gray, 200, 255, cv2.THRESH_TOZERO_INV )

# #白黒反転
# line_dst = cv2.bitwise_not(line_dst)

# #もっかいフィルタリング
# line_retval, line_dst = cv2.threshold(line_dst, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)

#線を検出
lines = cv2.HoughLinesP(scr_gray, rho=1, theta=numpy.pi/360, threshold=600, minLineLength=800, maxLineGap=600)


for line in lines:
	x1, y1, x2, y2 = line[0]
	
	#赤線
	result_img = cv2.line(result_img, (x1, y1), (x2, y2), (0,0,255), 1)
	

""" #五線認識ここまで
#音符のたま認識

#楽譜データを読み込む
scr = cv2.imread(scor_img, cv2.IMREAD_COLOR)

#画像のサイズを取得
height, width, channels = scr.shape
image_size = height * width

#グレースケール化 ①
scr_filled = cv2.cvtColor(scr, cv2.COLOR_RGB2GRAY)

#細い線とかをぼかす　ぼかし処理
scr_filled = cv2.bilateralFilter(scr_filled, 75, 75, 75)

#閾値指定してフィルタリング　②
retval, dst = cv2.threshold(scr_filled, 130, 255, cv2.THRESH_TOZERO_INV )

#白黒反転　③
dst = cv2.bitwise_not(dst)

#もっかいフィルタリング
retval, dst = cv2.threshold(dst, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)

#輪郭を抽出
cnt, hierarchy = cv2.findContours(dst, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

#抽出した領域を出力 抽出した領域に境界線を引いた画像を出力
dst = cv2.imread(scor_img, cv2.IMREAD_COLOR)
dst = cv2.drawContours(dst, cnt, -1, (0, 0, 255, 255), 2, cv2.LINE_AA)

#認識させるサイズを指定する
minsize = 500 #20→100→500
maxsize = 5000 #元元3000とか

#大きいor小さい領域は削除
for i, count in enumerate(cnt):
	#小さい領域の場合は無視
	area = cv2.contourArea(count)
	if area < minsize:
		continue
	
	#最大値の指定を追加
	if area > maxsize:
		continue
	
	#画像全体を占める領域を除外
	if image_size * 0.50 < area:
		continue
	
	#囲う線を描画する
	x,y,w,h = cv2.boundingRect(count)
	result_img = cv2.rectangle(result_img, (x, y), (x + w, y + h), (0, 255, 0), 3)
	
#音符認識ここまで """

#検出結果を表示
debug_image(result_img, 'result2.png')