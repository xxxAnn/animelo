import Anilist, json

client = Anilist.QueryClient()

media_list = client.media_list(username="xxxAnn", languages=["romaji", "english"])

d = [[el.title.romaji, el.title.english, el.id, el.coverImage.extraLarge] for el in media_list.entries]

with open("animes.json", "w") as f:
    f.write(json.dumps(d, indent=4))