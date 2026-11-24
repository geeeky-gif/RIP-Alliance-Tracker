import streamlit as st
import pandas as pd
import os
from datetime import datetime

st.set_page_config(page_title="RIP Alliance Command Center", layout="wide")

# ---------------------------------------------------------
# HIGH-PERFORMANCE COMMAND THEME (DARK GLOW & GLASSMORPHISM)
# ---------------------------------------------------------
st.markdown(
    """
    <style>
        .stApp, [data-testid="stAppViewContainer"], [data-testid="stHeader"] {
            background-color: #080b11 !important;
            color: #f1f5f9 !important;
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
        }
        [data-testid="stSidebar"] {
            background-color: #0c1017 !important;
            border-right: 1px solid rgba(255, 255, 255, 0.08);
        }
        [data-testid="stSidebar"] .stRadio label {
            color: #94a3b8 !important;
            font-weight: 500;
        }
        .command-hero {
            background: linear-gradient(135deg, rgba(15, 23, 42, 0.9) 0%, rgba(30, 41, 59, 0.8) 100%);
            border: 1px solid rgba(99, 102, 241, 0.3);
            border-radius: 14px;
            padding: 24px 28px;
            box-shadow: 0 10px 30px -10px rgba(99, 102, 241, 0.2);
            backdrop-filter: blur(10px);
            margin-bottom: 24px;
        }
        .command-hero h1 {
            color: #ffffff !important;
            margin: 0;
            font-size: 26px;
            font-weight: 800;
            letter-spacing: -0.5px;
            background: linear-gradient(90deg, #ffffff 30%, #818cf8 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        .command-hero p {
            color: #94a3b8 !important;
            margin: 6px 0 0 0;
            font-size: 14px;
        }
        [data-testid="stMetric"] {
            background: rgba(15, 23, 42, 0.6) !important;
            border: 1px solid rgba(255, 255, 255, 0.07) !important;
            padding: 16px 20px !important;
            border-radius: 12px !important;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2) !important;
            backdrop-filter: blur(8px);
        }
        [data-testid="stMetricLabel"] {
            color: #94a3b8 !important;
            font-size: 12px !important;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            font-weight: 600;
        }
        [data-testid="stMetricValue"] {
            color: #38bdf8 !important;
            font-size: 24px !important;
            font-weight: 700;
        }
        [data-testid="stDataFrame"] {
            background-color: rgba(15, 23, 42, 0.4) !important;
            border-radius: 12px;
            border: 1px solid rgba(255, 255, 255, 0.07);
        }
        .stButton button {
            background: rgba(30, 41, 59, 0.7);
            color: #f1f5f9;
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 8px;
            font-weight: 600;
            transition: all 0.25s ease;
        }
        .stButton button:hover {
            background: rgba(51, 65, 85, 0.9);
            border-color: #38bdf8;
            color: #ffffff;
            box-shadow: 0 0 15px rgba(56, 189, 248, 0.3);
        }
        button[kind="primary"] {
            background: linear-gradient(135deg, #0284c7 0%, #2563eb 100%) !important;
            color: #ffffff !important;
            border: none !important;
            box-shadow: 0 4px 15px rgba(37, 99, 235, 0.4);
        }
        button[kind="primary"]:hover {
            background: linear-gradient(135deg, #0369a1 0%, #1d4ed8 100%) !important;
            box-shadow: 0 6px 20px rgba(37, 99, 235, 0.6);
        }
        .stTabs [data-baseweb="tab-list"] {
            gap: 8px;
            background-color: rgba(15, 23, 42, 0.5);
            padding: 6px;
            border-radius: 10px;
            border: 1px solid rgba(255, 255, 255, 0.06);
        }
        .stTabs [data-baseweb="tab"] {
            color: #94a3b8;
            border-radius: 6px;
            font-weight: 600;
        }
        .stTabs [aria-selected="true"] {
            background: #2563eb !important;
            color: white !important;
        }
        .tier-card {
            background: rgba(15, 23, 42, 0.72);
            border: 1px solid rgba(255, 255, 255, 0.08);
            border-radius: 12px;
            padding: 16px 18px;
            margin-bottom: 16px;
            box-shadow: 0 6px 20px rgba(0, 0, 0, 0.25);
        }
        .tier-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            border-bottom: 1px solid rgba(255, 255, 255, 0.08);
            padding-bottom: 10px;
            margin-bottom: 12px;
        }
        .tier-title {
            font-size: 16px;
            font-weight: 700;
            letter-spacing: 0.3px;
        }
        .tier-badge {
            font-size: 12px;
            font-weight: 700;
            padding: 3px 10px;
            border-radius: 999px;
            background: rgba(56, 189, 248, 0.15);
            color: #38bdf8;
            border: 1px solid rgba(56, 189, 248, 0.3);
        }
        .member-pill-grid {
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
        }
        .member-pill {
            background: rgba(30, 41, 59, 0.85);
            border: 1px solid rgba(255, 255, 255, 0.08);
            border-radius: 8px;
            padding: 6px 10px;
            font-size: 13px;
            color: #f1f5f9;
            display: inline-flex;
            align-items: center;
            gap: 6px;
        }
        .member-pill-pct {
            color: #94a3b8;
            font-size: 11px;
            font-weight: 600;
        }
        .tier-empty {
            color: #64748b;
            font-size: 13px;
            font-style: italic;
        }
    </style>
    <div class="command-hero">
        <h1>RIP ALLIANCE COMMAND CENTER</h1>
        <p>Operational Intelligence & Member Analytics Hub</p>
    </div>
    """,
    unsafe_allow_html=True
)

