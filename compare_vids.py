from get_data import get_data
from check_angles import get_angles
import os
import sys
import cv2
import numpy as np

degree_tolerance = 10 # threshold for considering the angles similar
show_left_limb = True # show angles of left limb on the frame
show_right_limb = True # show angles of right limb on the frame
frame_display_delay = 50 # delay between frames, the higher this number, the slower the video playback

class colors:
    green = '\033[92m'
    red = '\033[91m'
    end = '\033[0m'

def compare_vids(vid_path1, vid_path2, left_limb, right_limb):
    vid_name1 = vid_path1.split('/')[-1].split('.')[0]
    vid_name2 = vid_path2.split('/')[-1].split('.')[0]
    json_path1 = 'results-' + vid_name1 + '/alphapose-results.json'
    json_path2 = 'results-' + vid_name2 + '/alphapose-results.json'
    if not os.path.isfile(json_path1):
        get_data(vid_path1)
    if not os.path.isfile(json_path2):
        get_data(vid_path2)
    angles1 = get_angles(json_path1)
    angles2 = get_angles(json_path2)

    rendered_vid1 = 'results-' + vid_name1 + '/AlphaPose_' + vid_name1 + '.mp4'
    rendered_vid2 = 'results-' + vid_name2 + '/AlphaPose_' + vid_name2 + '.mp4'

    cap1 = cv2.VideoCapture(rendered_vid1)
    cap2 = cv2.VideoCapture(rendered_vid2)

    i = 0
    while True:
        ret1, frame1 = cap1.read()
        ret2, frame2 = cap2.read()
        if not (ret1 and ret2):
            break 

        frame1 = cv2.resize(frame1, None, fx=0.4, fy=0.4, interpolation=cv2.INTER_LINEAR)
        frame2 = cv2.resize(frame2, None, fx=0.4, fy=0.4, interpolation=cv2.INTER_LINEAR)
        both_frames = np.concatenate((frame1, frame2), axis=1)
        
        lshoulder = abs(angles1[i][0] - angles2[i][0])
        lelbow = abs(angles1[i][1] - angles2[i][1])
        rshoulder = abs(angles1[i][2] - angles2[i][2])
        relbow = abs(angles1[i][3] - angles2[i][3])

        if left_limb: 
            color = (0, 255, 0) if lshoulder < degree_tolerance else (0, 0, 255) # BGR
            cv2.putText(both_frames, f'Left shoulder: {lshoulder}', (10,10), cv2.FONT_HERSHEY_SIMPLEX, 0.4, color, 1)
            color = (0, 255, 0) if lshoulder < degree_tolerance else (0, 0, 255)
            cv2.putText(both_frames, f'Left elbow: {lelbow}', (10,20), cv2.FONT_HERSHEY_SIMPLEX, 0.4, color, 1)

        if right_limb:
            color = (0, 255, 0) if lshoulder < degree_tolerance else (0, 0, 255)
            cv2.putText(both_frames, f'Right shoulder: {rshoulder}', (10,30), cv2.FONT_HERSHEY_SIMPLEX, 0.4, color, 1)
            color = (0, 255, 0) if lshoulder < degree_tolerance else (0, 0, 255)
            cv2.putText(both_frames, f'Right elbow: {relbow}', (10,40), cv2.FONT_HERSHEY_SIMPLEX, 0.4, color, 1)

        cv2.imshow('Frame', both_frames)

        if cv2.waitKey(frame_display_delay) & 0xFF == ord('q'):
            break
        i = i+1

    cap1.release()
    cap2.release()
    # cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print('Usage: python3 compare_vids.py [path to video 1] [path to video 2]')
        print('e.g. python3 compare_vids.py test-1.mp4 test-2.mp4')
        exit()

    compare_vids(sys.argv[1], sys.argv[2], show_left_limb, show_right_limb)

