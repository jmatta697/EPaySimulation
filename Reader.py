import cv2
import pyzbar.pyzbar as pyzbar
import simpleaudio as sa

wave_obj = sa.WaveObject.from_wave_file("read_complete.wav")

cap = cv2.VideoCapture(1)
font = cv2.FONT_HERSHEY_PLAIN

id_num = ''

while True:
    _, frame = cap.read()

    decodedObjects = pyzbar.decode(frame)

    for obj in decodedObjects:
        print(obj.data)
        id_num = obj.data

    cv2.imshow("Frame", frame)

    if id_num != '':
        play_obj = wave_obj.play()
        play_obj.wait_done()
        
        break

    key = cv2.waitKey(1)
    if key == 27:   # 27 = 'S' on keyboard
        break


cv2.destroyAllWindows()
cap.release()




# img = cv2.imread("test_QR1.png")
#
# decodedObjects = pyzbar.decode(img)
#
# for obj in decodedObjects:
#     print(obj.data)
#
# cv2.imshow("Image", img)
# cv2.waitKey(0)