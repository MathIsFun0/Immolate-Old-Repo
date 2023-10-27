from enum import Enum
import pyautogui
import keyboard
import pytesseract
import pyperclip
import numpy as np
from PIL import Image, ImageFilter
import time

# This is what stores all of the variables and info required by programs using Immolate.
version = "v0.01"

class options:
    exitKeyCombination = "ctrl+c"

# Helper functions for basic actions

# Helper Functions
def checkForExit():
    if keyboard.is_pressed("ctrl+c"):
        exit(0)

def click(pos):
    checkForExit()
    pyautogui.moveTo(pos[0], pos[1])
    time.sleep(0.05);
    pyautogui.click()

def reset():
    click(inGame.optionsButton);
    click(quickOptions.newRunButton);
    click(gameSelect.playButton);
    time.sleep(2.25);

def printSeed():
    click(inGame.optionsButton)
    click(quickOptions.copySeedButton)
    print(pyperclip.paste())

def readText(box):
    # Takes screenshot, makes it larger, runs OCR
    img = pyautogui.screenshot(region=(box[0],box[1],box[2]-box[0],box[3]-box[1]))
    width, height = img.size
    img = img.resize((width*3, height*3), resample=Image.NEAREST).filter(ImageFilter.SHARPEN);
    img = np.array(img)
    return pytesseract.image_to_string(img)


# Coordinates of buttons and bounding boxes of text
class mainMenu:
    playButton = (553, 911)
    optionsButton = (845, 907)
    quitButton = (1073, 907)
    collectionButton = (1357, 904)

class quickOptions:
    settingsButton = (965, 280)
    copySeedButton = (1080, 364)
    newRunButton = (963, 452)
    mainMenuButton = (958, 558)
    statsButton = (952, 632)
    collectionButton = (959, 726)
    backButton = (942, 824)

class gameSelect:
    newRunButton = (737, 135)
    pasteSeedButton = (1064, 774)
    seededRunButton = (722, 858)
    playButton = (958, 855)
    backButton = (951, 943)

class inGame: #General gameplay loop
    runInfoButton = (154, 747)
    optionsButton = (148, 918)
    playHandButton = (831, 989)
    discardButton = (1271, 946)

class blindMenu:
    smallBlindPlayButton = (725, 394)
    smallBlindSkipButton = (728, 781)
    bigBlindPlayButton = (1054, 387)
    bigBlindSkipButton = (1066, 800)
    bossBlindPlayButton = (1392, 394)
    tag1_selectedBox = (690, 835, 840, 911)
    tag2_deselectedBox = (1021, 925, 1172, 1000)
    tag2_selectedBox = (1024, 839, 1171, 911)

# Names or descriptions of things
class Joker(Enum):
    JOKER = "Joker"
    ZANY = "Zany Joker"
    MAD = "Mad Joker"
    CRAZY = "Crazy Joker"
    DROLL = "Droll Joker"
    HALF = "Half Joker"
    ICE_CREAM = "Ice Cream"
    JUGGLER = "Juggler"
    RUNNER = "Runner"
    GOLDEN = "Golden Joker"
    STENCIL = "Joker Stencil"
    FOUR_FINGERS = "Four Fingers"
    CEREMONIAL_DAGGER = "Ceremonial Dagger"
    BANNER = "Banner"
    MARBLE = "Marble Joker"
    LOYALTY_CARD = "Loyalty Card"
    EIGHT_BALL = "8 Ball"
    MISPRINT = "Misprint"
    BLUEPRINT = "Blueprint"
    RAISED_FIST = "Raised Fist"
    FIBONACCI = "Fibonacci"
    CARTOMANCER = "Cartomancer"
    ASTRONOMER = "Astronomer"
    ABSTRACT = "Abstract Joker"
    DELAYED_GRATIFICATION = "Delayed Gratification"
    GROS_MICHEL = "Gros Michel"
    EVEN_STEVEN = "Even Steven"
    ODD_TODD = "Odd Todd"
    SCHOLAR = "Scholar"
    BUSINESS_CARD = "Business Card"
    SUPERNOVA = "Supernova"
    RIDE_THE_BUS = "Ride the Bus"
    BLACKBOARD = "Blackboard"
    EGG = "Egg"
    BURGLAR = "Burglar"
    SCARY_FACE = "Scary Face"
    MYSTIC_SUMMIT = "Mystic Summit"
    DUSK = "Dusk"
    DNA = "DNA"
    SPLASH = "Splash"
    SMEARED = "Smeared Joker"
    CONSTELLATION = "Constellation"
    HIKER = "Hiker"
    SUPERPOSITION = "Superposition"
    TO_DO_LIST = "To Do List"


