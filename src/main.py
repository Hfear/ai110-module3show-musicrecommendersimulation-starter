"""
Music Recommender Simulation — main runner
"""

from src.recommender import load_songs, recommend_songs


def main() -> None:
    songs = load_songs("data/songs.csv")

    # --- User profile: dictionary base + liked songs bonus ---
    user_prefs = {
        "genre": "pop",
        "mood": "happy",
        "energy": 0.8,
        "liked_songs": ["Sunrise City", "Rooftop Lights", "Gym Hero"],
    }

    print("=" * 50)
    print("User Profile")
    print("=" * 50)
    print(f"  Genre:       {user_prefs['genre']}")
    print(f"  Mood:        {user_prefs['mood']}")
    print(f"  Energy:      {user_prefs['energy']}")
    print(f"  Liked songs: {', '.join(user_prefs['liked_songs'])}")
    print()

    recommendations = recommend_songs(user_prefs, songs, k=5)

    print("Top Recommendations")
    print("=" * 50)
    for i, (song, score, explanation) in enumerate(recommendations, 1):
        print(f"{i}. {song['title']} by {song['artist']}")
        print(f"   Genre: {song['genre']} | Mood: {song['mood']} | Energy: {song['energy']}")
        print(f"   Score: {score:.4f}")
        print(f"   Why:   {explanation}")
        print()


if __name__ == "__main__":
    main()