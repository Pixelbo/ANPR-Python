import numpy as np
import cv2

cap = cv2.VideoCapture(0)

def nothing(x):
    pass

### Create a black image, a window
cv2.namedWindow('image')
cv2.createTrackbar('High Saturation','image',360,360,nothing)
cv2.createTrackbar('High Value','image',55,360,nothing)


while (True):
    # Capture frame-by-frame
    ret, frame = cap.read()
    blur = cv2.GaussianBlur(frame, (5, 5), 0)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
    lower_black = np.array([0, 0, 0])
    upper_black = np.array([180,cv2.getTrackbarPos('High Saturation','image'),cv2.getTrackbarPos('High Value','image')])
    
    mask = cv2.inRange(gray, lower_black, upper_black)
    
    blur2 = cv2.GaussianBlur(mask, (5, 5), 0)
    
    # Bitwise-AND mask and original image
    res = cv2.bitwise_and(frame,frame, mask= mask)


    edges = cv2.Canny(blur2, 100,200)

    ret, thresh_img = cv2.threshold(edges, 91, 255, cv2.THRESH_BINARY)
    contours = cv2.findContours(thresh_img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)[-2]

    for c in contours:
        x, y, w, h = cv2.boundingRect(c)
        ratio = w / h
        area = w*h
        #
        if area > 500 and area < 4000 and ratio<=0.7 and ratio >=0.4:
            img = cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(frame, str(round(ratio,2)),(x,y), cv2.FONT_HERSHEY_SIMPLEX, 1 , (255,0,0))
            crop = img[y:y + h, x:x + w]


    cv2.imshow('mask', mask)
    cv2.imshow('frame', frame)
    cv2.imshow('edges', edges)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
