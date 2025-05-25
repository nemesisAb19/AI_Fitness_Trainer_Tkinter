import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
# from frames.CustomizeStreamingFrame import CustomizeStreamingFrame

class CustomizeSettings(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#121212")
        self.controller = controller

        self.sets = tk.IntVar(value=2)
        self.reps = tk.IntVar(value=5)
        self.rest = tk.IntVar(value=30)

        # Load assets
        logo_img = Image.open("assets/befit-logo-white.png").resize((150, 80))
        back_img = Image.open("assets/prev-icon.png").resize((120, 80))
        start_img = Image.open("assets/start-button.png").resize((300, 300))

        self.logo = ImageTk.PhotoImage(logo_img)
        self.back_icon = ImageTk.PhotoImage(back_img)
        self.start_icon = ImageTk.PhotoImage(start_img)

        from frames.BuildYourWorkout import BuildYourWorkout

        # === Top Bar ===
        nav_frame = tk.Frame(self, bg="#121212")
        nav_frame.pack(fill="x", pady=(10, 0))

        back_btn = tk.Label(nav_frame, image=self.back_icon, bg="#121212", cursor="hand2")
        back_btn.pack(side="left", padx=20)
        back_btn.bind("<Enter>", lambda e: back_btn.config(bg="#1a1a1a"))
        back_btn.bind("<Leave>", lambda e: back_btn.config(bg="#121212"))
        back_btn.bind("<Button-1>", lambda e: controller.show_frame(BuildYourWorkout, transition="slide-left"))

        logo_label = tk.Label(nav_frame, image=self.logo, bg="#121212")
        logo_label.pack(side="top")

        # === Heading ===
        tk.Label(
            self,
            text="Customize Build Your Workout",
            font=("Helvetica", 24, "bold"),
            fg="#ffffff",
            bg="#121212"
        ).pack(pady=(20, 10))

        # === Settings Form ===
        form_frame = tk.Frame(self, bg="#1e1e1e")
        form_frame.pack(pady=30, ipadx=40, ipady=20)

        label_style = {"font": ("Helvetica", 16), "bg": "#1e1e1e", "fg": "#ffffff", "anchor": "w"}
        spin_style = {"font": ("Helvetica", 14), "width": 5, "justify": "center"}

        for label_text, var in [("Sets", self.sets), ("Reps", self.reps), ("Rest Time (s)", self.rest)]:
            row = tk.Frame(form_frame, bg="#1e1e1e")
            row.pack(fill="x", pady=15)
            tk.Label(row, text=label_text, **label_style, width=20).pack(side="left", padx=(10, 20))
            ttk.Spinbox(row, from_=1, to=300, textvariable=var, **spin_style).pack(side="left")

        # === Start Button ===
        start_btn = tk.Label(self, image=self.start_icon, bg="#121212", cursor="hand2")
        start_btn.pack(pady=30)
        start_btn.bind("<Enter>", lambda e: start_btn.config(bg="#1a1a1a"))
        start_btn.bind("<Leave>", lambda e: start_btn.config(bg="#121212"))
        start_btn.bind("<Button-1>", self.start_workout)

    def start_workout(self, event=None):
        from frames.BuildYourWorkout import BuildYourWorkout
        selected_exercises = self.controller.frames[BuildYourWorkout].selected_exercises
        sets = self.sets.get()
        reps = self.reps.get()
        rest = self.rest.get()

        from frames.CustomizeStreamingFrame import CustomizeStreamingFrame
        self.controller.frames[CustomizeStreamingFrame].configure_stream(
            exercises=selected_exercises,
            sets=sets,
            reps=reps,
            rest_time=rest
        )
        self.controller.show_frame(CustomizeStreamingFrame, transition="slide-left")

