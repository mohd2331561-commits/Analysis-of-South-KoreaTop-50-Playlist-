import pandas as pd
import numpy as np

INPUT_FILE = "data/processed/cleaned_south_korea.csv"
OUTPUT_FILE = "data/processed/fandom_intensity_analysis.csv"

df = pd.read_csv(INPUT_FILE)

df["date"] = pd.to_datetime(df["date"])

artist_stats = df.groupby("artist").agg(
    songs=("song", "nunique"),
    chart_entries=("song", "count"),
    avg_rank=("position", "mean"),
    best_rank=("position", "min"),
    avg_popularity=("popularity", "mean"),
    peak_popularity=("popularity", "max")
).reset_index()

artist_stats["chart_strength"] = (
    (101 - artist_stats["avg_rank"]) +
    artist_stats["avg_popularity"]
) / 2

artist_stats["fandom_intensity"] = (
    artist_stats["chart_strength"] *
    np.log1p(artist_stats["chart_entries"])
)

artist_stats = artist_stats.sort_values(
    "fandom_intensity",
    ascending=False
).reset_index(drop=True)

artist_stats["fandom_rank"] = artist_stats.index + 1

print("\n" + "=" * 70)
print("STEP 15: FANDOM INTENSITY ANALYSIS")
print("=" * 70)

print("\nTOP 20 ARTISTS BY FANDOM INTENSITY")

print(
    artist_stats[
        [
            "fandom_rank",
            "artist",
            "songs",
            "chart_entries",
            "avg_rank",
            "best_rank",
            "avg_popularity",
            "fandom_intensity"
        ]
    ].head(20).to_string(index=False)
)

song_stats = df.groupby(
    ["song", "artist"]
).agg(
    chart_entries=("song", "count"),
    best_rank=("position", "min"),
    avg_rank=("position", "mean"),
    avg_popularity=("popularity", "mean")
).reset_index()

song_stats["song_fandom_intensity"] = (
    ((101 - song_stats["avg_rank"]) +
     song_stats["avg_popularity"]) / 2
    * np.log1p(song_stats["chart_entries"])
)

song_stats = song_stats.sort_values(
    "song_fandom_intensity",
    ascending=False
).reset_index(drop=True)

print("\nTOP 20 SONGS BY FANDOM INTENSITY")

print(
    song_stats[
        [
            "song",
            "artist",
            "chart_entries",
            "best_rank",
            "avg_rank",
            "avg_popularity",
            "song_fandom_intensity"
        ]
    ].head(20).to_string(index=False)
)

artist_stats.to_csv(OUTPUT_FILE, index=False)

print("\nFandom intensity analysis saved to:")
print(OUTPUT_FILE)

print("\n" + "=" * 70)
print("STEP 15 COMPLETED")
print("=" * 70)