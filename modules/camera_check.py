import cv2

def check_camera(index=0):
    cap = cv2.VideoCapture(index)
    
    if not cap.isOpened():
        print(f"❌ Camera at index {index} not detected.")
        return False
    else:
        print(f"✅ Camera at index {index} is working.")
        cap.release()
        return True

if __name__ == "__main__":
    check_camera()
