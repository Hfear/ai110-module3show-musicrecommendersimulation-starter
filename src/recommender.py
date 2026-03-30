from typing import List, Dict, Tuple
from dataclasses import dataclass, field
import csv

# ---------------------------------------------------------------------------
# Data classes
# ---------------------------------------------------------------------------

@dataclass
class Song:
    """Represents a song and its audio attributes."""
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float

@dataclass
class UserProfile:
    """Stores a user's explicit taste preferences plus a list of liked song titles."""
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool
    liked_songs: List[str] = field(default_factory=list)

# ---------------------------------------------------------------------------
# Scoring weights — must sum to 1.0
# ---------------------------------------------------------------------------

WEIGHTS = {
    "genre":        0.35,
    "mood":         0.25,
    "energy":       0.25,
    "acousticness": 0.15,
}
LIKED_BONUS = 0.10  # extra credit when candidate shares genre/mood with a liked song

# ---------------------------------------------------------------------------
# Core scoring function (Steps 2 & 3)
# ---------------------------------------------------------------------------

def score_song(user_prefs: Dict, song: Dict, all_songs: List[Dict]) -> Tuple[float, List[str]]:
    """Score one song against the user profile and return (score, reasons).

    The score is a float between 0.0 and 1.0.
    reasons is a list of strings explaining each point contribution,
    e.g. ['genre match (+0.35)', 'energy close (+0.23)'].
    """
    reasons: List[str] = []

    # Build centroid from liked songs (or fall back to explicit prefs)
    liked_titles = set(user_prefs.get("liked_songs", []))
    liked = [s for s in all_songs if s["title"] in liked_titles]

    if liked:
        genre_freq = sum(1 for s in liked if s["genre"] == song["genre"]) / len(liked)
        mood_freq  = sum(1 for s in liked if s["mood"]  == song["mood"])  / len(liked)
        avg_energy = sum(s["energy"]       for s in liked) / len(liked)
        avg_acous  = sum(s["acousticness"] for s in liked) / len(liked)
    else:
        genre_freq = 1.0 if song["genre"] == user_prefs.get("genre", "") else 0.0
        mood_freq  = 1.0 if song["mood"]  == user_prefs.get("mood",  "") else 0.0
        avg_energy = user_prefs.get("energy", 0.5)
        avg_acous  = 0.8 if user_prefs.get("likes_acoustic", False) else 0.2

    # --- Genre ---
    genre_pts = round(WEIGHTS["genre"] * genre_freq, 4)
    if genre_pts > 0:
        reasons.append(f"genre match (+{genre_pts})")

    # --- Mood ---
    mood_pts = round(WEIGHTS["mood"] * mood_freq, 4)
    if mood_pts > 0:
        reasons.append(f"mood match (+{mood_pts})")

    # --- Energy proximity: closer to centroid = higher score ---
    energy_sim = 1.0 - abs(song["energy"] - avg_energy)
    energy_pts = round(WEIGHTS["energy"] * energy_sim, 4)
    reasons.append(f"energy close (+{energy_pts})")

    # --- Acousticness proximity ---
    acous_sim = 1.0 - abs(song["acousticness"] - avg_acous)
    acous_pts = round(WEIGHTS["acousticness"] * acous_sim, 4)
    reasons.append(f"texture close (+{acous_pts})")

    score = genre_pts + mood_pts + energy_pts + acous_pts

    # --- Liked-song bonus ---
    bonus = 0.0
    if liked and (genre_freq > 0 or mood_freq > 0):
        bonus = round(LIKED_BONUS * max(genre_freq, mood_freq), 4)
        score += bonus
        reasons.append(f"liked-song bonus (+{bonus})")

    if len(reasons) == 2:  # only the two proximity lines, no matches
        reasons.append("closest available match by audio features")

    return round(score, 4), reasons

# ---------------------------------------------------------------------------
# OOP layer (required by tests/test_recommender.py)
# ---------------------------------------------------------------------------

class Recommender:
    """Wraps the catalog and exposes recommend() and explain_recommendation()."""

    def __init__(self, songs: List[Song]):
        """Initialise with a list of Song dataclass instances."""
        self.songs = songs

    def _song_to_dict(self, song: Song) -> Dict:
        """Convert a Song dataclass to the dict format expected by score_song."""
        return {
            "title": song.title, "genre": song.genre, "mood": song.mood,
            "energy": song.energy, "acousticness": song.acousticness,
        }

    def _profile_to_prefs(self, user: UserProfile) -> Dict:
        """Convert a UserProfile dataclass to the dict format expected by score_song."""
        return {
            "genre":          user.favorite_genre,
            "mood":           user.favorite_mood,
            "energy":         user.target_energy,
            "likes_acoustic": user.likes_acoustic,
            "liked_songs":    user.liked_songs,
        }

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        """Return the top-k Song objects ranked by score for the given UserProfile."""
        prefs     = self._profile_to_prefs(user)
        all_dicts = [self._song_to_dict(s) for s in self.songs]
        liked_set = set(user.liked_songs)

        # Score every non-liked song, then sort descending — sorted() is preferred
        # here because it returns a new list and leaves self.songs unchanged.
        # .sort() would mutate the original list in place.
        scored = [
            (song, score_song(prefs, self._song_to_dict(song), all_dicts)[0])
            for song in self.songs
            if song.title not in liked_set
        ]
        return [song for song, _ in sorted(scored, key=lambda x: x[1], reverse=True)[:k]]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        """Return a human-readable explanation of why song was recommended."""
        prefs     = self._profile_to_prefs(user)
        all_dicts = [self._song_to_dict(s) for s in self.songs]
        _, reasons = score_song(prefs, self._song_to_dict(song), all_dicts)
        return ", ".join(reasons)

# ---------------------------------------------------------------------------
# Functional API (required by src/main.py)
# ---------------------------------------------------------------------------

def load_songs(csv_path: str) -> List[Dict]:
    """Read songs.csv and return a list of dicts with correct numeric types."""
    songs = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            songs.append({
                "id":           int(row["id"]),
                "title":        row["title"],
                "artist":       row["artist"],
                "genre":        row["genre"],
                "mood":         row["mood"],
                "energy":       float(row["energy"]),
                "tempo_bpm":    float(row["tempo_bpm"]),
                "valence":      float(row["valence"]),
                "danceability": float(row["danceability"]),
                "acousticness": float(row["acousticness"]),
            })
    return songs


def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """Score every non-liked song, rank highest-to-lowest, return top-k as (song, score, reasons_str).

    Uses sorted() (not .sort()) so the original songs list is never mutated.
    sorted() vs .sort(): sorted() returns a brand-new list; .sort() modifies the list in place.
    """
    liked_set = set(user_prefs.get("liked_songs", []))

    scored = []
    for song in songs:
        if song["title"] in liked_set:
            continue
        pts, reasons = score_song(user_prefs, song, songs)
        scored.append((song, pts, " | ".join(reasons)))

    return sorted(scored, key=lambda x: x[1], reverse=True)[:k]