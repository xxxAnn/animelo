import requests, json

query = '''
query ($usr: String, $page: Int, $perPage: Int) { 
  Page (page: $page, perPage: $perPage) {
        mediaList (userName: $usr) {
            media {
                title {
                    romaji
                    english
                }
            }
        }
    }
}
'''

variables = {
    'usr': "xxxAnn",
    'page': 1,
    'perPage': 10
}

url = 'https://graphql.anilist.co'

i = 1

d = []

while True:
    data = [(r["media"]["title"]["romaji"], r["media"]["title"]["english"]) for r in 
            requests.post(url, json={'query': query, 'variables': variables}).json()["data"]["Page"]["mediaList"]]
    if data == []:
        break
    d.extend(data)
    i+=1
    variables['page'] = i

with open("animes.json", "w") as f:
    f.write(json.dumps(d))