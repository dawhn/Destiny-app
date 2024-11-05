import requests

from src.config import AUTH_TOKEN, API_BASE_URL
from src.token.oauth import client

from src.database.handling import get_membership_characters


def get_manifest():
    url = f"{API_BASE_URL}/Destiny2/Manifest/"
    header = {"X-API-KEY": client.api_key, "Authorization": f"Bearer {AUTH_TOKEN}"}

    manifest = (requests.get(url, headers=header)).json()
    mani_url = (
        f"http://www.bungie.net{manifest['Response']['mobileWorldContentPaths']['en']}"
    )

    r = requests.get(mani_url)
    return r


def get_activity_history(bungie_name: str, mode):
    membership, characters = get_membership_characters(bungie_name)
    header = {"X-API-KEY": client.api_key, "Authorization": f"Bearer {AUTH_TOKEN}"}
    char_history = []
    for char in characters:
        page = 0
        count = 250
        activity_list = []
        while True:
            url = f"{API_BASE_URL}/Destiny2/{membership.membership_type}/Account/{membership.membership_id}/Character/{char.character_id}/Stats/Activities?count={count}&mode={mode}&page={page}"
            res = (requests.get(url, headers=header)).json()

            if res["ErrorStatus"] == "Success" and res["ErrorCode"] == 1:
                if "activities" in res["Response"]:
                    count = len(res["Response"]["activities"])
                else:
                    break

                for activity in res["Response"]["activities"]:
                    if (
                        activity["values"]["completed"]["basic"]["displayValue"]
                        == "Yes"
                        and activity["values"]["completionReason"]["basic"][
                            "displayValue"
                        ]
                        == "Objective Completed"
                    ):
                        activity_list.append(activity)

                if count != 250:
                    break
                page += 1
            else:
                break
        char_history.append((activity_list, char))
    return char_history


def get_clan(membership):
    url = f"{API_BASE_URL}/GroupV2/User/{membership.membership_type}/{membership.membership_id}/0/1/"
    header = {"X-API-KEY": client.api_key, "Authorization": f"Bearer {AUTH_TOKEN}"}

    r = requests.get(url, headers=header)
    res = r.json()

    if res["ErrorStatus"] == "Success" and res["ErrorCode"] == 1:
        return res


def get_characters(membership):
    url = f"{API_BASE_URL}/Destiny2/{membership.membership_type}/Account/{membership.membership_id}/Stats/"
    header = {"X-API-KEY": client.api_key, "Authorization": f"Bearer {AUTH_TOKEN}"}

    res = (requests.get(url, headers=header)).json()

    if res["ErrorStatus"] == "Success" and res["ErrorCode"] == 1:
        return res


def get_character(membership, character_id, seal: bool):
    if seal:
        url = f"{API_BASE_URL}/Destiny2/{membership.membership_type}/Profile/{membership.membership_id}/Character/{character_id}/?components=200,700"
    else:
        url = f"{API_BASE_URL}/Destiny2/{membership.membership_type}/Profile/{membership.membership_id}/Character/{character_id}/?components=200"
    header = {"X-API-KEY": client.api_key, "Authorization": f"Bearer {AUTH_TOKEN}"}

    res = (requests.get(url, headers=header)).json()
    print("char", res)
    if res["ErrorStatus"] == "Success" and res["ErrorCode"] == 1:
        return res


def get_account_by_bungie_name(bungie_name: str):
    url = f"{API_BASE_URL}/Destiny2/SearchDestinyPlayerByBungieName/All/"
    name, code = bungie_name.split("#")
    header = {"X-API-Key": client.api_key, "Authorization": f"Bearer {AUTH_TOKEN}"}

    body = {"displayName": name, "displayNameCode": code}

    res = (requests.post(url, headers=header, json=body)).json()
    if res["ErrorStatus"] == "Success" and res["ErrorCode"] == 1:
        return res
    else:
        print(f"Error {res['ErrorCode']}: {res['ErrorStatus']}, {res['Message']}")
