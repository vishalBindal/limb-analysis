# limb-analysis

## Getting joint data

### Setup
1. Set up passwordless ssh login to vishal@10.237.23.241 (or any server where AlphaPose is installed). Follow instructions at https://linuxize.com/post/how-to-setup-passwordless-ssh-login/
2. Install opencv in a python 3.8 environment
```
conda create -n env python=3.8
conda activate env
pip install opencv-python
```

### Usage
```
python3 get_data.py <path to video file>
```
Results will be saved in *results-frame* directory in .json format, as given at https://github.com/MVIG-SJTU/AlphaPose/blob/master/docs/output.md
