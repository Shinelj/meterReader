import math
import numpy as np
import cv2
from algorithm.debug import *
from algorithm.Common import AngleFactory, meterFinderByTemplate
from algorithm.Common import *
import json
"""
获取图像的HSV空间的值
"""

def HSV(img):
    HSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    H, S, V = cv2.split(HSV)

    h = H.reshape(H.shape[0] * H.shape[1], order='C')
    s = S.reshape(S.shape[0] * S.shape[1], order='C')
    v = V.reshape(V.shape[0] * V.shape[1], order='C')

    return H, S, V, h, s, v
"""
对图像进行轮廓检测，获取图像的二值图
"""
def getBinary(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 100, 200, apertureSize=3)
    return edges
def searchUpBlack(raw, img, x, y):
    '''

    :param raw: 原图
    :param img: 二值图
    :param thre:
    :param x:
    :param y:
    :return:
    '''
    axis = 10  # axis是偏移因子
    grad_thre = 250  # 图像梯度变换阈值
    x = x - axis
    # cv2.circle(raw, (y, x), 3, (0, 0, 255), -1)
    a = 0
    b = 0

    while True:
        if x == 0:
            break;
        if a != 0 and b != 0:
            break;
        if abs(int(img[x][y] - img[x + 1][y])) > grad_thre:
            # cv2.circle(raw, (y,x), 3, (0, 255, 0), -1)
            if a == 0:
                a = x
            else:
                b = x
        x = x - 1  # 幅度更新
    # cv2.imwrite("ww.jpg",raw)
    return y, a, y, b
def searchRightRed(raw, img, x, y):
    '''

    :param raw: 原图
    :param img: 二值图
    :param thre:
    :param x:
    :param y:
    :return:
    '''
    axis = 10  # axis是偏移因子
    grad_thre = 250  # 图像梯度变换阈值
    x = x - axis
    # cv2.circle(raw, (y, x), 3, (0, 0, 255), -1)
    a = 0
    b = 0

    while True:
        if x == 0:
            break;
        if a != 0 and b != 0:
            break;
        if abs(int(img[x][y] - img[x + 1][y])) > grad_thre:
            # cv2.circle(raw, (y,x), 3, (0, 255, 0), -1)
            if a == 0:
                a = x
            else:
                b = x
        x = x - 1  # 幅度更新
    # cv2.imwrite("ww.jpg",raw)

    return y, a, y, b

# 裁剪目标区域值
def cutTarget(img, x1, y1, x2, y2,status):

    if status=="left":
        len = y1 - y2
        start_x = x1 - len
        start_y = y1 - len
    elif status=="right":
        len = y1 - y2
        len = len+15
        start_x = x1
        start_y = y1 - len
    return img[start_y:start_y + len, start_x:start_x + int(1.4*len)]

# 在H空间里统计某一种颜色出现的比率
def countTarPer(h_vec, which):
    black_thre = 110
    ax = 4
    n = 0
    N = 1
    if which == "black":
        for d in h_vec:
            N = N + 1
            if abs(d - black_thre) < ax:
                n = n + 1

    return n, float(n / N)

#type transform
def getMatInt(Mat):

    d = Mat.shape
    for i in range(d[2]):
        for n in range(d[0]):
            for m in range(d[1]):
                Mat[n,m,i] = int(Mat[n,m,i])
                # print(Mat[n,m,i])
    Mat = Mat.astype(np.uint8)
    return Mat
def gamma(image,thre):
    '''
    :param image: numpy type
           thre:float
    :return: image numpy
    '''
    f = image / 255.0
    # we can change thre accoding  to real condition
    # thre = 0.3
    out = np.power(f, thre)
    out = getMatInt(out * 255)
    return out

def onoffIndoor(image, info):
    """
    :param image:whole image
    :param info:bileiqi2 config
    :return:
    """
    x1=0
    y1=0
    x2=0
    y2=0
    X=0
    Y=0
    img = None

    binary = getBinary(image)
    X, Y, _, _ = meterLocationFinderBySIFT(image, info['template'])
    if info['name']=="onoffIndoor1_1":
        x1, y1, x2, y2 = searchUpBlack(image, binary, Y, X)
        img = cutTarget(image, x1, y1, x2, y2,"left")

    elif info['name']=="onoffIndoor3_1":
        x1, y1, x2, y2 = searchRightRed(image, binary, Y, X)
        img = cutTarget(image, x1, y1, x2, y2, "right")
        #获取目标区域
        img = gamma(img, 0.2)
        cv2.imwrite("res.jpg", img)
        img = getBinary(img)
        cv2.imwrite("ress.jpg",img)

    #H, _, _, h, _, _ = HSV(img)

    #n,per = countTarPer(h, "black")

    # status="p"
    #
    # if per > 0.5:
    #     status = "close"

    # res = {
    #     'status': status,
    #     'num': n,
    #     'per': per
    # }
    # res = json.dumps(res)
    #
    # return res
    # cv2.imwrite("tar.jpg",img)
