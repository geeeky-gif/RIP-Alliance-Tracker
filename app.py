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
        .tier-card {
            background: rgba(15, 23, 42, 0.75);
            border: 1px solid rgba(255, 255, 255, 0.08);
            border-radius: 12px;
            padding: 16px;
            margin-bottom: 14px;
            backdrop-filter: blur(8px);
        }
        .tier-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 10px;
            padding-bottom: 8px;
            border-bottom: 1px solid rgba(255, 255, 255, 0.08);
        }
        .tier-title {
            font-weight: 700;
            font-size: 15px;
        }
        .tier-badge {
            background: rgba(56, 189, 248, 0.15);
            color: #38bdf8;
            padding: 2px 10px;
            border-radius: 999px;
            font-size: 12px;
            font-weight: 700;
        }
        .member-pill {
            display: inline-block;
            background: rgba(30, 41, 59, 0.9);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 6px;
            padding: 4px 10px;
            margin: 3px;
            font-size: 13px;
            color: #e2e8f0;
        }
        .member-pill span {
            color: #94a3b8;
            font-size: 11px;
            margin-left: 4px;
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
    ("100% Attendance Group", 100.0, 100.1, "#10b981"),
    ("90% – 99% Group", 90.0, 100.0, "#34d399"),
    ("80% – 89% Group", 80.0, 90.0, "#38bdf8"),
    ("70% – 79% Group", 70.0, 80.0, "#60a5fa"),
    ("60% – 69% Group", 60.0, 70.0, "#818cf8"),
    ("50% – 59% Group", 50.0, 60.0, "#a78bfa"),
    ("40% – 49% Group", 40.0, 50.0, "#fbbf24"),
    ("30% – 39% Group", 30.0, 40.0, "#fb923c"),
    ("20% – 29% Group", 20.0, 30.0, "#f87171"),
    ("10% – 19% Group", 10.0, 20.0, "#ef4444"),
    ("0% – 9% Group", 0.0, 10.0, "#dc2626"),
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

def calculate_member_stats():
    roster_df = st.session_state.roster_df
    att_df = st.session_state.attendance_df
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
            "Absent Count": absent_cnt,
            "Total Logged": player_total_logged,
            "Attendance Rate": round(attendance_rate, 1)
        })

    return pd.DataFrame(stats), total_sessions

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
        "Military Rank": str(mil),
        "Alliance Rank": str(rank),
        "Status": str(status)
    }])
    st.session_state.roster_df = pd.concat([st.session_state.roster_df, new_row], ignore_index=True)
    save_roster()
    return True, f"Added **{clean_name}** to the roster!"

def add_member_to_session(session_id, event_name, event_date, player_name, status_val):
    clean_name = str(player_name).strip()
    if not clean_name:
        return False, "Player name cannot be empty."

    att_df = st.session_state.attendance_df
    existing_in_session = att_df[
        (att_df["Session ID"] == session_id) &
        (att_df["Player Name"].str.strip().str.lower() == clean_name.lower())
    ]
    if not existing_in_session.empty:
        return False, f"**{clean_name}** is already in this session."

    new_entry = pd.DataFrame([{
        "Session ID": session_id,
        "Event": event_name,
        "Date": str(event_date),
        "Player Name": clean_name,
        "Status": status_val
    }])
    st.session_state.attendance_df = pd.concat([st.session_state.attendance_df, new_entry], ignore_index=True)
    save_attendance()
    return True, f"Added **{clean_name}** ({status_val}) to this session!"

def remove_member_from_session(session_id, player_name):
    att_df = st.session_state.attendance_df
    if att_df.empty:
        return 0
    mask = (att_df["Session ID"] == session_id) & (att_df["Player Name"].str.strip().str.lower() == str(player_name).strip().lower())
    removed_count = int(mask.sum())
    if removed_count > 0:
        st.session_state.attendance_df = att_df[~mask].reset_index(drop=True)
        save_attendance()
    return removed_count

def migrate_attendance_names(rename_map):
    att_df = st.session_state.attendance_df
    if att_df.empty or not rename_map:
        return 0

    updated_df = att_df.copy()
    total_updated = 0

    for old_name, new_name in rename_map.items():
        if not old_name or not new_name or old_name == new_name:
            continue
        mask = updated_df["Player Name"].str.strip() == old_name.strip()
        count = int(mask.sum())
        if count > 0:
            updated_df.loc[mask, "Player Name"] = new_name.strip()
            total_updated += count

    if total_updated > 0:
        updated_df["_norm_name"] = updated_df["Player Name"].str.strip().str.lower()
        updated_df = updated_df.drop_duplicates(subset=["Session ID", "_norm_name"], keep="last").drop(columns=["_norm_name"]).reset_index(drop=True)
        st.session_state.attendance_df = updated_df
        save_attendance()

    return total_updated

def purge_player_from_all_attendance(player_name):
    att_df = st.session_state.attendance_df
    if att_df.empty:
        return 0
    mask = att_df["Player Name"].str.strip().str.lower() == str(player_name).strip().lower()
    removed_count = int(mask.sum())
    if removed_count > 0:
        st.session_state.attendance_df = att_df[~mask].reset_index(drop=True)
        save_attendance()
    return removed_count

