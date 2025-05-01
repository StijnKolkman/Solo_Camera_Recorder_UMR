# Single-Camera Tracking Setup

This repository provides a simplified, single-camera tracking and recording application derived from the original dual-camera system.

## Prerequisites

- **Python 3.7+**
- **Virtual environment** module (included with Python)
- **OpenCV**, **NumPy**, **Pillow**, **Tkinter** (usually bundled)

## Getting Started

Follow these steps in your VS Code integrated terminal (or any command prompt):

1. **Clone the repository**
   
   ```bash
   git clone https://github.com/<your-username>/<your-repo>.git
   cd <your-repo>
   ```

2. **Create a virtual environment**

   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment**

   - **Windows (PowerShell)**
     ```powershell
     .\venv\Scripts\Activate.ps1
     ```
   - **Windows (cmd.exe)**
     ```bat
     .\venv\Scripts\activate.bat
     ```
   - **macOS / Linux**
     ```bash
     source venv/bin/activate
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

   In the Python console (or by adding this call in `main.py`), invoke:
   ```python
   MotorVelocityInput(10, True, True)
   ```
   - `10` – speed value
   - `True` – clockwise rotation
   - `True` – run immediately

## Troubleshooting

- If you see an “invalid command name” error when closing the app, ensure the Tkinter `after()` callback is canceled before destroying the window.
- Adjust `camera_index` in `main.py` if your webcam has a different ID (default is `0`).

---

Happy tracking!

