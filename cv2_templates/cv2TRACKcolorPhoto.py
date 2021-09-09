import cv2
import numpy as np

cap = cv2.VideoCapture("DSC09513.JPG")

def nothing(x):
    pass

# Create a black image, a window
img = np.zeros((300,512,3), np.uint8)
cv2.namedWindow('image')

# create trackbars for color change
cv2.createTrackbar('lH','image',0,255,nothing)
cv2.createTrackbar('lS','image',0,255,nothing)
cv2.createTrackbar('lV','image',0,255,nothing)

cv2.createTrackbar('uH','image',0,255,nothing)
cv2.createTrackbar('uS','image',0,255,nothing)
cv2.createTrackbar('uV','image',0,255,nothing)

cv2.createTrackbar('l_or_u','image',0,1,nothing)



while(1):
    
    lB = cv2.getTrackbarPos('lH','image')
    lG = cv2.getTrackbarPos('lS','image')
    lR = cv2.getTrackbarPos('lV','image')
    
    uB = cv2.getTrackbarPos('uH','image')
    uG = cv2.getTrackbarPos('uS','image')
    uR = cv2.getTrackbarPos('uV','image')

    s = cv2.getTrackbarPos('l_or_u','image')


    if s == 1:
        img[:] = [uB,uG,uR]
    if s == 0:
        img[:] = [lB,lG,lR]


    cv2.imshow('image',img)

    # Take each frame
    _, frame = cap.read()

    # Convert BGR to HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    # Conert entrie BGR to HSV
    BGRl = np.uint8([[[lB,lG,lR ]]])
    BGRu = np.uint8([[[uB,uG,uR ]]])




    # define range of blue color in HSV
    lower_blue = np.array(BGRl)
    upper_blue = np.array(BGRu)

    # Threshold the HSV image to get only blue colors
    mask = cv2.inRange(hsv, lower_blue, upper_blue)

    # Bitwise-AND mask and original image
    res = cv2.bitwise_and(frame,frame, mask= mask)

    cv2.imshow('frame',frame)
    cv2.imshow('mask',mask)
    cv2.imshow('res',res)
    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        cv2.imwrite('color.png',frame)
        break

cv2.destroyAllWindows()
