import sys
import time
import subprocess
from threading import Thread

def install(pkg):
    subprocess.check_call([sys.executable, "-m", "pip", "install", pkg])

for pkg in ("PyQt5", "mss", "numpy", "opencv-python", "keyboard"):
    try:
        __import__(pkg)
    except ImportError:
        install(pkg)

import numpy as np
import cv2
import mss
import keyboard
from PyQt5 import QtCore, QtGui, QtWidgets

ACTIVE = False

def toggle_active(e):
    global ACTIVE
    ACTIVE = not ACTIVE
    print(f"[INFO] Aimbot {'activé' if ACTIVE else 'désactivé'}")

keyboard.on_press_key("f", toggle_active)

class Overlay(QtWidgets.QWidget):
    def __init__(self, w, h):
        super().__init__(None,
            QtCore.Qt.WindowStaysOnTopHint |
            QtCore.Qt.FramelessWindowHint  |
            QtCore.Qt.Tool)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setAttribute(QtCore.Qt.WA_TransparentForMouseEvents)
        self.setGeometry(0, 0, w, h)
        self.rect = None

    def paintEvent(self, e):
        if not self.rect:
            return
        qp = QtGui.QPainter(self)
        pen = QtGui.QPen(QtGui.QColor(255,255,0,200), 4)
        qp.setPen(pen)
        x, y, w, h = self.rect
        qp.drawRect(x, y, w, h)

    def update_box(self, rect):
        self.rect = rect
        self.update()

class Detector(Thread):
    def __init__(self, overlay):
        super().__init__(daemon=True)
        self.ov = overlay

    def run(self):
        time.sleep(1) 
        with mss.mss() as sct:
            MON = sct.monitors[1]          
            w, h = MON["width"], MON["height"]
            low1, hi1 = np.array([0,150,150]),   np.array([10,255,255])
            low2, hi2 = np.array([170,150,150]), np.array([180,255,255])
            kfx, kfy = int(w*0.7), int(h*0.2)

            while True:
                img   = sct.grab(MON)
                frame = cv2.cvtColor(np.array(img), cv2.COLOR_BGRA2BGR)

                if ACTIVE:
                    hsv  = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
                    mask = cv2.inRange(hsv, low1, hi1) | cv2.inRange(hsv, low2, hi2)
                    kern = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (9,9))
                    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE,  kern, iterations=4)
                    mask = cv2.morphologyEx(mask, cv2.MORPH_DILATE, kern, iterations=2)
                    mask[0:kfy, kfx:w] = 0
                    cnts,_ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                    cnts   = [c for c in cnts if cv2.contourArea(c) > 2000]
                    if cnts:
                        c = max(cnts, key=cv2.contourArea)
                        x,y,ww,hh = cv2.boundingRect(c)
                        self.ov.update_box((x, y, ww, hh))
                    else:
                        self.ov.update_box(None)
                else:
                    self.ov.update_box(None)

                time.sleep(1/60)

if __name__ == "__main__":
    with mss.mss() as sct:
        mon = sct.monitors[1]
        W, H = mon["width"], mon["height"]

    app = QtWidgets.QApplication([])
    ov  = Overlay(W, H)
    ov.show()

    Detector(ov).start()

    print("[INFO] Presse **F** pour activer/désactiver l’aimbot.")
    sys.exit(app.exec_())

