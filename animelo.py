import json
from random import choice

with open("animes.json", "r") as f:
    animes = json.loads(f.read())

with open("elo_raw.json", "r") as f:
    elo = json.loads(f.read())

x = int(input("How many times>> "))

def getAnime(id, animes):
    for x in animes:
        if x[2] == int(id):
            return x

K = 32
Scale = 17

def expected_win(a, b):
    return 1/(1+10**((b-a)/Scale)) 
try:
    for i in range(x):
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

        print(f"\n{n/10}%\n First anime win probability: {round(expected_win(elo[randomId1], elo[randomId2])*100,2)}%.\n")

        try:
            k = int(input(f"{getAnime(randomId1, animes)[0]} **OR** {getAnime(randomId2, animes)[0]} >> ")) 
        except:
            k = 0

        if k not in [1, 2]:
            k = 0

        a = elo[randomId1]
        b = elo[randomId2]
        a_c = 0
        b_c = 0
        if k == 0:
            a_c = K*(0.5 - expected_win(a, b))
            b_c = K*(0.5 - expected_win(b, a))
        if k == 1:
            a_c = K*(1 - expected_win(a, b))
            b_c = K*(0 - expected_win(b, a))
        if k == 2:
            a_c = K*(0 - expected_win(a, b))
            b_c = K*(1 - expected_win(b, a))
        a_c, b_c = round(a_c, 3), round(b_c, 3)
        elo[randomId1] += a_c
        elo[randomId2] += b_c
        print(f"First anime {'+' if a_c > 0 else ''}{a_c}. Second anime {'+' if b_c > 0 else ''}{b_c}.")
        



except:
    pass
finally:
    with open("elo_raw.json", "w") as f:
        f.write(json.dumps(elo))

    l = {}

    for k, v in elo.items():
        l[getAnime(k, animes)[0]] = round(v, 2)

    l = {k: v for k, v in sorted(l.items(), key=lambda i: i[1], reverse=True)}

    with open("elo.json", "w") as f:
        f.write(json.dumps(l, indent=4))


    