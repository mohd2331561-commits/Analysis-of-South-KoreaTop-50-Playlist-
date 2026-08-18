import pandas as pd
import numpy as np

df = pd.read_csv("Atlantic_South_Korea.csv")

print("=" * 60)
print("SOUTH KOREA TOP 50 MUSIC ANALYSIS")
print("STEP 1: DATA VALIDATION")
print("=" * 60)

print("\n1. DATASET SHAPE")
print("Rows:", df.shape[0])
print("Columns:", df.shape[1])

print("\n2. COLUMN NAMES")
for column in df.columns:
    print("-", column)

print("\n3. FIRST 5 ROWS")
print(df.head().to_string())

print("\n4. DATA TYPES")
print(df.dtypes)

print("\n5. MISSING VALUES")
missing = df.isnull().sum()
print(missing)

print("\n6. TOTAL MISSING VALUES")
print(missing.sum())

print("\n7. DUPLICATE ROWS")
print("Duplicate rows:", df.duplicated().sum())

print("\n8. DATE CONVERSION")
df["date"] = pd.to_datetime(df["date"], dayfirst=True)

print("First date:", df["date"].min().date())
print("Last date:", df["date"].max().date())
print("Unique dates:", df["date"].nunique())

print("\n9. RECORDS PER DAY")
daily_counts = df.groupby("date").size()
print(daily_counts.value_counts().sort_index())

print("\n10. DATES NOT HAVING EXACTLY 50 RECORDS")
invalid_dates = daily_counts[daily_counts != 50]

if len(invalid_dates) == 0:
    print("All dates have exactly 50 records.")
else:
    print(invalid_dates)

print("\n11. POSITION VALIDATION")
print("Minimum position:", df["position"].min())
print("Maximum position:", df["position"].max())
print("Unique positions:", df["position"].nunique())

invalid_positions = df[
    (df["position"] < 1) |
    (df["position"] > 50)
]

print("Invalid position records:", len(invalid_positions))

print("\n12. SONG AND ARTIST COUNTS")
print("Unique songs:", df["song"].nunique())
print("Unique artists:", df["artist"].nunique())

print("\n13. POPULARITY VALIDATION")
print("Minimum popularity:", df["popularity"].min())
print("Maximum popularity:", df["popularity"].max())
print("Average popularity:", round(df["popularity"].mean(), 2))
print("Median popularity:", df["popularity"].median())

print("\n14. DURATION VALIDATION")
print("Minimum duration ms:", df["duration_ms"].min())
print("Maximum duration ms:", df["duration_ms"].max())

df["duration_minutes"] = df["duration_ms"] / 60000

print("Average duration minutes:",
      round(df["duration_minutes"].mean(), 2))

print("\n15. ALBUM TYPE")
print(df["album_type"].value_counts())

print("\n16. EXPLICIT CONTENT")
print(df["is_explicit"].value_counts())

print("\n17. SONG-ARTIST IDENTIFIER")

df["song_id"] = (
    df["song"].astype(str).str.strip()
    + " - "
    + df["artist"].astype(str).str.strip()
)

print("Unique song IDs:", df["song_id"].nunique())

print("\n18. DUPLICATES BY DATE AND POSITION")
date_position_duplicates = df.duplicated(
    subset=["date", "position"]
).sum()

print("Duplicate date-position records:",
      date_position_duplicates)

print("\n19. DUPLICATES BY DATE AND SONG")
date_song_duplicates = df.duplicated(
    subset=["date", "song_id"]
).sum()

print("Duplicate date-song records:",
      date_song_duplicates)

print("\n20. FINAL DATASET INFORMATION")
print(df.info())

print("\n" + "=" * 60)
print("DATA VALIDATION COMPLETED")
print("=" * 60)
print("\n" + "=" * 60)
print("STEP 2: DUPLICATE AND DAILY RECORD INVESTIGATION")
print("=" * 60)

print("\n1. RECORD COUNT FOR EVERY DATE")

daily_counts = df.groupby("date").size()

print("\nDates with MORE than 50 records:")
print(daily_counts[daily_counts > 50])

print("\nDates with LESS than 50 records:")
print(daily_counts[daily_counts < 50])

print("\nTotal dates with exactly 50 records:",
      (daily_counts == 50).sum())

print("Total dates with more than 50 records:",
      (daily_counts > 50).sum())

