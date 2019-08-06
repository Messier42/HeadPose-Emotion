# encoding:utf-8
import sys, os, argparse
import urllib
import urllib.request
import cv2
import json
import utils
import math
import baidu_api


#定义输入参数
def parse_args():
    parser = argparse.ArgumentParser(description='Head pose estimation using the Baidu API.')
    parser.add_argument('--video', dest='video', help='Path of video',type=str)
    parser.add_argument('--output_string', dest='output_string', help='String appended to output file',type=str)
    parser.add_argument('--max_face_num', dest='max_face_num', help='Maximum number of face', type=int, default=2)
    parser.add_argument('--fps', dest='fps', help='The fps of the output video', type=int)
    args = parser.parse_args()
    return args


if __name__ == '__main__':
    args = parse_args()

    file = open('result/face/%s.txt' %args.output_string, 'w')

    video = cv2.VideoCapture(args.video) 

    # 定义输出视频格式 
    width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))   
    height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT)) 
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter('result/face/%s.mp4' %args.output_string, fourcc, args.fps, (width, height))
    
    count = 1   
    try:        
        while True:            
            ret, frame = video.read()
            if ret == False:
                break   

            # 视频转码       
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)            
            base64_data = utils.frame2base64(frame)   

            #调用API处理         
            content = baidu_api.face_detection(base64_data, args.max_face_num)

            # 处理返回的数据
            content = json.loads(content)
            error_code = content["error_code"]

            if error_code == 0:
                result = content["result"]
                face_num = int(result["face_num"])

                while face_num>0:
                    face_list = result["face_list"]

                    if(face_list[face_num-1]["face_probability"] > 0.5):

                        # 获取人脸位置信息
                        location = face_list[face_num-1]["location"]
                        x_min = float(location["left"])
                        y_min = float(location["top"])
                        rotation = int(location["rotation"])
                        width = float(location["width"]) 
                        height = float(location["height"]) 

                        # 计算矩形框中心点到左上顶点的距离
                        alpha = math.atan(width/height)
                        beta = math.radians(rotation)
                        cross_line = ((width ** 2 + height ** 2) ** 0.5)/2

                        # 计算矩形框中心点
                        td_x = x_min + math.sin(alpha-beta)*cross_line
                        td_y = y_min + math.cos(alpha-beta)*cross_line

                        # 头部姿态欧拉角
                        angle = face_list[face_num-1]["angle"]
                        yaw = float(angle["yaw"])
                        pitch = float(angle["pitch"])
                        roll  = float(angle["roll"])

                        # 画欧拉角
                        utils.draw_axis(frame, yaw, pitch, roll, tdx = td_x, tdy= td_y, size = height/2)
                        #utils.plot_pose_cube(frame, yaw, pitch, roll, tdx = td_x, tdy = td_y, size = height/2)

                        #标注人脸位置
                        utils.plot_pose_base(frame, yaw, pitch, roll, tdx = td_x, tdy = td_y)

                        #表情
                        emotion = face_list[face_num-1]["emotion"]
                        tpe = str(emotion["type"])
                        probability = str(emotion["probability"])

                        #显示表情
                        font = cv2.FONT_HERSHEY_COMPLEX
                        txt = tpe+', '+probability
                        if(tpe == 'angry'):
                            cv2.putText(frame, txt, (int(x_min)-100,int(y_min)-100), font, 1, (0,0,255), 2)
                        elif(tpe == 'happy'):
                            cv2.putText(frame, txt, (int(x_min)-100,int(y_min)-100), font, 1, (0,165,255), 2)
                        elif(tpe == 'fear'):
                            cv2.putText(frame, txt, (int(x_min)-100,int(y_min)-100), font, 1, (255,0,139), 2)
                        elif(tpe == 'disgust'):
                            cv2.putText(frame, txt, (int(x_min)-100,int(y_min)-100), font, 1, (0,255,0), 2)
                        elif(tpe == 'surprise'):
                            cv2.putText(frame, txt, (int(x_min)-100,int(y_min)-100), font, 1, (255,127,0), 2)
                        elif(tpe == 'sad'):
                            cv2.putText(frame, txt, (int(x_min)-100,int(y_min)-100), font, 1, (255,0,0), 2)
                        else:
                            cv2.putText(frame, txt, (int(x_min)-100,int(y_min)-100), font, 1, (0,255,255), 2)
                        
                        # print(yaw, pitch, roll)
                        print('frame %d, yaw: %f, pitch: %f, roll: %f' % (count, yaw, pitch, roll))
                        file.write('%d %f %f %f %s %s\n' % (count, yaw, pitch, roll, tpe, probability))

                    else:
                        print('no face')

                    face_num = face_num-1

                out.write(frame)

            else:
                print('no face in frame %d' % count)

            count = count+1

    except Exception as e:        
        print(e)  

    finally:        # 释放资源        
        video.release()
        out.release()

    file.close()
    print('file saved')
