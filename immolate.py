from enum import Enum
import pyautogui
import keyboard
from include import winocr
import pyperclip
import numpy as np
from PIL import Image, ImageFilter, ImageEnhance
from difflib import SequenceMatcher
import time
from dataclasses import dataclass

# This is what stores all of the variables and info required by programs using Immolate.
version = "v0.03"

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

def move(pos):
    checkForExit()
    pyautogui.moveTo(pos[0], pos[1])

def reset():
    click(inGame.optionsButton);
    click(quickOptions.newRunButton);
    click(gameSelect.playButton);
    time.sleep(2.25);

def printSeed():
    click(inGame.optionsButton)
    click(quickOptions.copySeedButton)
    print(pyperclip.paste())

def printSeedToFile(filename):
    printSeed()
    try:
        # Check if the file exists
        with open(filename, 'a') as file:
            # Append the text to the file
            file.write(pyperclip.paste() + '\n')
    except FileNotFoundError:
        # If the file doesn't exist, create it and write the text
        with open(filename, 'w') as file:
            file.write(pyperclip.paste() + '\n')

def readText(box):
    # Takes screenshot, makes it larger, runs OCR
    img = pyautogui.screenshot(region=(box[0],box[1],box[2]-box[0],box[3]-box[1]))
    width, height = img.size
    img = img.resize((width*3, height*3), resample=Image.NEAREST).filter(ImageFilter.SHARPEN);
    img = ImageEnhance.Contrast(img).enhance(1.5)
    return winocr.recognize_pil_sync(img, 'en')['text']

def readLine(box):
    # Takes screenshot, makes it larger, runs OCR
    # This one only returns the first line
    img = pyautogui.screenshot(region=(box[0],box[1],box[2]-box[0],box[3]-box[1]))
    width, height = img.size
    img = img.resize((width*3, height*3), resample=Image.NEAREST).filter(ImageFilter.SHARPEN);
    img = ImageEnhance.Contrast(img).enhance(1.5)
    try:
        result = winocr.recognize_pil_sync(img, 'en')['lines'][0]['text']
    except:
        result = ""
    return result

def readLastLine(box):
    # Takes screenshot, makes it larger, runs OCR
    # This one only returns the last line
    img = pyautogui.screenshot(region=(box[0],box[1],box[2]-box[0],box[3]-box[1]))
    width, height = img.size
    img = img.resize((width*3, height*3), resample=Image.NEAREST).filter(ImageFilter.SHARPEN);
    img = ImageEnhance.Contrast(img).enhance(1.5)
    try:
        result = winocr.recognize_pil_sync(img, 'en')['lines'][-1]['text']
    except:
        result = ""
    return result

def screenshot(box):
    # Takes screenshot of a certain box
    return pyautogui.screenshot(region=(box[0],box[1],box[2]-box[0],box[3]-box[1]))

def readTextNoEdits(box):
    # Takes screenshot, makes it larger, runs OCR
    # This one only returns the first line
    img = pyautogui.screenshot(region=(box[0],box[1],box[2]-box[0],box[3]-box[1]))
    try:
        result = winocr.recognize_pil_sync(img, 'en')['text']
    except:
        result = ""
    return result

def readLineNoEdits(box):
    # Takes screenshot, makes it larger, runs OCR
    # This one only returns the first line
    img = pyautogui.screenshot(region=(box[0],box[1],box[2]-box[0],box[3]-box[1]))
    try:
        result = winocr.recognize_pil_sync(img, 'en')['lines'][0]['text']
    except:
        result = ""
    return result

def readLastLineNoEdits(box):
    # Takes screenshot, makes it larger, runs OCR
    # This one only returns the last line
    img = pyautogui.screenshot(region=(box[0],box[1],box[2]-box[0],box[3]-box[1]))
    try:
        result = winocr.recognize_pil_sync(img, 'en')['lines'][-1]['text']
    except:
        result = ""
    return result

def readTextNoEditsFromScreenshot(img):
    try:
        result = winocr.recognize_pil_sync(img, 'en')['text']
    except:
        result = ""
    return result

def readLineNoEditsFromScreenshot(img):
    try:
        result = winocr.recognize_pil_sync(img, 'en')['lines'][0]['text']
    except:
        result = ""
    return result


def readLastLineNoEditsFromScreenshot(img):
    try:
        result = winocr.recognize_pil_sync(img, 'en')['lines'][-1]['text']
    except:
        result = ""
    return result

# Finds the closest value in an Enum of things (jokers, spectral cards, etc.) to a string
# Can be used to overcome the inaccuracy of OCR
def closestValue(enum, string):
    similarEnum = None
    maxSimilarity = 0.0

    for element in enum:
        similarity = SequenceMatcher(None, string, element.value).ratio()
        if similarity > maxSimilarity:
            maxSimilarity = similarity
            similarEnum = element
    if maxSimilarity < 0.5:
        return None #probably nothing
    return similarEnum

