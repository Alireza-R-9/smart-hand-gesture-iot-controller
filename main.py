import cv2
import numpy as np
from hand_detector import HandDetector
from gesture_controller import GestureController


def draw_progress_bar(img, perc, x=50, y=150, w=40, h=300, color=(0, 255, 0)):
    # کشیدن کادر سفید نوار
    cv2.rectangle(img, (x, y), (x + w, y + h), (255, 255, 255), 3)
    # پر کردن نوار به اندازه درصد
    fill = int((perc / 100) * h)
    cv2.rectangle(img, (x, y + h - fill), (x + w, y + h), color, cv2.FILLED)
    # نمایش درصد عددی بالای نوار
    cv2.putText(img, f'{int(perc)}%', (x - 10, y + h + 45),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 3)


def freq_label(perc):
    # بازه واقعی فرکانس 100Hz تا 5000Hz
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
    # بازه سرعت پخش 0.5x تا 2.0x
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

    while True:
        success, img = cap.read()
        if not success:
            break

        img = detector.find_hands(img)
        allHands = detector.get_landmarks(img)

        freq_perc = 0
        speed_perc = 0

        if len(allHands) >= 1:
            freq_perc = gesture_ctrl.get_distance_percentage(allHands[0])
        if len(allHands) >= 2:
            speed_perc = gesture_ctrl.get_distance_percentage(allHands[1])

        # رسم نوار فرکانس (چپ)
        draw_progress_bar(img, freq_perc, x=50, y=120, color=(0, 150, 255))
        cv2.putText(img, 'Frequency', (45, 100), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 150, 255), 3)
        cv2.putText(img, freq_label(freq_perc), (10, 490), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 150, 255), 2)

        # رسم نوار سرعت (راست)
        draw_progress_bar(img, speed_perc, x=img.shape[1] - 90, y=120, color=(0, 255, 150))
        cv2.putText(img, 'Speed', (img.shape[1] - 140, 100), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 255, 150), 3)
        cv2.putText(img, speed_label(speed_perc), (img.shape[1] - 280, 490), cv2.FONT_HERSHEY_SIMPLEX, 0.9,
                    (0, 255, 150), 2)

        cv2.imshow("Hand Gesture Frequency & Speed Control", img)

        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
