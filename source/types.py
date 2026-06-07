from dataclasses import dataclass


@dataclass
class Artist:
    mbid: str
    name: str
    sort_name: str
    disambiguation: str
    url: str


@dataclass
class Artists:
    artist: list[Artist]
    total: int
    page: int
    items_per_page: int
    type: str


@dataclass
class Song:
    name: str
    info: str | None
    with_: Artist | None
    tape: bool | None
    cover: Artist | None


@dataclass
class Set:
    song: list[Song]
    encore: int | None
    name: str | None


@dataclass
class Sets:
    set: list[Set]


@dataclass
class Coords:
    lat: float
    long: float


@dataclass
class Country:
    code: str
    name: str


@dataclass
class City:
    coords: Coords
    country: Country
    id: str
    name: str
    state: str
    state_code: str


@dataclass
class Venue:
    city: City
    id: str
    name: str
    url: str


@dataclass
class Tour:
    name: str


@dataclass
class Setlist:
    artist: Artist
    event_date: str
    id: str
    last_updated: str
    sets: Sets
    url: str
    venue: Venue
    version_id: str
    info: str | None
    tour: Tour | None


@dataclass
class Setlists:
    setlist: list[Setlist]
    total: int
    page: int
    items_per_page: int
    type: str
