import requests
import json
import time

url = 'https://graphql.anilist.co'

with open("animes.json", 'r') as f:
    animes = json.loads(f.read())

with open("code.txt", "r", encoding='utf-8') as f:
    code = f.read()

with open("secret.txt", "r", encoding='utf-8') as f:
    secret = f.read()


c = requests.post("https://anilist.co/api/v2/oauth/token", json={
    'grant_type': 'authorization_code',
    'client_id': 12213,
    'client_secret': secret,
    'redirect_uri': 'https://anilist.co/api/v2/oauth/pin',
    'code': code
}, headers={'Accept': 'application/json'}).json()

access_token = c["access_token"]

with open("elo_raw.json", "r") as f:
    elo = json.loads(f.read())

l = {}

for k, v in elo.items():
    l[int(k)] = round(v, 2)

l = {k: v for k, v in sorted(l.items(), key=lambda i: i[1], reverse=True)}
lwst = list(l.items())[-1][1]
hghst = list(l.items())[0][1]-lwst
l = {k: int(100*(v-lwst)/(hghst)) for k, v in l.items()}

for k, v in l.items():
    if k not in [anime[2] for anime in animes]:
        continue
    query = '''
    mutation ($mediaId: Int, $score: Float) {
        SaveMediaListEntry (mediaId: $mediaId, score: $score) {
            id
            score
        }
    }
    '''

    k = requests.post(url, json={'query': query, 'variables': {'mediaId': k, 'score': v}}, headers={'Authorization': f"Bearer {access_token}", 'Content-Type': 'application/json', 'Accept': 'application/json'}).json()
    print(k)
    id = k["data"]["SaveMediaListEntry"]["id"]

    query = '''
    mutation ($id: Int, $score: Float) {
        SaveMediaListEntry (id: $id, score: $score) {
            id
            score
        }
    }
    '''
    k = requests.post(url, json={'query': query, 'variables': {'id': id, 'score': v}}, headers={'Authorization': f"Bearer {access_token}", 'Content-Type': 'application/json', 'Accept': 'application/json'}).json()
    print(k)
    time.sleep(1.5)
