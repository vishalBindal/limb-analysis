# limb-analysis

### Setup
1. Set up passwordless ssh login to vishal@10.237.23.241 (or any server where AlphaPose is installed). Follow instructions at https://linuxize.com/post/how-to-setup-passwordless-ssh-login/
2. Install opencv in a python 3.8 environment
```
conda create -n env python=3.8
conda activate env
pip install opencv-python
```

### Usage

1. Comparing angles at shoulder and elbow in 2 videos
```
python3 compare_vids.py <path to video file 1> <path to video file 2>
```

2. Obtaining joint data from AlphaPose
```
python3 get_data.py <path to video file>
```
Results will be saved in *results-<video name>* directory in .json format, as given at https://github.com/MVIG-SJTU/AlphaPose/blob/master/docs/output.md
  
3. Obtaining angles at shoulder and elbow from json
```
python3 check_angles.py <path to json file>
```
