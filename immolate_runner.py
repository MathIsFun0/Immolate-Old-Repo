# This script assumes that you are playing fullscreen 1920x1080 with no CRT effect.
import immolate as im
from difflib import SequenceMatcher
import pyautogui, keyboard, time

polySeed = False
retrySeed = False
# User-modifiable variables
getMouseCoords = False # For getting new coords for buttons/cards
pyautogui.PAUSE = 0.05 # Time between actions
fileName = "polychromeAuraSeeds.txt"

def printToFile(filename, text):
    print(text)
    try:
        # Check if the file exists
        with open(filename, 'a') as file:
            # Append the text to the file
            file.write(text + '\n')
    except FileNotFoundError:
        # If the file doesn't exist, create it and write the text
        with open(filename, 'w') as file:
            file.write(text + '\n')

if getMouseCoords:
    print("Immolate " + im.version);
    print("Press Ctrl+X to capture cursor position...")
    while (True):
        keyboard.wait('ctrl+x')  # Wait for Ctrl+X to be pressed
        # Get the current mouse cursor position
        mouse_x, mouse_y = pyautogui.position()
        # Display the cursor position
        print(f"Cursor position: X={mouse_x}, Y={mouse_y}")

def detect_aura_value(packPos):
    global polySeed
    # Extra delays for consistency
    im.click(im.inGame.optionsButton)
    time.sleep(0.05)
    im.click(im.quickOptions.settingsButton)
    time.sleep(0.05)
    im.click(im.settings.game.decreaseGameSpeedButton)
    time.sleep(0.05)
    im.click(im.settings.game.decreaseGameSpeedButton)
    time.sleep(0.05)
    keyboard.press("esc")
    time.sleep(0.05)
    keyboard.release("esc")
    time.sleep(0.05)
    im.click(im.boosterPackMenu.packPosition[2][packPos])
    im.click(im.boosterPackMenu.packPosition[2][packPos])
    time.sleep(2)
    cards = 8 * [None]
    for i in range(8):
        im.move(im.boosterPackMenu.cardPosition[8][i])
        cards[i] = im.screenshot(im.boosterPackMenu.cardDescription[8][i])
    for i in range(8):
        line = im.readLastLineNoEditsFromScreenshot(cards[i])
        edition = im.closestValue(im.Edition, line)
        if edition == im.Edition.POLYCHROME:
            card = im.closestCard(im.readLineNoEditsFromScreenshot(cards[i]))
            printToFile(fileName, edition.value+" "+card.value())
            polySeed = True
        if edition == None:
            polySeed = True
    # Extra delays for consistency
    im.click(im.inGame.optionsButton)
    time.sleep(0.05)
    im.click(im.quickOptions.settingsButton)
    time.sleep(0.05)
    im.click(im.settings.game.increaseGameSpeedButton)
    time.sleep(0.05)
    im.click(im.settings.game.increaseGameSpeedButton)
    time.sleep(0.05)
    keyboard.press("esc")
    time.sleep(0.05)
    keyboard.release("esc")

if __name__ == "__main__":
    # This current demo reads out all the basic information gathered from skips in Ante 1
    # It also prints each seed that it finds
    # Example aura: 6WNHV6QC
    print("Immolate " + im.version);
    print("Hold Ctrl+C to exit...")
    time.sleep(5)
    while True:
        polySeed = False
        retrySeed = False
        time.sleep(0.4) # Wait for text to appear
        tag1 = im.closestValue(im.Tag, im.readText(im.blindMenu.tag1_selectedBox).replace("\n"," "))
        tag2 = im.closestValue(im.Tag, im.readText(im.blindMenu.tag2_deselectedBox).replace("\n"," "))
        if tag1 == im.Tag.ETHEREAL:
            im.click(im.blindMenu.smallBlindSkipButton)
            pack = tag1.associatedPack
            time.sleep(3) # Wait for opening animation
            for i in range(pack.numCards):
                im.move(im.boosterPackMenu.packPosition[pack.numCards][i])
                time.sleep(0.3) # Wait for text display animation
                closestCard = im.closestValue(pack.cardType, im.readLine(im.boosterPackMenu.packDescription[pack.numCards][i]))
                if (closestCard == im.Spectral.AURA): detect_aura_value(i)
            if tag2 == im.Tag.ETHEREAL:
                im.click(im.boosterPackMenu.skipButton)
                time.sleep(0.5) # Another delay to prevent bugs
        elif tag2 == im.Tag.ETHEREAL: 
            im.click(im.blindMenu.smallBlindSkipButton)
        if tag1 == im.Tag.BOSS:
            time.sleep(1) # Wait for reroll animation
        if tag2 == im.Tag.ETHEREAL:
            pack = tag2.associatedPack
            im.click(im.blindMenu.bigBlindSkipButton)
            time.sleep(3) # Wait for opening animation
            for i in range(pack.numCards):
                im.move(im.boosterPackMenu.packPosition[pack.numCards][i])
                time.sleep(0.3) # Wait for text display animation
                closestCard = im.closestValue(pack.cardType, im.readLine(im.boosterPackMenu.packDescription[pack.numCards][i]))
                if (closestCard == im.Spectral.AURA): detect_aura_value(i)
        if polySeed:
            im.printSeedToFile(fileName)
            printToFile(fileName, "---------")
        # In case Immolate gets stuck in settings menu...
        keyboard.press("esc")
        keyboard.release("esc")
        im.reset()