# Finds the closest value out of all 52 playing cards
# Can be used to overcome the inaccuracy of OCR
def closestCard(string):
    similarEnum = None
    maxSimilarity = 0.0

    for element in allCards:
        similarity = SequenceMatcher(None, string, element.value()).ratio()
        if similarity > maxSimilarity:
            maxSimilarity = similarity
            similarEnum = element
    
    return similarEnum


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

class settings:
    class game:
        increaseGameSpeedButton = (1076, 349)
        decreaseGameSpeedButton = (849, 345)

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
    
class boosterPackMenu:
    packPosition = {
        2: [(968, 842), (1146, 841)],
        5: [(641, 841), (852, 837), (1061, 835), (1271, 839), (1471, 831)]
    }
    packDescription = {
        2: [(867, 366, 1063, 500), (1056, 366, 1244, 500)],
        5: [(558, 366, 732, 500), (765, 366, 935, 500), (966, 366, 1152, 500),
         (1176, 366, 1352, 500), (1378, 366, 1563, 500)]
    }
    # Eventually these will probably just be the regular card positions shifted upwards
    cardPosition = {
        8: [(582, 459), (719, 460), (854, 441), (944, 430), (1110, 449),
            (1217, 468), (1378, 472), (1504, 489)]
    }
    cardDescription = {
        8: [(521, 144, 724, 350), (651, 144, 838, 350), (766, 144, 973, 350),
            (902, 144, 1901, 350), (1020, 144, 1219, 350), (1149, 144, 1340, 350),
            (1267, 144, 1469, 350), (1394, 144, 1583, 350)]
    }
    skipButton = (1057, 1006)

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
    ARCANA = "Arcana Pack", 3, Tarot
    JUMBO_ARCANA = "Jumbo Arcana Pack", 4, Tarot
    MEGA_ARCANA = "Mega Arcana Pack", 5, Tarot
    CELESTIAL = "Celestial Pack", 3, Planet
    JUMBO_CELESTIAL = "Jumbo Celestial Pack", 4, Planet
    MEGA_CELESTIAL = "Mega Celestial Pack", 5, Planet
    SPECTRAL = "Spectral Pack", 2, Spectral
    JUMBO_SPECTRAL = "Jumbo Spectral Pack", 3, Spectral
    MEGA_SPECTRAL = "Mega Spectral Pack", 4, Spectral

    # Kudos to https://stackoverflow.com/questions/12680080/python-enums-with-attributes
    def __new__(cls, *args, **kwds):
        obj = object.__new__(cls)
        obj._value_ = args[0]
        return obj

    def __init__(self, _: str, numCards: int = None, cardType: Enum = None):
        self._numCards_ = numCards
        self._cardType_ = cardType
        
    @property
    def numCards(self):
        return self._numCards_
    
    @property
    def cardType(self):
        return self._cardType_

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
    CHARM = "Gives a free Mega Arcana Pack", BoosterPack.MEGA_ARCANA
    METEOR = "Gives a free Mega Celestial Pack", BoosterPack.MEGA_CELESTIAL
    ENHANCED = "Enhanced card in the shop"
    HANDY = "Start round with an extra 3 Hands"
    GARBAGE = "Start round with an extra 3 Discards"
    ETHEREAL = "Gives a free Spectral Pack", BoosterPack.SPECTRAL

    # Kudos to https://stackoverflow.com/questions/12680080/python-enums-with-attributes
    def __new__(cls, *args, **kwds):
        obj = object.__new__(cls)
        obj._value_ = args[0]
        return obj

    def __init__(self, _: str, associatedPack: BoosterPack = None):
        self._associatedPack_ = associatedPack
        
    @property
    def associatedPack(self):
        return self._associatedPack_

class Edition(Enum):
    BASE = ""
    FOIL = "Foil"
    HOLOGRAPHIC = "Holographic"
    POLYCHROME = "Polychrome"
    NEGATIVE = "Negative"

class Suit(Enum):
    CLUBS = "Clubs"
    DIAMONDS = "Diamonds"
    HEARTS = "Hearts"
    SPADES = "Spades"

class Rank(Enum):
    ACE = "Ace"
    KING = "King"
    QUEEN = "Queen"
    JACK = "Jack"
    TEN = "10"
    # Why this weird ordering? If a single-digit rank isn't being recognized by OCR, it's usually 4
    FOUR = "4"
    NINE = "9"
    EIGHT = "8"
    SEVEN = "7"
    SIX = "6"
    FIVE = "5"
    THREE = "3"
    TWO = "2"

@dataclass
class Card:
    rank: Rank
    suit: Suit

    def value(self):
        return f"{self.rank.value} of {self.suit.value}"

# Precomputed variables
allCards = [Card(r, s) for r in Rank for s in Suit]