import tkinter as tk
from PIL import Image, ImageTk
import cv2
import numpy as np
from datetime import datetime
from tkinter import messagebox
from modules.ExercisesModule import SimulateTargetExercises

class CustomizeStreamingFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#121212")
        self.controller = controller
        self.video_fullscreen = False
        self.recording = False
        self.out = None
        self.exercise_generator = None
        self.current_generator = None

        # === Video Label ===
        self.video_label = tk.Label(self, bg="#000000", relief="groove")
        self.video_label.pack(padx=20, pady=(20, 10), expand=True, fill="both")

        # === Control Panel ===
        self.control_panel = tk.Frame(self, bg="#1e1e1e")
        self.control_panel.pack(side="bottom", pady=10)

        # Back Button
        from frames.CustomizeSettings import CustomizeSettings
        back_img = Image.open("assets/prev-icon.png").resize((40, 30))
        self.back_icon = ImageTk.PhotoImage(back_img)
        back_btn = tk.Label(self.control_panel, image=self.back_icon, bg="#1e1e1e", cursor="hand2")
        back_btn.pack(side="left", padx=10)
        back_btn.bind("<Button-1>", lambda e: self.go_back())

        # Fullscreen Toggle
        self.fullscreen_btn = tk.Button(self.control_panel, text="🖥️ Fullscreen", font=("Arial", 11), command=self.toggle_fullscreen)
        self.fullscreen_btn.pack(side="left", padx=10)

        # Record Button
        self.record_btn = tk.Button(self.control_panel, text="⏺️ Record", font=("Arial", 11), command=self.toggle_recording)
        self.record_btn.pack(side="left", padx=10)

        # ESC exits fullscreen
        self.bind_all("<Escape>", self.exit_fullscreen)

    def configure_stream(self, exercises, sets, reps, rest_time):
        """ Receives exercise names like ['Bicep Curl', 'Squats'] and settings. """
        def exercise_sequence_generator():
            for ex_name in exercises:
                simulator = SimulateTargetExercises(sets=sets, reps=reps, rest_time=rest_time)
                if ex_name.lower() == "bicep curl":
                    yield from simulator.bicep_curls()
                elif ex_name.lower() == "squats":
                    yield from simulator.squats()
                else:
                    print(f"🚫 Exercise '{ex_name}' is not implemented.")
        self.exercise_generator = exercise_sequence_generator()
        self.current_generator = iter(self.exercise_generator)
        self.update_stream()


    def update_stream(self):
        try:
            frame_bytes = next(self.current_generator)
            if frame_bytes is None:
                print("Received empty frame.")
                return
            image_array = cv2.imdecode(np.frombuffer(frame_bytes, np.uint8), cv2.IMREAD_COLOR)
            image_array = cv2.cvtColor(image_array, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(image_array)
            imgtk = ImageTk.PhotoImage(image=img)
            self.video_label.imgtk = imgtk
            self.video_label.configure(image=imgtk)

            # Recording
            if self.recording and self.out:
                self.out.write(cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR))

        except StopIteration:
            print("✅ All exercises completed.")
            self.go_back()
            return
        except Exception as e:
            print("Stream error:", e)
            return

        self.after(30, self.update_stream)

    # def toggle_fullscreen(self):
    #     if not self.video_fullscreen:
    #         self.video_label.pack_forget()
    #         self.video_label.pack(expand=True, fill="both")
    #         self.video_label.master.pack(expand=True, fill="both")
    #         self.control_panel.pack_forget()
    #         self.video_fullscreen = True
    #     else:
    #         self.exit_fullscreen()
    def toggle_fullscreen(self):
        if not self.video_fullscreen:
            # Hide the control panel and expand the video feed
            self.control_panel.pack_forget()
            self.video_label.pack_forget()
            self.video_label.pack(expand=True, fill="both")
            self.video_fullscreen = True
        else:
            self.exit_fullscreen()

    # def exit_fullscreen(self, event=None):
    #     if self.video_fullscreen:
    #         self.video_label.pack_forget()
    #         self.video_label.pack(padx=20, pady=(20, 10), expand=True, fill="both")
    #         self.control_panel.pack(side="bottom", pady=10)
    #         self.video_fullscreen = False
    def exit_fullscreen(self, event=None):
        if self.video_fullscreen:
            # Restore the control panel and reset the video feed size
            self.video_label.pack_forget()
            self.video_label.pack(padx=20, pady=(20, 10), expand=True, fill="both")
            self.control_panel.pack(side="bottom", pady=10)
            self.video_fullscreen = False

    def toggle_recording(self):
        self.recording = not self.recording
        if self.recording:
            filename = datetime.now().strftime("recording_%Y%m%d_%H%M%S.avi")
            fourcc = cv2.VideoWriter_fourcc(*'XVID')
            self.out = cv2.VideoWriter(filename, fourcc, 20.0, (640, 480))
            self.record_btn.config(text="⏹️ Stop")
            messagebox.showinfo("Recording Started", "Recording started! Saved in current folder.")
        else:
            self.stop_recording()

    def stop_recording(self):
        if self.out:
            self.out.release()
            self.out = None
        self.recording = False
        self.record_btn.config(text="⏺️ Record")
        messagebox.showinfo("Recording Stopped", "Recording saved.")

    def go_back(self):
        from frames.CustomizeSettings import CustomizeSettings
        if self.recording:
            messagebox.showwarning("Recording in Progress", "Please stop recording before going back.")
            return
        # self.stop_recording()
        self.controller.show_frame(CustomizeSettings)
