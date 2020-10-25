from flask import Flask
from flask import request
from flask_cors import CORS
import os
import base64
app = Flask(__name__)

@app.route('/encode', methods = ['POST'])
def encode():
    img = request.values.get('img')
    txt = request.values.get('txt')
    img_ori = base64.b64decode(img)
    with open('./upload/upload.png', 'wb') as f:
        f.write(img_ori)
    str_secret = txt
    cmd = ['python','--secret']
    pth_ecd_function = 'StegaStamp/encode_image.py'
    cmd_run = cmd[0] + ' ' + pth_ecd_function + ' ' + cmd[1] + ' ' + str_secret
    os.system(cmd_run) # launch image watermark model
    # to this step, encoded image is saved in ./save/decoded.png
	
    pth_encoded_img = 'save/decoded.png'
    with open(pth_encoded_img, 'rb') as f:
        img_ecd = f.read()
        img_ecd_base64 = base64.b64encode(img_ecd)
    os.system('rm upload/upload.png')
    os.system('rm save/decoded.png')

    return img_ecd_base64

@app.route('/decode', methods = ['POST'])
def deccode():
    img_ori = request.values.get('img')
    with open('upload/upload.png', 'wb') as f:
        f.write(img_ori)
    cmd = ['python', '--image']
    pth_dcd_function = 'StegaStamp/decode_image.py'
    cmd_run = cmd[0] + ' ' + pth_dcd_function
    os.system(cmd_run)
    pth_code = 'save/code.txt'
    with open(pth_code, 'r') as f:
        str_code = f.read()
    os.system('rm upload/upload.png')
    os.system('rm save/code.txt')
    return str_code

@app.route('/test', methods=['GET'])
def test():
    text = request.values.get("text")
    return text

if __name__ == '__main__':
    CORS(app, supports_credentials=True)
    app.run(
            host = '127.0.0.1',
            port = 5000,  
            debug = True 
            )
