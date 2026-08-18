import pandas as pd

cleaned = pd.read_csv("data/processed/cleaned_south_korea.csv")
reentry = pd.read_csv("data/processed/reentry_analysis.csv")
momentum = pd.read_csv("data/processed/momentum_analysis.csv")
sustainability = pd.read_csv("data/processed/sustainability_analysis.csv")
fandom = pd.read_csv("data/processed/fandom_intensity_analysis.csv")

print("\n" + "=" * 70)
print("STEP 16: FINAL PROJECT ANALYSIS")
print("=" * 70)

print("\nDATASET SUMMARY")
print("Total cleaned records:", len(cleaned))
print("Unique songs:", cleaned["song"].nunique())
print("Unique artists:", cleaned["artist"].nunique())
print("Date range:", cleaned["date"].min(), "to", cleaned["date"].max())

print("\nANALYSIS FILES")
print("Re-entry records:", len(reentry))
print("Momentum records:", len(momentum))
print("Sustainability records:", len(sustainability))
print("Fandom records:", len(fandom))

print("\nTOP 10 ARTISTS BY FANDOM INTENSITY")

print(
    fandom[
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
    ].head(10).to_string(index=False)
)

print("\nTOP 10 SONGS BY MOMENTUM")

if "momentum_score" in momentum.columns:
    print(
        momentum[
            ["song", "artist", "momentum_score"]
        ].sort_values(
            "momentum_score",
            ascending=False
        ).head(10).to_string(index=False)
    )

print("\nTOP 10 COMEBACKS BY IMPROVEMENT")

if "peak_improvement_vs_first_entry" in sustainability.columns:
    print(
        sustainability[
            [
                "song",
                "artist",
                "reentry_date",
                "reentry_rank",
                "peak_rank",
                "peak_improvement_vs_first_entry"
            ]
        ].sort_values(
            "peak_improvement_vs_first_entry",
            ascending=False
        ).head(10).to_string(index=False)
    )

summary = pd.DataFrame({
    "metric": [
        "Total Records",
        "Unique Songs",
        "Unique Artists",
        "Re-entry Records",
        "Momentum Records",
        "Sustainability Records",
        "Fandom Records"
    ],
    "value": [
        len(cleaned),
        cleaned["song"].nunique(),
        cleaned["artist"].nunique(),
        len(reentry),
        len(momentum),
        len(sustainability),
        len(fandom)
    ]
})

summary.to_csv(
    "data/processed/project_summary.csv",
    index=False
)

print("\nFinal project summary saved to:")
print("data/processed/project_summary.csv")

print("\n" + "=" * 70)
print("STEP 16 COMPLETED")
print("=" * 70)