print("Total dates with less than 50 records:",
      (daily_counts < 50).sum())


print("\n2. DUPLICATE DATE-POSITION RECORDS")

duplicate_date_position = df[
    df.duplicated(
        subset=["date", "position"],
        keep=False
    )
].sort_values(["date", "position"])

print(duplicate_date_position[
    ["date", "position", "song", "artist"]
].to_string(index=False))


print("\n3. DUPLICATE DATE-SONG RECORDS")

duplicate_date_song = df[
    df.duplicated(
        subset=["date", "song_id"],
        keep=False
    )
].sort_values(["date", "song_id"])

print(duplicate_date_song[
    ["date", "position", "song", "artist", "song_id"]
].to_string(index=False))


print("\n4. DUPLICATE RECORD COUNT BY DATE")

duplicate_counts_by_date = (
    duplicate_date_position
    .groupby("date")
    .size()
)

print(duplicate_counts_by_date)


print("\n5. POSITION DISTRIBUTION FOR PROBLEMATIC DATES")

problem_dates = duplicate_counts_by_date.index

for problem_date in problem_dates:
    print("\nDate:", problem_date.date())

    temp = df[df["date"] == problem_date].sort_values("position")

    print(
        temp[
            ["position", "song", "artist"]
        ].to_string(index=False)
    )


print("\n" + "=" * 60)
print("DUPLICATE INVESTIGATION COMPLETED")
print("=" * 60)
print("\n" + "=" * 60)
print("STEP 2: DAILY RECORD AND DUPLICATE INVESTIGATION")
print("=" * 60)

daily_counts = df.groupby("date").size()

print("\n1. DAILY RECORD COUNTS")
print(daily_counts.value_counts().sort_index())

print("\n2. DATES WITH MORE THAN 50 RECORDS")
print(daily_counts[daily_counts > 50])

print("\n3. DATES WITH LESS THAN 50 RECORDS")
print(daily_counts[daily_counts < 50])

print("\n4. SUMMARY")
print("Dates with exactly 50 records:",
      (daily_counts == 50).sum())

print("Dates with more than 50 records:",
      (daily_counts > 50).sum())

print("Dates with less than 50 records:",
      (daily_counts < 50).sum())

print("\n5. DUPLICATE DATE-POSITION RECORDS")

duplicates_position = df[
    df.duplicated(
        subset=["date", "position"],
        keep=False
    )
].sort_values(["date", "position"])

print(
    duplicates_position[
        ["date", "position", "song", "artist"]
    ].to_string(index=False)
)

print("\n6. DUPLICATE DATE-SONG RECORDS")

duplicates_song = df[
    df.duplicated(
        subset=["date", "song_id"],
        keep=False
    )
].sort_values(["date", "song_id"])

print(
    duplicates_song[
        ["date", "position", "song", "artist"]
    ].to_string(index=False)
)

print("\n7. PROBLEMATIC DATES")

problem_dates = daily_counts[daily_counts != 50]

if len(problem_dates) == 0:
    print("No dates have an incorrect number of records.")
else:
    for date, count in problem_dates.items():
        print(
            date.strftime("%Y-%m-%d"),
            "->",
            count,
            "records"
        )

print("\n" + "=" * 60)
print("STEP 2 COMPLETED")
print("=" * 60)
print("\n" + "=" * 60)
print("STEP 2: DAILY RECORD AND DUPLICATE INVESTIGATION")
print("=" * 60)

daily_counts = df.groupby("date").size()

print("\n1. DAILY RECORD COUNTS")
print(daily_counts.value_counts().sort_index())

print("\n2. DATES WITH MORE THAN 50 RECORDS")
print(daily_counts[daily_counts > 50])

print("\n3. DATES WITH LESS THAN 50 RECORDS")
print(daily_counts[daily_counts < 50])

print("\n4. SUMMARY")
print("Dates with exactly 50 records:",
      (daily_counts == 50).sum())

print("Dates with more than 50 records:",
      (daily_counts > 50).sum())

print("Dates with less than 50 records:",
      (daily_counts < 50).sum())

print("\n5. DUPLICATE DATE-POSITION RECORDS")

duplicates_position = df[
    df.duplicated(
        subset=["date", "position"],
        keep=False
    )
].sort_values(["date", "position"])

