import tkinter as tk

class TransitionManager:
    def __init__(self, root, container):
        self.root = root
        self.container = container

    def slide(self, current_frame, next_frame, direction="right", speed=20):
        width = self.container.winfo_width()
        next_frame.place(in_=self.container, x=width if direction == "right" else -width, y=0, relwidth=1, relheight=1)

        step = 40
        dx = step if direction == "right" else -step

        def animate():
            x_cur = current_frame.winfo_x()
            x_next = next_frame.winfo_x()

            if (direction == "right" and x_next <= 0) or (direction == "left" and x_next >= 0):
                next_frame.place_configure(x=0)
                current_frame.place_forget()
                return

            current_frame.place_configure(x=x_cur - dx)
            next_frame.place_configure(x=x_next - dx)
            self.root.after(speed, animate)

        animate()

    def fade(self, current_frame, next_frame, duration=300):
        next_frame.place(in_=self.container, x=0, y=0, relwidth=1, relheight=1)
        next_frame.lift()

        # Create a temporary black overlay canvas
        overlay = tk.Canvas(self.container, bg="black", highlightthickness=0)
        overlay.place(x=0, y=0, relwidth=1, relheight=1)

        steps = 10
        delay = duration // steps

        def fade_in_out(step=0):
            alpha = step / steps
            color = f"#{int(18 + (0 - 18) * alpha):02x}" * 3
            overlay.configure(bg=color)

            if step >= steps:
                overlay.destroy()
                current_frame.place_forget()
                return

            self.root.after(delay, lambda: fade_in_out(step + 1))

        fade_in_out()
