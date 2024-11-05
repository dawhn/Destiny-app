from src.api_requests import get_activity_history
from src.database.handling import create_activities

from src.utils.manifest_utils import read_activity_from_manifest


def get_activities(bungie_name: str, mode: int):
    char_history = get_activity_history(bungie_name, mode)
    print("char history loaded")

    for history, char in char_history:
        for activity in history:
            activity_data = read_activity_from_manifest(
                activity["activityDetails"]["directorActivityHash"]
            )
            create_activities(activity, activity_data, char)
