import cv2
from cvzone.HandTrackingModule import HandDetector
import numpy as np
import os as oss
import traceback

capture = cv2.VideoCapture(0)
hd = HandDetector(maxHands=1)
hd2 = HandDetector(maxHands=1)

count = len(oss.listdir("C:\\Users\\wissa\\Desktop\\Final-model\\A-Z_struct\\A"))
c_dir = 'A'

offset = 15
step = 1
flag = False
suv = 0

white = np.ones((400, 400), np.uint8) * 255
cv2.imwrite("C:\\Users\\wissa\\Desktop\\Final-model\\white.jpg", white)

# Define state lists
alphabet_states = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
special_states = ['Backspace', 'Next', 'Space']

while True:
    try:
        _, frame = capture.read()
        frame = cv2.flip(frame, 1)
        hands, img = hd.findHands(frame, draw=False, flipType=True)
        white = cv2.imread("C:\\Users\\wissa\\Desktop\\Final-model\\white.jpg")

        if hands:
            hand = hands[0]
            bbox = hand['bbox']
            x, y, w, h = bbox
            image = np.array(frame[y - offset:y + h + offset, x - offset:x + w + offset])

            handz, imz = hd2.findHands(image, draw=True, flipType=True)
            if handz:
                hand = handz[0]
                pts = hand['lmList']
                os = ((400 - w) // 2) - 15
                os1 = ((400 - h) // 2) - 15
                for t in range(0, 4, 1):
                    cv2.line(white, (pts[t][0] + os, pts[t][1] + os1), (pts[t + 1][0] + os, pts[t + 1][1] + os1), (0, 255, 0), 3)
                for t in range(5, 8, 1):
                    cv2.line(white, (pts[t][0] + os, pts[t][1] + os1), (pts[t + 1][0] + os, pts[t + 1][1] + os1), (0, 255, 0), 3)
                for t in range(9, 12, 1):
                    cv2.line(white, (pts[t][0] + os, pts[t][1] + os1), (pts[t + 1][0] + os, pts[t + 1][1] + os1), (0, 255, 0), 3)
                for t in range(13, 16, 1):
                    cv2.line(white, (pts[t][0] + os, pts[t][1] + os1), (pts[t + 1][0] + os, pts[t + 1][1] + os1), (0, 255, 0), 3)
                for t in range(17, 20, 1):
                    cv2.line(white, (pts[t][0] + os, pts[t][1] + os1), (pts[t + 1][0] + os, pts[t + 1][1] + os1), (0, 255, 0), 3)
                cv2.line(white, (pts[5][0] + os, pts[5][1] + os1), (pts[9][0] + os, pts[9][1] + os1), (0, 255, 0), 3)
                cv2.line(white, (pts[9][0] + os, pts[9][1] + os1), (pts[13][0] + os, pts[13][1] + os1), (0, 255, 0), 3)
                cv2.line(white, (pts[13][0] + os, pts[13][1] + os1), (pts[17][0] + os, pts[17][1] + os1), (0, 255, 0), 3)
                cv2.line(white, (pts[0][0] + os, pts[0][1] + os1), (pts[5][0] + os, pts[5][1] + os1), (0, 255, 0), 3)
                cv2.line(white, (pts[0][0] + os, pts[0][1] + os1), (pts[17][0] + os, pts[17][1] + os1), (0, 255, 0), 3)

                skeleton0 = np.array(white)
                zz = np.array(white)
                for i in range(21):
                    cv2.circle(white, (pts[i][0] + os, pts[i][1] + os1), 2, (0, 0, 255), 1)

                skeleton1 = np.array(white)

                cv2.imshow("1", skeleton1)

        frame = cv2.putText(frame, "dir=" + str(c_dir) + "  count=" + str(count), (50, 50),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            1, (255, 0, 0), 1, cv2.LINE_AA)
        cv2.imshow("frame", frame)
        interrupt = cv2.waitKey(1)
        if interrupt & 0xFF == 27:
            break

        if interrupt & 0xFF == ord('n'):
            if c_dir in alphabet_states:
                if c_dir != 'Z':
                    c_dir = chr(ord(c_dir) + 1)
                else:
                    c_dir = special_states[0]  
            elif c_dir == special_states[0]:  
                c_dir = special_states[1]  
            elif c_dir == special_states[1]:  
                c_dir = special_states[2]  
            elif c_dir == special_states[2]:  
                c_dir = alphabet_states[0]  

            count = len(oss.listdir(f"C:\\Users\\wissa\\Desktop\\Final-model\\A-Z_struct\\{c_dir}\\"))

        if interrupt & 0xFF == ord('a'):
            if flag:
                flag = False
            else:
                suv = 0
                flag = True

        print("=====",flag)
        if flag:
            if suv == 180:
                flag = False
            if step % 3 == 0:
                cv2.imwrite(f"C:\\Users\\wissa\\Desktop\\Final-model\\A-Z\\{c_dir}\\{str(count)}.jpg", skeleton1)
                count += 1
                suv += 1
            step += 1

    except Exception:
        print("==", traceback.format_exc())

capture.release()
cv2.destroyAllWindows()
