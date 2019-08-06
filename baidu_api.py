import urllib, urllib.request, sys
import ssl
import json

def get_access_token():
    # client_id 为官网获取的AK， client_secret 为官网获取的SK
    host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=[your client id]&client_secret=[your client secret]'
    request = urllib.request.Request(host)
    request.add_header('Content-Type', 'application/json; charset=UTF-8')
    response = urllib.request.urlopen(request)
    content = response.read()
    if (content):
        content = json.loads(content)
        #print(content["access_token"])
        return str(content["access_token"])

#人脸检测
def face_detection(base64_data, max_face_num):
    request_url = "https://aip.baidubce.com/rest/2.0/face/v3/detect"

    params = {'image': base64_data, 'image_type': 'BASE64','face_field':'emotion', 'max_face_num':max_face_num}
    params = urllib.parse.urlencode(params).encode("utf-8")

    access_token = get_access_token()

    request_url = request_url + "?access_token=" + access_token
    request = urllib.request.Request(url=request_url, data=params)
    request.add_header('Content-Type', 'application/json')
    response = urllib.request.urlopen(request)
    content = response.read()
    if content:
        return content
