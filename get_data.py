import cv2
import sys
import os
import shutil
import subprocess

TARGET_FPS = 10
RETAIN_IMAGES = False
SERVER = 'vishal@10.237.23.241'

def get_data_from_images(img_folder):
    subprocess.Popen(['scp', '-r', img_folder, SERVER+':~/AlphaPose/']).wait()
    subprocess.Popen(['ssh', SERVER, '~/AlphaPose/run_alphapose.sh', img_folder]).wait()
    subprocess.Popen(['scp', '-r', SERVER+':~/AlphaPose/results-'+img_folder, '.']).wait()
    subprocess.Popen(['ssh', SERVER, 'rm', '-r', '~/AlphaPose/results-'+img_folder, '~/AlphaPose/'+img_folder]).wait()

def get_data_from_video(vid_path, target_fps):
    cap = cv2.VideoCapture(vid_path)
    original_fps = cap.get(cv2.CAP_PROP_FPS)
    frames_skip = 0
    if original_fps > target_fps:
        frames_skip = original_fps // target_fps
    print('original fps:', original_fps)
    print('frames skip:', frames_skip)

    if not os.path.exists('./frames'):
        os.mkdir('frames')
    i = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        if i % int(frames_skip) == 0:
            cv2.imwrite('frames/'+str(i)+'.jpg', frame)
        i += 1
    
    print(i, 'frames present')
    cap.release()
    cv2.destroyAllWindows()

    get_data_from_images('frames')
    if not RETAIN_IMAGES:
        shutil.rmtree('frames')

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('Usage: python3 get_data.py [path to file]')
        print('e.g. python3 get_data.py awesome.mp4')
        exit()

    get_data_from_video(sys.argv[1], TARGET_FPS)