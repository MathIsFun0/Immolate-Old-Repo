# This script assumes that you are playing fullscreen 1920x1080 with no CRT effect.
import immolate as im
from difflib import SequenceMatcher
import pyautogui, pytesseract, keyboard, time

# User-modifiable variables
getMouseCoords = False # For getting new coords for buttons/cards
pyautogui.PAUSE = 0.05 # Time between actions
pytesseract.pytesseract.tesseract_cmd = "C:/Program Files/Tesseract-OCR/tesseract.exe" # Install location of tesseract, for reading text

def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()

if getMouseCoords:
    print("Immolate " + im.version);
    print("Press Ctrl+X to capture cursor position...")
    while (True):
        keyboard.wait('ctrl+x')  # Wait for Ctrl+X to be pressed
        # Get the current mouse cursor position
        mouse_x, mouse_y = pyautogui.position()
        # Display the cursor position
        print(f"Cursor position: X={mouse_x}, Y={mouse_y}")


if __name__ == "__main__":
    # Here's some code to find seeds with at least 1 Spectral Pack
    # This would be useful for SS searches
    print("Immolate " + im.version);
    print("Hold Ctrl+C to exit...")
    time.sleep(5)
    while True:
        im.reset()
        time.sleep(0.4) # Wait for animation
        tag1 = im.readText(im.blindMenu.tag1_selectedBox).replace("\n"," ")
        tag2 = im.readText(im.blindMenu.tag2_deselectedBox).replace("\n"," ")
        if max(similar(tag1, im.Tag.ETHEREAL.value),similar(tag2, im.Tag.ETHEREAL.value))>0.75:
            im.printSeed()