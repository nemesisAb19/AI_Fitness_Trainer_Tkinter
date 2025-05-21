import tkinter as tk
from PIL import Image, ImageTk, ImageSequence
import cv2
import threading
import mediapipe as mp

class PoseDetectionFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="black")
        self.controller = controller
        self.running = False
        self.fullscreen = False

        # Left Panel: GIF + Tips
        self.left_frame = tk.Frame(self, bg="black", width=640)
        self.left_frame.pack(side="left", fill="both", expand=True)

        self.gif_label = tk.Label(self.left_frame, bg="black")
        self.gif_label.pack(pady=10)

        self.gif = Image.open("assets/bicep_curl.gif")
        self.gif_frames = [
            ImageTk.PhotoImage(frame.copy().resize((600, 400)))
            for frame in ImageSequence.Iterator(self.gif)
        ]
        self.gif_index = 0
        self.animate_gif()

        # Exercise Tips
        tips_title = tk.Label(self.left_frame, text="Workout Tips", font=("Helvetica", 16, "bold"),
                              fg="white", bg="black")
        tips_title.pack(pady=(10, 0))

        tips_list = [
            "Keep your elbows stationary.",
            "Use slow, controlled motion.",
            "Exhale as you lift.",
            "Inhale as you lower.",
        ]

        for tip in tips_list:
            lbl = tk.Label(self.left_frame, text="• " + tip, font=("Helvetica", 12),
                           fg="white", bg="black", anchor="w", justify="left")
            lbl.pack(padx=20, anchor="w")

        # Right Panel: OpenCV Feed
        self.right_frame = tk.Frame(self, bg="black", width=640)
        self.right_frame.pack(side="right", fill="both", expand=True)

        # Top Row: Exit and Fullscreen
        self.top_right_controls = tk.Frame(self.right_frame, bg="black")
        self.top_right_controls.pack(fill="x", anchor="ne", padx=10, pady=5)

        self.cross_img = ImageTk.PhotoImage(Image.open("assets/cross-button.png").resize((30, 30)))
        self.cross_button = tk.Button(self.top_right_controls, image=self.cross_img, command=self.stop_stream,
                                      bg="black", borderwidth=0, highlightthickness=0, activebackground="black")
        self.cross_button.pack(side="right", padx=5)

        self.fullscreen_btn = tk.Button(self.top_right_controls, text="⛶", font=("Arial", 16),
                                        command=self.toggle_fullscreen, bg="black", fg="white",
                                        borderwidth=0, activebackground="black", activeforeground="white")
        self.fullscreen_btn.pack(side="right", padx=5)

        self.video_label = tk.Label(self.right_frame, bg="black")
        self.video_label.pack()

        # Start pose detection
        self.running = True
        threading.Thread(target=self.start_pose_detection, daemon=True).start()

    def animate_gif(self):
        self.gif_label.config(image=self.gif_frames[self.gif_index])
        self.gif_index = (self.gif_index + 1) % len(self.gif_frames)
        self.after(80, self.animate_gif)

    def toggle_fullscreen(self):
        self.fullscreen = not self.fullscreen
        self.controller.attributes("-fullscreen", self.fullscreen)

    def stop_stream(self):
        self.running = False
        self.controller.attributes("-fullscreen", False)
        self.controller.show_frame("WorkoutsFrame")  # Change as needed

    def start_pose_detection(self):
        mp_pose = mp.solutions.pose
        pose = mp_pose.Pose()
        cap = cv2.VideoCapture(0)

        while self.running and cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            frame = cv2.flip(frame, 1)
            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = pose.process(rgb)

            # Draw landmarks (optional)
            # mp.solutions.drawing_utils.draw_landmarks(frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

            img = Image.fromarray(rgb)
            img = img.resize((640, 480))
            imgtk = ImageTk.PhotoImage(image=img)

            self.video_label.imgtk = imgtk
            self.video_label.configure(image=imgtk)

        cap.release()
