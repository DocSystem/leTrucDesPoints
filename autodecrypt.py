"""
Python PDP to Text Converter

Originaly written by: Antoine SOUBEN-FINK
"""
from PIL import Image
from math import trunc

imToDecrypt = Image.open("end.png")
bgColor = imToDecrypt.getpixel((0, 0))

POINTS_COORDS = [[] for _ in range(8)]

DECRYPT_BIN = [[] for _ in range(8)]
DECRYPTED_STR = ""

for i in range(8):
    for j in range(8):
        POINTS_COORDS[i].append((trunc((300 + 200 * j) / 2000 * imToDecrypt.size[0]), trunc((300 + 200 * i)/2000 * imToDecrypt.size[1])))

for i in range(len(POINTS_COORDS)):
    for j in range(len(POINTS_COORDS[i])):
        if imToDecrypt.getpixel(POINTS_COORDS[i][j]) == bgColor:
            DECRYPT_BIN[i].append(1)
        else:
            DECRYPT_BIN[i].append(0)

for i in DECRYPT_BIN:
    j = "".join(map(str, i))
    DECRYPTED_STR += chr(int(j, 2))

print(DECRYPTED_STR)
