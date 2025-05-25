# --- BuildYourWorkout.py (Cleaned) ---
import tkinter as tk
from PIL import Image, ImageTk
from tkinter import Frame, Canvas, Entry
from frames.CustomizeSettings import CustomizeSettings

class BuildYourWorkout(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#121212")
        self.controller = controller
        self.selected_exercises = []

        from frames.NextPageFrame import NextPageFrame

        self.logo = ImageTk.PhotoImage(Image.open("assets/befit-logo-white.png").resize((150, 80)))
        self.back_icon = ImageTk.PhotoImage(Image.open("assets/prev-icon.png").resize((120, 80)))
        self.start_icon = ImageTk.PhotoImage(Image.open("assets/start-button-2-white.png").resize((160, 90)))

        tk.Label(self, image=self.logo, bg="#121212").place(relx=0.5, y=20, anchor="n")

        back_btn = tk.Label(self, image=self.back_icon, bg="#121212", cursor="hand2")
        back_btn.place(x=20, y=20)
        back_btn.bind("<Enter>", lambda e: back_btn.config(bg="#1a1a1a"))
        back_btn.bind("<Leave>", lambda e: back_btn.config(bg="#121212"))
        back_btn.bind("<Button-1>", lambda e: controller.show_frame(NextPageFrame))

        self.selected_frame = Frame(self, bg="#121212")
        self.selected_frame.place(relx=0.5, y=130, anchor="n", relwidth=0.9)

        self.heading = tk.Label(self, text="Recommended Exercises", font=("Helvetica", 28, "bold"), fg="white", bg="#121212")
        self.heading.place(x=55, y=200, anchor="w")

        self.search_var = tk.StringVar()
        self.search_var.trace("w", lambda *args: self.filter_exercises())

        self.search_entry = Entry(self, textvariable=self.search_var, font=("Helvetica", 12),
                                  bg="#1f1f1f", fg="gray", insertbackground="white",
                                  relief="flat", highlightthickness=1, highlightbackground="#333", width=30)
        self.search_entry.insert(0, "Search exercises...")
        self.search_entry.bind("<FocusIn>", lambda e: self.clear_placeholder())
        self.search_entry.bind("<FocusOut>", lambda e: self.add_placeholder())
        self.search_entry.place(x=60, y=240)

        container = Frame(self, bg="#121212")
        self.recommend_container = container
        container.place(x=0, y=310, relwidth=1, relheight=0.58)

        self.canvas = Canvas(container, bg="#121212", highlightthickness=0)
        self.canvas.pack(side="left", fill="both", expand=True)

        self.scrollable_frame = Frame(self.canvas, bg="#121212")
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.scrollable_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)

        self.exercises = ["Bicep Curl", "Squats", "Shoulder Press", "Push-Ups", "Mountain Climber", "Skipping", "Pull Ups", "Hip Thrust", "Tricep Dips"]

        self.start_btn = tk.Label(self, image=self.start_icon, bg="#121212", cursor="hand2")
        self.start_btn.bind("<Button-1>", self.go_to_customize_settings)
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
        filtered = [e for e in self.exercises if query in e.lower()] if query else self.exercises
        self.display_exercises(filtered)

    def on_card_click(self, exercise_name):
        if exercise_name in self.selected_exercises:
            self.selected_exercises.remove(exercise_name)
        else:
            self.selected_exercises.append(exercise_name)
        self.display_exercises(self.exercises)

    def display_exercises(self, exercise_list):
        for widget in self.scrollable_frame.winfo_children(): widget.destroy()
        for widget in self.selected_frame.winfo_children(): widget.destroy()

        row = col = 0
        for idx, name in enumerate(self.selected_exercises):
            self.create_card(self.selected_frame, name, idx + 1).grid(row=row, column=col, padx=20, pady=10)
            col = 0 if (col + 1) % 3 == 0 else col + 1
            row += 1 if col == 0 else 0

        self.update_positions()

        row = col = 0
        for name in exercise_list:
            if name not in self.selected_exercises:
                self.create_card(self.scrollable_frame, name).grid(row=row, column=col, padx=20, pady=20)
                col = 0 if (col + 1) % 3 == 0 else col + 1
                row += 1 if col == 0 else 0

    def create_card(self, parent, name, index=None):
        card = tk.Frame(parent, bg="#1f1f1f", width=250, height=100, bd=0, relief="flat", cursor="hand2")
        card.grid_propagate(False)
        label_text = f"{index}. {name}" if index else name
        tk.Label(card, text=label_text, font=("Helvetica", 13, "bold"), bg="#1f1f1f", fg="white").place(relx=0.5, rely=0.5, anchor="center")
        card.bind("<Enter>", lambda e: card.config(bg="#292929"))
        card.bind("<Leave>", lambda e: card.config(bg="#1f1f1f"))
        card.bind("<Button-1>", lambda e: self.on_card_click(name))
        return card

    def update_positions(self):
        self.update_idletasks()
        selected_height = self.selected_frame.winfo_height()
        selected_y = self.selected_frame.winfo_y()
        new_y = selected_y + selected_height + 50
        self.heading.place_configure(y=new_y)
        self.search_entry.place_configure(y=new_y + 40)
        self.canvas.master.place_configure(y=new_y + 100)
        if self.selected_exercises:
            self.start_btn.place(x=self.winfo_width() - 250, y=selected_y + 10)
        else:
            self.start_btn.place_forget()

    def go_to_customize_settings(self, event=None):
        self.controller.frames[CustomizeSettings].selected_exercises = self.selected_exercises
        self.controller.show_frame(CustomizeSettings, transition="slide-left")
