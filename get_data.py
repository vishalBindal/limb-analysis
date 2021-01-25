import cv2
import sys
import os
import shutil
import subprocess

SEND_IMAGES = False
RENDERED_DATA = True
TARGET_FPS = 10
SERVER = 'vishal@10.237.23.241'

def get_data_alphapose(path, results_dir_name, is_vid, get_rendered):
    '''
    Run AlphaPose remotely on data and get back the joint data
    path: path to video file or directory of images
    results_dir_name: name of directory where results are to be stored
    is_vid: True if video file, False if directory of images
    get_rendered: if rendered data is to be generated
    '''
    # SCP data to the server
    subprocess.run(['scp', '-r', path, SERVER+':~/AlphaPose/'])
    # Run alphapose
    end_path = path.split('/')[-1]
    alph_cmd = 'echo ; source ~/miniconda3/bin/activate alphapose ; cd ~/AlphaPose ;'
    alph_cmd += 'python scripts/demo_inference.py --cfg configs/coco/resnet/256x192_res50_lr1e-3_1x.yaml --checkpoint pretrained_models/fast_res50_256x192.pth'
    if is_vid:
        alph_cmd += f' --video {end_path} --outdir {results_dir_name}'
        if get_rendered:
            alph_cmd += ' --save_video'
    else:
        alph_cmd += f' --indir {end_path} --outdir {results_dir_name}'
        if get_rendered:
            alph_cmd += ' --save_img'
    subprocess.run(['ssh', SERVER] + alph_cmd.split())
    # SCP results back
    subprocess.run(['scp', '-r', SERVER+':~/AlphaPose/'+results_dir_name, '.'])
    # Delete data on server
    subprocess.run(['ssh', SERVER, 'rm', '-r', '~/AlphaPose/' + end_path, '~/AlphaPose/' + results_dir_name])

def get_images_from_video(vid_path, target_fps):
    cap = cv2.VideoCapture(vid_path)
    original_fps = cap.get(cv2.CAP_PROP_FPS)
    frames_skip = 0
    if original_fps > target_fps:
        frames_skip = original_fps // target_fps
    print('original fps:', original_fps)
    print('frames skip:', frames_skip)

    if not os.path.exists('./frames'):
        os.mkdir('frames')
    
    i, retained = 0, 0
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        if i % int(frames_skip) == 0:
            cv2.imwrite('frames/'+str(i)+'.jpg', frame)
            retained += 1
        i += 1
    
    print(f'{retained} out of {i} frames retained')
    cap.release()
    cv2.destroyAllWindows()

def get_data(vid_path):
    vid_name = vid_path.split('/')[-1].split('.')[0]
    if SEND_IMAGES:
        get_images_from_video(vid_path, TARGET_FPS)
        get_data_alphapose('frames', 'results-'+vid_name, False, RENDERED_DATA)
        shutil.rmtree('frames')
    else:
        get_data_alphapose(vid_path, 'results-'+vid_name, True, RENDERED_DATA)

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('Usage: python3 get_data.py [path to file]')
        print('e.g. python3 get_data.py awesome.mp4')
        exit()

    vid_path = sys.argv[1]
    get_data(vid_path)
    