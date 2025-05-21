import cv2

def main():
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("❌ Error: Could not open webcam.")
        return

    print("📷 Webcam stream started. Press 'q' to quit.")
    
    while True:
        ret, frame = cap.read()
        if not ret:
            print("❌ Failed to grab frame.")
            break

        cv2.imshow("Webcam Preview", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            print("👋 Closing webcam.")
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