def normalize_attendance_df(df):
    cleaned = df.copy()
    cleaned.columns = [str(c).strip() for c in cleaned.columns]

    if "Attended" in cleaned.columns and "Status" not in cleaned.columns:
        cleaned["Status"] = cleaned["Attended"].apply(
            lambda x: "Active" if str(x).strip().lower() in ["true", "1", "yes", "active"] else "Absent"
        )

    for col in ["Session ID", "Event", "Date", "Player Name", "Status"]:
        if col not in cleaned.columns:
            cleaned[col] = ""

    cleaned["Event"] = cleaned["Event"].fillna("").astype(str).str.strip()
    cleaned["Date"] = cleaned["Date"].fillna("").astype(str).str.strip()
    cleaned["Player Name"] = cleaned["Player Name"].fillna("").astype(str).str.strip()
    cleaned["Session ID"] = cleaned["Session ID"].fillna("").astype(str).str.strip()

    status_map = {
        "active": "Active",
        "attended": "Active",
        "zero points": "Zero Points",
        "zero_points": "Zero Points",
        "0 points": "Zero Points",
        "absent": "Absent",
        "missed": "Absent",
    }
    cleaned["Status"] = cleaned["Status"].fillna("Active").astype(str).str.strip().apply(
        lambda s: status_map.get(s.lower(), s if s in ATTENDANCE_STATUS_OPTIONS else "Active")
    )

    cleaned = cleaned[cleaned["Player Name"] != ""]

    missing_sid_mask = cleaned["Session ID"] == ""
    if missing_sid_mask.any():
        cleaned.loc[missing_sid_mask, "Session ID"] = cleaned.loc[missing_sid_mask].apply(
            lambda r: f"{r['Date'] or 'UnknownDate'}_{r['Event'] or 'ImportedEvent'}_Import",
            axis=1
        )

    return cleaned[["Session ID", "Event", "Date", "Player Name", "Status"]].reset_index(drop=True)

# ---------------------------------------------------------
# SIDEBAR NAVIGATION
# ---------------------------------------------------------
st.sidebar.markdown("### 📊 NAVIGATION")
page = st.sidebar.radio("Select View:", [
    "📈 Analytics Dashboard",
    "📊 Attendance Tiers (10% Blocks)",
    "📝 Quick Log / Edit Sessions",
    "✏️ Edit Roster",
    "📁 Upload Roster CSV",
    "📁 Upload Attendance CSV",
    "⚙️ Data Management"
])

# ---------------------------------------------------------
# PAGE 1: ANALYTICS DASHBOARD (THRESHOLD FILTERING)
# ---------------------------------------------------------
if page == "📈 Analytics Dashboard":
    st.subheader("📈 Alliance Intelligence & Threshold Filtering")

    roster_df = st.session_state.roster_df
    if roster_df.empty:
        st.warning("No players found in roster.")
    else:
        summary_df, total_sessions = calculate_member_stats()
        active_summary_df = summary_df[summary_df["Member Status"] == "Active"]

        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Active Roster", len(active_summary_df))
        m2.metric("Tracked Events", total_sessions)
        avg_att = active_summary_df["Attendance Rate"].mean() if not active_summary_df.empty else 0
        m3.metric("Alliance Turnout", f"{avg_att:.1f}%")
        total_zero_pts = summary_df["Zero Points Count"].sum() if not summary_df.empty else 0
        m4.metric("Zero-Point Instances", total_zero_pts, delta=f"-{total_zero_pts} inactive" if total_zero_pts > 0 else "Optimal", delta_color="inverse")

        st.markdown("---")
        st.markdown("#### 🎯 Filter Members by Attendance Threshold")

        f1, f2, f3, f4 = st.columns([2, 2.5, 1.5, 2])
        filter_mode = f1.selectbox(
            "Filter Condition",
            ["Below Threshold (<)", "At or Above Threshold (>=)", "Show All Members"],
            index=0
        )
        threshold_val = f2.slider(
            "Attendance Threshold (%)",
            min_value=0,
            max_value=100,
            value=70,
            step=5,
            disabled=(filter_mode == "Show All Members")
        )
        scope_filter = f3.selectbox(
            "Roster Scope",
            ["Active Only", "All Members"],
            index=0
        )
        sort_order = f4.selectbox(
            "Sort By",
            ["Lowest Attendance First", "Highest Attendance First", "Alphabetical (A-Z)"],
            index=0
        )

        filtered_df = summary_df.copy()
        if scope_filter == "Active Only":
            filtered_df = filtered_df[filtered_df["Member Status"] == "Active"]

        if filter_mode == "Below Threshold (<)":
            filtered_df = filtered_df[filtered_df["Attendance Rate"] < float(threshold_val)]
            section_label = f"Members Below {threshold_val}% Attendance ({len(filtered_df)})"
        elif filter_mode == "At or Above Threshold (>=)":
            filtered_df = filtered_df[filtered_df["Attendance Rate"] >= float(threshold_val)]
            section_label = f"Members At or Above {threshold_val}% Attendance ({len(filtered_df)})"
        else:
            section_label = f"All Roster Members ({len(filtered_df)})"

        if sort_order == "Lowest Attendance First":
            filtered_df = filtered_df.sort_values(by=["Attendance Rate", "Player Name"], ascending=
