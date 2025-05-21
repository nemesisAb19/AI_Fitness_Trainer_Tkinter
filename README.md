# AI Fitness Trainer - Tkinter App

 An AI-powered fitness trainer desktop application built with **Tkinter**, **MediaPipe**, and **OpenCV**, providing real-time pose tracking, workout feedback, and a sleek modern UI.

---

## 📁 Project Structure
AI_Fitness_Trainer_Tkinter/

├── .venv/

├── assets/

│   ├── bicep_curl.gif

│   ├── cross-button.png

│   └── befit-logo-white.png

│   ├── next-icon.png

│   ├── prev-icon.png

│   └── start-button.png

├── modules/

│   ├── __pycache__/

│   ├── __init__.py

│   ├── bicep_check.py

│   ├── PoseModule.py

│   ├── ExercisesModule.py

│   ├── AudioCommSys.py

│   ├── face_detection.py

│   ├── camera.py

│   └── camera_check.py

├── frames/

│   ├── __pycache__/

│   ├── __init__.py

│   ├── BicepCurlSettingsFrame.py	

│   ├── ExerciseFrame.py

│   ├── WorkoutsFrame.py

│   ├── NextPageFrame.py

│   └── StreamingFrame.py

├── utils/

│   ├── __pycache__/

│   └── TransitionManager.py

├── main.py

├── README.md

├── requirements.txt

└── .venv/

---

## Features

- Real-time **pose detection** and **repetition counting**
- **Voice feedback** using Text-to-Speech
- Modern **Tkinter UI** with smooth transitions and image cards
- Searchable, scrollable exercise list
- Exercise-specific settings (e.g., sets, reps, rest timer)
- Fullscreen stream, screenshot, and session recording support (coming soon)

---

## How to Run the Project

1. **Clone the repository:**
   ```bash
   https://github.com/nemesisAb19/AI_Fitness_Trainer_Tkinter.git
   cd AI_Fitness_Trainer_Tkinter

2. **Create a Virtual Environment (Optional but Recommended)**
   
   python -m venv .venv
   
   **Activate it:**
   
   a. On Windows:
   
   .venv\Scripts\activate
   
   b. On Mac/Linux:
   
   source .venv/bin/activate

4. Install Dependencies
   
   pip install -r requirements.txt

6. Run the App
   
   python main.py


## 📦 Dependencies
Main packages used:
- opencv-python
- mediapipe
- Pillow
- pyttsx3
- speechrecognition
- tkinter (comes with Python)


## Contributing
I just wanted to let you know that pull requests are welcome. For major changes, please open an issue first to discuss.


## 📃 License
This project is open-source and free to use.