print(
    duplicates_position[
        ["date", "position", "song", "artist"]
    ].to_string(index=False)
)

print("\n6. DUPLICATE DATE-SONG RECORDS")

duplicates_song = df[
    df.duplicated(
        subset=["date", "song_id"],
        keep=False
    )
].sort_values(["date", "song_id"])

print(
    duplicates_song[
        ["date", "position", "song", "artist"]
    ].to_string(index=False)
)

print("\n7. PROBLEMATIC DATES")

problem_dates = daily_counts[daily_counts != 50]

if len(problem_dates) == 0:
    print("No dates have an incorrect number of records.")
else:
    for date, count in problem_dates.items():
        print(
            date.strftime("%Y-%m-%d"),
            "->",
            count,
            "records"
        )

print("\n" + "=" * 60)
print("STEP 2 COMPLETED")
print("=" * 60)
print("\n" + "=" * 60)
print("STEP 3: DATA CLEANING")
print("=" * 60)

print("\nOriginal dataset rows:", len(df))

duplicate_date = pd.Timestamp("2025-03-01")

before = len(df)

df_clean = df[df["date"] != duplicate_date].copy()

duplicate_snapshot = df[df["date"] == duplicate_date].copy()

print("\nDuplicate date found:", duplicate_date.date())
print("Rows removed:", len(duplicate_snapshot))

print("\nRows after removing duplicate snapshot:", len(df_clean))

daily_counts_clean = df_clean.groupby("date").size()

print("\nDAILY RECORD VALIDATION AFTER CLEANING")

print("Minimum records per day:", daily_counts_clean.min())
print("Maximum records per day:", daily_counts_clean.max())

invalid_days = daily_counts_clean[daily_counts_clean != 50]

if len(invalid_days) == 0:
    print("SUCCESS: Every date now has exactly 50 records.")
else:
    print("WARNING: Some dates still do not have 50 records.")
    print(invalid_days)

print("\nRemoving unnecessary helper columns from final dataset")

df_clean = df_clean.drop(
    columns=["duration_minutes", "song_id"],
    errors="ignore"
)

df_clean["duration_minutes"] = df_clean["duration_ms"] / 60000

df_clean["song_id"] = (
    df_clean["song"].astype(str).str.strip()
    + " - "
    + df_clean["artist"].astype(str).str.strip()
)

output_file = "data/processed/cleaned_south_korea.csv"

df_clean.to_csv(
    output_file,
    index=False
)

print("\nCleaned dataset saved to:")
print(output_file)

print("\nFinal dataset shape:", df_clean.shape)

print("\nFinal columns:")
print(df_clean.columns.tolist())

print("\n" + "=" * 60)
print("STEP 3 COMPLETED")
print("=" * 60)
print("\n" + "=" * 60)
print("STEP 3: DATA CLEANING")
print("=" * 60)

print("\nOriginal dataset rows:", len(df))

duplicate_date = pd.Timestamp("2025-03-01")

duplicate_snapshot = df[df["date"] == duplicate_date].copy()

print("\nDuplicate date:", duplicate_date.date())
print("Rows found on duplicate date:", len(duplicate_snapshot))

df_clean = df[df["date"] != duplicate_date].copy()

print("Rows removed:", len(duplicate_snapshot))
print("Rows after cleaning:", len(df_clean))

daily_counts_clean = df_clean.groupby("date").size()

print("\nDAILY RECORD VALIDATION")

print("Minimum records per day:", daily_counts_clean.min())
print("Maximum records per day:", daily_counts_clean.max())

invalid_days = daily_counts_clean[daily_counts_clean != 50]

if len(invalid_days) == 0:
    print("SUCCESS: Every date has exactly 50 records.")
else:
    print("WARNING: Some dates do not have 50 records.")
    print(invalid_days)

df_clean["duration_minutes"] = df_clean["duration_ms"] / 60000

df_clean["song_id"] = (
    df_clean["song"].astype(str).str.strip()
    + " - "
    + df_clean["artist"].astype(str).str.strip()
)

output_file = "data/processed/cleaned_south_korea.csv"

df_clean.to_csv(output_file, index=False)

print("\nCleaned dataset saved to:")
print(output_file)

print("\nFinal dataset shape:", df_clean.shape)

print("\n" + "=" * 60)
print("STEP 3 COMPLETED")
print("=" * 60)