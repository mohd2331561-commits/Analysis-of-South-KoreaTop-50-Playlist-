import pandas as pd
import numpy as np

df = pd.read_csv("data/processed/cleaned_south_korea.csv")

df["date"] = pd.to_datetime(df["date"])

df = df.sort_values(["song_id", "date"])

results = []

for song_id, group in df.groupby("song_id"):

    group = group.sort_values("date").reset_index(drop=True)

    if len(group) < 2:
        continue

    for i in range(1, len(group)):

        current = group.iloc[i]
        previous = group.iloc[i - 1]

        gap = (current["date"] - previous["date"]).days

        if gap > 1:

            reentry_date = current["date"]

            previous_rank = previous["position"]
            reentry_rank = current["position"]

            rank_jump = previous_rank - reentry_rank

            previous_popularity = previous["popularity"]
            reentry_popularity = current["popularity"]

            popularity_change = (
                reentry_popularity - previous_popularity
            )

            popularity_change_rate = (
                popularity_change / previous_popularity * 100
                if previous_popularity != 0
                else 0
            )

            future = group[
                group["date"] >= reentry_date
            ].copy()

            future = future.sort_values("date")

            peak_rank = future["position"].min()

            peak_row = future.loc[
                future["position"].idxmin()
            ]

            peak_date = peak_row["date"]

            retention_days = (
                future["date"].max() - reentry_date
            ).days + 1

            peak_improvement = (
                reentry_rank - peak_rank
            )

            rank_recovery_speed = (
                peak_improvement / max(
                    (peak_date - reentry_date).days,
                    1
                )
            )

            rank_values = future["position"].values

            if len(rank_values) > 1:
                rank_volatility = np.std(
                    np.diff(rank_values)
                )
            else:
                rank_volatility = 0

            momentum_score = (
                max(rank_jump, 0) * 0.30
                + max(popularity_change_rate, 0) * 0.25
                + max(peak_improvement, 0) * 0.25
                + rank_recovery_speed * 0.20
            )

            results.append({

                "song_id": song_id,

                "song": current["song"],

                "artist": current["artist"],

                "reentry_date": reentry_date,

                "previous_rank": previous_rank,

                "reentry_rank": reentry_rank,

                "rank_jump": rank_jump,

                "previous_popularity": previous_popularity,

                "reentry_popularity": reentry_popularity,

                "popularity_change": popularity_change,

                "popularity_change_rate": popularity_change_rate,

                "peak_rank_after_reentry": peak_rank,

                "peak_date": peak_date,

                "peak_improvement": peak_improvement,

                "retention_days": retention_days,

                "rank_recovery_speed": rank_recovery_speed,

                "rank_volatility": rank_volatility,

                "momentum_score": momentum_score
            })


momentum_df = pd.DataFrame(results)


if len(momentum_df) > 0:

    momentum_df = momentum_df.sort_values(
        "momentum_score",
        ascending=False
    )


print("=" * 70)
print("STEP 13: MOMENTUM SPIKE ANALYSIS")
print("=" * 70)

print(
    "\nTotal comeback events:",
    len(momentum_df)
)


if len(momentum_df) > 0:

    print(
        "\nAverage Momentum Score:",
        round(momentum_df["momentum_score"].mean(), 2)
    )

    print(
        "Average Rank Jump:",
        round(momentum_df["rank_jump"].mean(), 2)
    )

    print(
        "Average Popularity Change Rate:",
        round(
            momentum_df["popularity_change_rate"].mean(),
            2
        ),
        "%"
    )

    print(
        "Average Retention Days:",
        round(
            momentum_df["retention_days"].mean(),
            2
        )
    )

    print(
        "\nTOP 20 COMEBACK EVENTS BY MOMENTUM SCORE"
    )

    print(
        momentum_df[
            [
                "song",
                "artist",
                "reentry_date",
                "rank_jump",
                "popularity_change_rate",
                "peak_rank_after_reentry",
                "retention_days",
                "rank_volatility",
                "momentum_score"
            ]
        ].head(20).to_string(index=False)
    )


output_file = (
    "data/processed/momentum_analysis.csv"
)

momentum_df.to_csv(
    output_file,
    index=False
)


print("\nMomentum analysis saved to:")

print(output_file)

print("\n" + "=" * 70)

print("STEP 13 COMPLETED")

print("=" * 70)