import numpy as np
import cv2

cap = cv2.VideoCapture(1)

def nothing(x):
    pass

cv2.namedWindow('image')
cv2.createTrackbar('canny','image',0,360,nothing)
while (1):
    ret, frame = cap.read()
    gray_vid = cv2.cvtColor(frame, cv2.IMREAD_GRAYSCALE)
    canny = cv2.getTrackbarPos('canny', 'image')
    edged_frame = cv2.Canny(frame, canny, 300)

    dilated, contours, hierarchy = cv2.findContours(edged_frame,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)


    for cnt in contours:
        if cv2.contourArea(cnt) > 30 and cv2.contourArea(cnt) < 100:
            [x, y, w, h] = cv2.boundingRect(cnt)
            hull = cv2.convexHull(cnt)
            cv2.drawContours(frame, [cnt], -1, (0, 255, 0), 3)
            if cv2.contourArea(hull) > 100:
                [x2, y2, w2, h2] = cv2.boundingRect(hull)
                extract = edged_frame[y2:y2 + h2, x2:x2 + w2]
                cv2.imshow('extract', extract)
                cv2.drawContours(frame, [hull], -1, (255, 0, 0), 3)
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)


    # show the output image
    cv2.imshow('Edges', edged_frame)
    cv2.imshow("output", frame)


    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break
cap.release()
cv2.destroyAllWindows()