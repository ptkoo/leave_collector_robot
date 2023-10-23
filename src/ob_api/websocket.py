import asyncio
# from websockets.client import connect # user for async request
from websockets.sync.client import connect # We have only one robot and one request each time. It is better to use synchronous function base.

import base64
import cv2
import numpy as np

def request_dir(im: np.array):
    with connect("ws://192.168.106.23:1234") as ws:
        img = cv2.resize(im, (256, 256))
        _, im_array = cv2.imencode('.png', img)
        im_byte = im_array.tobytes()
        encode_img = base64.b64encode(im_byte)
        ws.send(encode_img)

        message = ws.recv()
        direction = np.frombuffer(message, dtype=np.int16)

        return direction

if __name__ == "__main__":
    print(request_dir(cv2.imread('./left.png')))
