import json

from sqlmodel import select, func, case, update
from sqlalchemy.sql.operators import isnot
from sqlalchemy.exc import IntegrityError
from typing import List

from src.database.database import session
from src.database.models import (
    Account,
    DestinyMembership,
    Character,
    CharacterComponent,
    Activity,
)
from src.utils.helper import parse_time


def create_memberships(response, account, session) -> None:
    for membership in response["Response"]:
        destiny_membership = DestinyMembership(
            bungie_global_display_name=membership["bungieGlobalDisplayName"],
            bungie_global_display_name_code=membership["bungieGlobalDisplayNameCode"],
            membership_id=membership["membershipId"],
            membership_type=membership["membershipType"],
            account=account,
        )

        session.add(destiny_membership)
        session.commit()  # Commit after each membership addition
        session.refresh(destiny_membership)


def create_character(char, char_info, emblem_data, account: Account):
    try:
        character = Character(character_id=char["characterId"], account=account)
        session.add(character)
        session.commit()
        session.refresh(character)

        char_stats = char["merged"]["allTime"]

        char_comp = CharacterComponent(
            # stats
            deleted=char["deleted"],
            activities_cleared=char_stats["activitiesCleared"]["basic"]["displayValue"],
            kills=char_stats["kills"]["basic"]["displayValue"],
            deaths=char_stats["deaths"]["basic"]["displayValue"],
            opponents_defeated=char_stats["opponentsDefeated"]["basic"]["displayValue"],
            kda=char_stats["killsDeathsAssists"]["basic"]["displayValue"],
            kd=char_stats["killsDeathsRatio"]["basic"]["displayValue"],
            suicides=char_stats["suicides"]["basic"]["displayValue"],
            total_time_played=char_stats["secondsPlayed"]["basic"]["displayValue"],
            # info
            emblem_path=char_info["emblemPath"] if char_info is not None else None,
            emblem_path_bg=(
                char_info["emblemBackgroundPath"] if char_info is not None else None
            ),
            emblem_overlay=emblem_data[0] if char_info is not None else None,
            emblem_banner=emblem_data[1] if char_info is not None else None,
            title_hash=char_info["titleRecordHash"] if char_info is not None else None,
            last_played=char_info["dateLastPlayed"] if char_info is not None else None,
            light=char_info["light"] if char_info is not None else None,
            class_hash=char_info["classHash"] if char_info is not None else None,
            class_type=char_info["classType"] if char_info is not None else None,
            # parent
            character=character,
        )

        session.add(char_comp)
        session.commit()
        session.refresh(char_comp)
    except IntegrityError:
        session.rollback()
        print(f"Error registering character {char['characterId']}")


def create_account(response: dict, bungie_name: str) -> Account:
    try:
        # Try to create and add the account
        acc = Account(bungie_name=bungie_name)
        session.add(acc)
        session.commit()
        session.refresh(acc)

        # Process DestinyMemberships linked to the account
        create_memberships(response, acc, session)

    except IntegrityError:
        # If the bungie_name already exists, rollback and retrieve the existing account
        session.rollback()
        acc = session.exec(
            select(Account).where(Account.bungie_name == bungie_name)
        ).first()
    return acc


def add_clan_account(response: dict, account):
    query = (
        update(Account)
        .where(Account.id == account.id)
        .values(clan_group_id=response[0]["group"]["groupId"])
        .values(clan_name=response[0]["group"]["name"])
        .values(clan_tag=response[0]["group"]["clanInfo"]["clanCallsign"])
    )
    session.exec(query)
    session.commit()


def add_seals_account(seals, account):
    query = (
        update(Account).where(Account.id == account.id).values(seals=json.dumps(seals))
    )
    session.exec(query)
    session.commit()


