import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path
from datetime import date, timedelta

# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="South Korea Music Analytics",
    page_icon="🎵",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# DESIGN
# ============================================================

st.markdown("""
<style>

.stApp {
    background:
        radial-gradient(circle at 5% 5%, rgba(55,90,210,.25), transparent 30%),
        radial-gradient(circle at 95% 10%, rgba(125,65,205,.22), transparent 30%),
        linear-gradient(135deg,#070b24,#0c1230,#171039);
    color: white;
}

.block-container {
    max-width: 1500px;
    padding: 30px 35px 60px;
}

[data-testid="stSidebar"] {
    background: linear-gradient(180deg,#080d29,#0d1435,#15103b);
    border-right: 1px solid rgba(100,130,255,.35);
}

[data-testid="stSidebar"] > div:first-child {
    padding: 25px 18px;
}

.sidebar-title {
    color: white;
    font-size: 27px;
    font-weight: 800;
}

.sidebar-description {
    color: #aebbe8;
    font-size: 14px;
    line-height: 1.6;
    margin: 8px 0 22px;
}

.filter-label {
    color: #c4d0ff;
    font-weight: 700;
    font-size: 14px;
    margin: 15px 0 7px;
}

.search-result {
    background: rgba(55,75,155,.35);
    border: 1px solid rgba(100,130,255,.3);
    border-radius: 10px;
    padding: 9px;
    margin: 6px 0 10px;
    color: #dce5ff;
    font-size: 13px;
}

.hero {
    background: linear-gradient(120deg,#2b55bd,#4c37a7,#6835a8);
    border: 1px solid rgba(145,170,255,.45);
    border-radius: 25px;
    padding: 45px;
    margin-bottom: 25px;
    box-shadow: 0 20px 55px rgba(20,25,80,.35);
}

.hero-title {
    color: white;
    font-size: clamp(32px,5vw,65px);
    font-weight: 900;
    line-height: 1.05;
}

.hero-subtitle {
    color: #dce4ff;
    font-size: 18px;
    margin-top: 16px;
}

.overview {
    background: rgba(19,28,68,.9);
    border: 1px solid rgba(90,120,240,.35);
    border-radius: 20px;
    padding: 25px;
    margin-bottom: 25px;
}

.overview-title {
    color: white;
    font-size: 26px;
    font-weight: 800;
}

.overview-text {
    color: #adbae5;
    margin-top: 8px;
}

.info {
    background: linear-gradient(90deg,rgba(35,65,145,.75),rgba(70,40,130,.75));
    border: 1px solid rgba(110,140,255,.35);
    border-radius: 15px;
    padding: 17px;
    margin: 20px 0;
    color: #e3eaff;
}

.metric {
    background: linear-gradient(145deg,#17214d,#0d1433);
    border: 1px solid rgba(90,120,230,.4);
    border-radius: 18px;
    padding: 22px;
    min-height: 125px;
}

.metric-label {
    color: #aab8e8;
    font-size: 14px;
}

.metric-value {
    color: white;
    font-size: 32px;
    font-weight: 800;
    margin-top: 12px;
}

.section {
    background: rgba(14,21,52,.8);
    border: 1px solid rgba(85,115,230,.3);
    border-radius: 20px;
    padding: 20px;
    margin-top: 25px;
}

.section-title {
    color: white;
    font-size: 25px;
    font-weight: 800;
    margin-bottom: 15px;
}

.stButton button {
    width: 100%;
    min-height: 45px;
    border-radius: 11px;
    border: 0;
    background: linear-gradient(135deg,#3d76ff,#7149e7);
    color: white;
    font-weight: 700;
}

.stButton button:hover {
    box-shadow: 0 8px 25px rgba(70,90,255,.35);
    transform: translateY(-1px);
}

.stTextInput input {
    background: white !important;
    color: #17203d !important;
    border-radius: 11px !important;
}

.stMultiSelect div[data-baseweb="select"] {
    background: white !important;
    border-radius: 11px !important;
}

.stMultiSelect input {
    color: #17203d !important;
}

.stDateInput input {
    background: white !important;
    color: #17203d !important;
    border-radius: 11px !important;
}

@media(max-width:800px) {
    .block-container {
        padding: 15px;
    }

    .hero {
        padding: 28px 20px;
    }

    .hero-title {
        font-size: 36px;
    }

    .hero-subtitle {
        font-size: 15px;
    }

    .metric {
        margin-bottom: 12px;
    }
}

</style>
""", unsafe_allow_html=True)

