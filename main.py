import numpy as np
import cv2


def nothing(x):
    pass


### Create a black image, a window
cv2.namedWindow('image')

# create trackbars for color change
cv2.createTrackbar('min', 'image', 200, 500, nothing)
cv2.createTrackbar('max', 'image', 200, 500, nothing)

cap = cv2.VideoCapture(1)

while (True):
    # Capture frame-by-frame
    ret, frame = cap.read()

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    edges = cv2.Canny(blur, cv2.getTrackbarPos('min', 'image'), cv2.getTrackbarPos('max', 'image'))

    ret, thresh_img = cv2.threshold(edges, 91, 255, cv2.THRESH_BINARY)
    contours = cv2.findContours(thresh_img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)[-2]

    for c in contours:
        rect = cv2.minAreaRect(c)
        if rect[1][1] != 0:
            ratio = rect[1][0]/rect[1][1]
            area = rect[1][0]*rect[1][1]
            if area > 200 and ratio<0.7:
                box = cv2.boxPoints(rect)
                box = np.int0(box)
                im = cv2.drawContours(frame, [box], 0, (0, 0, 255), 2)
                cv2.putText(frame, str(round(ratio,2)),(int(rect[0][0]),int(rect[0][1])), cv2.FONT_HERSHEY_SIMPLEX, 1 , (255,0,0))

    cv2.imshow('edges', thresh_img)
    cv2.imshow('frame', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
