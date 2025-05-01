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

   In the Python console, invoke:
   ```python
   MotorVelocityInput(10, True, True)
   ```
   - `10` – speed value
   - `True` – clockwise rotation
   - `True` – run immediately

