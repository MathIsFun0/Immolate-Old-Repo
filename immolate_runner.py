# This script assumes that you are playing fullscreen 1920x1080 with no CRT effect.
import immolate as im
from difflib import SequenceMatcher
import pyautogui, keyboard, time

# User-modifiable variables
getMouseCoords = False # For getting new coords for buttons/cards
pyautogui.PAUSE = 0.05 # Time between actions

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
    # This current demo reads out all the basic information gathered from skips in Ante 1
    # It also prints each seed that it finds
    print("Immolate " + im.version);
    print("Hold Ctrl+C to exit...")
    time.sleep(5)
    while (True):
        print("------------------")
        im.reset()
        time.sleep(0.4) # Wait for text to appear
        tag1 = im.closestValue(im.Tag, im.readText(im.blindMenu.tag1_selectedBox).replace("\n"," "))
        tag2 = im.closestValue(im.Tag, im.readText(im.blindMenu.tag2_deselectedBox).replace("\n"," "))
        print(tag1)
        if tag1 != None and tag1.associatedPack != None:
            im.click(im.blindMenu.smallBlindSkipButton)
            pack = tag1.associatedPack
            time.sleep(3) # Wait for opening animation
            for i in range(pack.numCards):
                im.move(im.boosterPackMenu.packPosition[pack.numCards][i])
                time.sleep(0.3) # Wait for text display animation
                print(im.closestValue(pack.cardType, im.readLine(im.boosterPackMenu.packDescription[pack.numCards][i])))
            if tag2 != None and tag2.associatedPack != None:
                im.click(im.boosterPackMenu.skipButton)
                time.sleep(0.5) # Another delay to prevent bugs
        elif tag2 != None and tag2.associatedPack != None: 
            im.click(im.blindMenu.smallBlindSkipButton)
        if tag1 == im.Tag.BOSS:
            time.sleep(1) # Wait for reroll animation
        print(tag2)
        if tag2 != None and tag2.associatedPack != None:
            pack = tag2.associatedPack
            im.click(im.blindMenu.bigBlindSkipButton)
            time.sleep(3) # Wait for opening animation
            for i in range(pack.numCards):
                im.move(im.boosterPackMenu.packPosition[pack.numCards][i])
                time.sleep(0.3) # Wait for text display animation
                print(im.closestValue(pack.cardType, im.readLine(im.boosterPackMenu.packDescription[pack.numCards][i])))
        im.printSeed()