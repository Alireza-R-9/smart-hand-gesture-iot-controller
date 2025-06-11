import math

class GestureController:
    def __init__(self):
        # برای ناحیه فاصله‌ای که مقدار درصد را محاسبه می‌کنیم
        self.min_distance = 50   # حداقل فاصله (مثلاً نزدیک‌ترین)
        self.max_distance = 300  # حداکثر فاصله (مثلاً دورترین)

    def distance(self, point1, point2):
        """
        محاسبه فاصله اقلیدسی بین دو نقطه
        هر نقطه به صورت (x, y)
        """
        x1, y1 = point1
        x2, y2 = point2
        return math.hypot(x2 - x1, y2 - y1)

    def get_distance_percentage(self, hand_landmarks):
        """
        با فرض اینکه ورودی یک دست است
        فاصله بین انگشت شست (ایندکس 4) و انگشت اشاره (ایندکس 8)
        را می‌گیرد و آن را به درصد تبدیل می‌کند
        """
        thumb = hand_landmarks[4][1:]  # (x, y)
        index_finger = hand_landmarks[8][1:]  # (x, y)

        dist = self.distance(thumb, index_finger)
        # تبدیل فاصله به درصد بین 0 تا 100
        perc = (dist - self.min_distance) / (self.max_distance - self.min_distance) * 100
        return max(0, min(perc, 100))  # محدود کردن به بازه 0 تا 100

    def is_fist(self, lmList):
        """مشت بسته: همه انگشت‌ها خم شده‌اند (سر انگشت‌ها زیر مفصل دوم هستند)"""
        return all(lmList[i][2] > lmList[i - 2][2] for i in [8, 12, 16, 20])

    def is_hand_open(self, lmList):
        """کف دست باز: همه انگشت‌ها کشیده‌اند (سر انگشت‌ها بالای مفصل دوم هستند)"""
        return all(lmList[i][2] < lmList[i - 2][2] for i in [8, 12, 16, 20])
