import json
import pickle
import sqlite3
import zipfile
import os

from src.api_requests import get_manifest

hashes = {
    "DestinyActivityDefinition": "hash",
    "DestinyActivityTypeDefinition": "hash",
    "DestinyClassDefinition": "hash",
    "DestinyGenderDefinition": "hash",
    "DestinyInventoryBucketDefinition": "hash",
    "DestinyInventoryItemDefinition": "hash",
    "DestinyProgressionDefinition": "hash",
    "DestinyRaceDefinition": "hash",
    "DestinyUnlockDefinition": "hash",
    "DestinyHistoricalStatsDefinition": "statId",
    "DestinyStatDefinition": "hash",
    "DestinySandboxPerkDefinition": "hash",
    "DestinyDestinationDefinition": "hash",
    "DestinyPlaceDefinition": "hash",
    "DestinyStatGroupDefinition": "hash",
    "DestinyFactionDefinition": "hash",
    "DestinyVendorDefinition": "hash",
    "DestinyPresentationNodeDefinition": "hash",
}

hashes_trunc = {
    "DestinyInventoryItemDefinition": "hash",
    "DestinyTalentGridDefinition": "hash",
    "DestinyHistoricalStatsDefinition": "statId",
    "DestinyStatDefinition": "hash",
    "DestinySandboxPerkDefinition": "hash",
    "DestinyStatGroupDefinition": "hash",
}

manifest_data = None


def build_manifest():
    if not os.path.isfile(r"manifest.content"):
        r = get_manifest()

        with open("MANZIP", "wb") as zip_file:
            zip_file.write(r.content)
        print("Manifest Download complete")

        with zipfile.ZipFile("MANZIP") as zip_file:
            name = zip_file.namelist()
            zip_file.extractall()

        os.rename(name[0], "manifest.content")
        print("Manifest unzipped")

        all_data = build_dict(hashes)
        try:
            with open("manifest.pickle", "wb") as data:
                pickle.dump(all_data, data)
        except Exception as e:
            print(f"Error saving pickle: {e}")


def build_dict(hash_dict):
    # test
    con = sqlite3.connect("manifest.content")
    cur = con.cursor()

    all_data = {}
    # for every table name in the dictionary
    for table_name in hash_dict.keys():
        # Get a list of all the jsons from the table
        cur.execute("SELECT json from " + table_name)

        # get a list of tuples
        items = cur.fetchall()

        # create a list of jsons
        item_jsons = [json.loads(item[0]) for item in items]

        # create dict with hashes as keys
        item_dict = {}
        hash = hash_dict[table_name]
        for item in item_jsons:
            item_dict[item[hash]] = item

        # add the current dictionary to the main dict using the name of the table as a key.
        all_data[table_name] = item_dict
    return all_data


def load_manifest():
    if not os.path.exists("manifest.pickle"):
        build_manifest()

    global manifest_data
    if manifest_data is None:
        try:
            with open("manifest.pickle", "rb") as data:
                manifest_data = pickle.load(data)
        except Exception as e:
            print(f"Error loading pickle: {e}")

    return manifest_data


def read_activity_from_manifest(hash: int):
    manifest_data = load_manifest()
    activity = manifest_data["DestinyActivityDefinition"][hash]
    return activity


def read_emblem_banner(hash: int):
    manifest_data = load_manifest()
    emblem_banner = manifest_data["DestinyInventoryItemDefinition"][hash][
        "secondarySpecial"
    ]
    emblem_overlay = manifest_data["DestinyInventoryItemDefinition"][hash][
        "secondaryOverlay"
    ]
    return emblem_overlay, emblem_banner


def read_raid_seals(presentation_nodes):
    raid_seals = {
        "Salvation's Edge": "334829503",
        "Crota's End": "238107129",
        "Root of Nightmares": "1976056830",
        "King's Fall": "2613142083",
        "Vow of the Disciple": "2886738008",
        "Vault of Glass": "3734352323",
        "Deep Stone Crypt": "2960810718",
        "Garden of Salvation": "1827854727",
        "Last Wish": "1486062207",
        "Crown of Sorrow": "717225803",
    }

    manifest_data = load_manifest()

    seals = []

    for key, value in raid_seals.items():
        if value in presentation_nodes:
            seal_image = manifest_data["DestinyPresentationNodeDefinition"][int(value)][
                "displayProperties"
            ]["icon"]
            if (
                presentation_nodes[value]["progressValue"]
                == presentation_nodes[value]["completionValue"]
            ):
                # All triumphs are completed, seal is obtained
                seals.append({"name": key, "completed": "yes", "image": seal_image})
            else:
                seals.append({"name": key, "completed": "no", "image": seal_image})

    return seals
