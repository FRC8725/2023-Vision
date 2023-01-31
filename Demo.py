# from cscore import CameraServer
# from networktables import NetworkTables

import cv2 as cv
import numpy as np
import time
import json

import ConeDetection as CDetect


def main():

    with open('camera.json', 'r') as jsonfile:
        camera_data = json.load(jsonfile)
    # setting the cameara matrix
    # mtx = np.array([[669.76134921, 0., 364.47532344],
    #                 [0., 669.8613114, 225.14641631],
    #                 [0., 0., 1.]])
    width = camera_data['width']
    height = camera_data['height']
    fps = camera_data['fps']
    
    width = 320
    height = 240
    # dist = np.array(
    #     [[0.09899272, -0.34263704, 0.00170763,  0.01447023,  1.06025138]])
    # dist = np.array([[0., 0., 0., 0., 0.]])
    cap = cv.VideoCapture(0)
    cap.set(5, fps)
    cap.set(3, width)
    cap.set(4, height)

    if not cap.isOpened():
        print("CAM error")
        exit()

    img = np.zeros(shape=(height, width, 3), dtype=np.uint8)
    output_img = np.copy(img)

    while True:
        start_time = time.time()
        ret, frame = cap.read()

        if not ret:
            break
        
        CDetect.ConeDetection(frame, frame)

        # print(output_img)

        output_img = np.copy(frame)
        pocessing_time = time.time() - start_time
        fps = 1/pocessing_time
        cv.putText(output_img, str(round(fps, 1)), (0, 40), cv.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255))
        cv.imshow("processing", output_img)

        if cv.waitKey(1) == ord('p'):
            cv.imwrite('./calibration.jpg', output_img)

        if cv.waitKey(1) == ord('q'):
            break

    cap.release()
    cv.destroyAllWindows()

def demo():
    pass

if __name__ == '__main__':
    main()
else:
    demo()
