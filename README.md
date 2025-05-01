# Single-Camera Tracking Setup

This repository provides a simplified, single-camera tracking and recording application derived from the original dual-camera system.

## Prerequisites

- **Python 3.7+**
- **Virtual environment** module (included with Python)
- **OpenCV**, **NumPy**, **Pillow**, **Tkinter** (usually bundled)

## Getting Started
NOTE: make sure that you put in windows your system --> display --> scale setting at 100%. Otherwise the shown camera frame doesn't fit
Follow these steps in your VS Code integrated terminal (or any command prompt):

1. **Clone the repository**
   
   ```bash
   git clone https://github.com/StijnKolkman/Solo_Camera_Recorder_UMR.git
   cd Solo_Camera_Recorder_UMR
   ```

2. **Create a virtual environment**

   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment**
     ```powershell
     .\venv\Scripts\Activate
     ```

4. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. **Run the tracking application**

   ```bash
   python main.py
   ```

2. **Start the motor**

   In a new Python Terminal start the venv again and, invoke:
   ```python
   python MotorVelocityInput.py
   ```
   - `10` – speed value
   - `True` – clockwise rotation
   - `True` – run immediately

