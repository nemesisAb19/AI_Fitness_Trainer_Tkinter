import tkinter as tk
from frames.ExerciseFrame import ExerciseFrame
from frames.NextPageFrame import NextPageFrame
from utils.TransitionManager import TransitionManager
from frames.WorkoutsFrame import WorkoutsFrame
from frames.BicepCurlSettingsFrame import BicepCurlSettingsFrame
from frames.StreamingFrame import StreamingFrame
from frames.SquatsStreamingFrame import SquatsStreamingFrame

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("AI Fitness Trainer")
        self.geometry("1280x720")
        self.configure(bg="#121212")

        self.container = tk.Frame(self, bg="#121212")
        self.container.pack(fill="both", expand=True)

        self.frames = {}
        self.transition_manager = TransitionManager(self, self.container)
        self.current_frame = None

        # Add all frames, including PoseDetectionFrame
        for FrameClass in (ExerciseFrame, NextPageFrame, WorkoutsFrame, BicepCurlSettingsFrame, StreamingFrame, SquatsStreamingFrame):
            frame = FrameClass(self.container, self)
            self.frames[FrameClass] = frame
            # Do not pack or place here — handled during transition

        # Show the first frame instantly without animation
        self.show_frame(ExerciseFrame, transition=None)

    def show_frame(self, frame_class, transition=None):
        print(f"Navigating to frame: {frame_class.__name__}")
        next_frame = self.frames[frame_class]

        if self.current_frame is None or transition is None:
            next_frame.place(in_=self.container, x=0, y=0, relwidth=1, relheight=1)
            self.current_frame = next_frame
            return

        if transition == "slide-right":
            self.transition_manager.slide(self.current_frame, next_frame, direction="right")
        elif transition == "slide-left":
            self.transition_manager.slide(self.current_frame, next_frame, direction="left")
        elif transition == "fade":
            self.transition_manager.fade(self.current_frame, next_frame)

        self.current_frame = next_frame


if __name__ == "__main__":
    app = App()
    app.mainloop()