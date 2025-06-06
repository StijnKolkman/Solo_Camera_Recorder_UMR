"""

NOTE: ORIGINALLY THE CLASS WAS WRITTEN FOR TWO CAMERAS, THIS VERSION HOWEVER IS THE ADAPTATION FOR IF YOU USE ONE CAMERA

DualCameraApp Class

This class provides a graphical user interface (GUI) for recording video using two cameras 
simultaneously. It allows the user to control the recording process, including the ability 
to start/stop recording, adjust the camera focus, and save the recorded video files. The 
recorded files are saved in AVI format, and the filenames are generated dynamically based 
on user input.

Methods:
- __init__(window): Initializes the application window, sets up the GUI components, and initializes cameras.
- set_focus1(val): Sets the focus of camera 1 based on the slider value.
- set_focus2(val): Sets the focus of camera 2 based on the slider value.
- set_recording_done_callback(callback): Sets a callback function to be called when the recording is finished.
- toggle_recording(): Starts or stops the recording process.
- update_frame(): Continuously updates the frames from both cameras in the GUI.
- on_closing(): Releases the video capture objects and destroys the window when the application is closed.

Author: Stijn Kolkman (s.y.kolkman@student.utwente.nl)
Date: April 2025
"""

import cv2
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import time
import numpy as np 
import os
import subprocess 
import csv

cap_api = cv2.CAP_DSHOW  # Found to be the best API for using with logitech C920 in Windows. Other options are also possible

