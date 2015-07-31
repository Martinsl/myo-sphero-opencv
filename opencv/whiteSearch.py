import cv2
import numpy as np

# open camera
cap = cv2.VideoCapture('./sphero_floor2.mp4')

# camera loop
while(1):

    # read from camera capture
    ret, frame = cap.read()

    frame = cv2.resize(frame, (720, 480)) 
    # makes the image darker
    dark = (255.0)*(frame/255.0)**2
    dark = np.array(dark,dtype=np.uint8)

    # transform the image to hsv format
    # to find light colors easier
    hsv = cv2.cvtColor(dark, cv2.COLOR_BGR2HSV)

    # define range of white color in HSV
    lower_white = np.array([80,0,220], dtype=np.uint8)
    upper_white = np.array([179,255,255], dtype=np.uint8)

    # threshold the HSV image to get only white colors
    mask = cv2.inRange(hsv, lower_white, upper_white)

    # blur image to better recognize contours
    
    mask = cv2.medianBlur(mask, 7)
    mask = cv2.GaussianBlur(mask, (5,5),0)

    # reverse mask image
    #mask = (255-mask)

    # find all circles on image
    circles = cv2.HoughCircles(mask, cv2.HOUGH_GRADIENT, 4, 2000,
                               param1=50,param2=30,minRadius=1,maxRadius=30)

    # draw the circle contours
    if circles is not None:
        circles = np.round(circles[0, :]).astype("int")
        circle = circles[0]
        for (x, y, r) in circles:
            print(x, y, r)
            cv2.circle(frame, (x, y), r, (0, 255, 0), 4)
            cv2.rectangle(frame, (x - 5, y - 5), (x + 5, y + 5), (0, 128, 255), -1)

    # show images
    cv2.imshow('frame',frame)
    cv2.imshow('mask',mask)
    cv2.imshow('hsv',hsv)

    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break

cv2.destroyAllWindows()