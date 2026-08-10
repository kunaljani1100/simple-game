import pyautogui
import subprocess

# print(pyautogui.position())
# pyautogui.moveTo(500, 300)
# pyautogui.click(100, 100, 2)

script = '''
    tell application "System Events"
        repeat with p in application processes
            try
                repeat with w in windows of p
                    if name of w is "Maze Game" then
                        perform action "AXRaise" of w
                        set frontmost of p to true
                        return
                    end if
                end repeat
            end try
        end repeat
    end tell
    '''

subprocess.run(["osascript", "-e", script], check = True)
while True:
    pyautogui.press("down")