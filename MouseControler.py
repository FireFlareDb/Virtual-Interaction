import pyautogui

def getScreenSize():
    widht, heigh = pyautogui.size()
    return widht, heigh

def moveCursor(x, y):
    pyautogui.moveTo(x, y)

def click():
    pyautogui.click()