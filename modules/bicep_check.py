import cv2
from modules.ExercisesModule import SimulateTargetExercises

def main():
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("❌ Error: Could not open webcam.")
        return

    bicep_curl = SimulateTargetExercises()

    while True:
        success, frame = cap.read()
        if not success:
            print("❌ Failed to read frame.")
            break

        frame = bicep_curl.bicep_curls(frame)
        cv2.imshow("Bicep Curl Detection", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            print("👋 Exiting...")
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
