import cv2
import numpy as np
import threading
import time
import win32api
import pyautogui

from capture import Capture
from mouse import ArduinoMouse
from fov_window import show_detection_window, toggle_window

class Co:
    LOWER_COLOR = np.array([140, 120, 180])
    UPPER_COLOR = np.array([160, 200, 255])

    def __init__(self, x, y, xfov, yfov, FLI, MOV):
        self.arduinomouse = ArduinoMouse()
        self.grabber = Capture(x, y, xfov, yfov)
        self.flickspeed = FLI
        self.movespeed = MOV
        threading.Thread(target=self.listen, daemon=True).start()
        self.toggled = False
        self.window_toggled = False
        self.action_mode = 'he'
    def toggle(self):
        self.toggled = not self.toggled
        time.sleep(0.2)
    
    def listen(self):
        while True:
            if win32api.GetAsyncKeyState(0x22) < 0 :  #PGNdOWN
                self.action_mode = 'cli'  # Thiết lập chế độ 'fli'
                time.sleep(0.2)  # Đợi để tránh thực hiện nhiều lần
            elif win32api.GetAsyncKeyState(0x21) < 0 : #PGu
                self.action_mode = 'he'  # Thiết lập chế độ 'he'
                time.sleep(0.2)  # Đợi để tránh thực hiện nhiều lần
            if win32api.GetAsyncKeyState(0x06) < 0:  
                if self.action_mode == 'cli':
                    self.process("cli")
                elif self.action_mode == 'he':
                    self.process("he")
            if win32api.GetAsyncKeyState(0x76) < 0:
                toggle_window(self)
                time.sleep(0.2)
            if win32api.GetAsyncKeyState(0x05) < 0 and self.toggled:
                self.process("mov")
            # elif win32api.GetAsyncKeyState(0xA4) < 0 and self.toggled:
            #     self.process("cli")
            # elif win32api.GetAsyncKeyState(0x06) < 0 and  self.toggled:
            #     self.process("he")
            # elif win32api.GetAsyncKeyState(0x14) < 0 and self.toggled:  # Caps Lock key
            #     self.arduinomouse.dogle(0, 30)
            
            elif win32api.GetAsyncKeyState(0x14) < 0 and self.toggled: #caps
                self.process("flijet")
            elif win32api.GetAsyncKeyState(0xA4) < 0 and self.toggled: #alt
                self.process("fli")
                






    def process(self, action):
        screen = self.grabber.get_screen()
        hsv = cv2.cvtColor(screen, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, self.LOWER_COLOR, self.UPPER_COLOR)
        dilated = cv2.dilate(mask, None, iterations=5)
        contours, _ = cv2.findContours(dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        if not contours:
            return

        contour = max(contours, key=cv2.contourArea)
        x, y, w, h = cv2.boundingRect(contour)
        center = (x + w // 2, y + h // 2)
        y_offset = int(h * 0.44) #height of rec 30
        y_offsethead = int(h * 0.3) #height of rec 30
        y_offsetheadfli = int(h * 0.3)
















        if action == "mov":
            cX = center[0]
            cY = y + y_offset
            x_diff = cX - self.grabber.xfov // 2
            y_diff = cY - self.grabber.yfov // 2
            self.arduinomouse.move(x_diff * self.movespeed, y_diff * self.movespeed)

        elif action == "cli" and abs(center[0] - self.grabber.xfov // 2) <= 5 and abs(center[1] - self.grabber.yfov // 2) <= 10:
            self.arduinomouse.click()

        elif action == "fli":
            cX = center[0] + 2
            cY = y + y_offsetheadfli
            x_diff = cX - self.grabber.xfov // 2
            y_diff = cY - self.grabber.yfov // 2
            flickx = x_diff * self.flickspeed
            flicky = y_diff * self.flickspeed
            self.arduinomouse.flick(flickx, flicky)
            self.arduinomouse.click()
            time.sleep(0.1)

            # self.arduinomouse.flick(-(flickx), -(flicky))
        elif action == "flijet":
            cX = center[0] + 2
            cY = y + y_offsetheadfli
            x_diff = cX - self.grabber.xfov // 2
            y_diff = cY - self.grabber.yfov // 2
            flickx = x_diff * self.flickspeed
            flicky = y_diff * self.flickspeed
            self.arduinomouse.flick(flickx, flicky)
            self.arduinomouse.click()
            time.sleep(0.01)
        elif action == "he":
            cX = center[0]
            cY = y + y_offsethead
            x_diff = cX - self.grabber.xfov // 2
            y_diff = cY - self.grabber.yfov // 2
            self.arduinomouse.move(x_diff * self.movespeed, y_diff * self.movespeed)
            






