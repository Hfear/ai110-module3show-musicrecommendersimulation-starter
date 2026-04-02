# Model Card: Music Recommender Simulation

## 1. Model Name

**VibeFinder 1.0**

---

## 2. Intended Use and Non-Intended Use

**Intended for:**
Best used as a favorites-based playlist builder — it works well when a user has already listened to a variety of music and has clear preferences.

**Not intended for:**
Not reliable for users who mostly listen to one genre, or for discovering music in genres they've rarely explored — the small catalog and genre weighting mean those users get repetitive or mismatched results.

---

## 3. How the Model Works

The system looks at the songs you already like and builds an average picture of your taste — how energetic those songs are, how acoustic they sound, and what genre and mood come up most often. It then goes through every other song in the catalog and gives each one a score based on how close it is to that picture. Songs that match your most common genre get the most points. Songs that match your mood get the next most. Then energy and texture fill in the rest. If a song shares a genre or mood with any of your liked songs, it also gets a small bonus. The songs are sorted by score and the top five are returned.

---

## 4. Data

- 20 songs total in data/songs.csv (expanded from 10 in the starter)
- 13 genres: lofi, pop, rock, ambient, jazz, synthwave, indie pop, hip-hop, r&b, classical, metal, country, electronic
- 11 moods: chill, happy, intense, focused, relaxed, moody, energetic, sad, angry, nostalgic, romantic
- 10 songs were added manually to cover gaps in genre and mood diversity
- The catalog is still very small — only 1 to 2 songs per genre in most cases
- No real user listening data was used; all songs and features were generated for simulation

---

## 5. Strengths

- The chill lofi profile worked very well — Spacewalk Thoughts ranked first because it matched the chill mood and had very similar energy and acousticness to the liked songs, even though it is ambient not lofi
- The cold start profile (no liked songs) still returned reasonable results by falling back to the explicit genre and mood fields
- The reasons output makes it easy to see exactly why each song ranked where it did, which makes the system transparent and easy to debug

---

## 6. Limitations and Bias

The system over-prioritizes genre at a weight of 0.35, which means a song in the wrong genre gets a large automatic penalty even if its energy, mood, and texture are a perfect match. This became obvious in the High-Energy Pop profile: all three liked songs were already in the catalog, so the system could not recommend any pop songs. The top result was a rock song that scored well on energy and mood proximity but had no genre match at all, making the genre weight irrelevant for that profile.

The catalog is too small to provide meaningful variety. With only 1 song per genre in most cases, the system frequently falls back to energy proximity as the tiebreaker, which means songs from very different styles end up clustered together just because they have similar tempos.

The mood labels are assigned manually and subjectively. "Intense" appears on both a rock song and a pop workout song, which causes the system to treat them as equivalent in the mood dimension even though they feel very different as listening experiences.

The conflicting profile (high energy plus sad mood) exposed a gap: the only high-energy sad song in the catalog is Rainy Season, which is r&b and low energy. The system instead recommended Slow Burn Letter — same genre, but very low energy — because genre weight (0.35) dominated over the energy mismatch. A user who actually wants something loud and dark got something soft and melancholy.

The liked-song bonus slightly double-counts genre and mood, amplifying the genre bias for users with consistent taste and doing almost nothing for users with mixed taste.

---

## 7. Evaluation Process

Six profiles were tested: three standard listeners and three adversarial edge cases designed to break the system.

**Profile 1 — High-Energy Pop Fan**
Expected: Happy, high-energy pop songs. Reality: Zero pop songs — all liked songs were already in the catalog. Storm Runner (rock) ranked #1 purely by energy.

**Profile 2 — Chill Lofi Listener**
Expected: Mellow, low-energy lofi-style songs. Reality: Matched well. Spacewalk Thoughts (ambient/chill) ranked #1 — different genre but same vibe. Most accurate result of all six.

**Profile 3 — Deep Intense Rock Fan**
Expected: High-energy rock songs. Reality: Gym Hero (pop) ranked #1 because it shared the "intense" mood and 0.93 energy. Right feel, wrong genre.

**Edge Case A — High Energy + Sad Mood**
Expected: Something loud and dark. Reality: Slow Burn Letter (r&b, romantic, low energy 0.44) ranked #1 — genre match dominated and completely overrode the energy and mood mismatch.

**Edge Case B — Cold Start (no liked songs)**
Expected: System might break or return random results. Reality: Worked. Spacewalk Thoughts ranked #1 for an ambient/focused user. The fallback to explicit preferences held up.

**Edge Case C — Mixed Taste (3 different genres liked)**
Expected: Unclear results since taste is scattered. Reality: Concrete Garden (hip-hop) ranked #1 because hip-hop appeared in liked songs. Results were spread across genres with no strong pattern — energy was the main tiebreaker.

**Weight Experiment:** Doubling energy and halving genre weight produced the same ranking order for the pop fan. Energy was already the dominant signal — changing the weight only raised the scores, not the order.

---

## 8. Future Work

- Add more songs per genre so the system has real variety to choose from, not just the least-bad option
- Introduce a diversity penalty so the top 5 results cannot all be from the same genre or energy band
- Add tempo and valence as scoring features to better separate songs that have the same energy but a different feel
- Allow the user to give negative feedback — "never recommend metal" — as an exclusion filter
- Replace manual mood labels with a multi-label system so a song can be both intense and moody

---

## 9. Personal Reflection

Through this assignment I learned how you need to make your algorithms very dynamic and be sure to have factors from multiple sectors to account for human nuance. Even if I have a correct algo, it needs to accurately reflect human nature. We are attracted to certain features and not only exact genres or numbers, and we need to be able to understand this first to write something that reflects that.
AI tools helped do a lot of the syntax and coding, but their recommendations for the algo were far too granular and had no vision of how people's personal tastes could be reflected in music, and this made equations that were too stiff.
Pattern recognition can feel like the program is reading your mind, but really it's just fine-tuned guesses that are padded with information.
If I extended this project, I would want to have a recommended radio list based on a specific song, like how Spotify has implemented. I think that is a better way to do recommendations.
