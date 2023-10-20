# This script assumes that you are playing fullscreen 1920x1080 with no CRT effect.
import pyautogui
import keyboard
import pytesseract
import pyperclip
import cv2
import numpy as np
from PIL import Image, ImageFilter
from difflib import SequenceMatcher
import time


# User-modifiable variables
getMouseCoords = False # For getting new coords for buttons/cards
pyautogui.PAUSE = 0.05 # Time between actions

pytesseract.pytesseract.tesseract_cmd = "C:/Program Files/Tesseract-OCR/tesseract.exe" # Install location of tesseract, for reading text

# Variables for locations and information

# Program version
immolateVersion = "v0.01"

# Buttons - currently partially implemented
mainMenu_playBtn = (553, 911)

options_startNewRunBtn = (963, 452)
options_copySeedBtn = (1080, 364)
gameSelect_newRunBtn = (737, 135)
gameSelect_playBtn = (958, 855)
gameSelect_seededRunBtn = (722, 858)
gameSelect_pasteSeedBtn = (1064, 774)

inGame_optionsBtn = (148, 918)
inGame_playHandBtn = (831, 989)
inGame_discardBtn = (1271, 946)
blindMenu_smallBlindPlayBtn = (725, 394)
blindMenu_smallBlindSkipBtn = (728, 781)
blindMenu_bigBlindPlayBtn = (1054, 387)
blindMenu_bigBlindSkipBtn = (1066, 800)
blindMenu_bossPlayBtn = (1392, 394)
blindMenu_tag1_selectedBox = (690, 835, 840-690, 911-835)
blindMenu_tag2_deselectedBox = (1021, 925, 1172-1021, 1000-925)

# Strings for Tags
desc_uncommonTag = "Shop has an Uncommon Joker"
desc_rareTag = "1 in 3 chance for shop to have a Rare Joker"
desc_negativeTag = "1 in 5 chance for shop to have a Negative Joker"
desc_foilTag = "1 in 2 chance for shop to have a Foil Joker"
desc_holographicTag = "1 in 3 chance for shop to have a Holographic Joker"
desc_polychromeTag = "1 in 4 chance for shop to have a Polychrome Joker"
desc_investmentTag = "After defeating the Boss Blind, gain $15"
desc_voucherTag = "Adds one Voucher to the next shop"
desc_bossTag = "Rerolls the Boss Blind"
desc_goldSealTag = "Gold Seal card in the shop"
desc_charmTag = "Gives a free Mega Arcana Pack"
desc_meteorTag = "Gives a free Mega Celestial Pack"
desc_enhancedTag = "Enhanced card in the shop"
desc_handyTag = "Start round with an extra 3 Hands"
desc_garbageTag = "Start round with an extra 3 Discards"
desc_etherealTag = "Gives a free Spectral Pack"

# Helper Functions
def check_for_ctrl_c():
    if keyboard.is_pressed("ctrl+c"):
        exit(0)

def click(pos):
    check_for_ctrl_c()
    pyautogui.moveTo(pos[0], pos[1])
    time.sleep(0.05);
    pyautogui.click()

def reset():
    click(inGame_optionsBtn);
    click(options_startNewRunBtn);
    click(gameSelect_playBtn);
    time.sleep(2.25);

def print_seed():
    click(inGame_optionsBtn)
    click(options_copySeedBtn)
    print(pyperclip.paste())

def readText(box):
    # Takes screenshot, makes it larger, runs OCR
    img = pyautogui.screenshot(region=box)
    width, height = img.size
    img = img.resize((width*3, height*3), resample=Image.NEAREST).filter(ImageFilter.SHARPEN);
    img = np.array(img)
    return pytesseract.image_to_string(img)

def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()

if getMouseCoords:
    print("Immolate " + immolateVersion);
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
    print("Immolate " + immolateVersion);
    print("Hold Ctrl+C to exit...")
    time.sleep(5)
    while True:
        reset()
        time.sleep(0.4) # Wait for animation
        tag1 = readText(blindMenu_tag1_selectedBox).replace("\n"," ")
        tag2 = readText(blindMenu_tag2_deselectedBox).replace("\n"," ")
        if max(similar(tag1, desc_etherealTag),similar(tag2, desc_etherealTag))>0.75:
            print_seed()