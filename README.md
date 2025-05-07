# 🎯 AimAssist for Overwatch

**AimAssist** is a Python script that **enhances aiming in Overwatch** by visually highlighting enemies with a **yellow box overlay** based on color detection (not AI-based).  
Perfect for training, reflex improvement, or visual experimentation.

---

## ⚙️ Features

- 🔍 Real-time detection of enemies outlined in red using HSV color filtering
- 🟨 Draws a **yellow rectangle overlay** around the largest detected red contour
- 🖱️ Activates only when Overwatch is the active window
- ⌨️ Toggle on/off with the `F` key
- 🧪 100% visual overlay, does not control mouse or send inputs

---

## 🧰 Requirements

- Python 3.10+
- PyQt5 (for GUI overlay)
- OpenCV (for image processing)
- Overwatch in **Borderless Windowed mode**

---

## 📦 Installation

1. Clone this repo or download `aim.py`:
   ```bash
   git clone https://github.com/we-lord/AimAssist-Overwatch.git
   cd AimAssist-Overwatch
   ```

2. Install dependencies:
   ```bash
   pip install pyqt5 mss numpy opencv-python keyboard
   ```

---

## 🚀 Usage

1. Launch Overwatch
2. In your terminal:
   ```bash
   python aim.py
   ```
3. Press `F` to toggle the detection overlay on/off
4. When an enemy outlined in red is detected, a yellow rectangle will appear around them

---

## 🔐 Disclaimer

> This script is for **educational and training purposes only**.  
> It does not interact with Overwatch, does not send input, and does not modify the game in any way.  
> Purely visual and passive.

---

## 🧠 Roadmap

- ✅ Add toggle key support (`F`)
- 🔄 Improve multiple-target prioritization
- 🎯 Future: optional aim assistance (mouse movement)

---



© 2025 – Visual overlay training tool for Overwatch


