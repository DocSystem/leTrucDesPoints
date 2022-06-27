"""
Python Binary to PDP Generator

Originaly written by: Paul ZANOLIN
Edited by: Antoine SOUBEN-FINK
"""

from PIL import Image, ImageDraw
from random import randint, seed
import json
import logging

# =============    LOGGING CONFIGURATION    =============
class LoggingColorFormatter(logging.Formatter):
    grey = "\x1b[38;20m"
    yellow = "\x1b[33;20m"
    red = "\x1b[31;20m"
    bold_red = "\x1b[31;1m"
    reset = "\x1b[0m"
    format = "[%(levelname)s] %(message)s"
    FORMATS = {
        logging.DEBUG: grey + format + reset,
        logging.INFO: grey + format + reset,
        logging.WARNING: yellow + format + reset,
        logging.ERROR: red + format + reset,
        logging.CRITICAL: bold_red + format + reset
    }
    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
lch = logging.StreamHandler()
lch.setFormatter(LoggingColorFormatter())
logger.addHandler(lch)
# ============== END LOGGING CONFIGURATION ==============

with open("config.json", "r", encoding="utf-8") as f:
    config = json.load(f)

# =============      CONFIG      =============

MOT = config["mot"]
COLORS = {}
for c in config["colors"]:
    COLORS[c] = tuple(config["colors"][c])
LINES_COLORS = config["lines_colors"]
SHADOW_COLOR = tuple(config["shadow_color"])
lines = config["lines"]
drawLines = config["drawLines"]
drawShadows = config["drawShadows"]
randomLines = config["randomLines"]
testMode = config["testMode"]
liveLineMode = config["liveLineMode"]
psychedelicMode = config["psychedelicMode"]
seed(config["randomSeed"])

# =============    END CONFIG    =============

# =============    DATA VERIF    =============
if (len(MOT) != 8):
    logger.error("Le mot doit contenir exactement 8 caractères.")
    exit()
if (len(LINES_COLORS) != 8):
    logger.error("Le nombre de couleurs de lignes doit être égal à 8.")
    exit()
if drawShadows:
    logger.warning("Les ombres sont encore une fonctionnalité expérimentale.")
if randomLines:
    logger.info("Génération aléatoire des lignes activées !")
    logger.info("Seed utilisée : " + str(config["randomSeed"]))
# =============  END DATA VERIF  =============

data = []
for i in range(len(MOT)):
    data.append(format(ord(MOT[i]), '08b') + LINES_COLORS[i])

if randomLines:
    lines = []
    points = [[0 for _ in range(8)] for _ in range(8)]
    for i in range(8):
        for j in range(8):
            if data[i][j] == "1":
                points[i][j] = 0
            else:
                points[i][j] = 1
    for i in range(8):
        for j in range(8):
            if points[i][j] == 1:
                if i < 7 and j < 7:
                    if points[i+1][j] == 1 and points[i][j+1] == 1 and points[i+1][j+1] == 1 and LINES_COLORS[i] == LINES_COLORS[i+1] and randint(0, 1) == 0:
                        lines.append(str(i+1) + str(j) + str(i) + str(j+1) + LINES_COLORS[i])
                        lines.append(str(i) + str(j) + str(i+1) + str(j+1) + LINES_COLORS[i])
                    elif points[i+1][j] == 1 and points[i][j+1] == 1 and LINES_COLORS[i] == LINES_COLORS[i+1] and randint(0, 1) == 0:
                        lines.append(str(i) + str(j) + str(i) + str(j+1) + LINES_COLORS[i])
                        lines.append(str(i) + str(j) + str(i+1) + str(j) + LINES_COLORS[i])
                    elif points[i+1][j] == 1 and LINES_COLORS[i] == LINES_COLORS[i+1] and (not (str(i) + str(j-1) + str(i+1) + str(j) + LINES_COLORS[i]) in lines) and randint(0, 1) == 0:
                        lines.append(str(i) + str(j) + str(i+1) + str(j) + LINES_COLORS[i])
                    elif points[i][j+1] == 1 and (not (str(i) + str(j-1) + str(i+1) + str(j) + LINES_COLORS[i]) in lines) and randint(0, 1) == 0:
                        lines.append(str(i) + str(j) + str(i) + str(j+1) + LINES_COLORS[i])

def drawImage():
    # for test purpose
    if testMode:
        im = Image.open("baseTest.png")
    else:
        im = Image.open("base.png")

    im = im.transpose(Image.FLIP_TOP_BOTTOM)
    im = im.rotate(-90)

    d = ImageDraw.Draw(im)

    borderL = 33

    if drawLines and drawShadows:
        for line in lines:
            color = COLORS[line[4]]
            d.line([(330 + int(line[0]) * 200, 330 + int(line[1]) * 200),
                    (330 + int(line[2]) * 200, 330 + int(line[3]) * 200)], SHADOW_COLOR, 230 - 2 * borderL)

    for i in range(8):
        color = COLORS[data[i][8]]
        for j in range(8):
            if data[i][j] == "0":

                if drawShadows:
                    for f in range(25):
                        cornerTLeft = (246 + 200 * i + borderL + f * 8, 246 + 200 * j + borderL + f * 8)
                        # topLeft (border + espacement * numcolone + borderL+ un peu plus pour remplir le cercle)
                        cornerBRight = (446 + 200 * i - borderL - f * 8, 446 + 200 * j - borderL - f * 8)
                        # bottomRight
                        d.arc([cornerTLeft, cornerBRight], 0, 360, SHADOW_COLOR, 10)

                # full the circle
                for f in range(25):
                    cornerTLeft = (200 + 200 * i + borderL + f * 8, 200 + 200 * j + borderL + f * 8)
                    # topLeft (border + espacement * numcolone + borderL+ un peu plus pour remplir le cercle)
                    cornerBRight = (400 + 200 * i - borderL - f * 8, 400 + 200 * j - borderL - f * 8)
                    # bottomRight
                    d.arc([cornerTLeft, cornerBRight], 0, 360, color, 10)
                    if psychedelicMode:
                        d.arc([cornerTLeft, cornerBRight], 0, 360, SHADOW_COLOR, 10 - f)

    if drawLines:
        for line in lines:
            color = COLORS[line[4]]
            d.line([(300 + int(line[0]) * 200, 300 + int(line[1]) * 200),
                    (300 + int(line[2]) * 200, 300 + int(line[3]) * 200)], color, 200 - 2 * borderL)

    im = im.rotate(90)
    im = im.transpose(Image.FLIP_TOP_BOTTOM)
    #im.show()
    im.save("end.png")

if liveLineMode:
    logger.info("Add new lines by typing coords of the first point and the second point. For example, '0001' will add a line between the first and the second point of the first column.")
    logger.info("To remove a line, just type it again.")
    logger.info("Type 'q' to finish")
    newLine = ""
    testMode = True
    while newLine != "q":
        drawImage()
        newLine = input()
        if newLine != "q":
            if len(newLine) == 4:
                nl = newLine + LINES_COLORS[int(newLine[0])]
                if not nl in lines:
                    lines.append(nl)
                else:
                    lines.remove(nl)
        else:
            testMode = False
            drawImage()
else:
    drawImage()
logger.info("Done")