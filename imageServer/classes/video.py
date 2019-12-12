import cv2
import numpy as np

class Video:
    client = None
    v = None

    def __init__(self, client):
        super().__init__()
        self.v = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        if not self.v.isOpened():
            raise IOError("Cannot open video device")

        self.client = client

    def run(self):
        fps = 30
        curr_frame = 0

        while True:
            ret, frame = self.v.read()
            if ret is True:
                if curr_frame % (fps/10) == 0: # each third frame
                    # Resize
                    res = cv2.resize(frame, dsize=(224, 224), interpolation=cv2.INTER_CUBIC)

                    # Encoding
                    encode_param=[int(cv2.IMWRITE_JPEG_QUALITY),90]
                    result, imgencode = cv2.imencode('.jpg', res, encode_param)
                    data = np.array(imgencode)
                    stringData = data.tostring()

                    # Sending
                    self.client.send((str(len(stringData)).ljust(16)).encode("ascii"))
                    self.client.send(stringData)  # Send resized image
                
                if curr_frame < 29:
                    curr_frame += 1
                else:
                    curr_frame = 0

        v.release()