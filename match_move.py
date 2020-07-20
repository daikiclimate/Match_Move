import cv2
import matplotlib.pyplot as plt
import numpy as np
import utils
import time
import pprint

def get_images(magazine, box, ad):
    mag_img = cv2.imread(magazine)
    mag_img = cv2.cvtColor(mag_img, cv2.COLOR_BGR2RGB)

    box_img = cv2.imread(box)
    box_img = cv2.cvtColor(box_img, cv2.COLOR_BGR2RGB)

    ad_img = cv2.imread(ad)
    ad_img = cv2.cvtColor(ad_img, cv2.COLOR_BGR2RGB)
    return mag_img, box_img, ad_img

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
    src = cv2.cvtColor(src, cv2.COLOR_RGB2BGR)
    target = cv2.cvtColor(target, cv2.COLOR_RGB2BGR)
    cv2.imwrite('draw_match.jpg', cv2.drawMatches(src, kp1, target, kp2, matches[:10], None, flags=2))
    return src_pts, dst_pts

def get_homography(src_pts, dst_pts):
    # h = utils.calculate_homography_matrix(src_pts.reshape(-1,2), dst_pts.reshape(-1,2))
    h, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC)

    # h = utils.calculate_homography_matrix(dst_pts.reshape(-1,2), src_pts.reshape(-1,2))
    return h

def transform_homography(ad_img, h, im2):
    ad_img = cv2.warpPerspective(ad_img, h, (im2.shape[1],im2.shape[0]))
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
    box_img = cv2.cvtColor(box_img, cv2.COLOR_BGR2RGB)

    ad_img = cv2.imread(ad)
    ad_img = cv2.cvtColor(ad_img, cv2.COLOR_BGR2RGB)

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

def main(base = "images/mag1.jpg", box = "images/box1.jpg", ad = "images/ad2.jpg", output_name = "output.jpg"):


    print("start")
    print(output_name)
    t1 = time.time()
    mag_img, box_img, ad_img = get_images(base, box, ad)
    ad_img[ad_img==0] = 1

    # box_img = cv2.resize(box_img, (ad_img.shape[1],ad_img.shape[0]))
    orgHeight, orgWidth = box_img.shape[:2]
    size = (orgWidth//5,orgHeight//5)
    box_img = cv2.resize(box_img, size)

    ad_img = cv2.resize(ad_img, (box_img.shape[1], box_img.shape[0]))
    # m = cv2.rectangle(mag_img, (1,270), (1690,945), (0, 0, 0),thickness=-1)


    # src_pts, dst_pts = get_match_features(box_img ,m)
    src_pts, dst_pts = get_match_features(box_img ,mag_img)
    # print(src_pts.shape)

    h = get_homography(src_pts, dst_pts)
    # h = get_homography(dst_pts, src_pts)
    pprint.pprint(h)

    transformed_ad = transform_homography(ad_img, h, mag_img)
    # cv2.imwrite("tmp.jpg", transformed_ad)

    output = fusion(mag_img, transformed_ad)
    output = cv2.cvtColor(output, cv2.COLOR_RGB2BGR)
    cv2.imwrite(output_name, output)
    print("finish")
    print("time:",round(time.time()-t1),"sec")
    return output



if __name__=="__main__":
    # main()
    main("images/fail.png", "images/box5.png", "images/ad3.png","puma.jpg")
