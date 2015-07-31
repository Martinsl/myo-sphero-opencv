import numpy as np
import cv2
import math

class App(object):
    def __init__(self, video_src):
        self.cam = cv2.VideoCapture(0)
        ret, self.frame = self.cam.read()
        cv2.namedWindow('frame')
        cv2.setMouseCallback('frame', self.onmouse)

        self.selection = None
        self.circle = None
        self.tracking_state = 0
        self.show_backproj = False
        self.frame_counter = 0
        self.confidence = 0.0
        self.destination = None
        self.sphero = None
        self.counter = 0

    def onmouse(self, event, x, y, flags, param):
        x, y = np.int16([x, y])
        if event == cv2.EVENT_LBUTTONDOWN:
            self.destination = x, y

    def angleMovement(self):
        x0, y0 = self.sphero
        x1, y1 = self.destination

        xSide = x0 - x1
        ySide = y0 - y1

        if abs(xSide) < 20 and abs(ySide) < 20:
            return "STOP"

        if ySide == 0 and xSide < 0: # go left
            return 270
        elif ySide == 0 and xSide > 0: # go right
            return 90
        elif xSide == 0 and ySide < 0: # go back
            return 180
        elif xSide == 0 and ySide > 0: # go forward
            return 0
        else:
            xSideAbs = abs(xSide)
            ySideAbs = abs(ySide)

            ctan = xSideAbs/float(ySideAbs)
            angle = math.degrees(math.atan(ctan))

            if xSide < 0 and ySide < 0: # inverse angle
                angle = 180 - angle
            elif ySide < 0 and xSide > 0: #
                angle = 180 + angle
            elif ySide > 0 and xSide > 0: # both positives
                angle = 360 - angle
            return int(angle)

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
            ret, self.frame = self.cam.read()
            vis = self.frame.copy()
            self.hsv = cv2.cvtColor(self.frame, cv2.COLOR_BGR2HSV)

            # define range of white color in HSV
            lower_white = np.array([80,0,220], dtype=np.uint8)
            upper_white = np.array([180,255,255], dtype=np.uint8)
            self.mask = cv2.inRange(self.hsv, lower_white, upper_white)

            self.mask = cv2.GaussianBlur(self.mask, (5,5),0)
            self.mask = cv2.medianBlur(self.mask, 7)

            if self.circle != None:
                # retrieve circle data
                x_circle, y_circle, r = self.circle

                # modify circle data to create a rectangle
                x0, y0, x1, y1 = x_circle-r, y_circle-r, x_circle+r, y_circle+r

                # create track window data as x, y, w, h
                self.track_window = (x0-r, y0-r, r*2, r*2)

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
                self.selection = None
                prob = cv2.calcBackProject([self.hsv], [0], self.hist, [0, 180], 1)
                prob &= self.mask
                term_crit = ( cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 1 )

                ret, self.track_window = cv2.meanShift(prob, self.track_window, term_crit)

                x, y, w, h = self.track_window
                vis = cv2.rectangle(vis, (x,y), (x+w, y+h), 255,2)
                self.hasCircle(self.mask, x, y, w ,h)
                self.sphero = x+w/2, y+w/2
            else:
                self.sphero = None
                self.search(self.mask)

            if self.confidence < 0.4:
                self.tracking_state = 0
            elif self.confidence > 0.6:
                self.tracking_state = 1

            self.counter += 1
            if self.counter == 6:
                self.counter = 0
                if self.sphero != None and self.destination != None:
                    x0, y0 = self.sphero
                    x1, y1 = self.destination
                    cv2.circle(self.frame, (x0, y0), 10, (0, 255, 0), -1)
                    if x0 != x1 or y0 != y1:
                        print "%02d" % (self.angleMovement(), )
                    else:
                        self.destination = None

            #print self.confidence

            #cv2.imshow('hsv', self.hsv)
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
                self.destination = None
            if ch == ord('s'):
                self.destination = None
                print("STOP")

        cv2.destroyAllWindows()

if __name__ == '__main__':
    import sys
    try:
        video_src = sys.argv[1]
    except:
        video_src = 0
    print __doc__
    App(video_src).run()