import tkinter as tk
from PIL import Image, ImageTk, ImageSequence
import cv2
import numpy as np
from tkinter import messagebox
from datetime import datetime


class StreamingFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#121212")
        self.controller = controller
        self.stream_generator = None
        self.recording = False
        self.out = None
        self.video_fullscreen = False

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # === Video Feed ===
        self.video_container = tk.Frame(self, bg="#121212")
        self.video_container.grid(row=0, column=0, sticky='nsew', padx=20, pady=(20, 5))
        self.video_label = tk.Label(self.video_container, bg="#000000", relief="groove")
        self.video_label.pack(expand=True, fill="both")

        # === Control Buttons Below Video ===
        control_panel = tk.Frame(self, bg="#1e1e1e")
        control_panel.grid(row=1, column=0, sticky="ew", padx=20, pady=(0, 20))

        from frames.BicepCurlSettingsFrame import BicepCurlSettingsFrame

        # Back Button
        back_img = Image.open("assets/prev-icon.png").resize((40, 30))
        self.back_icon = ImageTk.PhotoImage(back_img)
        back_btn = tk.Label(control_panel, image=self.back_icon, bg="#1e1e1e", cursor="hand2")
        back_btn.pack(side="left", padx=10)
        back_btn.bind("<Button-1>", lambda e: controller.show_frame(BicepCurlSettingsFrame))

        # Fullscreen Button
        fullscreen_btn = tk.Button(control_panel, text="🖥️ Fullscreen", font=("Arial", 11), command=self.toggle_video_fullscreen)
        fullscreen_btn.pack(side="left", padx=10)

        # Record Button
        self.record_btn = tk.Button(control_panel, text="⏺️ Record", font=("Arial", 11), command=self.toggle_recording)
        self.record_btn.pack(side="left", padx=10)

        # === GIF ===
        self.gif_label = tk.Label(self, bg="#121212")
        self.gif_label.grid(row=0, column=1, rowspan=2, sticky='nsew', padx=20, pady=20)

        # === Tips Below GIF ===
        self.tips_label = tk.Label(
            self, text="", font=("Arial", 12), fg="#ffffff", bg="#1e1e1e",
            justify="left", anchor="nw", padx=20, pady=10, wraplength=300
        )
        self.tips_label.grid(row=2, column=1, sticky="nsew", padx=20, pady=(0, 20))

    def set_exercise(self, generator_func, gif_path, tips_text, exercise_type):
        """
        Set the exercise layout, GIF, and tips dynamically based on the exercise type.
        """
        # Clear the current layout
        self.clear_layout()

        # Set the stream generator
        self.stream_generator = generator_func()

        # Load the appropriate GIF
        gif = Image.open(gif_path)
        self.gif_frames = [ImageTk.PhotoImage(frame.copy().convert("RGBA")) for frame in ImageSequence.Iterator(gif)]
        self.current_gif_frame = 0
        self.update_gif()

        # Update the layout based on the exercise type
        if exercise_type == "bicep_curls":
            self.setup_bicep_curl_layout(tips_text)
        elif exercise_type == "squats":
            self.setup_squats_layout(tips_text)

        # Start the stream
        self.update_stream()

    def clear_layout(self):
        """
        Clear all widgets from the layout to prepare for a new exercise layout.
        """
        for widget in self.winfo_children():
            widget.grid_forget()
            widget.pack_forget()

    def setup_bicep_curl_layout(self, tips_text):
        """
        Set up the layout for the bicep curls exercise.
        """
        # Video feed
        self.video_container.grid(row=0, column=0, sticky='nsew', padx=20, pady=(20, 5))
        self.video_label.pack(expand=True, fill="both")

        # GIF
        self.gif_label.grid(row=0, column=1, rowspan=2, sticky='nsew', padx=20, pady=20)

        # Tips
        self.tips_label.config(text=tips_text)
        self.tips_label.grid(row=2, column=1, sticky="nsew", padx=20, pady=(0, 20))

    def setup_squats_layout(self, tips_text):
        """
        Set up the layout for the squats exercise.
        """
        # Video feed
        self.video_container.grid(row=0, column=0, sticky='nsew', padx=20, pady=(20, 5))
        self.video_label.pack(expand=True, fill="both")

        # GIF
        self.gif_label.grid(row=0, column=1, rowspan=2, sticky='nsew', padx=20, pady=20)

        # Tips
        self.tips_label.config(text=tips_text)
        self.tips_label.grid(row=2, column=1, sticky="nsew", padx=20, pady=(0, 20))

    def toggle_video_fullscreen(self):
        """
        Toggle fullscreen mode for the video feed.
        """
        if not self.video_fullscreen:
            # Enter fullscreen
            self.gif_label.grid_remove()
            self.tips_label.grid_remove()

            self.video_label.pack_forget()
            self.video_label.pack(expand=True, fill="both", padx=0, pady=0)

            self.video_container.grid_forget()
            self.video_container.grid(row=0, column=0, columnspan=2, sticky="nsew", padx=0, pady=0)

            self.video_fullscreen = True
        else:
            # Exit fullscreen
            self.video_label.pack_forget()
            self.video_label.pack(expand=True, fill="both")

            self.video_container.grid_forget()
            self.video_container.grid(row=0, column=0, sticky='nsew', padx=20, pady=(20, 5))

            self.gif_label.grid(row=0, column=1, rowspan=2, sticky='nsew', padx=20, pady=20)
            self.tips_label.grid(row=2, column=1, sticky="nsew", padx=20, pady=(0, 20))

            self.video_fullscreen = False

    def toggle_recording(self):
        """
        Toggle recording of the video feed.
        """
        self.recording = not self.recording
        if self.recording:
            filename = datetime.now().strftime("recording_%Y%m%d_%H%M%S.avi")
            fourcc = cv2.VideoWriter_fourcc(*'XVID')
            self.out = cv2.VideoWriter(filename, fourcc, 20.0, (640, 480))
            self.record_btn.config(text="⏹️ Stop")
            messagebox.showinfo("Recording Started", "Recording started! It will be saved in the current folder.")
        else:
            if self.out:
                self.out.release()
                self.out = None
            self.record_btn.config(text="⏺️ Record")
            messagebox.showinfo("Recording Stopped", "Recording saved!")

    def update_stream(self):
        """
        Update the video stream in the video feed.
        """
        if self.stream_generator:
            try:
                frame_bytes = next(self.stream_generator)
                if frame_bytes is None:
                    print("No frame data received. Stopping stream.")
                    return
                image_array = cv2.imdecode(np.frombuffer(frame_bytes, dtype=np.uint8), cv2.IMREAD_COLOR)
                image_array = cv2.cvtColor(image_array, cv2.COLOR_BGR2RGB)
                img = Image.fromarray(image_array)
                imgtk = ImageTk.PhotoImage(image=img)
                self.video_label.imgtk = imgtk
                self.video_label.configure(image=imgtk)

                if self.recording and self.out:
                    bgr_frame = cv2.cvtColor(image_array, cv2.COLOR_RGB2BGR)
                    self.out.write(bgr_frame)

            except StopIteration:
                print("Stream generator finished.")
                return
            except Exception as e:
                print(f"Error in update_stream: {e}")
                return
            self.after(30, self.update_stream)
        else:
            print("Stream generator is not set. Please set it using set_exercise.")

    def update_gif(self):
        """
        Update the GIF animation in the GIF label.
        """
        self.gif_label.configure(image=self.gif_frames[self.current_gif_frame])
        self.current_gif_frame = (self.current_gif_frame + 1) % len(self.gif_frames)
        self.after(100, self.update_gif)