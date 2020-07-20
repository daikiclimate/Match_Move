import os
import argparse
from PIL import Image
import cv2
import time
import match_move

def load_args():
    parser = argparse.ArgumentParser(description='match move')  
    parser.add_argument('video_name', help='置き換えるよう画像。探索する大きい画像')    
    parser.add_argument('box', help='探索したい領域')
    parser.add_argument('ad', help='探索してきた領域を置き換える用画像')

    parser.add_argument('--output_video',default = "output.mp4" ,help='探索してきた領域を置き換える用画像')
    parser.add_argument('--param',default = 1 ,help='探索してきた領域を置き換える用画像')
    parser.add_argument('--fix',default = 1 ,help='ホモグラフィー行列を失敗した時に修正する')
    parser.add_argument('--psnr_th',default = 4 ,help='psnrが一定値以上の場合に崩壊と判断')
    args = parser.parse_args()
    return args


def load_video(video_name):
    video = cv2.VideoCapture(video_name)
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

    out = cv2.VideoWriter(
            # "output/output.mp4",
            "output/" + args.output_video,
            fourcc,
            30,
            (int(W),int(H))
            )

    t = 0
    while True:
       ret, frame = video.read()
       if ret==False:
           break

       #マッチムーブの結果を返す
       output_frame,psnr = match_move.video_function(base = frame, box = args.box, ad = args.ad)
       
       if False:
           print(t, psnr)
           #途中の出力をフレーム単位で保存する。
           #でバグで使用可能
           cv2.imwrite("tmp/tmp"+str(t)+".jpg", output_frame)
           t += 1

       if args.fix:
           if psnr > args.psnr_th:
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
