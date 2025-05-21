import tkinter as tk
from PIL import Image, ImageTk, ImageDraw
from frames.WorkoutsFrame import WorkoutsFrame

class NextPageFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#121212")
        self.controller = controller

        from frames.ExerciseFrame import ExerciseFrame

        # Load images
        logo_img = Image.open("assets/befit-logo-white.png").resize((150, 80))
        back_img = Image.open("assets/prev-icon.png").resize((120, 80))
        next_img = Image.open("assets/next-icon.png").resize((120, 80))  # Add this in assets

        self.logo = ImageTk.PhotoImage(logo_img)
        self.back_icon = ImageTk.PhotoImage(back_img)
        self.next_icon = ImageTk.PhotoImage(next_img)

        # Back button
        back_btn = tk.Label(self, image=self.back_icon, bg="#121212", cursor="hand2")
        back_btn.place(x=20, y=20)
        back_btn.bind("<Enter>", lambda e: back_btn.config(bg="#1a1a1a"))
        back_btn.bind("<Leave>", lambda e: back_btn.config(bg="#121212"))
        back_btn.bind("<Button-1>", lambda e: controller.show_frame(ExerciseFrame, transition="slide-left"))

        # Logo
        logo_label = tk.Label(self, image=self.logo, bg="#121212")
        logo_label.place(relx=0.5, y=20, anchor="n")

        # Container for vertical cards
        self.card_frame = tk.Frame(self, bg="#121212")
        self.card_frame.place(relx=0.5, rely=0.5, anchor="center")

        self.titles = [
            "Workouts",
            "Build Your Own Workout",
            "Browse Your Workouts"
        ]

        # Start fade-in animation
        self.card_widgets = []
        self.animate_cards(index=0)

        # Next icon button
        next_btn = tk.Label(self, image=self.next_icon, bg="#121212", cursor="hand2")
        next_btn.place(relx=0.96, rely=0.93, anchor="se")
        next_btn.bind("<Enter>", lambda e: next_btn.config(bg="#1a1a1a"))
        next_btn.bind("<Leave>", lambda e: next_btn.config(bg="#121212"))
        # next_btn.bind("<Button-1>", lambda e: controller.show_frame(AnotherFrame))  # Placeholder

    def animate_cards(self, index):
        if index >= len(self.titles):
            return
        card = self.create_rounded_card(self.card_frame, self.titles[index])
        card.pack(pady=15)
        self.card_widgets.append(card)
        self.after(200, lambda: self.animate_cards(index + 1))  # 200ms delay per card

    def create_rounded_card(self, parent, title):
        # Canvas for rounded effect
        canvas = tk.Canvas(parent, width=320, height=100, bg="#121212", bd=0, highlightthickness=0)
        radius = 20

        # Rounded rectangle
        canvas.create_arc((0, 0, radius*2, radius*2), start=90, extent=90, fill="#1e1e1e", outline="#1e1e1e")
        canvas.create_arc((320-radius*2, 0, 320, radius*2), start=0, extent=90, fill="#1e1e1e", outline="#1e1e1e")
        canvas.create_arc((0, 100-radius*2, radius*2, 100), start=180, extent=90, fill="#1e1e1e", outline="#1e1e1e")
        canvas.create_arc((320-radius*2, 100-radius*2, 320, 100), start=270, extent=90, fill="#1e1e1e", outline="#1e1e1e")
        canvas.create_rectangle((radius, 0, 320 - radius, 100), fill="#1e1e1e", outline="#1e1e1e")
        canvas.create_rectangle((0, radius, 320, 100 - radius), fill="#1e1e1e", outline="#1e1e1e")

        # Title text
        text = canvas.create_text(160, 50, text=title, fill="white", font=("Helvetica", 14, "bold"))

        # Hover effect
        def on_enter(e):
            for i in range(canvas.find_all().__len__() - 1):  # Exclude text
                canvas.itemconfig(i + 1, fill="#333333", outline="#333333")
            canvas.itemconfig(text, fill="#a855f7")

        def on_leave(e):
            for i in range(canvas.find_all().__len__() - 1):
                canvas.itemconfig(i + 1, fill="#1e1e1e", outline="#1e1e1e")
            canvas.itemconfig(text, fill="white")

        canvas.bind("<Enter>", on_enter)
        canvas.bind("<Leave>", on_leave)

        # 🟢 Navigate on click if title is "Workouts"
        if title == "Workouts":
            canvas.bind("<Button-1>", lambda e: self.controller.show_frame(WorkoutsFrame, transition="slide-right"))

        return canvas
