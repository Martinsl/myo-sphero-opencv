import numpy as np
import cv2

class App(object):
    def __init__(self, video_src):
        self.cam = cv2.VideoCapture(video_src)
        ret, self.frame = self.cam.read()
        cv2.namedWindow('frame')

        self.selection = None
        self.circle = None
        self.tracking_state = 0
        self.show_backproj = False

    def search(self):
        hsv = cv2.cvtColor(self.frame.copy(), cv2.COLOR_BGR2HSV)        
        lower_white = np.array([0,0,230], dtype=np.uint8)
        upper_white = np.array([0,0,255], dtype=np.uint8)
        while_mask = cv2.inRange(hsv, lower_white, upper_white)
        circles = cv2.HoughCircles(while_mask, cv2.HOUGH_GRADIENT, 4, 2000,
                               param1=50,param2=30,minRadius=1,maxRadius=30)
        if circles is not None:
            circles = np.round(circles[0, :]).astype("int")
            self.circle = circles[0]
            self.tracking_state = 1

    def run(self):
        while True:
            ret, self.frame = self.cam.read()
            self.frame = cv2.resize(self.frame, (720, 480))
            vis = self.frame.copy()
            hsv = cv2.cvtColor(self.frame, cv2.COLOR_BGR2HSV)

            # define range of white color in HSV
            lower_white = np.array([0,0,220], dtype=np.uint8)
            upper_white = np.array([0,0,255], dtype=np.uint8)
            mask = cv2.inRange(hsv, lower_white, upper_white)

            if self.circle != None:
                x_circle, y_circle, r = self.circle
                x0, y0, x1, y1 = x_circle-r/2, y_circle-r/2, x_circle+r/2, y_circle+r/2
                self.track_window = (x0, y0, x1, y1)
                hsv_roi = hsv[y0:y1, x0:x1]
                mask_roi = mask[y0:y1, x0:x1]
                roi_hist = cv2.calcHist([hsv],[0],mask,[16],[0,180])
                cv2.normalize(roi_hist,roi_hist,0,255,cv2.NORM_MINMAX)
                self.hist = roi_hist.reshape(-1)

                vis_roi = vis[y0:y1, x0:x1]
                cv2.bitwise_not(vis_roi, vis_roi)
                vis[mask == 0] = 0

            if self.tracking_state == 1:
                self.selection = None
                prob = cv2.calcBackProject([hsv], [0], self.hist, [0, 180], 1)
                prob &= mask
                term_crit = ( cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 1 )

                ret, self.track_window = cv2.meanShift(prob, self.track_window, term_crit)

                x, y, w, h = self.track_window
                vis = cv2.rectangle(vis, (x,y), (x+w,y+h), 255,2) 
            else:
                self.search()               

            cv2.imshow('frame', vis)

            ch = 0xFF & cv2.waitKey(5)
            if ch == 27:
                break
            if ch == ord('b'):
                self.show_backproj = not self.show_backproj
        cv2.destroyAllWindows()

if __name__ == '__main__':
    import sys
    try:
        video_src = sys.argv[1]
    except:
        video_src = 0
    print __doc__
    App(video_src).run()