import eel
import json

from src.utils.user import get_user
from src.utils.activities import get_activities

from src.database.handling import get_user_raids, get_player

eel.init("app")


@eel.expose
def search_player(query):
    print(f"Search query received: {query}")
    get_user(query)
    get_activities(query, 4)


@eel.expose
def fetch_player(query):
    player = get_player(query)
    print(f"player {query} returned")
    return json.dumps(player)


@eel.expose
def fetch_player_raids(query):
    raids = get_user_raids(query)
    print(f"player {query} raids returned")
    return json.dumps(raids)


def start_app():
    eel.start("web/index.html", size=(1280, 720), mode="chrome")
