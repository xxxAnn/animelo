import json
from random import choice
import io
import pygame as pg
from urllib import request

with open("animes.json", 'r') as f:
    animes = json.loads(f.read())

with open("elo_raw.json", "r") as f:
    elo = json.loads(f.read())

IMAGE_SIZE = (200, 300)
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
    print(f"{getAnime(id1, animes)[0]} {'+' if a_c > 0 else ''}{a_c}. {getAnime(id2, animes)[0]} {'+' if b_c > 0 else ''}{b_c}.")

def newImage():
    img1 = genImage(randomId1)
    img2 = genImage(randomId2)
    screen.blit(img1, (0, 0))
    screen.blit(img2, (IMAGE_SIZE[0], 0))
    pg.display.flip()
    print(f"\n{getAnime(randomId1, animes)[0]} VS {getAnime(randomId2, animes)[0]}")

# --
# --
# --

xxx = int(input("How many times>> "))

pg.init()

white = (255, 255, 255)

screen = pg.display.set_mode((400,300),  pg.RESIZABLE )

randomId1, randomId2 = getRandomIds()

newImage()

pg.display.flip()
try:
    m = 0
    while m < xxx:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                raise SystemExit
            if event.type == pg.MOUSEBUTTONDOWN:
                k = 0
                x, y = event.pos
                if event.button == 1:
                    if x >= IMAGE_SIZE[0]:
                        print("Second anime wins")
                        k = 2
                    if x < IMAGE_SIZE[0]:
                        print("First anime wins.")
                        k = 1
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
    print("Finalizing")
    with open("elo_raw.json", "w") as f:
        f.write(json.dumps(elo))

    l = {}

    for k, v in elo.items():
        l[getAnime(k, animes)[0]] = round(v, 2)

    l = {k: v for k, v in sorted(l.items(), key=lambda i: i[1], reverse=True)}

    with open("elo.json", "w") as f:
        f.write(json.dumps(l, indent=4))

    print("Updated")
