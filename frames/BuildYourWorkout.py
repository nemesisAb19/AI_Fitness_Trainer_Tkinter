import tkinter as tk
from PIL import Image, ImageTk
from tkinter import Canvas, Frame, Entry

class BuildYourWorkout(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#121212")
        self.controller = controller

        self.card_widgets = []
        self.selected_exercises = []

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

        # ==== Selected Exercises Frame ====
        self.selected_frame = Frame(self, bg="#121212")
        self.selected_frame.place(relx=0.5, y=130, anchor="n", relwidth=0.9)

        # Heading
        self.heading = tk.Label(self, text="Recommended Exercises", font=("Helvetica", 28, "bold"),
                           fg="white", bg="#121212")
        self.heading.place(x=55, y=200, anchor="w")

        # Exercises list
        self.exercises = [
            "Bicep Curl", "Squats", "Shoulder Press",
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
        self.search_entry.place(x=60, y=240)

        # Scrollable Canvas for Recommended Exercises
        container = Frame(self, bg="#121212")
        self.recommend_container = container  # Store reference
        container.place(x=0, y=310, relwidth=1, relheight=0.58)

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

    def filter_exercises(self):
        query = self.search_var.get().strip().lower()
        if not query or query == "search exercises...":
            filtered = self.exercises
        else:
            filtered = [e for e in self.exercises if query in e.lower()]
        self.display_exercises(filtered)

    def on_card_click(self, exercise_name):
        if exercise_name in self.selected_exercises:
            self.selected_exercises.remove(exercise_name)
        else:
            self.selected_exercises.append(exercise_name)
        self.display_exercises(self.exercises)

    def display_exercises(self, exercise_list):
        # Clear existing
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        for widget in self.selected_frame.winfo_children():
            widget.destroy()

        # ==== Selected Exercises Display ====
        row = 0
        col = 0
        for idx, name in enumerate(self.selected_exercises):
            card = self.create_card(self.selected_frame, name, numbered=True, index=idx + 1)
            card.grid(row=row, column=col, padx=20, pady=10)
            col += 1
            if col >= 3:
                col = 0
                row += 1

        # Dynamically adjust the position of the text and search box
        self.update_positions()

        # Force update to compute height
        self.selected_frame.update_idletasks()
        selected_height = self.selected_frame.winfo_height()
        selected_y = self.selected_frame.winfo_y()

        # Move recommended section below selected section
        new_y = selected_y + selected_height + 50  # 50px margin
        self.canvas.master.place_configure(y=new_y)

        # ==== Recommended Exercises Display ====
        row = 0
        col = 0
        max_cols = 3

        for i, name in enumerate(exercise_list):
            if name in self.selected_exercises:
                continue  # Already displayed above
            card = self.create_card(self.scrollable_frame, name)
            card.grid(row=row, column=col, padx=20, pady=20)
            col += 1
            if col >= max_cols:
                col = 0
                row += 1

    def create_card(self, parent, name, numbered=False, index=None):
        card = tk.Frame(parent, bg="#1f1f1f", width=250, height=100, bd=0, relief="flat", cursor="hand2")
        card.grid_propagate(False)

        display_text = f"{index}. {name}" if numbered else name
        label = tk.Label(card, text=display_text, font=("Helvetica", 13, "bold"),
                         bg="#1f1f1f", fg="white")
        label.place(relx=0.5, rely=0.5, anchor="center")

        # Hover effect
        def on_enter(e): card.config(bg="#292929")
        def on_leave(e): card.config(bg="#1f1f1f")
        card.bind("<Enter>", on_enter)
        card.bind("<Leave>", on_leave)

        # Selection toggle
        card.bind("<Button-1>", lambda e: self.on_card_click(name))

        return card
    
    def update_positions(self):
        # Wait for the selected_frame to update its height
        self.update_idletasks()

        # Get the height of the selected_frame
        selected_frame_height = self.selected_frame.winfo_height()

        # Adjust the position of the text and search box
        new_y = 130 + selected_frame_height + 20  # 20px margin
        self.heading.place_configure(y=new_y)
        self.search_entry.place_configure(y=new_y + 40)  # 40px below the heading