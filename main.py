import cv2
import numpy as np

cap = cv2.VideoCapture(1)


def nothing(x):
    pass


cv2.namedWindow("trackbars")

cv2.createTrackbar("min", "trackbars", 0, 5000, nothing)
cv2.createTrackbar("max", "trackbars", 0, 5000, nothing)

while True:
    # Capture frame-by-frame
    _, frame = cap.read()

    toGray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # Convert to GRAY for Threshold
    thresHold = cv2.adaptiveThreshold(toGray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11,
                                      2)  # "Smoothing color and edges"
    blurThresHold = cv2.GaussianBlur(thresHold, (5, 5), 0)  # blur

    hsv = cv2.cvtColor(blurThresHold, cv2.COLOR_GRAY2BGR)  # REConvert to BGR
    hsv = cv2.cvtColor(hsv, cv2.COLOR_BGR2HSV)  # REREConvert to HSV

    lower_black = np.array([0, 0, 0])  # Lowest black color
    upper_black = np.array([180, 360, 55])  # Highest white color

    mask = cv2.inRange(hsv, lower_black, upper_black)  # Color filter

    blurMask = cv2.GaussianBlur(mask, (5, 5), 0)  # Blur the mask

    edges = cv2.Canny(blurMask, 100, 200)  # Find the EDGES

    _, thresh_img = cv2.threshold(edges, 91, 255, cv2.THRESH_BINARY)  # Smooth color gradients into binary

    contours = cv2.findContours(thresh_img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)[-2]  # Find the COUNTOURS

    for ctn in contours:  # Color in black small noise
        x, y, w, h = cv2.boundingRect(ctn)
        ratio = w / h
        area = w * h

        if not (cv2.getTrackbarPos("min", "trackbars") < area < cv2.getTrackbarPos("max", "trackbars")) or not (
                0.7 >= ratio >= 0.3):
            cv2.fillPoly(thresh_img, pts=[ctn], color=0)
            continue

    # test = cv2.morphologyEx(edges, cv2.MORPH_CLOSE, cv2.getStructuringElement(cv2.MORPH_ELLIPSE , (10, 10)))

    contours = cv2.findContours(thresh_img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)[-2]  # Find the COUNTOURS

    for ctn in contours:
        x, y, w, h = cv2.boundingRect(ctn)
        ratio = w / h
        area = w * h

        if cv2.getTrackbarPos("min", "trackbars") < area < cv2.getTrackbarPos("max",
                                                                              "trackbars") and 0.7 >= ratio >= 0.3:
            crop = frame[y:y + h, x:x + w]

            maskCrop = cv2.inRange(crop, lower_black, upper_black)  # Color filter
            ratio_black = cv2.countNonZero(maskCrop) / crop.size

            cv2.putText(frame, str(round(ratio_black * 100, 2)), (x, y), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0))
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

    cv2.imshow('mask', thresh_img)
    cv2.imshow('frame', frame)
    cv2.imshow('edges', edges)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
