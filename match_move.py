import cv2
import numpy as np
import time
import pprint
import argparse

def load_args():
    parser = argparse.ArgumentParser(description='match move')  
    parser.add_argument('base', help='置き換えるよう画像。探索する大きい画像')    
    parser.add_argument('box', help='探索したい領域')
    parser.add_argument('ad', help='探索してきた領域を置き換える用画像')
    parser.add_argument('--output',default = "output/output.jpg" ,help='探索してきた領域を置き換える用画像')
    parser.add_argument('--param',default = 1 ,help='探索してきた領域を置き換える用画像')
    args = parser.parse_args()
    return args


def get_images(src, box, ad):

    src_img = cv2.imread(src)

    box_img = cv2.imread(box)

    ad_img = cv2.imread(ad)
    return src_img, box_img, ad_img

def get_match_features(src, target):
    akaze = cv2.AKAZE_create()
    kp1, des1 = akaze.detectAndCompute(src, None)
    kp2, des2 = akaze.detectAndCompute(target, None)

    bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)

    matches = bf.match(des1, des2)

    matches = sorted(matches, key=lambda x: x.distance)
    good_match_rate = 0.5
    good = matches[:int(len(matches) * good_match_rate)]
    src_pts = np.float32(
            [kp1[m.queryIdx].pt for m in good]).reshape(-1, 1, 2)
    dst_pts = np.float32(
           [kp2[m.trainIdx].pt for m in good]).reshape(-1, 1, 2)
    cv2.imwrite('draw_match.jpg', cv2.drawMatches(src, kp1, target, kp2, matches[:10], None, flags=2))
    return src_pts, dst_pts

def get_homography(src_pts, dst_pts):
    h, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC)
    return h

def transform_homography(ad_img, h, after_img_shape):
    ad_img = cv2.warpPerspective(ad_img, h, (after_img_shape.shape[1],after_img_shape.shape[0]))
    return ad_img

def fusion(src, generated):
    height,width,c = src.shape
    src = src.reshape(-1)
    generated = generated.reshape(-1)
    
    generated[generated==0] = src[generated==0]
    return generated.reshape(height,width,c)


def video_function(base , box = "images/box1.jpg", ad = "images/ad2.jpg"):
    mag_img = base[:]

    box_img = cv2.imread(box)

    ad_img = cv2.imread(ad)

    p = 20
    orgHeight, orgWidth = box_img.shape[:2]
    size = (orgWidth//p,orgHeight//p)
    box_img = cv2.resize(box_img, size)

    ad_img = cv2.resize(ad_img, (box_img.shape[1], box_img.shape[0]))

    src_pts, dst_pts = get_match_features(box_img ,mag_img)
    # print(src_pts.shape)
    
    h = get_homography(src_pts, dst_pts)
    if True:
        h_inv = get_homography(dst_pts, src_pts)

        transformed_src = transform_homography(mag_img, h, box_img)
        # print("psnr:",cv2.PSNR(transformed_src, box_img))
        psnr = cv2.PSNR(transformed_src, box_img)
    # h = get_homography(dst_pts, src_pts)
    # pprint.pprint(h)

    transformed_ad = transform_homography(ad_img, h, mag_img)
    # cv2.imwrite("tmp.jpg", transformed_ad)

    output = fusion(mag_img, transformed_ad)
    return output,psnr

# def main(base = "images/mag1.jpg", box = "images/box1.jpg", ad = "images/ad2.jpg", output_name = "output.jpg"):
def main():
    args = load_args()
    base = args.base
    box = args.box
    ad = args.ad
    output_name = args.output
    param = int(args.param)

    print("start")
    print(output_name)
    t1 = time.time()
    base_img, box_img, ad_img = get_images(base, box, ad)


    #うまくいかない際のパラメータ
    #box画像があまりにも大きいとおかしくなる時がある
    #その時は小さくする
    orgHeight, orgWidth = box_img.shape[:2]
    size = (orgWidth//param,orgHeight//param)
    box_img = cv2.resize(box_img, size)

    #差し替え用広告画像の初期設定。必須
    ad_img[ad_img==0] = 1
    ad_img = cv2.resize(ad_img, (box_img.shape[1], box_img.shape[0]))

    #特徴点抽出
    src_pts, dst_pts = get_match_features(base_img ,box_img)

    #ホモグラフィー行列の導出抽出
    h = get_homography(dst_pts, src_pts)
    pprint.pprint(h)

    #広告画像の変換
    transformed_ad = transform_homography(ad_img, h, base_img)

    #特定領域のみを置き換え
    output_img = fusion(base_img, transformed_ad)

    #書き込み
    cv2.imwrite(output_name, output_img)
    print("finish")
    print("time:",round(time.time()-t1,2),"sec")


if __name__=="__main__":
    main()
    # main("images/fail.png", "images/box5.png", "images/ad3.png","puma.jpg")