# ---------------------------------------------------------
# CONSTANTS & FILE PATHS
# ---------------------------------------------------------
ROSTER_FILE = "roster_data.csv"
ATTENDANCE_FILE = "attendance_matrix.csv"

EVENTS_LIST = [
    "Elite Wars", "Fortress War", "Realm Conquest",
    "Realm Invasion", "Territory Defense", "Territory Expulsion",
    "Alliance Conquest", "Frenzy", "Void", "Elite Adventures"
]

CASTLE_LEVEL_OPTIONS = [str(i) for i in range(1, 41)] + ["S1", "S2", "S3"]
LORD_LEVEL_OPTIONS = [str(i) for i in range(0, 81)]
MILITARY_RANK_OPTIONS = [
    "",
    "Sargeant",
    "Sergant Major",
    "Liutenant Knight",
    "Centurion",
    "Sriker Battalion",
    "Legion Officer",
    "Legion Commander",
    "High Commander",
    "Royal Commander",
    "Captain",
    "General",
    "Commander-in-Chief",
    "Overseer",
    "Grand Marshal",
    "Star Marshal",
    "Legendary Marshal",
    "War Lord"
]
STATUS_OPTIONS = ["Active", "Inactive"]
ALLIANCE_RANK_OPTIONS = ["Alliance Leader", "Deputy", "Officer", "Elite", "Member"]
ATTENDANCE_STATUS_OPTIONS = ["Active", "Zero Points", "Absent"]

TIER_DEFINITIONS = [
    ("100%", "100% Attendance Group", 100.0, 100.1, "#34d399"),
    ("90%", "90% – 99% Attendance Group", 90.0, 100.0, "#38bdf8"),
    ("80%", "80% – 89% Attendance Group", 80.0, 90.0, "#818cf8"),
    ("70%", "70% – 79% Attendance Group", 70.0, 80.0, "#a78bfa"),
    ("60%", "60% – 69% Attendance Group", 60.0, 70.0, "#facc15"),
    ("50%", "50% – 59% Attendance Group", 50.0, 60.0, "#fbbf24"),
    ("40%", "40% – 49% Attendance Group", 40.0, 50.0, "#fb923c"),
    ("30%", "30% – 39% Attendance Group", 30.0, 40.0, "#f97316"),
    ("20%", "20% – 29% Attendance Group", 20.0, 30.0, "#f87171"),
    ("10%", "10% – 19% Attendance Group", 10.0, 20.0, "#ef4444"),
    ("0%", "0% – 9% Attendance Group", 0.0, 10.0, "#dc2626"),
]

# ---------------------------------------------------------
# STATE INITIALIZATION
# ---------------------------------------------------------
if "roster_df" not in st.session_state:
    if os.path.exists(ROSTER_FILE):
        try:
            st.session_state.roster_df = pd.read_csv(ROSTER_FILE, dtype=str)
        except Exception:
            st.session_state.roster_df = pd.DataFrame(columns=["Player Name", "Castle Level", "Lord Level", "Military Rank", "Alliance Rank", "Status"])
    else:
        initial_roster = []
        for i in range(1, 101):
            initial_roster.append({
                "Player Name": f"Player_{i:03d}",
                "Castle Level": "40" if i <= 10 else "35",
                "Lord Level": "50",
                "Military Rank": "Captain",
                "Alliance Rank": "Leader" if i == 1 else ("Officer" if i <= 5 else "Member"),
                "Status": "Active"
            })
        st.session_state.roster_df = pd.DataFrame(initial_roster)
        st.session_state.roster_df.to_csv(ROSTER_FILE, index=False)