def create_activities(activity: dict, activity_data: dict, character: Character):
    try:
        act = Activity(
            opponents_defeated=activity["values"]["opponentsDefeated"]["basic"][
                "displayValue"
            ],
            deaths=activity["values"]["deaths"]["basic"]["displayValue"],
            completed=activity["values"]["completed"]["basic"]["displayValue"],
            duration=activity["values"]["activityDurationSeconds"]["basic"][
                "displayValue"
            ],
            seconds_duration=parse_time(
                activity["values"]["activityDurationSeconds"]["basic"]["displayValue"]
            ),
            activity_hash=activity["activityDetails"]["directorActivityHash"],
            mode=activity["activityDetails"]["mode"],
            name=activity_data["originalDisplayProperties"]["name"],
            image=activity_data["pgcrImage"],
            difficulty=(
                activity_data["selectionScreenDisplayProperties"]["name"]
                if "selectionDisplayProperties" in activity_data
                else "standard"
            ),
            character=character,
        )

        session.add(act)
        session.commit()
        session.refresh(act)
    except IntegrityError:
        session.rollback()


def get_membership(bungie_name: str) -> DestinyMembership:
    statement = (
        select(DestinyMembership)
        .join(DestinyMembership.account)
        .where(Account.bungie_name == bungie_name)
        .where(DestinyMembership.membership_type == 3)
    )
    membership = session.exec(statement).first()
    return membership


def get_all_characters(bungie_name: str) -> List[Character]:
    statement = (
        select(Character)
        .join(Character.account)
        .where(Account.bungie_name == bungie_name)
    )
    characters = session.exec(statement).all()
    return characters


def get_membership_characters(bungie_name: str):
    return get_membership(bungie_name), get_all_characters(bungie_name)


def seconds_to_time(seconds: int):
    # Break down time using divmod
    days, seconds = divmod(seconds, 86400)
    hours, seconds = divmod(seconds, 3600)
    minutes, seconds = divmod(seconds, 60)

    # List of time components with their labels
    time_components = [(days, "d"), (hours, "h"), (minutes, "m"), (seconds, "s")]

    non_zero_components = [
        f"{value}{label}" for value, label in time_components if value > 0
    ]
    formatted_duration = " ".join(non_zero_components[:2])

    return formatted_duration


def get_user_raids(bungie_name: str):
    subquery = (
        select(
            Activity.name,
            func.count().label("clears"),
            func.min(Activity.seconds_duration).label("min_seconds_duration"),
            func.avg(Activity.seconds_duration).label("avg_seconds_duration"),
        )
        .join(Activity.character)
        .join(Character.account)
        .where(Account.bungie_name == bungie_name)
        .group_by(Activity.name)
    ).subquery()

    query = (
        select(
            Activity.name,
            Activity.image,
            subquery.c.clears,
            Activity.duration.label("fastest"),  # Get duration based on min seconds
            (func.sum(case((Activity.deaths == 0, 1), else_=0)) > 0).label("flawless"),
            subquery.c.avg_seconds_duration,
        )
        .join(
            subquery,
            (Activity.name == subquery.c.name)
            & (Activity.seconds_duration == subquery.c.min_seconds_duration),
        )
        .group_by(Activity.name)
    )

    raids = session.exec(query).all()
    raids_dicts = [
        {
            "name": item[0],
            "image": item[1],
            "clears": item[2],
            "fastest": item[3],
            "flawless": item[4],
            "avg": seconds_to_time(int(item[5])),
        }
        for item in raids
    ]
    return raids_dicts


def get_player(bungie_name: str):
    query = (
        select(
            CharacterComponent.emblem_banner,
            CharacterComponent.emblem_overlay,
            Account.clan_name,
            Account.clan_tag,
            Account.bungie_name,
            Account.seals,
        )
        .join(CharacterComponent.character)
        .join(Character.account)
        .where(Account.bungie_name == bungie_name)
        .where(isnot(CharacterComponent.last_played, None))
        .order_by(CharacterComponent.last_played.desc())
    )

    player = session.exec(query).first()
    player_dict = {
        "banner": f"https://www.bungie.net{player[0]}",
        "logo": f"https://www.bungie.net{player[1]}",
        "clan_name": player[2],
        "clan_tag": player[3],
        "name": player[4],
        "seals": player[5],
    }
    return player_dict
