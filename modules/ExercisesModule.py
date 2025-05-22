import time
import cv2
import numpy as np
import modules.PoseModule as pm
from modules.AudioCommSys import AudioFeedbackSystem


class Utilities:
    def get_performance_bar_color(self, per):
        if 0 < per <= 30:
            return (51, 51, 255)        # Blue
        elif 30 < per <= 60:
            return (0, 165, 255)        # Orange-ish
        elif 60 <= per <= 100:
            return (0, 255, 255)        # Light cyan
        return (0, 205, 205)            # Default fallback

    def draw_performance_bar(self, img, per, bar_pos, color, count):
        h, w = img.shape[:2]
        bar_width = int(w * 0.03)
        x2 = w - 60
        x1 = x2 - bar_width  # Shift bar to the left
        top, bottom = int(h * 0.15), int(h * 0.90)
        fill = int(np.interp(per, (0, 100), (bottom, top)))

        # Draw border and fill
        cv2.rectangle(img, (x1, top), (x2, bottom), color, 3)
        cv2.rectangle(img, (x1, fill), (x2, bottom), color, cv2.FILLED)

        # Draw percentage just above the bar
        cv2.putText(img, f"{int(per)}%", (x1 - 10, top - 10),
                    cv2.FONT_HERSHEY_PLAIN, 2, color, 2)

    def display_rep_count(self, img, count, total_reps):
        cv2.putText(img, f'Reps: {count}/{total_reps}', (30, 100),
                    cv2.FONT_HERSHEY_PLAIN, 2.5, (255, 255, 255), 4)

    def repetition_counter(self, per, count, direction):
        if per == 100 and direction == 0:
            count += 1
            direction = 1
        elif per == 0 and direction == 1:
            direction = 0
        return {"count": count, "direction": direction}

    def _yield_image_frame(self, img):
        _, jpeg = cv2.imencode('.jpg', img)
        return jpeg.tobytes()


class SimulateTargetExercises:
    def __init__(self, sets=1, rest_time=30, difficulty_level=1, reps=2):
        self.sets = sets
        self.rest_time = rest_time
        self.difficulty_level = difficulty_level
        self.reps = reps
        self.count = 0

    def is_bicep_curl_detected(self, landmarks):
        return True  # Placeholder for future detection logic

    def bicep_curls(self):
        utils = Utilities()
        cap = cv2.VideoCapture(0)
        detector = pm.posture_detector()
        speaker = AudioFeedbackSystem()

        for current_set in range(1, self.sets + 1):
            print(f"Set {current_set}/{self.sets}")
            count, direction = 0, 0
            total_reps = self.reps * self.difficulty_level

            while count < total_reps:
                success, img = cap.read()
                if not success:
                    print("❌ Could not read from webcam.")
                    break

                img = detector.find_person(img, draw=False)
                landmarks = detector.find_landmarks(img, draw=False)

                if landmarks:
                    if self.is_bicep_curl_detected(landmarks):
                        self.count += 0  # Placeholder

                    angle = detector.find_angle(img, 12, 14, 16)
                    per = np.interp(angle, (50, 160), (0, 100))
                    bar_pos = np.interp(per, (0, 100), (650, 100)) # Calculate bar position
                    color = utils.get_performance_bar_color(per)

                    if per in [0, 100]:
                        color = (0, 255, 0)
                        rep_data = utils.repetition_counter(per, count, direction)
                        count, direction = rep_data["count"], rep_data["direction"]

                        if rep_data["count"] > self.count:
                            self.count = rep_data["count"]
                            speaker.say(f"{self.count}")

                    utils.display_rep_count(img, count, total_reps)     # Reps displayed first
                    utils.draw_performance_bar(img, per, bar_pos, color, count)               # Then bar displayed

                yield utils._yield_image_frame(img)

            print(f"✅ Completed Set {current_set}")

            if current_set < self.sets:
                rest_start = time.time()
                while time.time() - rest_start < self.rest_time:
                    rest_img = np.zeros((720, 1280, 3), dtype=np.uint8)
                    cv2.putText(
                        rest_img,
                        f"Rest: {int(self.rest_time - (time.time() - rest_start))}s",
                        (500, 360),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        2,
                        (0, 255, 255),
                        4
                    )
                    yield utils._yield_image_frame(rest_img)

        cap.release()
        try:
            cv2.destroyAllWindows()
        except cv2.error as e:
            print(f"cv2.destroyAllWindows() failed: {e}")


    #SQUATS
    def squats(self):
        utils = Utilities()
        cap = cv2.VideoCapture(0)
        detector = pm.posture_detector()
        speaker = AudioFeedbackSystem()

        for current_set in range(1, self.sets + 1):
            print(f"Set {current_set}/{self.sets}")
            count, direction = 0, 0
            total_reps = self.reps * self.difficulty_level

            while count < total_reps:
                success, img = cap.read()
                if not success or img is None:
                    print("❌ Could not read from webcam.")
                    break

                img = detector.find_person(img, draw=False)
                landmarks = detector.find_landmarks(img, draw=False)

                if landmarks:
                    # Calculate leg angles
                    right_leg_angle = detector.find_angle(img, 24, 26, 28)
                    left_leg_angle = detector.find_angle(img, 23, 25, 27)

                    # Use average angle for more stability
                    avg_leg_angle = (left_leg_angle + right_leg_angle) / 2

                    per = np.interp(avg_leg_angle, (190, 240), (0, 100))
                    bar_pos = np.interp(per, (0, 100), (650, 100))
                    color = utils.get_performance_bar_color(per)

                    if per in [0, 100]:
                        color = (0, 255, 0)
                        rep_data = utils.repetition_counter(per, count, direction)
                        count, direction = rep_data["count"], rep_data["direction"]

                        if rep_data["count"] > self.count:
                            self.count = rep_data["count"]
                            speaker.say(f"{self.count}")

                    utils.display_rep_count(img, count, total_reps)
                    utils.draw_performance_bar(img, per, bar_pos, color, count)

                yield utils._yield_image_frame(img)

            print(f"✅ Completed Set {current_set}")

            if current_set < self.sets:
                rest_start = time.time()
                while time.time() - rest_start < self.rest_time:
                    rest_img = np.zeros((720, 1280, 3), dtype=np.uint8)
                    cv2.putText(
                        rest_img,
                        f"Rest: {int(self.rest_time - (time.time() - rest_start))}s",
                        (500, 360),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        2,
                        (0, 255, 255),
                        4
                    )
                    yield utils._yield_image_frame(rest_img)

        cap.release()
        try:
            cv2.destroyAllWindows()
        except cv2.error as e:
            print(f"cv2.destroyAllWindows() failed: {e}")

