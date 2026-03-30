# 🎵 Music Recommender Simulation

## Project Summary

In this project you will build and explain a small music recommender system.

Your goal is to:

- Represent songs and a user "taste profile" as data
- Design a scoring rule that turns that data into recommendations
- Evaluate what your system gets right and wrong
- Reflect on how this mirrors real world AI recommenders

DESCP:
First we build a quick profile of the user from the songs they already like. That profile lets us rank new songs against their favorites and find music that aligns with their vibe, even if it’s in a completely different genre.

---

## How The System Works

- We look at the songs a user already likes and build a quick profile from them
- That profile is just the average feel of their liked songs: average energy, average acousticness, most common genre, most common mood
- We then score every other song in the catalog by how close it is to that profile
- Songs that match the genre or mood of the liked songs score higher
- Songs that feel similar in energy and texture also score higher, even if the genre is different
- We rank all the scores and return the top matches

### Song features

- genre - style of the track (lofi, pop, rock, jazz, ambient, synthwave, indie pop)
- mood - emotional feel (chill, happy, intense, focused, relaxed, moody)
- energy - how driving or mellow the song is (0 to 1)
- acousticness - how organic vs produced the sound is (0 to 1)
- valence - how bright or dark the song feels (0 to 1)

### UserProfile (built from liked songs, not filled in manually)

- Average energy of liked songs
- Average acousticness of liked songs
- Most common genre across liked songs
- Most common mood across liked songs
- The original liked songs list (used for soft frequency scoring)

---

## Getting Started

### Project Structure

```
music-recommender/
├── data/
│   └── songs.csv          # song catalog (10 songs)
├── src/
│   ├── main.py            # entry point
│   └── recommender.py     # Song, UserProfile, Recommender classes
├── tests/
│   └── test_recommender.py
├── model_card.md
├── requirements.txt
└── README.md
```

### Setup

1. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv .venv
   source .venv/bin/activate      # Mac or Linux
   .venv\Scripts\activate         # Windows

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Run the app:

```bash
python -m src.main
```

### Running Tests

Run the starter tests with:

```bash
pytest
```

You can add more tests in `tests/test_recommender.py`.

---

## Experiments You Tried

Use this section to document the experiments you ran. For example:

- What happened when you changed the weight on genre from 2.0 to 0.5
- What happened when you added tempo or valence to the score
- How did your system behave for different types of users

---

## Limitations and Risks

Summarize some limitations of your recommender.

Examples:

- It only works on a tiny catalog
- It does not understand lyrics or language
- It might over favor one genre or mood

You will go deeper on this in your model card.

---

## Reflection

Read and complete `model_card.md`:

[**Model Card**](model_card.md)

Write 1 to 2 paragraphs here about what you learned:

- about how recommenders turn data into predictions
- about where bias or unfairness could show up in systems like this


---
