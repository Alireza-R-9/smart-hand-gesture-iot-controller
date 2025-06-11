import cv2
import numpy as np
import time
from hand_detector import HandDetector
from gesture_controller import GestureController


def draw_progress_bar_vertical(img, perc, x=50, y=150, w=40, h=300, color=(0, 255, 0)):
    cv2.rectangle(img, (x, y), (x + w, y + h), (255, 255, 255), 3)
    fill = int((perc / 100) * h)
    cv2.rectangle(img, (x, y + h - fill), (x + w, y + h), color, cv2.FILLED)
    cv2.putText(img, f'{int(perc)}%', (x - 10, y + h + 45),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 3)


def draw_progress_bar_horizontal(img, perc, y=50, h=30, color=(255, 100, 255)):
    w = 300
    x = (img.shape[1] - w) // 2
    cv2.rectangle(img, (x, y), (x + w, y + h), (255, 255, 255), 3)
    fill = int((perc / 100) * w)
    cv2.rectangle(img, (x, y), (x + fill, y + h), color, cv2.FILLED)
    cv2.putText(img, f'{int(perc)}%', (x + w + 10, y + h - 5),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
    cv2.putText(img, 'Volume', (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, color, 2)


def freq_label(perc):
    freq_hz = np.interp(perc, [0, 100], [100, 5000])
    if freq_hz < 300:
        return f"Very Low ({int(freq_hz)} Hz)"
    elif freq_hz < 800:
        return f"Low ({int(freq_hz)} Hz)"
    elif freq_hz < 2000:
        return f"Medium ({int(freq_hz)} Hz)"
    elif freq_hz < 3500:
        return f"High ({int(freq_hz)} Hz)"
    else:
        return f"Very High ({int(freq_hz)} Hz)"


def speed_label(perc):
    speed = np.interp(perc, [0, 100], [0.5, 2.0])
    if speed < 0.7:
        return f"Very Slow ({speed:.2f}x)"
    elif speed < 0.9:
        return f"Slow ({speed:.2f}x)"
    elif speed < 1.2:
        return f"Medium ({speed:.2f}x)"
    elif speed < 1.5:
        return f"Fast ({speed:.2f}x)"
    else:
        return f"Very Fast ({speed:.2f}x)"


def main():
    cap = cv2.VideoCapture(0)
    detector = HandDetector(maxHands=2)
    gesture_ctrl = GestureController()

    freq_perc = 50
    speed_perc = 50
    vol_perc = 70
    last_freq_perc = freq_perc
    last_speed_perc = speed_perc

    gesture_text = ""  # متن ژست برای نمایش روی تصویر

    last_action_time = 0
    action_interval = 3  # ثانیه بین تغییرات آهنگ
    last_track_action = None  # "next" یا "prev" یا None

    # اضافه شده برای نمایش پیام تغییر آهنگ به مدت 2 ثانیه
    gesture_text_show_time = 0
    gesture_text_duration = 2  # ثانیه

    while True:
        success, img = cap.read()
        if not success:
            break

        img = detector.find_hands(img)
        allHands = detector.get_landmarks(img)

        # مقدار پیش‌فرض متن ژست
        gesture_text = ""

        if len(allHands) == 2:
            # به‌روزرسانی فرکانس و سرعت فقط وقتی دو دست هست
            freq_perc = gesture_ctrl.get_distance_percentage(allHands[0])
            speed_perc = gesture_ctrl.get_distance_percentage(allHands[1])
            last_freq_perc = freq_perc
            last_speed_perc = speed_perc

            # فاصله شست‌ها برای ولوم
            hand1_x = np.mean([pt[1] for pt in allHands[0]])
            hand2_x = np.mean([pt[1] for pt in allHands[1]])

            if hand1_x < hand2_x:
                left_thumb = allHands[0][4][1:]
                right_thumb = allHands[1][4][1:]
            else:
                left_thumb = allHands[1][4][1:]
                right_thumb = allHands[0][4][1:]

            dist = gesture_ctrl.distance(left_thumb, right_thumb)
            vol_perc = np.interp(dist, [50, 300], [0, 100])
            vol_perc = max(0, min(vol_perc, 100))

            # وقتی دو دست هست، فرمان تغییر آهنگ غیرفعال است
            last_track_action = None

        elif len(allHands) == 1:
            # فقط یک دست هست
            freq_perc = last_freq_perc
            speed_perc = last_speed_perc

            fingers_count = gesture_ctrl.count_fingers(allHands[0])
            current_time = time.time()

            if fingers_count == 5:
                gesture_text = "Pause"
            elif fingers_count == 0:
                gesture_text = "Play"

            # فرمان آهنگ بعدی (دو انگشت) یا قبلی (سه انگشت)
            if fingers_count == 2:
                if last_track_action != "next" or (current_time - last_action_time) > action_interval:
                    last_action_time = current_time
                    last_track_action = "next"
                    gesture_text = "Next Track"
                    gesture_text_show_time = current_time  # شروع زمان نمایش پیام
                    # اینجا کد رفتن به آهنگ بعدی رو قرار بده

            elif fingers_count == 3:
                if last_track_action != "prev" or (current_time - last_action_time) > action_interval:
                    last_action_time = current_time
                    last_track_action = "prev"
                    gesture_text = "Previous Track"
                    gesture_text_show_time = current_time  # شروع زمان نمایش پیام
                    # اینجا کد برگشت به آهنگ قبلی رو قرار بده

            else:
                # اگر تعداد انگشتان 1، 4 یا غیره بود فرمان تغییر آهنگ لغو می‌شود
                last_track_action = None

        else:
            # دست نشان داده نشده؛ مقادیر قبلی باقی بماند
            freq_perc = last_freq_perc
            speed_perc = last_speed_perc
            last_track_action = None

        # پاک کردن پیام تغییر آهنگ بعد از 2 ثانیه
        current_time = time.time()
        if current_time - gesture_text_show_time > gesture_text_duration:
            if gesture_text in ["Next Track", "Previous Track"]:
                gesture_text = ""

        # رسم نوارها و متن‌ها
        draw_progress_bar_vertical(img, freq_perc, x=50, y=120, color=(0, 150, 255))
        cv2.putText(img, 'Frequency', (45, 100), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 150, 255), 3)
        cv2.putText(img, freq_label(freq_perc), (10, 490), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 150, 255), 2)

        draw_progress_bar_vertical(img, speed_perc, x=img.shape[1] - 90, y=120, color=(0, 255, 150))
        cv2.putText(img, 'Speed', (img.shape[1] - 140, 100), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 255, 150), 3)
        cv2.putText(img, speed_label(speed_perc), (img.shape[1] - 280, 490), cv2.FONT_HERSHEY_SIMPLEX, 0.9,
                    (0, 255, 150), 2)

        draw_progress_bar_horizontal(img, vol_perc, y=50, color=(255, 100, 255))

        # نمایش متن ژست روی تصویر (وسط پایین)
        if gesture_text:
            cv2.putText(img, gesture_text, (img.shape[1] // 2 - 150, img.shape[0] - 50),
                        cv2.FONT_HERSHEY_SIMPLEX, 1.3, (0, 255, 255), 3, cv2.LINE_AA)

        cv2.imshow("Hand Gesture Frequency & Speed Control", img)

        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
