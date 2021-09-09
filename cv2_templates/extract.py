import cv2

cap = cv2.cv2.VideoCapture(1)
ret, frame = cap.read()
gray=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)

contours =  cv2.findContours(gray ,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)[-2]
idx =0
for cnt in contours:
    idx += 1
    x,y,w,h = cv2.boundingRect(cnt)
    roi=frame[y:y+h,x:x+w]
    #cv2.imwrite(str(idx) + '.jpg', roi)
    cv2.rectangle(frame,(x,y),(x+w,y+h),(200,0,0),2)
cv2.imshow('img',frame)
cv2.waitKey(0)