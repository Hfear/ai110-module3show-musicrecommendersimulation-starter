"""
Music Recommender Simulation — main runner

Runs multiple user profiles to stress-test the scoring logic,
then runs one weight-shift experiment (double energy / halve genre).
"""

from src.recommender import load_songs, recommend_songs, score_song, WEIGHTS


def print_profile(label: str, user_prefs: dict, recommendations: list) -> None:
    """Print a clean terminal block for one profile's results."""
    print()
    print("=" * 55)
    print(f"  {label}")
    print("=" * 55)
    print(f"  Genre: {user_prefs.get('genre')}  |  Mood: {user_prefs.get('mood')}  |  Energy: {user_prefs.get('energy')}")
    liked = user_prefs.get("liked_songs", [])
    if liked:
        print(f"  Liked: {', '.join(liked)}")
    print()
    for i, (song, score, reasons_str) in enumerate(recommendations, 1):
        print(f"  {i}. {song['title']} by {song['artist']}")
        print(f"     {song['genre']} / {song['mood']} / energy {song['energy']}")
        print(f"     Score: {score:.4f}")
        for reason in reasons_str.split(" | "):
            print(f"       - {reason}")
        print()


def main() -> None:
    songs = load_songs("data/songs.csv")
    print(f"Loaded songs: {len(songs)}")

    # ------------------------------------------------------------------
    # Profile 1 — High-Energy Pop fan
    # ------------------------------------------------------------------
    pop_fan = {
        "genre": "pop",
        "mood": "happy",
        "energy": 0.8,
        "liked_songs": ["Sunrise City", "Rooftop Lights", "Gym Hero"],
    }

    # ------------------------------------------------------------------
    # Profile 2 — Chill Lofi listener
    # ------------------------------------------------------------------
    lofi_listener = {
        "genre": "lofi",
        "mood": "chill",
        "energy": 0.38,
        "liked_songs": ["Midnight Coding", "Library Rain", "Focus Flow"],
    }

    # ------------------------------------------------------------------
    # Profile 3 — Deep Intense Rock fan
    # ------------------------------------------------------------------
    rock_fan = {
        "genre": "rock",
        "mood": "intense",
        "energy": 0.92,
        "liked_songs": ["Storm Runner", "Iron Current"],
    }

    # ------------------------------------------------------------------
    # Edge case A — Conflicting prefs: high energy but sad mood
    # (adversarial: can the system handle a user who wants aggressive
    #  sound but dark emotional tone?)
    # ------------------------------------------------------------------
    conflicted = {
        "genre": "r&b",
        "mood": "sad",
        "energy": 0.88,
        "liked_songs": ["Rainy Season"],
    }

    # ------------------------------------------------------------------
    # Edge case B — No liked songs at all (cold start)
    # (adversarial: what happens with zero context?)
    # ------------------------------------------------------------------
    cold_start = {
        "genre": "ambient",
        "mood": "focused",
        "energy": 0.3,
        "liked_songs": [],
    }

    # ------------------------------------------------------------------
    # Edge case C — Every liked song is a different genre (mixed taste)
    # (adversarial: does the system collapse or spread results?)
    # ------------------------------------------------------------------
    mixed_taste = {
        "genre": "jazz",
        "mood": "relaxed",
        "energy": 0.5,
        "liked_songs": ["Coffee Shop Stories", "Night Drive Loop", "Back Block Anthem"],
    }

    profiles = [
        ("Profile 1: High-Energy Pop Fan",       pop_fan),
        ("Profile 2: Chill Lofi Listener",        lofi_listener),
        ("Profile 3: Deep Intense Rock Fan",      rock_fan),
        ("Edge Case A: High Energy + Sad Mood",   conflicted),
        ("Edge Case B: Cold Start (no liked)",    cold_start),
        ("Edge Case C: Mixed Taste (3 genres)",   mixed_taste),
    ]

    for label, prefs in profiles:
        recs = recommend_songs(prefs, songs, k=5)
        print_profile(label, prefs, recs)

    # ------------------------------------------------------------------
    # Weight experiment: double energy weight, halve genre weight
    # Tests system sensitivity — do rankings shift meaningfully?
    # Original: genre=0.35, energy=0.25
    # Experiment: genre=0.175, energy=0.50  (remaining weights unchanged)
    # ------------------------------------------------------------------
    print()
    print("=" * 55)
    print("  EXPERIMENT: Double Energy / Halve Genre Weight")
    print("  Original:   genre=0.35  energy=0.25")
    print("  Modified:   genre=0.175 energy=0.50")
    print("=" * 55)

    original_weights = dict(WEIGHTS)
    import src.recommender as rec_module
    rec_module.WEIGHTS["genre"]  = 0.175
    rec_module.WEIGHTS["energy"] = 0.50

    recs_exp = recommend_songs(pop_fan, songs, k=5)
    print_profile("Pop Fan — Experimental Weights", pop_fan, recs_exp)

    # Restore original weights
    rec_module.WEIGHTS.update(original_weights)
    print("  (weights restored to original)")
    print()


if __name__ == "__main__":
    main()
