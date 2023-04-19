# Copyright (c) Ann Mauduy-Decius

import json
from random import choice
import io
import os
import pygame as pg
from urllib import request
import time

with open("animes.json", 'r') as f:
    animes = json.loads(f.read())

with open("elo_raw.json", "r") as f:
    elo = json.loads(f.read())

TOTAL_WINDOW = (900, 690)
IMAGE_SIZE = (TOTAL_WINDOW[0]/2, TOTAL_WINDOW[1])
UPDATE_EVERY = 30
POINT = 0
Scale = 17
HIGHEST = 1
LOWEST = 1
DOUBLE = False
CHOICES = []

MAX_SCORE = 71.0001
MIN_SCORE = 70
MAX_SCORE_DRIFT = 200
MIN_SCORE_DRIFT = -100

image_cache = {}

def kConst(rating):
    if not DOUBLE:
        if rating < 30:
            return 48
        return 32
    else:
        if rating < 30:
            return 96
        return 64

def getAnime(id, animes):
    for x in animes:
        if x[2] == int(id):
            return x
    return None
        
def genImage(id):
    anime = getAnime(id, animes)
    if os.path.exists(f"cache/{id}.png"):
        image = pg.image.load(f"cache/{id}.png")
    else:
        image_url = anime[3]
        req = request.Request(image_url, headers={'User-Agent': 'Magic Browser'})
        con = request.urlopen(req).read()
        image_file = io.BytesIO(con)
        image = pg.image.load(image_file)
    image = pg.transform.scale(image, IMAGE_SIZE)
    pg.image.save(image, f"cache/{id}.png")
    return image

def getRandomIds():
    global POINT
    if len(CHOICES) > POINT:
        c = CHOICES[POINT]
        POINT += 1
        return c

    randomId1, randomId2 = -1, -1
    elo[-1] = 0
    while (getAnime(randomId1, animes) == None or getAnime(randomId2, animes) == None):

        randomId1 = str(choice([el[2] for el in animes]))
        if randomId1 not in elo:
                elo[randomId1] = 20
        while getScore(elo[randomId1]) < MIN_SCORE or getScore(elo[randomId1]) > MAX_SCORE:
            randomId1 = str(choice([el[2] for el in animes]))
            if randomId1 not in elo:
                elo[randomId1] = 20
        randomId2 = str(choice([el[2] for el in animes]))

        if randomId1 not in elo:
            elo[randomId1] = 20
        if randomId2 not in elo:
            elo[randomId2] = 20

        while randomId1 == randomId2:
            randomId2 = str(choice([el[2] for el in animes]))
            if randomId1 not in elo:
                elo[randomId1] = 20
            if randomId2 not in elo:
                elo[randomId2] = 20
        
        n = 0   

        while abs(getScore(elo[randomId1]) - getScore(elo[randomId2])) > MAX_SCORE_DRIFT or n > 300 or abs(getScore(elo[randomId1]) - getScore(elo[randomId2])) < MIN_SCORE_DRIFT:
            randomId2 = str(choice([el[2] for el in animes]))

            if randomId1 not in elo:
                elo[randomId1] = 20
            if randomId2 not in elo:
                elo[randomId2] = 20
            n+=1


        

    CHOICES.append((randomId1, randomId2))
    POINT += 1
    return randomId1, randomId2


def getScore(elo):
    return int(100*(elo-LOWEST)/HIGHEST)

def expectedWin(a, b):
    return 1/(1+10**((b-a)/Scale)) 

