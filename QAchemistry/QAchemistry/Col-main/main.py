import os
import time
import keyboard
import pyautogui
from termcolor import colored
from clo import Co

#Set
TOGGLE_KEY = 'F1'
XFOV = 35
YFOV = 35
IN_SENSITIVITY = 0.4
FLI = 1.07437623 * (IN_SENSITIVITY ** -0.9936827126)
MOV = 1 / (5 * IN_SENSITIVITY) #1.2 /3111

monitor = pyautogui.size()
CENTER_X, CENTER_Y = monitor.width // 2, monitor.height // 2

def main():
    os.system('title QAchem')
    color = Co(CENTER_X - XFOV // 2, CENTER_Y - YFOV // 2, XFOV, YFOV, FLI, MOV)


    print(colored('[Info]', 'green'), colored('Ne flash Made By', 'white'), colored('QAchemistry', 'magenta'))
    status = '0'
    
    try:
        while True:
            if keyboard.is_pressed(TOGGLE_KEY):
                color.toggle()
                status = '1 ' if color.toggled else 'Disabled'
            print(f'\r{colored("[Status]", "green")} {colored(status, "white")}', end='')
            time.sleep(0.01)
    except (KeyboardInterrupt, SystemExit):
        print(colored('\n[Info]', 'green'), colored('Exiting...', 'white') + '\n')
    finally:
        color.close()

if __name__ == '__main__':
    main()
