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
            background: rgba(15, 23, 42, 0.75);
            border: 1px solid rgba(255, 255, 255, 0.09);
            border-radius: 12px;
            padding: 14px 16px;
            margin-bottom: 14px;
            backdrop-filter: blur(8px);
        }
        .tier-card-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            border-bottom: 1px solid rgba(255, 255, 255, 0.08);
            padding-bottom: 8px;
            margin-bottom: 10px;
        }
        .tier-title {
            font-size: 15px;
            font-weight: 700;
            color: #f8fafc;
        }
        .tier-badge {
            font-size: 12px;
            font-weight: 700;
            padding: 2px 10px;
            border-radius: 999px;
            background: rgba(56, 189, 248, 0.15);
            color: #38bdf8;
            border: 1px solid rgba(56, 189, 248, 0.35);
        }
        .tier-member-row {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 4px 0;
            font-size: 13px;
            color: #cbd5e1;
            border-bottom: 1px dashed rgba(255, 255, 255, 0.04);
        }
        .tier-member-row:last-child {
            border-bottom: none;
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

TIER_ORDER = [
    "100% Group",
    "90% - 99% Group",
    "80% - 89% Group",
    "70% - 79% Group",
    "60% - 69% Group",
    "50% - 59% Group",
    "40% - 49% Group",
    "30% - 39% Group",
    "20% - 29% Group",
    "10% - 19% Group",
    "0% - 9% Group"
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

def get_attendance_tier(rate):
    if rate >= 100.0:
        return "100% Group"
    bucket = int(rate // 10) * 10
    bucket = max(0, min(90, bucket))
    return f"{bucket}% - {bucket + 9}% Group"

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
    "📝 Quick Log / Edit Sessions",
    "✏️ Edit Roster",
    "📁 Upload Roster CSV",
    "📁 Upload Attendance CSV",
    "⚙️ Data Management"
])

# ---------------------------------------------------------
# PAGE 1: ANALYTICS DASHBOARD
# ---------------------------------------------------------
if page == "📈 Analytics Dashboard":
    st.subheader("📈 Alliance Intelligence & Attendance Analytics")

    roster_df = st.session_state.roster_df
    att_df = st.session_state.attendance_df

    if roster_df.empty:
        st.warning("No players found in roster.")
    else:
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

            rounded_rate = round(attendance_rate, 1)
            stats.append({
                "Player Name": p_name,
                "Castle Level": p_row.get("Castle Level", "—"),
                "Lord Level": p_row.get("Lord Level", "—"),
                "Alliance Rank": p_row.get("Alliance Rank", "—"),
                "Member Status": p_status,
                "Active Count": active_cnt,
                "Zero Points Count": zero_cnt,
                "Total Logged": player_total_logged,
                "Attendance Rate": rounded_rate,
                "Attendance Tier": get_attendance_tier(rounded_rate)
            })

        summary_df = pd.DataFrame(stats)
        active_summary_df = summary_df[summary_df["Member Status"] == "Active"]

        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Active Roster", len(active_summary_df))
        m2.metric("Tracked Events", total_sessions)
        avg_att = active_summary_df["Attendance Rate"].mean() if not active_summary_df.empty else 0
        m3.metric("Alliance Turnout", f"{avg_att:.1f}%")
        total_zero_pts = summary_df["Zero Points Count"].sum() if not summary_df.empty else 0
        m4.metric("Zero-Point Instances", total_zero_pts, delta=f"-{total_zero_pts} inactive" if total_zero_pts > 0 else "Optimal", delta_color="inverse")

        st.markdown("---")

        tab_explorer, tab_tiers = st.tabs(["🎯 Threshold Explorer & Roster", "📊 10% Attendance Bracket Grid"])

        # -------------------------------------------------
        # TAB A: INTERACTIVE THRESHOLD SLIDER & FILTER
        # -------------------------------------------------
        with tab_explorer:
            f1, f2, f3, f4 = st.columns([2, 2.5, 1.5, 1.5])
            filter_mode = f1.selectbox(
                "View Section",
                ["All Members", "Below Threshold (<)", "At or Above Threshold (≥)"],
                index=0
            )
            threshold_val = f2.slider(
                "Attendance Threshold (%)",
                min_value=0,
                max_value=100,
                value=70,
                step=5,
                disabled=(filter_mode == "All Members")
            )
            status_filter = f3.selectbox(
                "Member Status",
                ["Active Only", "All", "Inactive Only"],
                index=0
            )
            rank_filter = f4.selectbox(
                "Alliance Rank",
                ["All Ranks"] + ALLIANCE_RANK_OPTIONS,
                index=0
            )

            filtered_df = summary_df.copy()
            if status_filter == "Active Only":
                filtered_df = filtered_df[filtered_df["Member Status"] == "Active"]
            elif status_filter == "Inactive Only":
                filtered_df = filtered_df[filtered_df["Member Status"] == "Inactive"]

            if rank_filter != "All Ranks":
                filtered_df = filtered_df[filtered_df["Alliance Rank"] == rank_filter]

            if filter_mode == "Below Threshold (<)":
                filtered_df = filtered_df[filtered_df["Attendance Rate"] < threshold_val].sort_values(
                    by=["Attendance Rate", "Player Name"], ascending=[True, True]
                )
                section_caption = f"Showing **{len(filtered_df)}** member(s) **below {threshold_val}%** attendance"
            elif filter_mode == "At or Above Threshold (≥)":
                filtered_df = filtered_df[filtered_df["Attendance Rate"] >= threshold_val].sort_values(
                    by=["Attendance Rate", "Player Name"], ascending=[False, True]
                )
                section_caption = f"Showing **{len(filtered_df)}** member(s) **at or above {threshold_val}%** attendance"
            else:
                filtered_df = filtered_df.sort_values(by="Player Name", key=lambda c: c.str.lower())
                section_caption = f"Showing all **{len(filtered_df)}** matching member(s)"

            st.caption(section_caption)

            if filtered_df.empty:
                st.info("No members match the selected threshold and filters.")
            else:
                display_df = filtered_df.copy()
                display_df["Turnout"] = (display_df["Active Count"] + display_df["Zero Points Count"]).astype(str) + " / " + display_df["Total Logged"].astype(str)

                st.dataframe(
                    display_df[[
                        "Player Name",
                        "Castle Level",
                        "Lord Level",
                        "Alliance Rank",
                        "Member Status",
                        "Attendance Tier",
                        "Turnout",
                        "Active Count",
                        "Zero Points Count",
                        "Attendance Rate"
                    ]],
                    column_config={
                        "Active Count": st.column_config.NumberColumn("Active Part."),
                        "Zero Points Count": st.column_config.NumberColumn("Zero Pts"),
                        "Attendance Rate": st.column_config.ProgressColumn(
                            "Attendance %",
                            min_value=0,
                            max_value=100,
                            format="%.1f%%"
                        )
                    },
                    use_container_width=True,
                    hide_index=True
                )

        # -------------------------------------------------
        # TAB B: 10% ATTENDANCE BRACKET GRID
        # -------------------------------------------------
        with tab_tiers:
            t_col1, t_col2 = st.columns([2, 3])
            tier_status_filter = t_col1.radio(
                "Roster Scope",
                ["Active Members Only", "All Members"],
                horizontal=True,
                key="tier_scope_radio"
            )
            hide_empty_tiers = t_col2.checkbox("Hide empty 10% brackets", value=False)

            tier_source_df = active_summary_df if tier_status_filter == "Active Members Only" else summary_df

            # Compact visual distribution bar across the 10% brackets
            tier_counts_series = pd.Series(
                {tier: int((tier_source_df["Attendance Tier"] == tier).sum()) for tier in TIER_ORDER}
            )
            st.markdown("#### 📈 Headcount by 10% Attendance Bracket")
            st.bar_chart(tier_counts_series, color="#38bdf8", height=220)

            st.markdown("---")
            st.markdown("#### 🗂️ Member Breakdown by 10% Bracket")

            tiers_to_render = [
                t for t in TIER_ORDER
                if not hide_empty_tiers or int((tier_source_df["Attendance Tier"] == t).sum()) > 0
            ]

            if not tiers_to_render:
                st.info("No members found for the selected scope.")
            else:
                grid_cols = st.columns(3)
                for idx, tier_label in enumerate(tiers_to_render):
                    tier_members = tier_source_df[tier_source_df["Attendance Tier"] == tier_label].sort_values(
                        by=["Attendance Rate", "Player Name"], ascending=[False, True]
                    )
                    member_count = len(tier_members)

                    if member_count == 0:
                        rows_html = '<div style="color:#64748b; font-size:12px; padding:6px 0;">No members in this bracket</div>'
                    else:
                        row_items = []
                        for _, m_row in tier_members.iterrows():
                            turnout_txt = f"{m_row['Active Count'] + m_row['Zero Points Count']}/{m_row['Total Logged']}"
                            row_items.append(
                                f'<div class="tier-member-row">'
                                f'<span><strong>{m_row["Player Name"]}</strong> <span style="color:#64748b; font-size:11px;">({m_row["Alliance Rank"]})</span></span>'
                                f'<span style="color:#38bdf8; font-weight:600;">{m_row["Attendance Rate"]:.1f}% <span style="color:#94a3b8; font-weight:400;">[{turnout_txt}]</span></span>'
                                f'</div>'
                            )
                        rows_html = "".join(row_items)

                    card_html = (
                        f'<div class="tier-card">'
                        f'<div class="tier-card-header">'
                        f'<span class="tier-title">{tier_label}</span>'
                        f'<span class="tier-badge">{member_count}</span>'
                        f'</div>'
                        f'{rows_html}'
                        f'</div>'
                    )
                    with grid_cols[idx % 3]:
                        st.markdown(card_html, unsafe_allow_html=True)

# ---------------------------------------------------------
# PAGE 2: QUICK LOG / EDIT SESSIONS
# ---------------------------------------------------------
elif page == "📝 Quick Log / Edit Sessions":
    st.subheader("📝 Event Session Management")

    tab_new, tab_edit = st.tabs(["➕ Log New Session", "✏️ Edit Existing Session"])

    with tab_new:
        col1, col2, col3 = st.columns(3)
        selected_event = col1.selectbox("Event Type", EVENTS_LIST, key="new_ev")
        event_date = col2.date_input("Event Date", datetime.now(), key="new_dt")
        session_label = col3.text_input("Session Identifier (Optional)", placeholder="e.g., Run 1, Match 2", key="new_lbl")

        unique_suffix = session_label.strip() if session_label.strip() else "Default"
        session_id = f"{event_date}_{selected_event}_{unique_suffix}"

        with st.expander("➕ Spot a New Teammate? Quick-Add to Roster & Session"):
            with st.form("quick_add_session_member", clear_on_submit=True):
                qa1, qa2, qa3, qa4 = st.columns([3, 1.5, 1.5, 2])
                qa_name = qa1.text_input("New Player Name", placeholder="Exact in-game name")
                qa_castle = qa2.selectbox("Castle Level", CASTLE_LEVEL_OPTIONS, index=34)
                qa_rank = qa3.selectbox("Alliance Rank", ALLIANCE_RANK_OPTIONS, index=4)
                qa_att_status = qa4.selectbox("Status for This Event", ATTENDANCE_STATUS_OPTIONS, index=0)

                if st.form_submit_button("Add & Include in Session", type="primary"):
                    ok, msg = add_member_to_roster(
                        name=qa_name,
                        castle=qa_castle,
                        rank=qa_rank,
                        status="Active"
                    )
                    if ok:
                        st.session_state[f"quick_status_{session_id}_{qa_name.strip()}"] = qa_att_status
                        st.success(f"{msg} Included below as **{qa_att_status}**.")
                    else:
                        st.error(msg)

        roster_names = get_sorted_roster_names(active_only=True)

        if not roster_names:
            st.error("No active players found in roster. Add a teammate above or update statuses in the Roster Editor.")
        else:
            st.markdown("---")
            st.markdown("### 📋 Active Members Attendance Matrix")
            st.info("Listing **Active** members alphabetically. Default status is **Active**.")

            initial_statuses = [
                st.session_state.get(f"quick_status_{session_id}_{name}", "Active")
                for name in roster_names
            ]

            session_grid_df = pd.DataFrame({
                "Player Name": roster_names,
                "Status": initial_statuses
            })

            edited_session_df = st.data_editor(
                session_grid_df,
                column_config={
                    "Player Name": st.column_config.TextColumn("Player Name", disabled=True),
                    "Status": st.column_config.SelectboxColumn(
                        "Attendance Status",
                        options=ATTENDANCE_STATUS_OPTIONS,
                        required=True
                    )
                },
                hide_index=True,
                use_container_width=True,
                key=f"editor_new_{session_id}"
            )

            st.markdown("---")
            if st.button("💾 Save New Event Session", type="primary", use_container_width=True):
                final_session_id = session_id if session_label.strip() else f"{event_date}_{selected_event}_{datetime.now().strftime('%H%M%S')}"
                new_records = []
                for _, row in edited_session_df.iterrows():
                    new_records.append({
                        "Session ID": final_session_id,
                        "Event": selected_event,
                        "Date": str(event_date),
                        "Player Name": row["Player Name"],
                        "Status": row["Status"]
                    })

                new_df = pd.DataFrame(new_records)
                st.session_state.attendance_df = st.session_state.attendance_df[st.session_state.attendance_df["Session ID"] != final_session_id]
                st.session_state.attendance_df = pd.concat([st.session_state.attendance_df, new_df], ignore_index=True)
                save_attendance()
                st.success(f"Successfully recorded session **{selected_event}** on **{event_date}**!")

    with tab_edit:
        att_df = st.session_state.attendance_df
        if att_df.empty or "Session ID" not in att_df.columns:
            st.info("No recorded sessions available to edit.")
        else:
            unique_sessions = att_df[["Session ID", "Event", "Date"]].drop_duplicates().to_dict('records')

            selected_session_to_edit = st.selectbox(
                "Select Session to Edit",
                options=unique_sessions,
                format_func=lambda x: f"{x['Event']} on {x['Date']} (ID: {x['Session ID']})"
            )

            if selected_session_to_edit:
                target_session_id = selected_session_to_edit["Session ID"]
                session_logs = att_df[att_df["Session ID"] == target_session_id]

                current_statuses = {row["Player Name"]: row["Status"] for _, row in session_logs.iterrows()}
                session_players = sorted(session_logs["Player Name"].dropna().unique().tolist(), key=lambda x: x.lower())
                session_players_lower = {p.strip().lower() for p in session_players}

                st.markdown(f"### Editing Session: **{selected_session_to_edit['Event']}** ({selected_session_to_edit['Date']})")

                col_add_exp, col_rem_exp = st.columns(2)

                with col_add_exp.expander("➕ Add Missing Member to This Session"):
                    all_roster_names = get_sorted_roster_names(active_only=False)
                    missing_from_session = [n for n in all_roster_names if n.strip().lower() not in session_players_lower]

                    add_tab_existing, add_tab_new = st.tabs(["From Existing Roster", "New Player"])

                    with add_tab_existing:
                        if not missing_from_session:
                            st.info("All current roster members are already in this session.")
                        else:
                            with st.form(f"add_existing_to_session_{target_session_id}", clear_on_submit=True):
                                chosen_member = st.selectbox("Select Roster Member", missing_from_session)
                                chosen_status = st.selectbox("Attendance Status", ATTENDANCE_STATUS_OPTIONS, index=0)

                                if st.form_submit_button("Add Member to Session", type="primary", use_container_width=True):
                                    ok, msg = add_member_to_session(
                                        session_id=target_session_id,
                                        event_name=selected_session_to_edit["Event"],
                                        event_date=selected_session_to_edit["Date"],
                                        player_name=chosen_member,
                                        status_val=chosen_status
                                    )
                                    if ok:
                                        st.success(msg)
                                        st.rerun()
                                    else:
                                        st.error(msg)

                    with add_tab_new:
                        with st.form(f"add_new_to_session_{target_session_id}", clear_on_submit=True):
                            ns_name = st.text_input("New Player Name", placeholder="Exact in-game name")
                            ns_castle = st.selectbox("Castle Level", CASTLE_LEVEL_OPTIONS, index=34)
                            ns_rank = st.selectbox("Alliance Rank", ALLIANCE_RANK_OPTIONS, index=4)
                            ns_status = st.selectbox("Attendance Status", ATTENDANCE_STATUS_OPTIONS, index=0)

                            if st.form_submit_button("Add to Roster & Session", type="primary", use_container_width=True):
                                clean_ns = ns_name.strip()
                                ok_roster, msg_roster = add_member_to_roster(
                                    name=clean_ns,
                                    castle=ns_castle,
                                    rank=ns_rank,
                                    status="Active"
                                )
                                if ok_roster:
                                    ok_sess, msg_sess = add_member_to_session(
                                        session_id=target_session_id,
                                        event_name=selected_session_to_edit["Event"],
                                        event_date=selected_session_to_edit["Date"],
                                        player_name=clean_ns,
                                        status_val=ns_status
                                    )
                                    if ok_sess:
                                        st.success(f"{msg_roster} {msg_sess}")
                                        st.rerun()
                                    else:
                                        st.error(msg_sess)
                                else:
                                    st.error(msg_roster)

                with col_rem_exp.expander("🗑️ Remove Member from This Session"):
                    if not session_players:
                        st.info("No members in this session.")
                    else:
                        with st.form(f"remove_from_session_{target_session_id}", clear_on_submit=True):
                            members_to_remove = st.multiselect(
                                "Select Member(s) to Remove from This Event",
                                options=session_players,
                                help="Removes their entry from this specific session only. Does not delete them from your main roster."
                            )
                            if st.form_submit_button("Remove Selected from Session", use_container_width=True):
                                if not members_to_remove:
                                    st.warning("Select at least one member to remove.")
                                else:
                                    removed_total = 0
                                    for m in members_to_remove:
                                        removed_total += remove_member_from_session(target_session_id, m)
                                    st.success(f"Removed {removed_total} entry(s) from this session!")
                                    st.rerun()

                st.info("Modify statuses in the table below and click **Update Session Matrix**.")

                edit_grid_data = []
                for p_name in session_players:
                    stat = current_statuses.get(p_name, "Active")
                    if stat not in ATTENDANCE_STATUS_OPTIONS:
                        stat = "Active"
                    edit_grid_data.append({"Player Name": p_name, "Status": stat})

                edit_session_df = pd.DataFrame(edit_grid_data)

                updated_session_df = st.data_editor(
                    edit_session_df,
                    column_config={
                        "Player Name": st.column_config.TextColumn("Player Name", disabled=True),
                        "Status": st.column_config.SelectboxColumn(
                            "Attendance Status",
                            options=ATTENDANCE_STATUS_OPTIONS,
                            required=True
                        )
                    },
                    hide_index=True,
                    use_container_width=True,
                    key=f"editor_edit_{target_session_id}"
                )

                st.markdown("---")
                col_save, col_del = st.columns([2, 1])

                if col_save.button("💾 Update Session Matrix", type="primary", use_container_width=True):
                    updated_records = []
                    for _, row in updated_session_df.iterrows():
                        updated_records.append({
                            "Session ID": target_session_id,
                            "Event": selected_session_to_edit["Event"],
                            "Date": selected_session_to_edit["Date"],
                            "Player Name": row["Player Name"],
                            "Status": row["Status"]
                        })

                    st.session_state.attendance_df = st.session_state.attendance_df[st.session_state.attendance_df["Session ID"] != target_session_id]
                    updated_df = pd.DataFrame(updated_records)
                    st.session_state.attendance_df = pd.concat([st.session_state.attendance_df, updated_df], ignore_index=True)
                    save_attendance()
                    st.success("Session successfully updated!")

                if col_del.button("🗑️ Delete Entire Session", use_container_width=True):
                    st.session_state.attendance_df = st.session_state.attendance_df[st.session_state.attendance_df["Session ID"] != target_session_id]
                    save_attendance()
                    st.warning("Session deleted permanently!")
                    st.rerun()

# ---------------------------------------------------------
# PAGE 3: EDIT ROSTER (ADD MEMBER + RENAME WITH HISTORY + MERGE/PURGE)
# ---------------------------------------------------------
elif page == "✏️ Edit Roster":
    st.subheader("✏️ Direct Roster Management")
    st.markdown("Add new members, rename existing players (**past attendance history automatically moves with them**), or merge/clean up duplicate avatar names.")

    top_col1, top_col2 = st.columns(2)

    with top_col1.expander("➕ Add New Member to Roster", expanded=False):
        with st.form("add_new_member_roster_form", clear_on_submit=True):
            r1, r2, r3 = st.columns(3)
            add_name = r1.text_input("Player Name", placeholder="Enter exact player name")
            add_rank = r2.selectbox("Alliance Rank", ALLIANCE_RANK_OPTIONS, index=4)
            add_status = r3.selectbox("Member Status", STATUS_OPTIONS, index=0)

            r4, r5, r6 = st.columns(3)
            add_castle = r4.selectbox("Castle Level", CASTLE_LEVEL_OPTIONS, index=34)
            add_lord = r5.selectbox("Lord Level", LORD_LEVEL_OPTIONS, index=50)
            add_mil = r6.selectbox("Military Rank", MILITARY_RANK_OPTIONS, index=0)

            if st.form_submit_button("➕ Add Member", type="primary", use_container_width=True):
                ok, msg = add_member_to_roster(
                    name=add_name,
                    castle=add_castle,
                    lord=add_lord,
                    mil=add_mil,
                    rank=add_rank,
                    status=add_status
                )
                if ok:
                    st.success(msg)
                    st.rerun()
                else:
                    st.error(msg)

    with top_col2.expander("🔀 Merge / Purge Duplicate Avatar History", expanded=False):
        att_df = st.session_state.attendance_df
        roster_names_all = get_sorted_roster_names(active_only=False)
        att_names_all = sorted(att_df["Player Name"].dropna().unique().tolist(), key=lambda x: x.lower()) if not att_df.empty else []
        all_known_names = sorted(list(set(roster_names_all + att_names_all)), key=lambda x: x.lower())

        if not all_known_names:
            st.info("No player records found yet.")
        else:
            merge_tab, purge_tab = st.tabs(["Merge Old Name → Current Name", "Remove Name Completely"])

            with merge_tab:
                with st.form("merge_duplicate_history_form"):
                    old_avatar = st.selectbox("Old / Duplicate Avatar Name", all_known_names, key="merge_old")
                    target_avatar = st.selectbox("Merge Into Current Roster Member", roster_names_all if roster_names_all else all_known_names, key="merge_new")
                    remove_old_from_roster = st.checkbox("Also delete old avatar row from Roster", value=True)

                    if st.form_submit_button("Merge Attendance History", type="primary", use_container_width=True):
                        if old_avatar.strip().lower() == target_avatar.strip().lower():
                            st.error("Select two different names to merge.")
                        else:
                            moved = migrate_attendance_names({old_avatar: target_avatar})
                            if remove_old_from_roster:
                                st.session_state.roster_df = st.session_state.roster_df[
                                    st.session_state.roster_df["Player Name"].str.strip().str.lower() != old_avatar.strip().lower()
                                ].reset_index(drop=True)
                                save_roster()
                            st.success(f"Merged **{moved}** attendance record(s) from **{old_avatar}** into **{target_avatar}**!")
                            st.rerun()

            with purge_tab:
                with st.form("purge_phantom_member_form"):
                    purge_target = st.selectbox("Select Name to Remove", all_known_names, key="purge_sel")
                    purge_roster = st.checkbox("Remove from Roster", value=True)
                    purge_att = st.checkbox("Remove from All Attendance Logs", value=True)

                    if st.form_submit_button("Remove Selected Member", use_container_width=True):
                        removed_att = purge_player_from_all_attendance(purge_target) if purge_att else 0
                        if purge_roster:
                            st.session_state.roster_df = st.session_state.roster_df[
                                st.session_state.roster_df["Player Name"].str.strip().str.lower() != purge_target.strip().lower()
                            ].reset_index(drop=True)
                            save_roster()
                        st.success(f"Removed **{purge_target}** ({removed_att} attendance record(s) cleared).")
                        st.rerun()

    st.markdown("---")
    roster_df = st.session_state.roster_df.copy()
    sorted_roster = roster_df.sort_values(by="Player Name", key=lambda col: col.str.lower()).reset_index(drop=True)

    edited_roster_data = []
    rename_mappings = {}

    for idx, row in sorted_roster.iterrows():
        p_name = row["Player Name"]
        with st.expander(f"🛡️ {p_name} — Rank: {row.get('Alliance Rank', 'Member')} | Status: {row.get('Status', 'Active')}"):
            c1, c2, c3 = st.columns(3)

            new_name = c1.text_input("Player Name (renaming keeps all history)", value=p_name, key=f"edit_name_{idx}")

            curr_rank = row.get("Alliance Rank", "Member")
            rank_idx = ALLIANCE_RANK_OPTIONS.index(curr_rank) if curr_rank in ALLIANCE_RANK_OPTIONS else 4
            new_rank = c2.selectbox("Alliance Rank", ALLIANCE_RANK_OPTIONS, index=rank_idx, key=f"edit_rank_{idx}")

            curr_status = row.get("Status", "Active")
            status_idx = STATUS_OPTIONS.index(curr_status) if curr_status in STATUS_OPTIONS else 0
            new_status = c3.selectbox("Member Status", STATUS_OPTIONS, index=status_idx, key=f"edit_status_{idx}", help="Set to Inactive to exclude from future event sessions while preserving past records.")

            c4, c5, c6 = st.columns(3)

            curr_castle = str(row.get("Castle Level", "40"))
            castle_idx = CASTLE_LEVEL_OPTIONS.index(curr_castle) if curr_castle in CASTLE_LEVEL_OPTIONS else 0
            new_castle = c4.selectbox("Castle Level", CASTLE_LEVEL_OPTIONS, index=castle_idx, key=f"edit_castle_{idx}")

            curr_lord = str(row.get("Lord Level", "50"))
            lord_idx =
