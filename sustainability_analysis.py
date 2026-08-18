import pandas as pd
import numpy as np

df = pd.read_csv("data/processed/cleaned_south_korea.csv")

df["date"] = pd.to_datetime(df["date"])

df = df.sort_values(["song_id", "date"])


results = []


for song_id, group in df.groupby("song_id"):

    group = group.sort_values("date").copy()

    dates = sorted(group["date"].unique())

    if len(dates) < 2:
        continue

    song = group["song"].iloc[0]
    artist = group["artist"].iloc[0]

    first_entry_date = dates[0]

    first_entry_data = group[
        group["date"] == first_entry_date
    ].iloc[0]

    first_entry_rank = first_entry_data["position"]

    first_entry_popularity = first_entry_data["popularity"]


    runs = []

    current_run = [dates[0]]

    for i in range(1, len(dates)):

        gap = (
            pd.Timestamp(dates[i])
            - pd.Timestamp(dates[i - 1])
        ).days

        if gap == 1:
            current_run.append(dates[i])
        else:
            runs.append(current_run)
            current_run = [dates[i]]

    runs.append(current_run)


    if len(runs) <= 1:
        continue


    first_run = runs[0]


    first_run_data = group[
        group["date"].isin(first_run)
    ]

    first_entry_retention = len(first_run)

    first_entry_peak_rank = (
        first_run_data["position"].min()
    )

    first_entry_average_rank = (
        first_run_data["position"].mean()
    )

    first_entry_average_popularity = (
        first_run_data["popularity"].mean()
    )


    for run_number, run in enumerate(runs[1:], start=1):

        run_data = group[
            group["date"].isin(run)
        ].copy()

        run_data = run_data.sort_values("date")


        reentry_date = run[0]

        reentry_row = run_data.iloc[0]

        reentry_rank = reentry_row["position"]

        reentry_popularity = reentry_row["popularity"]


        peak_rank = run_data["position"].min()

        peak_row = run_data.loc[
            run_data["position"].idxmin()
        ]

        peak_date = peak_row["date"]


        retention_days = len(run)


        average_rank = run_data["position"].mean()

        average_popularity = run_data["popularity"].mean()


        days_to_peak = (
            pd.Timestamp(peak_date)
            - pd.Timestamp(reentry_date)
        ).days


        peak_improvement = (
            reentry_rank - peak_rank
        )


        if days_to_peak > 0:

            rank_recovery_speed = (
                peak_improvement / days_to_peak
            )

        else:

            rank_recovery_speed = peak_improvement


        rank_decay = (
            run_data["position"].iloc[-1]
            - peak_rank
        )


        rank_stability = run_data["position"].std()

        if pd.isna(rank_stability):
            rank_stability = 0


        results.append({

            "song_id": song_id,

            "song": song,

            "artist": artist,

            "comeback_number": run_number,

            "reentry_date": reentry_date,

            "reentry_rank": reentry_rank,

            "reentry_popularity": reentry_popularity,

            "peak_rank": peak_rank,

            "peak_date": peak_date,

            "retention_days": retention_days,

            "average_rank": average_rank,

            "average_popularity": average_popularity,

            "rank_decay": rank_decay,

            "days_to_peak": days_to_peak,

            "rank_recovery_speed": rank_recovery_speed,

            "rank_stability": rank_stability,

            "first_entry_rank": first_entry_rank,

            "first_entry_popularity": first_entry_popularity,

            "first_entry_peak_rank": first_entry_peak_rank,

            "first_entry_retention_days": first_entry_retention,

            "first_entry_average_rank": first_entry_average_rank,

            "first_entry_average_popularity": first_entry_average_popularity,

            "rank_improvement_vs_first_entry": (
                first_entry_rank - reentry_rank
            ),

            "peak_improvement_vs_first_entry": (
                first_entry_peak_rank - peak_rank
            ),

            "retention_change_vs_first_entry": (
                retention_days - first_entry_retention
            )
        })


sustainability_df = pd.DataFrame(results)


print("=" * 70)
print("STEP 14: MOMENTUM SUSTAINABILITY ANALYSIS")
print("=" * 70)


print(
    "\nTotal comeback events:",
    len(sustainability_df)
)


print(
    "Unique songs with comebacks:",
    sustainability_df["song_id"].nunique()
    if len(sustainability_df) > 0 else 0
)


if len(sustainability_df) > 0:

    print(
        "\nAverage Post-Comeback Retention:",
        round(
            sustainability_df[
                "retention_days"
            ].mean(),
            2
        ),
        "days"
    )

    print(
        "Average Rank Decay:",
        round(
            sustainability_df[
                "rank_decay"
            ].mean(),
            2
        )
    )

    print(
        "Average Rank Stability:",
        round(
            sustainability_df[
                "rank_stability"
            ].mean(),
            2
        )
    )

    print(
        "Average Rank Improvement vs First Entry:",
        round(
            sustainability_df[
                "rank_improvement_vs_first_entry"
            ].mean(),
            2
        )
    )

    print(
        "Average Peak Improvement vs First Entry:",
        round(
            sustainability_df[
                "peak_improvement_vs_first_entry"
            ].mean(),
            2
        )
    )


    print("\nTOP COMEBACKS BY RETENTION")

    print(
        sustainability_df[
            [
                "song",
                "artist",
                "reentry_date",
                "retention_days",
                "peak_rank",
                "rank_decay"
            ]
        ]
        .sort_values(
            "retention_days",
            ascending=False
        )
        .head(20)
        .to_string(index=False)
    )


    print(
        "\nTOP COMEBACKS BY PEAK IMPROVEMENT"
    )

    print(
        sustainability_df[
            [
                "song",
                "artist",
                "reentry_date",
                "reentry_rank",
                "peak_rank",
                "first_entry_peak_rank",
                "peak_improvement_vs_first_entry"
            ]
        ]
        .sort_values(
            "peak_improvement_vs_first_entry",
            ascending=False
        )
        .head(20)
        .to_string(index=False)
    )


output_file = (
    "data/processed/sustainability_analysis.csv"
)

sustainability_df.to_csv(
    output_file,
    index=False
)


print(
    "\nSustainability analysis saved to:"
)

print(output_file)


print("\n" + "=" * 70)

print("STEP 14 COMPLETED")

print("=" * 70)