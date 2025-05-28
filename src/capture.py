import cv2


class Capture():
    def __init__(self, id_camera):
        self.id_camera = id_camera

    def initialize_camera(self):
        self.cap = cv2.VideoCapture(self.id_camera)

    def get_frame(self):
        self.initialize_camera()
        for _ in range(5):
            self.cap.grab()

        ret, frame = self.cap.read()

        if ret:
            self.release()
            return frame
        else:
            print("None: ret")
            return frame

    def release(self):
        self.cap.release()
