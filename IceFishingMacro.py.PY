# Made by Glyphaj
import pyautogui
import numpy as np
from PIL import ImageGrab
import time
import sys
import os
import ctypes
import pygetwindow as gw
import threading

specific_green_1 = np.array([0, 255, 170])
specific_green_2 = np.array([100, 0, 33])

exit_flag = False

BRIGHT_RED = "\033[1;31m"
RESET_COLOR = "\033[0m"

def set_window_title(title="Python"):
    if os.name == 'nt':
        ctypes.windll.kernel32.SetConsoleTitleW(title)

def detect_specific_green():
    screen = np.array(ImageGrab.grab())
    mask_1 = np.all(screen == specific_green_1, axis=-1)
    mask_2 = np.all(screen == specific_green_2, axis=-1)
    return np.any(mask_1) or np.any(mask_2)

def typing_animation(message, speed=0.05):
    for char in message:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(speed)
    print()

def control_mouse():
    mouse_down = False
    try:
        while not exit_flag:
            if detect_specific_green():
                if not mouse_down:
                    pyautogui.mouseDown()
                    mouse_down = True
            else:
                if mouse_down:
                    pyautogui.mouseUp()
                    mouse_down = False
            time.sleep(0.1)
    except KeyboardInterrupt:
        print("Program exited.")

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_red_ascii_art():
    RED = "\033[1;31m"
    RESET = "\033[0m"
    FISHKISS_ASCII = """
 ██████╗ ██╗  ██╗   ██╗██████╗ ██╗  ██╗     █████╗      ██╗
██╔════╝ ██║  ╚██╗ ██╔╝██╔══██╗██║  ██║    ██╔══██╗     ██║
██║  ███╗██║   ╚████╔╝ ██████╔╝███████║    ███████║     ██║
██║   ██║██║    ╚██╔╝  ██╔═══╝ ██╔══██║    ██╔══██║██   ██║
╚██████╔╝███████╗██║   ██║     ██║  ██║    ██║  ██║╚█████╔╝
 ╚═════╝ ╚══════╝╚═╝   ╚═╝     ╚═╝  ╚═╝    ╚═╝  ╚═╝ ╚════╝ 
                                                          
    """
    
    sys.stdout.write(RED + FISHKISS_ASCII + RESET)
    print()

def minimize_terminal():
    if os.name == 'nt':
        windows = gw.getWindowsWithTitle("Command")
        if not windows:
            windows = gw.getWindowsWithTitle("Python")
        if windows:
            window = windows[0]
            window.minimize()
            time.sleep(1)
        else:
            print("No terminal window found with the expected title.")
    else:
        print("Terminal minimization is not implemented for this platform.")

def main():
    global exit_flag

    try:
        set_window_title("Python")
        
        clear_screen()
        typing_animation("Do you want to enable the macro? [Yes/No]", speed=0.05)

        while not exit_flag:
            user_input = input().strip().lower()

            if user_input == "yes":
                clear_screen()
                print("Macro Enabled")
                print_red_ascii_art()

                pyautogui.click()
                control_mouse()

                minimize_terminal()
                break

            elif user_input == "no":
                clear_screen()
                print("Macro Disabled")
                exit_flag = True
                break

            else:
                print("Invalid input. Please type 'Yes' or 'No'.")
        
        if exit_flag:
            print("Exiting program...")
            sys.exit()

    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit(1)

if __name__ == "__main__":
    def keep_window_title():
        while True:
            set_window_title("Python")
            time.sleep(1)

    title_thread = threading.Thread(target=keep_window_title, daemon=True)
    title_thread.start()

    main()
