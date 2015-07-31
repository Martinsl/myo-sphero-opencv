import numpy as np
import cv2

class App(object):
    def __init__(self, video_src):
        self.cam = cv2.VideoCapture(video_src)
        ret, self.frame = self.cam.read()
        cv2.namedWindow('frame')
        cv2.setMouseCallback('frame', self.onmouse)
        
        self.sphero = None
        self.destination = None

    def onmouse(self, event, x, y, flags, param):
        x, y = np.int16([x, y]) # BUG
        if event == cv2.EVENT_LBUTTONDOWN:
            self.destination = x, y
    
    def horizontalMovement(self):
        x0, y0 = self.sphero
        x1, y1 = self.destination

        movDiff = x0 - x1;

        if movDiff < -10:
            # moves circle
            self.sphero = x0+2, y0
            print "RIGHT"
        elif movDiff > 10:
            # moves circle
            self.sphero = x0-2, y0
            print "LEFT"
        else:
            # stops circle once it is close enough to the destination
            self.destination = x0, y1
            print "STOP"

    def verticalMovement(self):
        x0, y0 = self.sphero
        x1, y1 = self.destination

        movDiff = y0 - y1;

        if movDiff >= 15:
            # moves circle
            self.sphero = x0, y0-2
            print "FORWARD"
        elif movDiff < -15:
            # moves circle
            self.sphero = x0, y0+2
            print "BACK"
        else:
            # stops circle once it is close enough to the destination
            self.destination = x1, y0
            print "STOP"
        

    def run(self):
        while True:
            ret, self.frame = self.cam.read()          

            if self.sphero != None and self.destination != None:
                x0, y0 = self.sphero
                x1, y1 = self.destination

                # draws circle on image
                cv2.circle(self.frame, (x0, y0), 10, (0, 255, 0), -1)
                if x0 != x1:
                    self.horizontalMovement()
                elif y0 != y1:
                    self.verticalMovement()
                #self.sphero = None
                #self.destination = None

            cv2.imshow('frame', self.frame)

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