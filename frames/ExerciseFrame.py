import tkinter as tk
from tkinter import PhotoImage, Canvas, Frame, Scrollbar
from PIL import Image, ImageTk
import os
from frames.NextPageFrame import NextPageFrame

class ExerciseFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#121212")
        self.controller = controller

        assets_path = os.path.join(os.path.dirname(__file__), "..", "assets")
        logo_path = os.path.join(assets_path, "befit-logo-white.png")
        back_icon_path = os.path.join(assets_path, "prev-icon.png")

        # Load and resize logo
        logo_img = Image.open(logo_path).resize((150, 80),  Image.Resampling.LANCZOS)
        self.logo_photo = ImageTk.PhotoImage(logo_img)
        logo_label = tk.Label(self, image=self.logo_photo, bg="#121212")
        logo_label.place(relx=0.5, y=20, anchor="n")

        # Load and resize back icon
        back_img = Image.open(back_icon_path).resize((120, 80),  Image.Resampling.LANCZOS)
        self.back_photo = ImageTk.PhotoImage(back_img)
        self.back_btn = tk.Label(self, image=self.back_photo, bg="#121212", cursor="hand2")
        self.back_btn.place(x=20, y=20)
        self.back_btn.bind("<Button-1>", lambda e: self.go_back())
        self.back_btn.bind("<Enter>", lambda e: self.back_btn.config(bg="#1f1f1f"))
        self.back_btn.bind("<Leave>", lambda e: self.back_btn.config(bg="#121212"))

        # Workout Tips Section
        self.create_workout_tips()

    def go_back(self):
        self.controller.show_previous_frame()

    def create_workout_tips(self):
        tips = [
            {"title": "01 Set Clear Goals", "desc": "Define what you want to achieve—whether it's weight loss, muscle gain, or improved endurance. Clear goals give direction and purpose to your workouts."},
            {"title": "02 Create a Workout Plan", "desc": "Map out a weekly schedule that aligns with your fitness goals. A consistent and structured plan increases your chances of long-term success."},
            {"title": "03 Focus on Compound Workouts", "desc": "Incorporate exercises that target multiple muscle groups, like squats and bench presses, to maximize efficiency and effectiveness."},
            {"title": "04 Progressive Overload", "desc": "Gradually increase weight, reps, or intensity over time to continuously challenge your body and stimulate growth."},
            {"title": "05 Listen to Your Body During Workouts", "desc": "Pay attention to fatigue, pain, or discomfort. Rest when needed and avoid pushing through injury to prevent setbacks."},
            {"title": "06 Prioritize Recovery Between Workouts", "desc": "Allow your body ample time to recover through sleep, rest days, and stretching. Recovery is just as vital as training."},
            # {"title": "07 Stay Hydrated During and After Workouts", "desc": "Proper hydration supports muscle function, energy levels, and recovery. Drink water before, during, and after exercise."},
            # {"title": "08 Vary Your Workouts Regularly", "desc": "Switch up your routine to avoid plateaus and boredom. Try different exercises, intensities, or workout styles."},
            # {"title": "09 Stay Consistent with Your Workouts", "desc": "Consistency trumps perfection. Aim to stick to your schedule, even if you’re not always at 100%."},
            # {"title": "10 Track Your Progress with Workouts", "desc": "Use a fitness journal or app to log workouts, weights, and milestones. Tracking helps you stay motivated and measure results."},
            # {"title": "11 Warm Up Properly Before Workouts", "desc": "Start each session with dynamic stretches or light cardio to prepare your muscles and reduce the risk of injury."},
            # {"title": "12 Focus on Proper Form During Workouts", "desc": "Good form prevents injuries and ensures you're targeting the right muscles. Don't compromise form for heavier weights."},
            # {"title": "13 Include Restorative Activities Between Workouts", "desc": "Incorporate yoga, stretching, or massage to boost recovery, flexibility, and mental relaxation."},
            # {"title": "14 Stay Motivated with Your Workouts", "desc": "Set mini goals, reward progress, or find a workout buddy. Motivation is key to keeping up your routine."},
            # {"title": "15 Be Patient with Your Workouts", "desc": "Fitness progress takes time. Celebrate small wins, and trust the process while staying committed."},
            # {"title": "16 Visualize Success with Your Workouts", "desc": "Picture yourself achieving your goals. Visualization enhances focus, confidence, and workout performance."}
        ]

        container = Frame(self, bg="#121212")
        container.place(relx=0.5, rely=0.15, relwidth=0.9, relheight=0.8, anchor="n")

        canvas = Canvas(container, bg="#121212", highlightthickness=0)
        scrollable_frame = Frame(canvas, bg="#121212")

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.pack(fill="both", expand=True)

        def on_mousewheel(event):
            canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

        scrollable_frame.bind("<Enter>", lambda e: canvas.bind_all("<MouseWheel>", on_mousewheel))
        scrollable_frame.bind("<Leave>", lambda e: canvas.unbind_all("<MouseWheel>"))

        def update_scrollregion(event):
            canvas.configure(scrollregion=canvas.bbox("all"))

        scrollable_frame.bind("<Configure>", update_scrollregion)

        for tip in tips:
            card = Frame(scrollable_frame, bg="#1f1f1f", padx=20, pady=10)
            card.pack(pady=8, fill="x", expand=True)

            title_label = tk.Label(card, text=tip["title"], fg="#a855f7", bg="#1f1f1f", font=("Helvetica", 12, "bold"))
            title_label.pack(anchor="w")

            desc_label = tk.Label(card, text=tip["desc"], fg="#ffffff", bg="#1f1f1f", font=("Helvetica", 10), wraplength=1000, justify="left")
            desc_label.pack(anchor="w", pady=4)

            for widget in [card, title_label, desc_label]:
                widget.bind("<Enter>", lambda e, c=card: c.config(bg="#292929"))
                widget.bind("<Leave>", lambda e, c=card: c.config(bg="#1f1f1f"))

        # NEXT ICON BUTTON
        next_icon_img = Image.open("assets/next-icon.png")
        next_icon_img = next_icon_img.resize((120, 80), Image.LANCZOS)
        self.next_icon = ImageTk.PhotoImage(next_icon_img)

        self.next_btn = tk.Label(self, image=self.next_icon, bg="#121212", cursor="hand2")
        self.next_btn.place(relx=0.95, rely=0.95, anchor="se")

        def on_next_enter(e):
            self.next_btn.config(bg="#1a1a1a")
            self.next_btn.place_configure(relx=0.955)

        def on_next_leave(e):
            self.next_btn.config(bg="#121212")
            self.next_btn.place_configure(relx=0.95)

        self.next_btn.bind("<Enter>", on_next_enter)
        self.next_btn.bind("<Leave>", on_next_leave)
        self.next_btn.bind("<Button-1>", lambda e: self.controller.show_frame(NextPageFrame, transition="slide-right"))

