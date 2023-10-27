from websockets.sync.client import connect

import base64
import cv2
import numpy as np

def fetch_dir(IP: str, Port: str, img: np.array):
    with connect(str("ws://" + IP + ":" + Port)) as ws:
        img = cv2.resize(img, (256, 256))
        _, im_array = cv2.imencode('.png', img)
        im_byte = im_array.tobytes()
        encode_img = base64.b64encode(im_byte)
        ws.send(encode_img)

        message = ws.recv()
        direction = np.frombuffer(message, dtype=np.int16)
        
        return direction