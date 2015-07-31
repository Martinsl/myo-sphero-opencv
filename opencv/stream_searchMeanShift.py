import numpy as np
import cv2

class App(object):
    def __init__(self, video_src):
        # reads from camera
        self.cam = cv2.VideoCapture(0)

        ret, self.frame = self.cam.read()
        cv2.namedWindow('frame')

        self.circle = None
        self.tracking_state = 0
        self.show_backproj = False
        self.frame_counter = 0
        self.confidence = 0.0

    def hasCircle(self, mask, x, y, w, h):
        
        # select region of interest
        mask = mask[y:y+h*2, x:x+w*2]

        # search for circles
        circles = cv2.HoughCircles(mask, cv2.HOUGH_GRADIENT, 4, 2000,
                               param1=50,param2=30,minRadius=1,maxRadius=30)

        if circles is not None:
            self.confidence /= 0.99
        else:
            self.confidence *= 0.99

        # keep confidence between 0 and 1
        self.confidence = np.clip(self.confidence, 0, 1)

    def search(self, mask):
        # look for circles
        circles = cv2.HoughCircles(mask, cv2.HOUGH_GRADIENT, 4, 2000,
                               param1=50,param2=30,minRadius=1,maxRadius=30)

        if circles is not None:
            circles = np.round(circles[0, :]).astype("int")
            self.circle = circles[0]
            self.tracking_state = 1
            self.confidence = 1
        else:
            self.confidence = 0

    def run(self):
        while True:
            # reads camera feed
            ret, self.frame = self.cam.read()
            vis = self.frame.copy()

            # transform to HSV
            self.hsv = cv2.cvtColor(self.frame, cv2.COLOR_BGR2HSV)

            # define range of white color in HSV
            lower_white = np.array([0,0,220], dtype=np.uint8)
            upper_white = np.array([0,0,255], dtype=np.uint8)
            self.mask = cv2.inRange(self.hsv, lower_white, upper_white)

            self.mask = cv2.medianBlur(self.mask, 3)

            # creates histogram to use on meanShift function
            if self.circle != None:
                # retrieve circle data, x and y are the central position
                x_circle, y_circle, r = self.circle

                # modify circle data to create a rectangle
                x0, y0, x1, y1 = x_circle-r, y_circle-r, x_circle+r, y_circle+r

                # create track rectangle data as x, y, w, h
                self.track_window = (x0, y0, 2*r, 2*r)

                hsv_roi = self.hsv[y0:y1, x0:x1]
                self.mask_roi = self.mask[y0:y1, x0:x1]

                roi_hist = cv2.calcHist([self.hsv],[0],self.mask,[16],[0,180])
                cv2.normalize(roi_hist,roi_hist,0,255,cv2.NORM_MINMAX)
                self.hist = roi_hist.reshape(-1)

                vis_roi = vis[y0:y1, x0:x1]

                cv2.bitwise_not(vis_roi, vis_roi)
                vis[self.mask == 0] = 0

                self.circle = None

            if self.tracking_state == 1:
                prob = cv2.calcBackProject([self.hsv], [0], self.hist, [0, 180], 1)
                prob &= self.mask
                term_crit = ( cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 1 )

                ret, self.track_window = cv2.meanShift(prob, self.track_window, term_crit)

                x, y, w, h = self.track_window

                # draws rectangle on tracking area
                vis = cv2.rectangle(vis, (x,y), (x+w,y+h), 255,2)

                # checks if is tracking a circle
                self.hasCircle(self.mask, x, y, w ,h)
            else:
                self.search(self.mask)

            if self.confidence < 0.4:
                self.tracking_state = 0
            elif self.confidence > 0.6:
                self.tracking_state = 1

            
            cv2.imshow('hsv', self.hsv)
            cv2.imshow('frame', vis)
            cv2.imshow('mask', self.mask)

            ch = 0xFF & cv2.waitKey(5)
            if ch == 27:
                break
            if ch == ord('b'):
                self.show_backproj = not self.show_backproj
            # change tracking area
            if ch == ord('c'):
                self.tracking_state = 0
                self.confidence = 0
        cv2.destroyAllWindows()

if __name__ == '__main__':
    import sys
    try:
        video_src = sys.argv[1]
    except:
        video_src = 0
    print __doc__
    App(video_src).run()