import math
import numpy as np


class GestureController:
    def __init__(self, min_dist=30, max_dist=220):
        self.min_dist = min_dist
        self.max_dist = max_dist

    def distance(self, p1, p2):
        return math.hypot(p2[0] - p1[0], p2[1] - p1[1])

    def get_distance_percentage(self, lmList):
        if not lmList or len(lmList) < 9:
            return 0

        thumb_tip = lmList[4][1:]
        index_tip = lmList[8][1:]
        length = self.distance(thumb_tip, index_tip)

        perc = np.interp(length, [self.min_dist, self.max_dist], [0, 100])
        perc = max(0, min(perc, 100))

        return perc

    def detect_gesture(self, lmList):
        if not lmList:
            return "None"

        thumb_tip = lmList[4][1:]
        index_tip = lmList[8][1:]
        length = self.distance(thumb_tip, index_tip)

        if length < 40:
            return "STOP"
        return "None"
