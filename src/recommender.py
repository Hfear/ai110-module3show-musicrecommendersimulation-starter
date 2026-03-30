from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass, field
import csv

@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
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
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool
    liked_songs: List[str] = field(default_factory=list)  # song titles the user already likes


# --- Scoring weights ---
WEIGHTS = {
    "genre":        0.35,
    "mood":         0.25,
    "energy":       0.25,
    "acousticness": 0.15,
}
LIKED_BONUS = 0.10  # bonus added when a candidate matches genre/mood of a liked song


def _score_song_dict(song: Dict, user_prefs: Dict, all_songs: List[Dict]) -> Tuple[float, str]:
    """
    Score a single song dict against a user_prefs dict.
    Returns (score, explanation).
    """
    reasons = []

    # Derive liked-song context if provided
    liked_titles = set(user_prefs.get("liked_songs", []))
    liked = [s for s in all_songs if s["title"] in liked_titles]

    # Soft genre/mood frequency from liked songs
    if liked:
        genre_freq = sum(1 for s in liked if s["genre"] == song["genre"]) / len(liked)
        mood_freq  = sum(1 for s in liked if s["mood"]  == song["mood"])  / len(liked)
        avg_energy = sum(s["energy"] for s in liked) / len(liked)
        avg_acous  = sum(s["acousticness"] for s in liked) / len(liked)
    else:
        # Fall back to explicit profile values
        genre_freq = 1.0 if song["genre"] == user_prefs.get("genre", "") else 0.0
        mood_freq  = 1.0 if song["mood"]  == user_prefs.get("mood",  "") else 0.0
        avg_energy = user_prefs.get("energy", 0.5)
        avg_acous  = 0.2 if not user_prefs.get("likes_acoustic", False) else 0.8

    # Core score
    genre_score = WEIGHTS["genre"]        * genre_freq
    mood_score  = WEIGHTS["mood"]         * mood_freq
    energy_score = WEIGHTS["energy"]      * (1.0 - abs(song["energy"] - avg_energy))
    acous_score  = WEIGHTS["acousticness"]* (1.0 - abs(song["acousticness"] - avg_acous))

    score = genre_score + mood_score + energy_score + acous_score

    # Liked-songs bonus: small boost when genre OR mood matches a liked song
    bonus = 0.0
    if liked and (genre_freq > 0 or mood_freq > 0):
        bonus = LIKED_BONUS * max(genre_freq, mood_freq)
        score += bonus

    # Build plain-English explanation
    if genre_freq > 0:
        reasons.append(f"genre match ({song['genre']})")
    if mood_freq > 0:
        reasons.append(f"mood match ({song['mood']})")
    energy_diff = abs(song["energy"] - avg_energy)
    if energy_diff < 0.15:
        reasons.append(f"energy is close ({song['energy']:.2f} vs target {avg_energy:.2f})")
    if bonus > 0:
        reasons.append("similar to your liked songs")
    if not reasons:
        reasons.append("closest available match by audio features")

    explanation = ", ".join(reasons)
    return round(score, 4), explanation


class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def _to_dict(self, song: Song) -> Dict:
        return {
            "title": song.title, "genre": song.genre, "mood": song.mood,
            "energy": song.energy, "acousticness": song.acousticness,
        }

    def _user_prefs(self, user: UserProfile) -> Dict:
        return {
            "genre": user.favorite_genre,
            "mood":  user.favorite_mood,
            "energy": user.target_energy,
            "likes_acoustic": user.likes_acoustic,
            "liked_songs": user.liked_songs,
        }

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        prefs = self._user_prefs(user)
        all_dicts = [self._to_dict(s) for s in self.songs]
        liked_titles = set(user.liked_songs)

        scored = []
        for song in self.songs:
            if song.title in liked_titles:
                continue  # don't recommend songs they already like
            score, _ = _score_song_dict(self._to_dict(song), prefs, all_dicts)
            scored.append((song, score))

        scored.sort(key=lambda x: x[1], reverse=True)
        return [song for song, _ in scored[:k]]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        prefs = self._user_prefs(user)
        all_dicts = [self._to_dict(s) for s in self.songs]
        _, explanation = _score_song_dict(self._to_dict(song), prefs, all_dicts)
        return explanation


def load_songs(csv_path: str) -> List[Dict]:
    """
    Loads songs from a CSV file.
    Required by src/main.py
    """
    songs = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
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
    """
    Functional implementation of the recommendation logic.
    Required by src/main.py
    Expected return format: (song_dict, score, explanation)
    """
    liked_titles = set(user_prefs.get("liked_songs", []))
    results = []
    for song in songs:
        if song["title"] in liked_titles:
            continue
        score, explanation = _score_song_dict(song, user_prefs, songs)
        results.append((song, score, explanation))

    results.sort(key=lambda x: x[1], reverse=True)
    return results[:k]