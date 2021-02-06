import json 
import sys
import math
  
def calc_slope(p1,p2):
    if p1[0] - p2[0] == 0:
        return float('inf')
    else:
        return abs((p1[1] - p2[1])/(p1[0] - p2[0]))

def read_angles(data):
    angles = []
    lengths = []

    for frame in data:
        joints = frame['keypoints']
        left_shoulder = (joints[15],joints[16])
        right_shoulder = (joints[18],joints[19])
        left_elbow = (joints[21],joints[22])
        right_elbow = (joints[24],joints[25])
        left_wrist = (joints[27],joints[28])
        right_wrist = (joints[30],joints[31])

        slope_shoulders = calc_slope(left_shoulder,right_shoulder)

        slope_left_shoulder_to_elbow = calc_slope(left_shoulder,left_elbow)
        slope_left_elbow_to_wrist = calc_slope(left_elbow,left_wrist)

        slope_right_shoulder_to_elbow = calc_slope(right_shoulder,right_elbow)
        slope_right_elbow_to_wrist = calc_slope(right_elbow,right_wrist)

        #angle1 is angle between line connecting the shoulders to the line connecting left shoulder and elbow
        tan_angle1 = abs((slope_shoulders - slope_left_shoulder_to_elbow)/(1 + slope_shoulders*slope_left_shoulder_to_elbow))
        angle1 = math.degrees(math.atan(tan_angle1))

        #angle2 is angle between line connecting left elbow and wrist to line connecting left shoulder and elbow
        tan_angle2 = abs((slope_left_elbow_to_wrist - slope_left_shoulder_to_elbow)/(1 + slope_left_elbow_to_wrist*slope_left_shoulder_to_elbow))
        angle2 = math.degrees(math.atan(tan_angle2))

        #angle3 is angle between line connecting the shoulders to the line connecting right shoulder and elbow
        tan_angle3 = abs((slope_shoulders - slope_right_shoulder_to_elbow)/(1 + slope_shoulders*slope_right_shoulder_to_elbow))
        angle3 = math.degrees(math.atan(tan_angle3))

        #angle4 is angle between line connecting right elbow and wrist to line connecting left shoulder and elbow
        tan_angle4 = abs((slope_right_elbow_to_wrist - slope_right_shoulder_to_elbow)/(1 + slope_right_elbow_to_wrist*slope_right_shoulder_to_elbow))
        angle4 = math.degrees(math.atan(tan_angle4))

        angles.append((angle1,angle2,angle3,angle4))

        #length1 is length of segment from left shoulder to left elbow
        length1 = math.sqrt((left_shoulder[0] - left_elbow[0])**2 + (left_shoulder[1] - left_elbow[1])**2)

        #length2 is length of segment from left elbow to left wrist
        length2 = math.sqrt((left_wrist[0] - left_elbow[0])**2 + (left_wrist[1] - left_elbow[1])**2)

        #length3 is length of segment from right shoulder to right elbow
        length3 = math.sqrt((right_shoulder[0] - right_elbow[0])**2 + (right_shoulder[1] - right_elbow[1])**2)

        #length4 is length of segment from right elbow to right wrist
        length4 = math.sqrt((right_wrist[0] - right_elbow[0])**2 + (right_wrist[1] - right_elbow[1])**2)

        lengths.append((length1, length2, length3, length4))

    return angles, lengths

def get_angles(file_path):
    # Opening JSON file 
    f = open(file_path,) 
    
    # returns JSON object as  
    # a dictionary 
    data = json.load(f) 
    
    # the data is a list of dictionaries where each dictionary captures a frame
    # refer the github page for info on the contents of the dictionary
    # We have assumed the presence of just 1 person in the frame
    angles = read_angles(data)

    # Closing file 
    f.close()
     
    return angles

if __name__ == '__main__':
    angles = get_angles(sys.argv[1],)
    frame = 1
    for angle in angles:
        print('frame' , frame , ':' , angle)
        frame+=1