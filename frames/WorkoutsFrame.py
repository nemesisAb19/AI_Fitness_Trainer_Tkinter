import tkinter as tk
from tkinter import Canvas, Frame, Entry
from PIL import Image, ImageTk
from frames.BicepCurlSettingsFrame import BicepCurlSettingsFrame

class WorkoutsFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#121212")
        self.controller = controller

        self.card_widgets = []

        from frames.NextPageFrame import NextPageFrame

        # Load images
        logo_img = Image.open("assets/befit-logo-white.png").resize((150, 80))
        back_img = Image.open("assets/prev-icon.png").resize((120, 80))

        self.logo = ImageTk.PhotoImage(logo_img)
        self.back_icon = ImageTk.PhotoImage(back_img)

        # Back button
        back_btn = tk.Label(self, image=self.back_icon, bg="#121212", cursor="hand2")
        back_btn.place(x=20, y=20)
        back_btn.bind("<Enter>", lambda e: back_btn.config(bg="#1a1a1a"))
        back_btn.bind("<Leave>", lambda e: back_btn.config(bg="#121212"))
        back_btn.bind("<Button-1>", lambda e: controller.show_frame(NextPageFrame, transition="slide-left"))

        # Logo
        logo_label = tk.Label(self, image=self.logo, bg="#121212")
        logo_label.place(relx=0.5, y=20, anchor="n")

        # Heading
        heading = tk.Label(self, text="Hustle for that Muscle", font=("Helvetica", 28, "bold"),
                           fg="white", bg="#121212")
        heading.place(relx=0.5, y=120, anchor="n")

        # Exercises list
        self.exercises = [
            "Bicep Curl", "Squat", "Shoulder Press",
            "Push-Ups", "Mountain Climber", "Skipping",
            "Pull Ups", "Hip Thrust", "Tricep Dips"
        ]

        # Search bar
        self.search_var = tk.StringVar()
        self.search_var.trace("w", lambda name, index, mode: self.filter_exercises())

        self.search_entry = Entry(self, textvariable=self.search_var, font=("Helvetica", 12),
                                  bg="#1f1f1f", fg="gray", insertbackground="white",
                                  relief="flat", highlightthickness=1, highlightbackground="#333", width=30)
        self.search_entry.insert(0, "Search exercises...")
        self.search_entry.bind("<FocusIn>", lambda e: self.clear_placeholder())
        self.search_entry.bind("<FocusOut>", lambda e: self.add_placeholder())
        self.search_entry.place(x=60, y=180)

        # Scrollable Canvas
        container = Frame(self, bg="#121212")
        container.place(relx=0.5, rely=0.38, anchor="n", relwidth=0.9, relheight=0.58)

        self.canvas = Canvas(container, bg="#121212", highlightthickness=0)
        self.canvas.pack(side="left", fill="both", expand=True)

        self.scrollable_frame = Frame(self.canvas, bg="#121212")
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")

        self.scrollable_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)

        self.display_exercises(self.exercises)

    def _on_mousewheel(self, event):
        self.canvas.yview_scroll(-1 * int(event.delta / 120), "units")

    def clear_placeholder(self):
        if self.search_entry.get() == "Search exercises...":
            self.search_entry.delete(0, tk.END)
            self.search_entry.config(fg="white")

    def add_placeholder(self):
        if not self.search_entry.get():
            self.search_entry.insert(0, "Search exercises...")
            self.search_entry.config(fg="gray")

    def display_exercises(self, exercise_list):
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        self.card_widgets.clear()

        row = 0
        col = 0
        max_cols = 3

        for i, name in enumerate(exercise_list):
            card = tk.Frame(self.scrollable_frame, bg="#1f1f1f", width=250, height=100, bd=0, relief="flat")
            card.grid(row=row, column=col, padx=20, pady=20)
            card.grid_propagate(False)

            label = tk.Label(card, text=name, font=("Helvetica", 13, "bold"),
                             bg="#1f1f1f", fg="white")
            label.place(relx=0.5, rely=0.5, anchor="center")

            # Hover effect
            def on_enter(e, c=card): c.config(bg="#292929")
            def on_leave(e, c=card): c.config(bg="#1f1f1f")
            card.bind("<Enter>", on_enter)
            card.bind("<Leave>", on_leave)

            if name.lower() == "bicep curl":
                card.bind("<Button-1>", lambda e: self.controller.show_frame(BicepCurlSettingsFrame, transition="slide-right"))

            self.card_widgets.append(card)

            col += 1
            if col >= max_cols:
                row += 1
                col = 0

    def filter_exercises(self):
        query = self.search_var.get().strip().lower()
        if not query or query == "search exercises...":
            filtered = self.exercises
        else:
            filtered = [e for e in self.exercises if query in e.lower()]
        self.display_exercises(filtered)
