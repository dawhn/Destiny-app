from typing import List, Optional

from sqlmodel import Field, Relationship, SQLModel


class Account(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    bungie_name: str = Field(index=True, unique=True)

    clan_group_id: Optional[int]
    clan_name: Optional[str]
    clan_tag: Optional[str]

    seals: Optional[str]

    destinyMemberships: List["DestinyMembership"] = Relationship(
        back_populates="account"
    )
    characters: List["Character"] = Relationship(back_populates="")


class Character(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    character_id: Optional[int] = Field(index=True, unique=True)

    account: Optional[Account] = Relationship(back_populates="characters")
    account_id: Optional[int] = Field(default=None, foreign_key="account.id")

    # inventory: List["Item"] = Relationship(back_populates="inventory_holder")
    # equipment: List["Item"] = Relationship(back_populates="equipment_holder")
    character_component: Optional["CharacterComponent"] = Relationship(
        back_populates="character"
    )
    activities: List["Activity"] = Relationship(back_populates="character")


# class Item(SQLModel, table=True):
#    id: Optional[int] = Field(default=None, primary_key=True)

#    inventory_holder_id: Optional[int] = Field(default=None, foreign_key="character.id")
#    equipment_holder_id: Optional[int] = Field(default=None, foreign_key="character.id")

#    inventory_holder: Optional[Character] = Relationship(back_populates="inventory")
#    equipment_holder: Optional[Character] = Relationship(back_populates="equipment")


class CharacterComponent(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    # stats
    deleted: Optional[bool]
    activities_cleared: Optional[int]
    kills: Optional[int]
    deaths: Optional[int]
    opponents_defeated: Optional[int]
    kda: Optional[float]
    kd: Optional[float]
    suicides: Optional[int]
    total_time_played: Optional[str]

    # info
    emblem_path: Optional[str]
    emblem_path_bg: Optional[str]
    emblem_overlay: Optional[str]
    emblem_banner: Optional[str]
    title_hash: Optional[int]
    last_played: Optional[str]
    light: Optional[int]
    class_hash: Optional[int]
    class_type: Optional[int]

    character: Optional[Character] = Relationship(back_populates="character_component")
    character_id: Optional[int] = Field(default=None, foreign_key="character.id")


class Activity(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    opponents_defeated: Optional[int]
    deaths: Optional[int]
    completed: Optional[str]
    duration: Optional[str]
    seconds_duration: Optional[int]
    activity_hash: Optional[int]
    mode: Optional[int]
    name: Optional[str]
    image: Optional[str]
    difficulty: Optional[str]

    character: Optional[Character] = Relationship(back_populates="activities")
    character_id: Optional[int] = Field(default=None, foreign_key="character.id")


class DestinyMembership(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    bungie_global_display_name: Optional[str]
    bungie_global_display_name_code: Optional[int]
    membership_id: Optional[str]
    membership_type: Optional[int]

    account: Optional[Account] = Relationship(back_populates="destinyMemberships")
    account_id: Optional[int] = Field(default=None, foreign_key="account.id")