# ============================================================
# FIND DATA
# ============================================================

APP_DIR = Path(__file__).resolve().parent

files = [
    APP_DIR / "cleaned_south_korea.csv",
    APP_DIR / "Atlantic_South_Korea.csv",
    APP_DIR / "data" / "processed" / "cleaned_south_korea.csv",
    APP_DIR.parent / "data" / "processed" / "cleaned_south_korea.csv",
    APP_DIR.parent / "Atlantic_South_Korea.csv"
]

DATA_FILE = next(
    (file for file in files if file.exists()),
    None
)

if DATA_FILE is None:
    st.error("CSV file not found. Please ensure the data file is placed in the correct directory.")
    st.stop()

# ============================================================
# LOAD DATA
# ============================================================

@st.cache_data
def load_data(file):
    return pd.read_csv(file)

df = load_data(DATA_FILE)

# ============================================================
# COLUMN FINDER
# ============================================================

def find_column(names):
    columns = {
        str(c).strip().lower(): c
        for c in df.columns
    }
    
    for name in names:
        if name.lower() in columns:
            return columns[name.lower()]
            
    for column in df.columns:
        column_text = str(column).lower()
        for name in names:
            if name.lower() in column_text:
                return column
                
    return None

artist_col = find_column([
    "artist", "artists", "artist_name", "performer"
])

song_col = find_column([
    "song", "song_name", "track", "track_name", "title"
])

date_col = find_column([
    "date", "chart_date", "entry_date", "week", "datetime"
])

rank_col = find_column([
    "rank", "chart_rank", "position", "peak_rank"
])

# ============================================================
# VALIDATE
# ============================================================

if artist_col is None:
    st.error("Artist column not found.")
    st.write("Available columns:", list(df.columns))
    st.stop()

if date_col is None:
    st.error("Date column not found.")
    st.write("Available columns:", list(df.columns))
    st.stop()

# ============================================================
# CLEAN DISPLAY COPY
# ============================================================

df[artist_col] = (
    df[artist_col]
    .fillna("")
    .astype(str)
    .str.strip()
)

df["_date"] = pd.to_datetime(
    df[date_col],
    errors="coerce"
)

df = df.dropna(subset=["_date"]).copy()

if rank_col:
    df[rank_col] = pd.to_numeric(
        df[rank_col],
        errors="coerce"
    )

# ============================================================
# DATE LIMITS
# ============================================================
# Safely handle dates in case the dataset becomes completely empty after dropping NaTs
min_dt = df["_date"].min()
max_dt = df["_date"].max()

if pd.isna(min_dt) or pd.isna(max_dt):
    DATA_MIN_DATE = date.today()
    DATA_MAX_DATE = date.today()
else:
    DATA_MIN_DATE = min_dt.date()
    DATA_MAX_DATE = max_dt.date()

CALENDAR_MIN_DATE = date(1900, 1, 1)
CALENDAR_MAX_DATE = max(
    date.today(),
    DATA_MAX_DATE
)

# ============================================================
# SESSION STATE
# ============================================================

