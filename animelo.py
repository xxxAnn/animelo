import json
from random import choice
import io
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
K = 32
Scale = 17

def getAnime(id, animes):
    for x in animes:
        if x[2] == int(id):
            return x
        
def genImage(id):
    anime = getAnime(id, animes)
    image_url = anime[3]
    req = request.Request(image_url, headers={'User-Agent': 'Magic Browser'})
    con = request.urlopen(req).read()
    image_file = io.BytesIO(con)
    image = pg.image.load(image_file)
    image = pg.transform.scale(image, IMAGE_SIZE)
    return image

def getRandomIds():
    n = 0
    ne = False
    while (n < 1000 and ne == False):
        randomId1 = str(choice([el[2] for el in animes]))
        randomId2 = str(choice([el[2] for el in animes]))

        while randomId2 == randomId1:
            randomId2 = str(choice([el[2] for el in animes]))
        if elo[randomId1] == 20 or elo[randomId1] == 36:
            ne = True
        n += 1

    if randomId1 not in elo:
        elo[randomId1] = 20
    if randomId2 not in elo:
        elo[randomId2] = 20
    return randomId1, randomId2


def expectedWin(a, b):
    return 1/(1+10**((b-a)/Scale)) 

def updateElo(id1, id2, animes, k):
    a = elo[id1]
    b = elo[id2]
    a_c = 0
    b_c = 0
    if k == 0:
        a_c = K*(0.5 - expectedWin(a, b))
        b_c = K*(0.5 - expectedWin(b, a))
    if k == 1:
        a_c = K*(1 - expectedWin(a, b))
        b_c = K*(0 - expectedWin(b, a))
    if k == 2:
        a_c = K*(0 - expectedWin(a, b))
        b_c = K*(1 - expectedWin(b, a))
    a_c, b_c = round(a_c, 3), round(b_c, 3)
    elo[id1] += a_c
    elo[id2] += b_c
    print(f"{getAnime(id1, animes)[0]} {'+' if a_c >= 0 else ''}{a_c}. {getAnime(id2, animes)[0]} {'+' if b_c >= 0 else ''}{b_c}.")

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
        f.write(json.dumps(elo))

    l = {}

    for k, v in elo.items():
        l[getAnime(k, animes)[0]] = round(v, 2)

    l = {k: v for k, v in sorted(l.items(), key=lambda i: i[1], reverse=True)}
    lwst = list(l.items())[-1][1]
    hghst = list(l.items())[0][1]-lwst
    l = {k: int(100*(v-lwst)/(hghst)) for k, v in l.items()}

    with open("elo.json", "w") as f:
        f.write(json.dumps(l, indent=4))

    print("Updated\n")

# --
# --
# --

xxx = 999999#int(input("How many times>> "))

pg.init()

white = (255, 255, 255)

screen = pg.display.set_mode(TOTAL_WINDOW,  pg.RESIZABLE)
pg.display.set_caption("AnimElo")
pg.mouse.set_cursor(pg.SYSTEM_CURSOR_HAND)

randomId1, randomId2 = getRandomIds()

newImage()

pg.display.flip()
try:
    m = 0
    lst = time.time()
    while m < xxx:
        if time.time() - lst > UPDATE_EVERY:
            save()
            lst = time.time()
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                raise SystemExit
            if event.type == pg.MOUSEBUTTONDOWN:
                k = -1
                x, y = event.pos
                if event.button == 1:
                    if x >= IMAGE_SIZE[0]:
                        print("Second anime wins")
                        k = 2
                    if x < IMAGE_SIZE[0]:
                        print("First anime wins.")
                        k = 1
                elif event.button > 3:
                    print("Skip")
                else:
                    print("Draw")
                    k = 0
                
                updateElo(randomId1, randomId2, animes, k)

                m+=1
                if m == xxx:
                    break
                
                randomId1, randomId2 = getRandomIds()

                newImage()
except:
    pass
finally:
    save()