for col, default_val in [("Castle Level", "40"), ("Lord Level", "50"), ("Military Rank", ""), ("Alliance Rank", "Member"), ("Status", "Active")]:
    if col not in st.session_state.roster_df.columns:
        st.session_state.roster_df[col] = default_val

if "attendance_df" not in st.session_state:
    if os.path.exists(ATTENDANCE_FILE):
        try:
            st.session_state.attendance_df = pd.read_csv(ATTENDANCE_FILE, dtype=str)
            if not st.session_state.attendance_df.empty:
                if "Attended" in st.session_state.attendance_df.columns and "Status" not in st.session_state.attendance_df.columns:
                    st.session_state.attendance_df["Status"] = st.session_state.attendance_df["Attended"].apply(
                        lambda x: "Active" if str(x).lower() == "true" else "Absent"
                    )
        except Exception:
            st.session_state.attendance_df = pd.DataFrame(columns=["Session ID", "Event", "Date", "Player Name", "Status"])
    else:
        st.session_state.attendance_df = pd.DataFrame(columns=["Session ID", "Event", "Date", "Player Name", "Status"])

def save_roster():
    st.session_state.roster_df.to_csv(ROSTER_FILE, index=False)

def save_attendance():
    st.session_state.attendance_df.to_csv(ATTENDANCE_FILE, index=False)

def get_sorted_roster_names(active_only=True):
    if "roster_df" in st.session_state and not st.session_state.roster_df.empty:
        df = st.session_state.roster_df
        if active_only:
            df = df[df["Status"] == "Active"]
        names = df["Player Name"].dropna().astype(str).tolist()
        return sorted(names, key=lambda x: x.lower())
    return []

def build_member_stats_df():
    roster_df = st.session_state.roster_df
    att_df = st.session_state.attendance_df
    if roster_df.empty:
        return pd.DataFrame(), 0

    total_sessions = att_df["Session ID"].nunique() if not att_df.empty else 0
    stats = []

    for _, p_row in roster_df.iterrows():
        p_name = p_row["Player Name"]
        p_status = p_row["Status"]

        if total_sessions > 0 and not att_df.empty:
            p_logs = att_df[(att_df["Player Name"] == p_name) & (att_df["Status"].isin(["Active", "Zero Points", "Absent"]))]
            active_cnt = len(p_logs[p_logs["Status"] == "Active"])
            zero_cnt = len(p_logs[p_logs["Status"] == "Zero Points"])
            absent_cnt = len(p_logs[p_logs["Status"] == "Absent"])

            player_total_logged = active_cnt + zero_cnt + absent_cnt
            showed_up_cnt = active_cnt + zero_cnt
            attendance_rate = (showed_up_cnt / player_total_logged) * 100 if player_total_logged > 0 else 0.0
        else:
            active_cnt, zero_cnt, absent_cnt, player_total_logged = 0, 0, 0, 0
            attendance_rate = 0.0

        stats.append({
            "Player Name": p_name,
            "Castle Level": p_row.get("Castle Level", "—"),
            "Lord Level": p_row.get("Lord Level", "—"),
            "Alliance Rank": p_row.get("Alliance Rank", "—"),
            "Member Status": p_status,
            "Active Count": active_cnt,
            "Zero Points Count": zero_cnt,
            "Total Logged": player_total_logged,
            "Attendance Rate": round(attendance_rate, 1)
        })

    summary_df = pd.DataFrame(stats)
    if not summary_df.empty:
        summary_df = summary_df.sort_values(
            by=["Attendance Rate", "Player Name"],
            ascending=[False, True],
            key=lambda col: col.str.lower() if col.dtype == "object" else col
        ).reset_index(drop=True)

    return summary_df, total_sessions

def add_member_to_roster(name, castle="35", lord="50", mil="", rank="Member", status="Active"):
    clean_name = str(name).strip()
    if not clean_name:
        return False, "Player name cannot be empty."

    existing_names = st.session_state.roster_df["Player Name"].dropna().astype(str).str.strip().str.lower().tolist()
    if clean_name.lower() in existing_names:
        return False, f"**{clean_name}** is already on the roster."

    new_row = pd.DataFrame([{
        "Player Name": clean_name,
        "Castle Level": str(castle),
        "Lord Level": str(lord),
