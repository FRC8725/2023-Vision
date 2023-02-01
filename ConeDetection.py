import cv2 as cv
from math import atan, degrees, asin
import numpy as np

def ConeDetection(img, output_img):
    imgc = np.copy(img)
    blurred = cv.GaussianBlur(imgc, (11, 11), 0)
    hsv = cv.cvtColor(blurred, cv.COLOR_BGR2HSV)
    
    lThreshold = np.array([0, 100, 50])
    hThreshold = np.array([40, 255, 255])
    thresh = cv.inRange(hsv, lThreshold, hThreshold)
    thresh = cv.dilate(thresh, None, iterations=2)
    thresh = cv.erode(thresh, None, iterations=2)
    
    # cv.imshow('threshold', thresh)
    
    cnts, _ = cv.findContours(thresh, cv.RETR_TREE, cv.CHAIN_APPROX_NONE)
    angle = 0
    
    if len(cnts) != 0:
        
        cnt = max(cnts, key = cv.contourArea)
        approx = cv.approxPolyDP(cnt, 0.01*cv.arcLength(cnt, True), True)
        # hull = cv.convexHull(approx)
        _, triangle = cv.minEnclosingTriangle(approx)
        
        output_img = cv.drawContours(output_img, [approx], -1, (0,255,255), 3)
        p1 = tuple(np.array(triangle[0][0], np.int32).tolist())
        p2 = tuple(np.array(triangle[1][0], np.int32).tolist())
        p3 = tuple(np.array(triangle[2][0], np.int32).tolist())
        cv.line(output_img, p1, p2, (0, 255, 0), 4, cv.LINE_AA)
        cv.line(output_img, p3, p2, (0, 255, 0), 4, cv.LINE_AA)
        cv.line(output_img, p1, p3, (0, 255, 0), 4, cv.LINE_AA)
        p1p2 = cv.norm(p1, p2, cv.NORM_L2)
        p2p3 = cv.norm(p2, p3, cv.NORM_L2)
        p1p3 = cv.norm(p1, p3, cv.NORM_L2)
        
        if p1 == None or p2 == None or p3 == None: return 0;
        
        if p1p2 < p2p3 and p1p2 < p1p3:
            mid = (int((p1[0]+p2[0])/2), int((p1[1]+p2[1])/2))
            if (p3[0]-mid[0] == 0): angle = atan(p3[1]-mid[1])
            else: angle = atan((p3[1]-mid[1])/(p3[0]-mid[0]))
            if (p3[0]-mid[0] < 0): angle -= 3.14;
        elif p2p3 < p1p2 and p2p3 < p1p3:
            mid = (int((p2[0]+p3[0])/2), int((p2[1]+p3[1])/2))
            if (p1[0]-mid[0] == 0): angle = atan(p1[1]-mid[1])
            else: angle = atan((p1[1]-mid[1])/(p1[0]-mid[0]))
            if (p1[0]-mid[0] < 0): angle -= 3.14;
        elif p1p3 < p2p3 and p1p3 < p1p2:
            mid = (int((p1[0]+p3[0])/2), int((p1[1]+p3[1])/2))
            if (p2[0]-mid[0] == 0): angle = atan(p2[1]-mid[1])
            else: angle = atan((p2[1]-mid[1])/(p2[0]-mid[0]))
            if (p2[0]-mid[0] < 0): angle -= 3.14;
    print(angle + 3.14/2)
    return angle + 3.14 / 2
                
            
if __name__ == '__main__':
    import Demo
    Demo.main()