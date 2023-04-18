This is a program that asks you which of two anime you prefer and uses all your answers to give a rating out of 100 to each anime.
It also contains tools to automatically update and pull from Anilist.co using the GraphQL Anilist v2 API.

**How to use**
Delete the contents of "elo_raw.json" and replace them with "{}"
Before running "get_animes.py" you need to replace "USERNAME = xxxAnn" with your
own anilist username. If you use MAL, create an anilist account and export the MAL list to anilist.
Then run "get_animes.py" then "animelo.py"


You can run "auto_update.py" to automatically update your Anilist.
however, you will need to get an OAuth token for your Anilist account and create a file called "code.txt" and put it there.
Also you will need to get your client secret and create a file called secret.txt and put it in there.