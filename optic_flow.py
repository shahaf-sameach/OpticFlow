import numpy as np
from utils import dist
from video_proccessor import VideoProccessor
import cv2


class OpticFlow:

    def __init__(self, file_name):
        self.file_name = file_name

    def get_optic_flow_diff(self):
        cap = cv2.VideoCapture(self.file_name)

        # params for ShiTomasi corner detection
        feature_params = dict(maxCorners=100,
                              qualityLevel=0.3,
                              minDistance=7,
                              blockSize=7)

        # Parameters for lucas kanade optical flow
        lk_params = dict(winSize=(15, 15),
                         maxLevel=2,
                         criteria=(cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03))

        # Take first frame and find corners in it
        ret, old_frame = cap.read()
        old_gray = cv2.cvtColor(old_frame, cv2.COLOR_BGR2GRAY)
        p0 = cv2.goodFeaturesToTrack(old_gray, mask=None, **feature_params)

        dist_arr = []

        while(1):
            ret, frame = cap.read()

            if frame is None:
                break

            frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            # calculate optical flow
            # print "frame_gray %s" % frame_gray
            # print "old_gray %s" % old_gray

            if not np.any(old_gray) or not np.any(frame_gray):
                old_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                p0 = cv2.goodFeaturesToTrack(old_gray, mask=None, **feature_params)
                dist_arr.append(None)
                print old_gray
                print frame_gray
                continue

            p1, st, err = cv2.calcOpticalFlowPyrLK(old_gray, frame_gray, p0, None, **lk_params)

            # Select good points
            if p1 is None:
                dist_arr.append(None)
                old_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                p0 = cv2.goodFeaturesToTrack(old_gray, mask=None, **feature_params)
                continue

            good_new = p1[st == 1]
            good_old = p0[st == 1]

            dist_arr.append(dist(good_new, good_old))

            # Now update the previous frame and previous points
            old_gray = frame_gray.copy()
            p0 = good_new.reshape(-1, 1, 2)

        cap.release()
        return dist_arr

if __name__ == '__main__':
    INPUT_FILE = 'videos/RoofJump.mp4'
    OUTPUT_FILE = 'videos/RoofJump_2fps.mp4'
    FPS = 2

    vp = VideoProccessor(INPUT_FILE)
    file_name = vp.encode(output_file=OUTPUT_FILE, fps=FPS)

    of = OpticFlow(file_name)
    diff = of.get_optic_flow_diff()
    print diff
    print 'done'
