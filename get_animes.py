import Anilist, json
from Anilist.scheme import mediaScheme
import logging

client = Anilist.QueryClient(logging.WARNING)
list_query = client.media_list()

list_query.search(
    mediaScheme().title.romaji,

    paginate=True,

    userName="xxxAnn"
)

result = list_query.results_take_all()

d = [[el.media.title.romaji, el.media.title.english, el.media.id, el.media.coverImage.extraLarge] for el in result]

with open("animes.json", "w") as f:
    f.write(json.dumps(d, indent=4))