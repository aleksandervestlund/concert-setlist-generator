from collections.abc import Container, Iterable, Mapping, Sequence


def build_master_playlist(
    all_setlists: list[list[str]],
    song_aliases: Mapping[str, str],
    songs_to_ignore: Container[str],
    mock_album_db: Mapping[str, list[str]],
    additional_songs: Iterable[str] | None = None,
) -> list[str]:
    if additional_songs is not None:
        all_setlists.extend([[song] for song in additional_songs])

    master_playlist = list(all_setlists)[0]

    for setlist in all_setlists[1:]:
        merge_setlist_with_master(
            master_playlist,
            setlist,
            song_aliases,
            songs_to_ignore,
            mock_album_db,
        )

    return master_playlist


def get_canonical_name(song_name: str, song_aliases: Mapping[str, str]) -> str:
    cleaned = song_name.strip().lower()
    return song_aliases.get(cleaned, cleaned)


def find_in_master(
    song_name: str,
    master_playlist: Iterable[str],
    song_aliases: Mapping[str, str],
) -> int:
    canonical_target = get_canonical_name(song_name, song_aliases)

    for idx, item in enumerate(master_playlist):
        if get_canonical_name(item, song_aliases) == canonical_target:
            return idx
    return -1


def get_album(
    song_name: str,
    mock_album_db: Mapping[str, list[str]],
    song_aliases: Mapping[str, str],
) -> list[str]:
    canonical_name = get_canonical_name(song_name, song_aliases)
    return mock_album_db.get(canonical_name, [])


def merge_setlist_with_master(
    master_playlist: list[str],
    current_setlist: Sequence[str],
    song_aliases: Mapping[str, str],
    songs_to_ignore: Container[str],
    mock_album_db: Mapping[str, list[str]],
) -> None:
    for i, song in enumerate(current_setlist):
        if find_in_master(song, master_playlist, song_aliases) != -1:
            continue
        if song.lower() in songs_to_ignore:
            continue
        if insert_by_neighbor_context(
            master_playlist, song, current_setlist, i, song_aliases
        ):
            continue
        if not (album_tracks := get_album(song, mock_album_db, song_aliases)):
            raise ValueError(f"Could not find album for song {song!r}")
        if (alb_i := find_album_index(album_tracks, song, song_aliases)) == -1:
            continue
        if not insert_by_neighbor_context(
            master_playlist, song, album_tracks, alb_i, song_aliases
        ):
            raise ValueError(
                f"Could not insert song {song!r} into master playlist. Playlist: {master_playlist}"
            )


def find_album_index(
    album_tracks: Iterable[str], song: str, song_aliases: Mapping[str, str]
) -> int:
    canonical_song = get_canonical_name(song, song_aliases)

    for idx, t in enumerate(album_tracks):
        if get_canonical_name(t, song_aliases) == canonical_song:
            return idx
    return -1


def insert_by_neighbor_context(
    master_playlist: list[str],
    song: str,
    reference_sequence: Sequence[str],
    target_idx: int,
    song_aliases: Mapping[str, str],
) -> bool:
    max_dist = max(target_idx, len(reference_sequence) - 1 - target_idx)

    for d in range(1, max_dist + 1):
        if (ahead_idx := target_idx + d) < len(reference_sequence):
            anchor = reference_sequence[ahead_idx]
            if (
                master_idx := find_in_master(
                    anchor, master_playlist, song_aliases
                )
            ) != -1:
                master_playlist.insert(master_idx, song)
                return True

        if (behind_idx := target_idx - d) >= 0:
            anchor = reference_sequence[behind_idx]
            if (
                master_idx := find_in_master(
                    anchor, master_playlist, song_aliases
                )
            ) != -1:
                master_playlist.insert(master_idx + 1, song)
                return True

    return False