def updateElo(id1, id2, animes, k):
    a = elo[id1]
    b = elo[id2]
    a_c = 0
    b_c = 0
    if k == 0:
        a_c = kConst(a)*(0.5 - expectedWin(a, b))
        b_c = kConst(b)*(0.5 - expectedWin(b, a))
    if k == 1:
        a_c = kConst(a)*(1 - expectedWin(a, b))
        b_c = kConst(b)*(0 - expectedWin(b, a))
    if k == 2:
        a_c = kConst(a)*(0 - expectedWin(a, b))
        b_c = kConst(b)*(1 - expectedWin(b, a))
    if k == 3:
        a_c = kConst(a)*(0 - expectedWin(a, b))
        b_c = kConst(b)*(0 - expectedWin(b, a))

    a_c, b_c = round(a_c, 3), round(b_c, 3)
    elo[id1] += a_c
    elo[id2] += b_c
    print(f"{getAnime(id1, animes)[0]} {'+' if a_c >= -0.005 else ''}{round(100*a_c/HIGHEST, 2)} points. New score: {int(100*(elo[id1]-LOWEST)/HIGHEST)}/100. Previous Score: {int(100*((elo[id1]-a_c)-LOWEST)/HIGHEST)}/100.\n{getAnime(id2, animes)[0]} {'+' if b_c >= -0.005 else ''}{round(100*b_c/HIGHEST, 2)} points. New score: {int(100*(elo[id2]-LOWEST)/HIGHEST)}/100. Previous Score: {int(100*((elo[id2]-b_c)-LOWEST)/HIGHEST)}/100.")

vsimg = pg.image.load("vs.png")
VSIMG_SIZE = (50, 50)

def newImage():
    img1 = genImage(randomId1)
    img2 = genImage(randomId2)
    screen.blit(img1, (0, 0))
    screen.blit(img2, (IMAGE_SIZE[0], 0))
    print(f"\n{getAnime(randomId1, animes)[0]} VS {getAnime(randomId2, animes)[0]}")
    img = pg.transform.scale(vsimg, VSIMG_SIZE)
    screen.blit(img, ((TOTAL_WINDOW[0]-VSIMG_SIZE[0])/2, (TOTAL_WINDOW[1]- VSIMG_SIZE[1])/2))
    pg.display.flip()


def save():
    print("\nUpdating...")
    with open("elo_raw.json", "w") as f:
        f.write(json.dumps(elo, indent=4))

    l = {}

    for k, v in elo.items():
        if getAnime(k, animes) != None:
            l[getAnime(k, animes)[0]] = round(v, 2)

    l = {k: v for k, v in sorted(l.items(), key=lambda i: i[1], reverse=True)}
    LOWEST = list(l.items())[-1][1]
    HIGHEST = list(l.items())[0][1]-LOWEST
    l = {k: int(round(100*(v-LOWEST)/(HIGHEST), 0)) for k, v in l.items()}

    with open("elo.json", "w") as f:
        f.write(json.dumps(l, indent=4))

    print("Updated\n")
    return HIGHEST, LOWEST

# --
# --
# --

xxx = 999999#int(input("How many times>> "))

pg.init()

white = (255, 255, 255)

screen = pg.display.set_mode(TOTAL_WINDOW)
pg.display.set_caption("AnimElo")
pg.mouse.set_cursor(pg.SYSTEM_CURSOR_HAND)

HIGHEST, LOWEST = save()

randomId1, randomId2 = getRandomIds()

newImage()

pg.display.flip()
try:
    HIGHEST, LOWEST = save()
    m = 0
    lst = time.time()
    while m < xxx:
        if time.time() - lst > UPDATE_EVERY:
            HIGHEST, LOWEST = save()
            lst = time.time()
        for event in pg.event.get():
            EVENT_FLAG = False
            if event.type == pg.QUIT:
                pg.quit()
                raise SystemExit
            if event.type == pg.MOUSEBUTTONDOWN:
                EVENT_FLAG = True
                k = -1
                x, y = event.pos
                DOUBLE = False
                if event.button == 1:
                    if x >= IMAGE_SIZE[0]:
                        print("Second anime wins")
                        k = 2
                    if x < IMAGE_SIZE[0]:
                        print("First anime wins.")
                        k = 1
                elif event.button == 5:
                    print("Skip")
                elif event.button == 4:
                    print(POINT)
                    if POINT > 1:
                        POINT -= 2
                else:
                    print("Draw")
                    k = 0
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    print("Both lose")
                    k = 3
                EVENT_FLAG = True
            if EVENT_FLAG:
                
                updateElo(randomId1, randomId2, animes, k)

                m+=1
                if m == xxx:
                    break
                
                randomId1, randomId2 = getRandomIds()

                newImage()
except Exception as e:
    raise e
finally:
    save()
