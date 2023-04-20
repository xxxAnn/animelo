import Anilist, json
import logging

client = Anilist.QueryClient(logging.WARNING)

media_list = client.media_list(username="xxxAnn", languages=["romaji", "english"])

d = [[el.title.romaji, el.title.english, el.id, el.coverImage.extraLarge] for el in media_list.entries]

with open("animes.json", "w") as f:
    f.write(json.dumps(d, indent=4))