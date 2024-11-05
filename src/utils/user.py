from src.api_requests import (
    get_account_by_bungie_name,
    get_characters,
    get_character,
    get_clan,
)
from src.database.handling import (
    create_account,
    create_character,
    get_membership,
    add_clan_account,
    add_seals_account,
)

from src.utils.manifest_utils import read_emblem_banner, read_raid_seals


def get_user(bungie_name: str):
    res_acc = get_account_by_bungie_name(bungie_name)
    account = create_account(res_acc, bungie_name)

    membership = get_membership(bungie_name)

    res_clan = get_clan(membership)

    if len(res_clan["Response"]["results"]) >= 1:
        add_clan_account(res_clan["Response"]["results"], account)
        print("clan added")

    res_chars = get_characters(membership)
    first = True
    for char_stats in res_chars["Response"]["characters"]:
        character_id = char_stats["characterId"]
        if char_stats["deleted"] == 0:
            char = get_character(membership, character_id, first)
            char_info = char["Response"]["character"]["data"]
            if first:
                seals = read_raid_seals(
                    char["Response"]["presentationNodes"]["data"]["nodes"]
                )
                add_seals_account(seals, account)
            emblem_data = read_emblem_banner(char_info["emblemHash"])
            create_character(char_stats, char_info, emblem_data, account)
            first = False
        else:
            create_character(char_stats, None, None, account)
