# Head pose estimation
This is an example of using Baidu API to estimate the head pose in the video instead of the still image. 

### How to use?
First of all, go to [https://ai.baidu.com/tech/face/detect](https://ai.baidu.com/tech/face/detect), where you can use their API for face detection. Click `立即使用` button and after signing up and signing in, you'll get an `API Key` and a `Secret Key`. Follow the instruction in the documentation and replace both `API Key` and `Secret Key` in [baidu_api.py](https://github.com/Messier42/head-pose/blob/master/baidu_api.py).

Then, set a new directory called `video` and put your video file into it. And set another new directory called `result` where the output result will be stored.

Finally, run `python baidu_face.py --video VIDEO_PATH --output_string STRING_OF_OUTPUT_FILE --max_face_num MAXIMUM_NUMBER_OF_FACE_IN_THE_VIDEO` and you'll get the result.

### P.S.
You can use the API totally for free for non-commercial use. 

The default output format of the video is `.mp4@14.85fps`, but you can change it by editing the source code in [baidu_face.py](https://github.com/Messier42/head-pose/blob/master/baidu_face.py).

[utils.py](https://github.com/Messier42/head-pose/blob/master/utils.py) comes from [https://github.com/natanielruiz/deep-head-pose/blob/master/code/utils.py](https://github.com/natanielruiz/deep-head-pose/blob/master/code/utils.py)
@InProceedings{Ruiz_2018_CVPR_Workshops,
author = {Ruiz, Nataniel and Chong, Eunji and Rehg, James M.},
title = {Fine-Grained Head Pose Estimation Without Keypoints},
booktitle = {The IEEE Conference on Computer Vision and Pattern Recognition (CVPR) Workshops},
month = {June},
year = {2018}
}

## Hope you enjoy it :)
