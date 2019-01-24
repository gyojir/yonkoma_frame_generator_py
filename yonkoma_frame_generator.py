#! /usr/bin/env python
# coding= utf-8
# -*- coding: utf-8 -*-

import cv2
import numpy as np

margin = 69				# 余白
interval = 69			# コマとコマの間隔
border_thickness = 14	# 枠の太さ
title_height = 220		# タイトルの高さ
segment_height = 771	# コマの高さ
segment_width = 1143	# コマの幅
segment_count = 4		# コマの数

# 画像高さ
image_height = margin * 2 \
             + title_height \
             + segment_height * segment_count \
             + border_thickness * 2 * (1+segment_count) \
             + interval * segment_count

# 画像幅
image_width = margin * 2 \
            + segment_width \
            + border_thickness * 2

# コマの右端位置（枠線含む）
right_end = image_width - margin

# コマから次のコマへの距離
segment_pitch = border_thickness*2 + segment_height + interval

# 出力画像
image = np.full((image_height, image_width), 255, dtype=np.uint8)

# 横線の一行分
horizontal_line = [0 if (margin <= x and x < right_end) else 255 for x in range(image_width)]

# 縦線の一行分
vertical_line = [0 if (margin <= x and x < margin + border_thickness) 
                   or (right_end - border_thickness <= x and x < right_end)
                 else 255 for x in range(image_width)]

# if文の中で１つの変数を使いまわす用
def add(t, v):
    t[0] += v
    return True

# コマを上から描いていく
for y, img_x in enumerate(image):
    tmp = [margin]
    
    if y < tmp[0]:
        pass    
    # タイトルの上側
    elif add(tmp, border_thickness) and y < tmp[0]:
        image[y] = horizontal_line
    # タイトルの側線
    elif add(tmp, title_height) and y < tmp[0]:
        image[y] = vertical_line
    # タイトルの下側
    elif add(tmp, border_thickness) and y < tmp[0]:
        image[y] = horizontal_line
    # ここから各コマ
    elif add(tmp, interval) and ((y - tmp[0]) / segment_pitch) < segment_count:
        # 1コマ目を基準とした座標を、コマとコマの距離で割った余りがコマ内でのy座標
        segment_y = (y - tmp[0]) % segment_pitch

        tmp[0] = 0
        # コマの上側
        if add(tmp, border_thickness) and segment_y < tmp[0]:
            image[y] = horizontal_line
        # コマの側線
        elif add(tmp, segment_height) and  segment_y < tmp[0]:
            image[y] = vertical_line
        # コマの下側
        elif add(tmp, border_thickness) and  segment_y < tmp[0]:
            image[y] = horizontal_line

# 出力
cv2.imwrite('img.png', image)