import math

class GestureController:
    def __init__(self):
        self.min_distance = 50
        self.max_distance = 300

    def distance(self, point1, point2):
        x1, y1 = point1
        x2, y2 = point2
        return math.hypot(x2 - x1, y2 - y1)

    def get_distance_percentage(self, hand_landmarks):
        thumb = hand_landmarks[4][1:]
        index_finger = hand_landmarks[8][1:]
        dist = self.distance(thumb, index_finger)
        perc = (dist - self.min_distance) / (self.max_distance - self.min_distance) * 100
        return max(0, min(perc, 100))

    def get_hand_gesture(self, hand_landmarks):
        fingers = []
        tips = [4, 8, 12, 16, 20]

        if hand_landmarks[tips[0]][1] > hand_landmarks[tips[0] - 1][1]:
            fingers.append(1)
        else:
            fingers.append(0)

        for id in range(1, 5):
            if hand_landmarks[tips[id]][2] < hand_landmarks[tips[id] - 2][2]:
                fingers.append(1)
            else:
                fingers.append(0)

        totalFingers = sum(fingers)

        if totalFingers == 0:
            return "FIST"
        elif totalFingers == 5:
            return "FIVE"
        else:
            return "UNKNOWN"

    def count_fingers(self, hand_landmarks):
        fingers = []
        tips = [4, 8, 12, 16, 20]

        if hand_landmarks[tips[0]][1] > hand_landmarks[tips[0] - 1][1]:
            fingers.append(1)
        else:
            fingers.append(0)

        for id in range(1, 5):
            if hand_landmarks[tips[id]][2] < hand_landmarks[tips[id] - 2][2]:
                fingers.append(1)
            else:
                fingers.append(0)

        return sum(fingers)

    def is_four_fingers(self, hand_landmarks):

        return self.count_fingers(hand_landmarks) == 4
