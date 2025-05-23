import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from modules.ExercisesModule import SimulateTargetExercises
from frames.StreamingFrame import StreamingFrame

class BicepCurlSettingsFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#121212")
        self.controller = controller

        from frames.WorkoutsFrame import WorkoutsFrame

        # === Load images ===
        logo_img = Image.open("assets/befit-logo-white.png").resize((150, 80))
        back_img = Image.open("assets/prev-icon.png").resize((120, 80))
        start_img = Image.open("assets/start-button.png").resize((300, 300))

        self.logo = ImageTk.PhotoImage(logo_img)
        self.back_icon = ImageTk.PhotoImage(back_img)
        self.start_icon = ImageTk.PhotoImage(start_img)

        self.sets = tk.IntVar(value=2)
        self.reps = tk.IntVar(value=3)
        self.rest = tk.IntVar(value=15)

        # === Top Navigation Bar ===
        nav_frame = tk.Frame(self, bg="#121212")
        nav_frame.pack(fill="x", pady=(10, 0))

        back_btn = tk.Label(nav_frame, image=self.back_icon, bg="#121212", cursor="hand2")
        back_btn.pack(side="left", padx=20)
        back_btn.bind("<Enter>", lambda e: back_btn.config(bg="#1a1a1a"))
        back_btn.bind("<Leave>", lambda e: back_btn.config(bg="#121212"))
        back_btn.bind("<Button-1>", lambda e: controller.show_frame(WorkoutsFrame, transition="slide-left"))

        logo_label = tk.Label(nav_frame, image=self.logo, bg="#121212")
        logo_label.pack(side="top")

        # === Title ===
        tk.Label(
            self,
            text="Customize Your Bicep Curl",
            font=("Helvetica", 24, "bold"),
            fg="#ffffff",
            bg="#121212"
        ).pack(pady=(20, 10))

        # === Settings Form Frame ===
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
        start_btn.bind("<Button-1>", self.start_exercise)

    def start_exercise(self, event=None):
        exercise = SimulateTargetExercises(
            sets=self.sets.get(),
            reps=self.reps.get(),
            rest_time=self.rest.get()
        )
        # self.controller.frames[StreamingFrame].set_exercise(exercise.bicep_curls)
        # Dynamically select the exercise based on the exercise_type attribute
        if self.exercise_type == "bicep_curls":
            self.controller.frames[StreamingFrame].set_exercise(exercise.bicep_curls, "assets/bicep_curl.gif")
        # elif self.exercise_type == "squats":
        #     self.controller.frames[StreamingFrame].set_exercise(exercise.squats, "assets/gif_squats_men.gif")

        # if self.exercise_type == "bicep_curls":
        #     self.controller.frames[StreamingFrame].set_exercise(
        #         exercise.bicep_curls,
        #         "assets/bicep_curl.gif",
        #         (
        #             "💪 Bicep Curl Form Tips:\n"
        #             "- Keep elbows close to your torso.\n"
        #             "- Use full range of motion.\n"
        #             "- Avoid swinging your body.\n"
        #             "- Controlled movement only.\n"
        #             "- Exhale up, inhale down."
        #         ),
        #         "bicep_curls"
        #     )
        # elif self.exercise_type == "squats":
        #     self.controller.frames[StreamingFrame].set_exercise(
        #         exercise.squats,
        #         "assets/gif_squats_men.gif",
        #         (
        #             "🏋️ Squats Form Tips:\n"
        #             "- Keep your back straight.\n"
        #             "- Push your hips back as you lower.\n"
        #             "- Keep your knees behind your toes.\n"
        #             "- Engage your core throughout.\n"
        #             "- Exhale up, inhale down."
        #         ),
        #         "squats"
        #     )
        self.controller.show_frame(StreamingFrame, transition="slide-left")