class DualCameraApp:
    def __init__(self, window):
        self.window = window
        self.window.title("Dual Camera Recorder")
        self.recording = False
        self.recorded_file_names = None 
        self.N_frames_cam1 = 0
        self.record_start_time = None
        # keep a handle for the after() call
        self._after_id = None

        # Define the size of the GUI
        self.window.geometry("1920x1080")

        # Here the camera's are defined. Camera's can have different numbers on different computers, so change the number if needed (default is cap1 = 1, cap2 = 0)
        self.cap1 = cv2.VideoCapture(0, cap_api)

        # Camera resolution
        self.cap1.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
        self.cap1.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

        # Camera framerate
        self.cap1.set(cv2.CAP_PROP_FPS, 30)

        # Camera compression technique --> If turned off the FPS will be really low (around 5 fps)
        fourcc = cv2.VideoWriter_fourcc(*'MJPG')
        self.cap1.set(cv2.CAP_PROP_FOURCC, fourcc)

        #Turns off the autofocus 
        self.cap1.set(cv2.CAP_PROP_AUTOFOCUS, 0)

        # === GUI components ===
        # Label to display the text "File name:"
        self.filename_label = tk.Label(window, text="File name:")
        self.filename_label.pack(pady=(10, 0))

        # Entry widget to allow the user to input a file name
        self.filename_entry = tk.Entry(window)
        self.filename_entry.insert(0, "Recording")
        self.filename_entry.pack(pady=(0, 10))

        # Frame container that holds the two video display labels side by side
        self.frame_container = tk.Frame(window)
        self.frame_container.pack()

        # Label for displaying the first video feed, placed on the left side of the frame container
        self.video_label1 = tk.Label(self.frame_container)
        self.video_label1.pack(side="left", padx=10)

        # Label and slider for adjusting the focus of the first camera
        self.focus_label1 = tk.Label(window, text="Focus Camera 1")
        self.focus_label1.pack()

        # Slider for setting the focus of Camera 1, with a range from 0 to 255
        self.focus_slider1 = ttk.Scale(window, from_=0, to=255, orient='horizontal', length=400, command=self.set_focus1)
        self.focus_slider1.set(58)  # Set the default focus value for Camera 1 to 58
        self.focus_slider1.pack()

        # Label to display the current focus value for Camera 1
        self.focus_value_label1 = tk.Label(window, text=f"Focus Camera 1 Value: {self.focus_slider1.get()}")
        self.focus_value_label1.pack()

        # Button to start or stop recording
        self.record_button = tk.Button(window, text="Start recording", command=self.toggle_recording, bg="red", fg="white")
        self.record_button.pack(pady=10)

        # Label to display the names of the recorded files (empty initially)
        self.recorded_files_label = tk.Label(window, text="", fg="blue")
        self.recorded_files_label.pack(pady=10)

        #Initiate timestamps array
        self.timestamps = []

        # Method to continuously update the frame (e.g., display live video feed)
        self.update_frame()

        # Ensuring proper cleanup
        self.window.protocol("WM_DELETE_WINDOW", self.on_closing)

    def set_focus1(self, val):
        # Update the focus on camera1
        focus_value = float(val)
        self.cap1.set(cv2.CAP_PROP_FOCUS, focus_value)
        if hasattr(self, 'focus_value_label1'):  # Ensure the label exists before updating
            # Update the label
            self.focus_value_label1.config(text=f"Focus Camera 1 Value: {focus_value:.2f}")

    def set_recording_done_callback(self, callback):
        # needed to send to  main that the recording is done and the tracker should start
        self.recording_done_callback = callback

    def toggle_recording(self):
        self.recording = not self.recording
        filename = self.filename_entry.get().strip() or "recording"
        output_dir = os.path.join(os.getcwd(), filename)
        os.makedirs(output_dir, exist_ok=True)

        cam1_filename = os.path.join(output_dir, f"{filename}_cam1.avi")

        if self.recording:
            # Create video writer
            self.N_frames_cam1 = 0
            self.record_start_time = time.time()
            self.record_button.config(text="Stop recording", bg="gray")
            self.recorded_files_label.config(text="Recording in progress...")
            print(f"Started recording: {cam1_filename}")
            
            self.out1 = cv2.VideoWriter(cam1_filename, cv2.VideoWriter_fourcc(*'XVID'), 30, (1920, 1080))

        else:
            # Stop recording and calculate FPS
            duration = time.time() - self.record_start_time
            fps_value = self.N_frames_cam1 / duration if duration > 0 else 30.0
            print(f"Duration: {duration:.2f}s — FPS: {fps_value:.2f}")

            # Adjust the FPS value of the video writers after recording
            self.out1.set(cv2.CAP_PROP_FPS, fps_value)
            self.out1.release()

            self.record_button.config(text="Start recording", bg="red")
            files_text = f"Recorded files:\n{cam1_filename}"
            self.recorded_files_label.config(text=files_text)
            print("Recording done and saved")
            self.recorded_file_names = (cam1_filename)  # Store filenames

            # Save timestamps to CSV
            timestamp_filename = os.path.join(output_dir, f"{filename}_timestamps.csv")
            with open(timestamp_filename, "w", newline="") as f:
                writer = csv.writer(f)
                writer.writerow(["Frame", "Timestamp (s)"])
                for i, ts in enumerate(self.timestamps):
                    writer.writerow([i, ts])
            self.timestamps = []  # Clear timestamps after saving

            print(f"[INFO] Timestamps saved to {timestamp_filename}")

            # Call the callback when recording is done and change the fps to the correct value, but only if files are recorded
            if hasattr(self, 'recording_done_callback') and self.recorded_file_names:
                self.recording_done_callback()  # Notify that recording is done

    def update_frame(self):
        # Check if the window is still open before updating
        if not self.window.winfo_exists():
            return  # Exit the function if the window is closed
        
         #Read the frames
        ret1, frame1 = self.cap1.read()

        if self.recording and ret1:
            # Save frames
            self.N_frames_cam1 += 1
            self.out1.write(frame1)

            # Only log timestamp if both frames were successfully saved
            timestamp = time.time() - self.record_start_time
            self.timestamps.append(timestamp)

        #Undistort the frames --> I UNDISTORT IN THE TRAJECTORY GENERATOR CLASS
        #frame1 = cv2.undistort(frame1, self.camera_matrix1, self.dist_coeffs1)
        #frame2 = cv2.undistort(frame2, self.camera_matrix2, self.dist_coeffs2)

        if ret1:
            # Update the GUI with the frame --> first the frame is resized to fit in the GUI 
            frame1_resized = cv2.resize(frame1, (1344, 756), interpolation=cv2.INTER_LINEAR)
            frame_rgb1 = cv2.cvtColor(frame1_resized, cv2.COLOR_BGR2RGB)
            img1 = ImageTk.PhotoImage(Image.fromarray(frame_rgb1))
            self.video_label1.imgtk = img1
            self.video_label1.config(image=img1)

        self._after_id = self.window.after(10, self.update_frame)

    def on_closing(self):
        # cancel the pending after() callback so it won't fire
        if self._after_id is not None:
            self.window.after_cancel(self._after_id)
            self._after_id = None

        self.cap1.release()
        self.window.destroy()

# Used if the recorder class is called seperately
if __name__ == "__main__":
    root = tk.Tk()
    app = DualCameraApp(root)
    root.mainloop()
