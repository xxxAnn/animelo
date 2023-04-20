import json
import time
import Anilist

with open("animes.json", 'r') as f:
    animes = json.loads(f.read())

with open("elo_raw.json", "r") as f:
    elo = json.loads(f.read())

l = {}

for k, v in elo.items():
    l[int(k)] = round(v, 2)

l = {k: v for k, v in sorted(l.items(), key=lambda i: i[1], reverse=True)}
lwst = list(l.items())[-1][1]
hghst = list(l.items())[0][1]-lwst
l = {k: int(100*(v-lwst)/(hghst)) for k, v in l.items()}

auth = Anilist.Auth.from_config_file("config.json")
mutate_client = Anilist.MutationClient(auth)

for k, v in l.items():
    
    mutate_client.media_entry(k).set_score(v)

    time.sleep(1.5)