defaults = {
    "search_artist": "",
    "selected_artists": [],
    "start_date": DATA_MIN_DATE,
    "end_date": DATA_MAX_DATE,
    "applied_artists": [],
    "applied_start": DATA_MIN_DATE,
    "applied_end": DATA_MAX_DATE
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value

# ============================================================
# ARTIST LIST
# ============================================================

all_artists = sorted(
    df[artist_col]
    .dropna()
    .unique()
    .tolist(),
    key=lambda x: str(x).lower()
)

# ============================================================
# CALLBACKS
# ============================================================

def select_all():
    search = st.session_state.search_artist.strip().lower()
    if search:
        matches = [
            artist for artist in all_artists
            if search in str(artist).lower()
        ]
        st.session_state.selected_artists = matches
    else:
        st.session_state.selected_artists = all_artists.copy()


def clear_artists():
    st.session_state.selected_artists = []


def full_range():
    st.session_state.start_date = DATA_MIN_DATE
    st.session_state.end_date = DATA_MAX_DATE


def last_30():
    st.session_state.start_date = max(
        DATA_MIN_DATE,
        DATA_MAX_DATE - timedelta(days=29)
    )
    st.session_state.end_date = DATA_MAX_DATE


def last_90():
    st.session_state.start_date = max(
        DATA_MIN_DATE,
        DATA_MAX_DATE - timedelta(days=89)
    )
    st.session_state.end_date = DATA_MAX_DATE


def this_year():
    year_start = date(DATA_MAX_DATE.year, 1, 1)
    st.session_state.start_date = max(
        DATA_MIN_DATE,
        year_start
    )
    st.session_state.end_date = DATA_MAX_DATE


def apply_filter():
    start = st.session_state.start_date
    end = st.session_state.end_date

    if start > end:
        start, end = end, start
        st.session_state.start_date = start
        st.session_state.end_date = end

    st.session_state.applied_artists = (
        st.session_state.selected_artists.copy()
    )
    st.session_state.applied_start = start
    st.session_state.applied_end = end


def reset_filter():
    st.session_state.search_artist = ""
    st.session_state.selected_artists = []
    st.session_state.start_date = DATA_MIN_DATE
    st.session_state.end_date = DATA_MAX_DATE
    st.session_state.applied_artists = []
    st.session_state.applied_start = DATA_MIN_DATE
    st.session_state.applied_end = DATA_MAX_DATE

# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:
    st.markdown(
        '<div class="sidebar-title">Dashboard Filters</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="sidebar-description">'
        'Search and filter the South Korea music chart dataset.'
        '</div>',
        unsafe_allow_html=True
    )

    # --------------------------------------------------------
    # SEARCH
    # --------------------------------------------------------

    st.markdown(
        '<div class="filter-label">Search Artist</div>',
        unsafe_allow_html=True
    )

    st.text_input(
        "Artist Search",
        key="search_artist",
        placeholder="Type artist name...",
        label_visibility="collapsed"
    )

    search = st.session_state.search_artist.strip().lower()

    if search:
        matching_artists = [
            artist for artist in all_artists
            if search in str(artist).lower()
        ]

        if matching_artists:
            st.markdown(
                f'<div class="search-result">'
                f'Found {len(matching_artists)} artist(s)'
                f'</div>',
                unsafe_allow_html=True
            )

            for artist in matching_artists[:15]:
                st.markdown(
                    f'<div class="search-result">'
                    f'{artist}'
                    f'</div>',
                    unsafe_allow_html=True
                )

            if len(matching_artists) > 15:
                st.caption(f"+ {len(matching_artists) - 15} more")
        else:
            st.warning("No artist found.")
    else:
        matching_artists = all_artists

    # --------------------------------------------------------
    # SELECT ARTIST
    # --------------------------------------------------------

    st.markdown(
        '<div class="filter-label">Select Artist(s)</div>',
        unsafe_allow_html=True
    )

    options = list(
        dict.fromkeys(
            matching_artists
            + [
                artist for artist in st.session_state.selected_artists
                if artist in all_artists
            ]
        )
    )

    st.multiselect(
        "Artist Selection",
        options=options,
        key="selected_artists",
        placeholder="Choose one or more artists",
        label_visibility="collapsed"
    )

    # --------------------------------------------------------
    # SELECT / CLEAR
    # --------------------------------------------------------

    c1, c2 = st.columns(2)

    with c1:
        st.button(
            "Select All",
            key="select_all_button",
            on_click=select_all,
            use_container_width=True
        )

    with c2:
        st.button(
            "Clear",
            key="clear_button",
            on_click=clear_artists,
            use_container_width=True
        )

    st.markdown("---")

    # --------------------------------------------------------
    # DATE RANGE
    # --------------------------------------------------------

    st.markdown(
        '<div class="filter-label">Date Range</div>',
        unsafe_allow_html=True
    )

    st.date_input(
        "Start Date",
        key="start_date",
        min_value=CALENDAR_MIN_DATE,
        max_value=CALENDAR_MAX_DATE,
        format="DD/MM/YYYY"
    )

    st.date_input(
        "End Date",
        key="end_date",
        min_value=CALENDAR_MIN_DATE,
        max_value=CALENDAR_MAX_DATE,
        format="DD/MM/YYYY"
    )

    if st.session_state.start_date > st.session_state.end_date:
        st.warning("Start date is after end date.")

    # --------------------------------------------------------
    # QUICK FILTERS
    # --------------------------------------------------------

    st.markdown(
        '<div class="filter-label">Quick Filters</div>',
        unsafe_allow_html=True
    )

    q1, q2 = st.columns(2)

    with q1:
        st.button(
            "Full Range",
            key="full_range_button",
            on_click=full_range,
            use_container_width=True
        )

        st.button(
            "Last 90 Days",
            key="last_90_button",
            on_click=last_90,
            use_container_width=True
        )

    with q2:
        st.button(
            "Last 30 Days",
            key="last_30_button",
            on_click=last_30,
            use_container_width=True
        )

        st.button(
            "This Year",
            key="this_year_button",
            on_click=this_year,
            use_container_width=True
        )

    st.markdown("---")

    # --------------------------------------------------------
    # APPLY / RESET
    # --------------------------------------------------------

    st.button(
        "Apply Filters",
        key="apply_button",
        on_click=apply_filter,
        use_container_width=True
    )

    st.button(
        "Reset Filters",
        key="reset_button",
        on_click=reset_filter,
        use_container_width=True
    )

# ============================================================
# FILTER DATA
# ============================================================

filtered_df = df[
    (df["_date"].dt.date >= st.session_state.applied_start) &
    (df["_date"].dt.date <= st.session_state.applied_end)
].copy()

if st.session_state.applied_artists:
    filtered_df = filtered_df[
        filtered_df[artist_col].isin(st.session_state.applied_artists)
    ].copy()

# ============================================================
# HERO
# ============================================================

st.markdown(
    """
    <div class="hero">
        <div class="hero-title">
            South Korea Top 50 Music Analytics
        </div>
        <div class="hero-subtitle">
            Comeback Momentum, Chart Re-entry,
            Sustainability and Fandom Intensity Analysis
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

# ============================================================
# OVERVIEW
# ============================================================

st.markdown(
    """
    <div class="overview">
        <div class="overview-title">
            Dashboard Overview
        </div>
        <div class="overview-text">
            Use the interactive filters from the left sidebar
            to explore chart performance, artists and songs.
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

# ============================================================
# METRICS
# ============================================================

records = len(filtered_df)
artists = filtered_df[artist_col].nunique()

if song_col:
    songs = filtered_df[song_col].nunique()
else:
    songs = 0

if rank_col and not filtered_df.empty:
    valid_rank = filtered_df[rank_col].dropna()
    if not valid_rank.empty:
        best_rank = int(valid_rank.min())
    else:
        best_rank = "N/A"
else:
    best_rank = "N/A"

# ============================================================
# INFO
# ============================================================

st.markdown(
    f"""
    <div class="info">
        Showing <b>{records:,}</b> chart records
        &nbsp; | &nbsp;
        <b>{songs:,}</b> songs
        &nbsp; | &nbsp;
        <b>{artists:,}</b> artists
        &nbsp; | &nbsp;
        Date:
        <b>{st.session_state.applied_start.strftime("%d/%m/%Y")}</b>
        -
        <b>{st.session_state.applied_end.strftime("%d/%m/%Y")}</b>
    </div>
    """,
    unsafe_allow_html=True
)

# ============================================================
# METRIC CARDS
# ============================================================

m1, m2, m3, m4 = st.columns(4)

with m1:
    st.markdown(
        f"""
        <div class="metric">
            <div class="metric-label">
                Chart Records
            </div>
            <div class="metric-value">
                {records:,}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

with m2:
    st.markdown(
        f"""
        <div class="metric">
            <div class="metric-label">
                Unique Songs
            </div>
            <div class="metric-value">
                {songs:,}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

with m3:
    st.markdown(
        f"""
        <div class="metric">
            <div class="metric-label">
                Unique Artists
            </div>
            <div class="metric-value">
                {artists:,}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

with m4:
    st.markdown(
        f"""
        <div class="metric">
            <div class="metric-label">
                Best Chart Rank
            </div>
            <div class="metric-value">
                #{best_rank}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

# ============================================================
# NO DATA
# ============================================================

if filtered_df.empty:
    st.warning("No data found for the selected filters.")
    st.stop()

# ============================================================
# CHART PERFORMANCE
# ============================================================

if rank_col:
    chart_df = filtered_df.copy()
    chart_df[rank_col] = pd.to_numeric(
        chart_df[rank_col],
        errors="coerce"
    )
    
    chart_df = chart_df.dropna(subset=[rank_col])
    
    daily = (
        chart_df
        .groupby("_date", as_index=False)[rank_col]
        .mean()
    )

    daily.rename(
        columns={rank_col: "Average Rank"},
        inplace=True
    )

    fig = px.line(
        daily,
        x="_date",
        y="Average Rank",
        markers=True
    )

    fig.update_traces(
        line=dict(width=3),
        marker=dict(size=5)
    )

    fig.update_yaxes(
        autorange="reversed",
        title="Average Chart Rank"
    )

    fig.update_xaxes(title="Date")

    fig.update_layout(
        title="Chart Performance Over Time",
        template="plotly_dark",
        height=450,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(8,13,38,.4)",
        margin=dict(l=20, r=20, t=60, b=20)
    )

    st.markdown(
        '<div class="section">'
        '<div class="section-title">'
        'Chart Performance Over Time'
        '</div>',
        unsafe_allow_html=True
    )

    st.plotly_chart(fig, use_container_width=True)

    st.markdown('</div>', unsafe_allow_html=True)

# ============================================================
# ARTIST PERFORMANCE
# ============================================================

artist_stats = (
    filtered_df[artist_col]
    .value_counts()
    .head(15)
    .reset_index()
)

artist_stats.columns = ["Artist", "Chart Records"]

fig_artist = px.bar(
    artist_stats.sort_values("Chart Records"),
    x="Chart Records",
    y="Artist",
    orientation="h"
)

fig_artist.update_layout(
    title="Artist Performance",
    template="plotly_dark",
    height=500,
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(8,13,38,.4)",
    margin=dict(l=20, r=20, t=60, b=20)
)

st.markdown(
    '<div class="section">'
    '<div class="section-title">'
    'Artist Performance'
    '</div>',
    unsafe_allow_html=True
)

st.plotly_chart(fig_artist, use_container_width=True)

st.markdown('</div>', unsafe_allow_html=True)

# ============================================================
# SONG PERFORMANCE
# ============================================================

if song_col:
    song_stats = (
        filtered_df[song_col]
        .value_counts()
        .head(15)
        .reset_index()
    )

    song_stats.columns = ["Song", "Chart Records"]

    fig_song = px.bar(
        song_stats.sort_values("Chart Records"),
        x="Chart Records",
        y="Song",
        orientation="h"
    )

    fig_song.update_layout(
        title="Song Performance",
        template="plotly_dark",
        height=520,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(8,13,38,.4)",
        margin=dict(l=20, r=20, t=60, b=20)
    )

    st.markdown(
        '<div class="section">'
        '<div class="section-title">'
        'Song Performance'
        '</div>',
        unsafe_allow_html=True
    )

    st.plotly_chart(fig_song, use_container_width=True)

    st.markdown('</div>', unsafe_allow_html=True)

# ============================================================
# FILTERED DATA
# ============================================================

st.markdown(
    '<div class="section">'
    '<div class="section-title">'
    'Filtered Chart Data'
    '</div>',
    unsafe_allow_html=True
)

display_df = filtered_df.copy()

if "_date" in display_df.columns:
    display_df["_date"] = (
        display_df["_date"]
        .dt.strftime("%Y-%m-%d")
    )

st.dataframe(
    display_df,
    use_container_width=True,
    height=450,
    hide_index=True
)

st.markdown('</div>', unsafe_allow_html=True)

# ============================================================
# FOOTER
# ============================================================

st.markdown(
    """
    <div style="
        text-align:center;
        padding:35px 10px;
        color:#7f8dbc;
        font-size:14px;
    ">
        South Korea Top 50 Music Analytics Dashboard
    </div>
    """,
    unsafe_allow_html=True
)
