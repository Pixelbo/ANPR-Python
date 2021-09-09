import cv2
import numpy as np

cap = cv2.VideoCapture(0)

def nothing(x):
    pass

### Create a black image, a window
cv2.namedWindow('image')

# create trackbars for color change
cv2.createTrackbar('lH','image',0,360,nothing)
cv2.createTrackbar('lS','image',0,255,nothing)
cv2.createTrackbar('lV','image',0,255,nothing)

cv2.createTrackbar('uH','image',0,360,nothing)
cv2.createTrackbar('uS','image',0,255,nothing)
cv2.createTrackbar('uV','image',0,255,nothing)

##cv2.createTrackbar('l_or_u','image',0,1,nothing)
useTrackbar = 1


while(1):
    
    if useTrackbar != 0:
        lH = cv2.getTrackbarPos('lH','image')
        lS = cv2.getTrackbarPos('lS','image')
        lV = cv2.getTrackbarPos('lV','image')

        uH = cv2.getTrackbarPos('uH','image')
        uS = cv2.getTrackbarPos('uS','image')
        uV = cv2.getTrackbarPos('uV','image')
    else:
        lB = 240
        lG = 255
        lR = 0
        uB = 247
        uG = 255
        uR= 173
    


    # Take each frame
    _, frame = cap.read()

    # Convert BGR to HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    BGRl = np.uint8([[[lH,lS,lV ]]])
    BGRu = np.uint8([[[uH,uS,uV ]]])


    # define range of blue color in HSV
    lower_blue = np.array(BGRl)
    upper_blue = np.array(BGRu)

    # Threshold the HSV image to get only blue colors
    mask = cv2.inRange(hsv, lower_blue, upper_blue)

    # Bitwise-AND mask and original image
    res = cv2.bitwise_and(frame,frame, mask= mask)

    # Capture frame-by-frame
    ret, frame = cap.read()

    # Our operations on the frame come here
##    gray = cv2.cvtColor(res, cv2.COLOR_BGR2GRAY)
##    blur = cv2.GaussianBlur(gray,(5,5),0)
##    ret, thresh_img = cv2.threshold(blur,91,255,cv2.THRESH_BINARY)
##    contours =  cv2.findContours(thresh_img,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)[-2]
    
    kernel = np.ones((5,5),np.uint8)
    erodekernel = np.ones((3,3), np.uint8)
    eroded = cv2.erode(mask, erodekernel, iterations = 2)
    dilatekernel = np.ones((8,8), np.uint8)
    dilated = cv2.dilate(eroded, dilatekernel, iterations = 3)
    dilated,contours,hierarchy = cv2.findContours(dilated,cv2.RETR_CCOMP,cv2.CHAIN_APPROX_SIMPLE)

    
    
    
    for cnt in contours:
        hull = cv2.convexHull(cnt)
        (x,y),radius = cv2.minEnclosingCircle(cnt)
        center = (int(x),int(y))
        radius = int(radius)
        if cv2.contourArea(cnt)>1000:
            for c in contours:
                cv2.drawContours(frame, [c], -1, (0,255,0), 3)
                cv2.drawContours(res, [c], -1, (0,255,0), 3)
                if cv2.contourArea(hull)>2500:
                    cv2.drawContours(frame, [hull], -1, (255,0,0), 3)
                    cv2.drawContours(res, [hull], -1, (255,0,0), 3)
                    

    cv2.imshow('frame',frame)
    cv2.imshow('mask',mask)
    cv2.imshow('res',res)
    

    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        cv2.imwrite('color.png',res)
        break

cv2.destroyAllWindows()
