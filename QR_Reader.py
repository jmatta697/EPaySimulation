import cv2
import pyzbar.pyzbar as pyzbar
import simpleaudio as sa


class QRReader:
    # (a video source of 0 defaults to the internal laptop web cam)
    def __init__(self, video_source):
        # open video source
        self.cap = cv2.VideoCapture(video_source)
        # error check to see is video capture source opens successfully
        if not self.cap.isOpened():
            raise ValueError("Unable to open video source", video_source)
        # set video capture window size
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 120)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 120)
        # 'read complete' sound
        self.read_complete_sound_obj = sa.WaveObject.from_wave_file("Sounds/read_complete.wav")
        # display text - (for debugging)
        self.debug_font = cv2.FONT_HERSHEY_PLAIN
        # set QR data to empty string
        self.QR_data_str = ''

    def run_reader(self):
        while True:
            _, frame = self.cap.read()
            decoded_objects = pyzbar.decode(frame)
            for obj in decoded_objects:
                print(f'The QR Reader has read >>> {obj.data}')
                self.QR_data_str = obj.data
            cv2.imshow("Frame", frame)
            if self.QR_data_str != '':
                play_obj = self.read_complete_sound_obj.play()
                play_obj.wait_done()
                break
            key = cv2.waitKey(1)
            if key == 113:  # 113 = 'q' on keyboard (for 'quit' to close the screen)
                break
        self.cap.release()
        cv2.destroyAllWindows()

        return self.QR_data_str