class Tarot(Enum):
    FOOL = "The Fool"
    MAGICIAN = "The Magician"
    HIGH_PRIESTESS = "The High Priestess"
    EMPRESS = "The Empress"
    EMPEROR = "The Emperor"
    HIEROPHANT = "The Hierophant"
    LOVERS = "The Lovers"
    CHARIOT = "The Chariot"
    JUSTICE = "Justice"
    HERMIT = "The Hermit"
    WHEEL_OF_FORTUNE = "The Wheel of Fortune"
    STRENGTH = "Strength"
    HANGED_MAN = "The Hanged Man"
    DEATH = "Death"
    TEMPERANCE = "Temperance"
    DEVIL = "The Devil"
    TOWER = "The Tower"
    STAR = "The Star"
    MOON = "The Moon"
    SUN = "The Sun"
    JUDGEMENT = "Judgement"
    WORLD = "The World"

class Planet(Enum):
    MERCURY = "Mercury"
    VENUS = "Venus"
    EARTH = "Earth"
    MARS = "Mars"
    JUPITER = "Jupiter"
    SATURN = "Saturn"
    URANUS = "Uranus"
    NEPTUNE = "Neptune"
    PLUTO = "Pluto"
    PLANET_X = "Planet X"
    CERES = "Ceres"

class Spectral(Enum):
    FAMILIAR = "Familiar"
    GRIM = "Grim"
    INCANTATION = "Incantation"
    TALISMAN = "Talisman"
    AURA = "Aura"
    WRAITH = "Wraith"
    SIGIL = "Sigil"
    OUIJA = "Ouija"
    ECTOPLASM = "Ectoplasm"
    IMMOLATE = "Immolate"

class BoosterPack(Enum):
    ARCANA = "Arcana Pack"
    JUMBO_ARCANA = "Jumbo Arcana Pack"
    MEGA_ARCANA = "Mega Arcana Pack"
    CELESTIAL = "Celestial Pack"
    JUMBO_CELESTIAL = "Jumbo Celestial Pack"
    MEGA_CELESTIAL = "Mega Celestial Pack"
    SPECTRAL = "Spectral Pack"
    JUMBO_SPECTRAL = "Jumbo Spectral Pack"
    MEGA_SPECTRAL = "Mega Spectral Pack"

class Tag(Enum):
    UNCOMMON = "Shop has an Uncommon Joker"
    RARE = "1 in 3 chance for shop to have a Rare Joker"
    NEGATIVE = "1 in 5 chance for shop to have a Negative Joker"
    FOIL = "1 in 2 chance for shop to have a Foil Joker"
    HOLOGRAPHIC = "1 in 3 chance for shop to have a Holographic Joker"
    POLYCHROME = "1 in 4 chance for shop to have a Polychrome Joker"
    INVESTMENT = "After defeating the Boss Blind, gain $15"
    VOUCHER = "Adds one Voucher to the next shop"
    BOSS = "Rerolls the Boss Blind"
    GOLD_SEAL = "Gold Seal card in the shop"
    CHARM = "Gives a free Mega Arcana Pack"
    METEOR = "Gives a free Mega Celestial Pack"
    ENHANCED = "Enhanced card in the shop"
    HANDY = "Start round with an extra 3 Hands"
    GARBAGE = "Start round with an extra 3 Discards"
    ETHEREAL = "Gives a free Spectral Pack"