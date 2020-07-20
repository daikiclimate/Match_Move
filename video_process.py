import os
import argparse
from PIL import Image
import cv2
import time
import match_move

def load_args():
    parser = argparse.ArgumentParser(description='match move')  
    # 3. parser.add_argumentで受け取る引数を追加していく
    parser.add_argument('video_name', help='-')    
    # 必須の引数を追加
    parser.add_argument('box_name', help='-')
    parser.add_argument('ad_name', help='-')
    args = parser.parse_args()
    return args

def load_video(video_name):
    video = cv2.VideoCapture("videos/"+video_name)
    if video.isOpened():
        return video
    else:
        print("failed load video")
        exit()

def main():
    #video名前など取得
    args = load_args()

    #videoのロード
    video = load_video(args.video_name)
    # 幅
    W = video.get(cv2.CAP_PROP_FRAME_WIDTH)
    # 高さ
    H = video.get(cv2.CAP_PROP_FRAME_HEIGHT)

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    # fourcc = cv2.VideoWriter_fourcc(*'XVID')

    out = cv2.VideoWriter(
            'output/'+args.video_name,
            fourcc,
            30,
            (int(W),int(H))
            )

    t = 0
    psnr_th = 4
    while True:
       ret, frame = video.read()
       if ret==False:
           break
       output_frame,psnr = match_move.video_function(base = frame)
       print(t, psnr)
       
       if True:
           cv2.imwrite("tmp/tmp"+str(t)+".jpg", output_frame)
           t += 1
       # match_move.video_function(base = frame, args.box_name, args.ad_name)
       if psnr > psnr_th:
           print("fixed")
           output_frame = previous_frame
       else:
           previous_frame = output_frame
       out.write(output_frame) 
    
    cv2.destroyAllWindows()
    out.release()
    video.release()

if __name__=="__main__":
    main()
