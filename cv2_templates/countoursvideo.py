import numpy as np
import cv2


cap = cv2.VideoCapture(0)

while(True):
    
  # Capture frame-by-frame
    ret, frame = cap.read()

    # Our operations on the frame come here
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray,(5,5),0)
    ret, thresh_img = cv2.threshold(blur,91,255,cv2.THRESH_BINARY)

    contours =  cv2.findContours(thresh_img,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)[-2]


    
    for cnt in contours:

        [x,y,w,h] = cv2.boundingRect(cnt)
        hull = cv2.convexHull(cnt)
        
#        (x,y),radius = cv2.minEnclosingCircle(cnt)
#        center = (int(x),int(y))
#        radius = int(radius)
        
        if cv2.contourArea(cnt)>2500:
                cv2.drawContours(frame, [cnt], -1, (0,255,0), 3)
                if cv2.contourArea(hull)>6000:
                    cv2.drawContours(frame, [hull], -1, (255,0,0), 3)
                    cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)
#                if radius > 10:
#                    cv2.circle(frame,center,radius,(0,0,255),2)
        

    # Display the resulting frame
    cv2.imshow('frame',frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()

#            if cv2.arcLength(cnt,True)>1000:
 #               print(cv2.arcLength(cnt,True))
