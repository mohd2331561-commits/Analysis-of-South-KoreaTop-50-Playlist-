import pandas as pd

df = pd.read_csv("data/processed/cleaned_south_korea.csv")

df["date"] = pd.to_datetime(df["date"])

df = df.sort_values(["song_id", "date"])

results = []

for song_id, group in df.groupby("song_id"):

    group = group.sort_values("date")

    dates = sorted(group["date"].unique())

    first_entry = dates[0]
    last_entry = dates[-1]

    chart_days = len(dates)

    reentry_dates = []
    exit_gaps = []

    previous_date = dates[0]

    for current_date in dates[1:]:

        gap = (current_date - previous_date).days

        if gap > 1:
            reentry_dates.append(current_date)
            exit_gaps.append(gap - 1)

        previous_date = current_date

    reentry_count = len(reentry_dates)

    song_name = group["song"].iloc[0]
    artist_name = group["artist"].iloc[0]

    results.append({
        "song_id": song_id,
        "song": song_name,
        "artist": artist_name,
        "first_entry_date": first_entry,
        "last_entry_date": last_entry,
        "chart_days": chart_days,
        "reentry_count": reentry_count,
        "reentry_dates": ", ".join(
            date.strftime("%Y-%m-%d")
            for date in reentry_dates
        ),
        "exit_gap_days": ", ".join(
            str(gap)
            for gap in exit_gaps
        )
    })

reentry_df = pd.DataFrame(results)

reentry_df = reentry_df.sort_values(
    ["reentry_count", "chart_days"],
    ascending=[False, False]
)

print("=" * 70)
print("CHART RE-ENTRY ANALYSIS")
print("=" * 70)

print("\nTotal unique songs:", len(reentry_df))

print(
    "\nSongs with at least one re-entry:",
    (reentry_df["reentry_count"] > 0).sum()
)

print(
    "\nSongs with no re-entry:",
    (reentry_df["reentry_count"] == 0).sum()
)

print("\nTop 20 Songs by Re-entry Count")

print(
    reentry_df[
        [
            "song",
            "artist",
            "reentry_count",
            "chart_days",
            "reentry_dates",
            "exit_gap_days"
        ]
    ].head(20).to_string(index=False)
)

output_file = "data/processed/reentry_analysis.csv"

reentry_df.to_csv(
    output_file,
    index=False
)

print("\nRe-entry analysis saved to:")
print(output_file)

print("\n" + "=" * 70)
print("RE-ENTRY ANALYSIS COMPLETED")
print("=" * 70)