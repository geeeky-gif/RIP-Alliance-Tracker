import streamlit as st
import pandas as pd
import os
import math
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
EDITOR_PASSWORD = "rip123"

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

# ---------------------------------------------------------
# STATE INITIALIZATION
# ---------------------------------------------------------
if "editor_unlocked" not in st.session_state:
    st.session_state.editor_unlocked = False

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

def require_editor_access(section_label):
    """Prompts once per session for the editor password before rendering protected pages."""
    if st.session_state.editor_unlocked:
        return True

    st.subheader(f"🔒 {section_label} — Editor Access Required")
    st.info("The Analytics Dashboard is open to view. Enter the editor password once to unlock editing and data tools for this session.")

    with st.form(f"unlock_form_{section_label}"):
        entered_pwd = st.text_input("Editor Password", type="password", placeholder="Enter password")
        submitted = st.form_submit_button("🔓 Unlock Editor", type="primary")
        if submitted:
            if entered_pwd == EDITOR_PASSWORD:
                st.session_state.editor_unlocked = True
                st.success("Editor unlocked for this session.")
                st.rerun()
            else:
                st.error("Incorrect password.")
    return False

def get_sorted_roster_names(active_only=True):
    if "roster_df" in st.session_state and not st.session_state.roster_df.empty:
        df = st.session_state.roster_df
        if active_only:
            df = df[df["Status"] == "Active"]
        names = df["Player Name"].dropna().astype(str).tolist()
        return sorted(names, key=lambda x: x.lower())
    return []

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
# SIDEBAR NAVIGATION & SESSION LOCK STATUS
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

st.sidebar.markdown("---")
if st.session_state.editor_unlocked:
    st.sidebar.success("🔓 Editor Mode: Unlocked")
    if st.sidebar.button("🔒 Lock Editor", use_container_width=True):
        st.session_state.editor_unlocked = False
        st.rerun()
else:
    st.sidebar.caption("🔒 Editor Mode: Locked (View-Only)")
    with st.sidebar.expander("Unlock Editor"):
        sb_pwd = st.text_input("Password", type="password", key="sidebar_pwd_input")
        if st.button("Unlock", key="sidebar_unlock_btn", use_container_width=True):
            if sb_pwd == EDITOR_PASSWORD:
                st.session_state.editor_unlocked = True
                st.rerun()
            else:
                st.error("Incorrect password.")

# ---------------------------------------------------------
# PAGE 1: ANALYTICS DASHBOARD (PUBLIC VIEW)
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
        active_summary_df = summary_df[summary_df["Member Status"] == "Active"].copy()

        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Active Roster", len(active_summary_df))
        m2.metric("Tracked Events", total_sessions)
        avg_att = active_summary_df["Attendance Rate"].mean() if not active_summary_df.empty else 0
        m3.metric("Alliance Turnout", f"{avg_att:.1f}%")
        total_zero_pts = active_summary_df["Zero Points Count"].sum() if not active_summary_df.empty else 0
        m4.metric("Zero-Point Instances", total_zero_pts, delta=f"-{total_zero_pts} inactive" if total_zero_pts > 0 else "Optimal", delta_color="inverse")

        st.markdown("---")
        st.markdown("### 🎯 Attendance Cutoff & Top Performers")

        min_threshold = st.slider(
            "Attendance Threshold (%)",
            min_value=0,
            max_value=100,
            value=80,
            step=5,
            help="Left chart shows active members attending at or above this percentage. Right leaderboard shows the top percentile tier (100% minus slider)."
        )

        qualifying_df = active_summary_df[active_summary_df["Attendance Rate"] >= min_threshold].sort_values(
            by=["Attendance Rate", "Active Count", "Player Name"],
            ascending=[False, False, True],
            key=lambda col: col.str.lower() if col.name == "Player Name" else col
        ).copy()

        top_percentile_pct = max(0, 100 - min_threshold)
        total_active_count = len(active_summary_df)
        if total_active_count > 0:
            if top_percentile_pct == 0:
                top_tier_count = 1
            else:
                top_tier_count = max(1, math.ceil(total_active_count * (top_percentile_pct / 100.0)))
        else:
            top_tier_count = 0

        k1, k2, k3 = st.columns(3)
        k1.metric(f"Active Members >= {min_threshold}%", f"{len(qualifying_df)} / {total_active_count}")
        k2.metric("Top Tier Cutoff", f"Top {top_percentile_pct if top_percentile_pct > 0 else 100}%")
        k3.metric("Top Tier Shown", top_tier_count)

        left_vis, right_vis = st.columns([3, 2])

        with left_vis:
            st.markdown(f"#### 📊 Active Members Attending >= {min_threshold}%")
            if qualifying_df.empty:
                st.info(f"No active members have attended at least {min_threshold}% of events.")
            else:
                bar_df = qualifying_df.iloc[::-1].set_index("Player Name")[["Attendance Rate"]]
                st.caption(f"Showing {len(bar_df)} active member(s) at or above {min_threshold}%")
                st.bar_chart(bar_df, horizontal=True, height=420, color="#38bdf8")

        with right_vis:
            st.markdown(f"#### 🏆 Top Performers (Top {top_percentile_pct if top_percentile_pct > 0 else 100}% of Active)")
            ranked_active = active_summary_df.sort_values(
                by=["Attendance Rate", "Active Count", "Total Logged", "Player Name"],
                ascending=[False, False, False, True],
                key=lambda col: col.str.lower() if col.name == "Player Name" else col
            ).copy()

            if ranked_active.empty or top_tier_count == 0:
                st.info("No active member attendance data available yet.")
            else:
                top_lb = ranked_active.head(top_tier_count).copy()
                top_lb.insert(0, "Rank", range(1, len(top_lb) + 1))
                top_lb["Turnout"] = (top_lb["Active Count"] + top_lb["Zero Points Count"]).astype(str) + "/" + top_lb["Total Logged"].astype(str)
                top_lb["Rate"] = top_lb["Attendance Rate"].astype(str) + "%"
                st.dataframe(
                    top_lb[["Rank", "Player Name", "Rate", "Turnout", "Zero Points Count"]].rename(
                        columns={"Zero Points Count": "0-Pt"}
                    ),
                    use_container_width=True,
                    hide_index=True,
                    height=420
                )

        st.markdown("---")
        st.markdown("#### 📋 Active Member Performance Matrix")
        display_df = active_summary_df.sort_values(
            by=["Attendance Rate", "Active Count", "Player Name"],
            ascending=[False, False, True],
            key=lambda col: col.str.lower() if col.name == "Player Name" else col
        ).copy()
        display_df["Turnout"] = (display_df["Active Count"] + display_df["Zero Points Count"]).astype(str) + " / " + display_df["Total Logged"].astype(str)
        display_df["Active Part."] = display_df["Active Count"].astype(str)
        display_df["Zero Points"] = display_df["Zero Points Count"].astype(str)
        display_df["Attendance %"] = display_df["Attendance Rate"].astype(str) + "%"

        st.dataframe(display_df[["Player Name", "Castle Level", "Lord Level", "Alliance Rank", "Turnout", "Active Part.", "Zero Points", "Attendance %"]], use_container_width=True, hide_index=True)

# ---------------------------------------------------------
# PAGE 2: QUICK LOG / EDIT SESSIONS (PROTECTED)
# ---------------------------------------------------------
elif page == "📝 Quick Log / Edit Sessions":
    if require_editor_access("Quick Log / Edit Sessions"):
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
# PAGE 3: EDIT ROSTER (PROTECTED)
# ---------------------------------------------------------
elif page == "✏️ Edit Roster":
    if require_editor_access("Edit Roster"):
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
                merge_tab, purge_tab = st.tabs(["Merge Old Name -> Current Name", "Remove Name Completely"])

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
                lord_idx = LORD_LEVEL_OPTIONS.index(curr_lord) if curr_lord in LORD_LEVEL_OPTIONS else 0
                new_lord = c5.selectbox("Lord Level", LORD_LEVEL_OPTIONS, index=lord_idx, key=f"edit_lord_{idx}")

                curr_mil = str(row.get("Military Rank", ""))
                mil_idx = MILITARY_RANK_OPTIONS.index(curr_mil) if curr_mil in MILITARY_RANK_OPTIONS else 0
                new_mil = c6.selectbox("Military Rank", MILITARY_RANK_OPTIONS, index=mil_idx, key=f"edit_mil_{idx}")

                clean_new_name = new_name.strip() if new_name.strip() else p_name
                if clean_new_name != p_name:
                    rename_mappings[p_name] = clean_new_name

                edited_roster_data.append({
                    "Player Name": clean_new_name,
                    "Castle Level": new_castle,
                    "Lord Level": new_lord,
                    "Military Rank": new_mil,
                    "Alliance Rank": new_rank,
                    "Status": new_status
                })

        st.markdown("---")
        if st.button("💾 Save All Roster Changes", type="primary", use_container_width=True):
            new_df = pd.DataFrame(edited_roster_data)
            new_df["_norm"] = new_df["Player Name"].str.strip().str.lower()
            new_df = new_df.drop_duplicates(subset=["_norm"], keep="last").drop(columns=["_norm"]).reset_index(drop=True)

            st.session_state.roster_df = new_df
            save_roster()

            migrated_records = migrate_attendance_names(rename_mappings)
            if migrated_records > 0:
                st.success(f"Roster updated and migrated **{migrated_records}** historical attendance record(s) to the new name(s)!")
            else:
                st.success("Roster profiles updated successfully!")
            st.rerun()

# ---------------------------------------------------------
# PAGE 4: UPLOAD ROSTER CSV (PROTECTED)
# ---------------------------------------------------------
elif page == "📁 Upload Roster CSV":
    if require_editor_access("Upload Roster CSV"):
        st.subheader("📁 Simple Roster Import")
        st.markdown("Upload a CSV file containing columns: `Player Name`, `Castle Level`, `Lord Level`, `Military Rank`, `Alliance Rank`, `Status`.")

        uploaded_file = st.file_uploader("Choose CSV file", type=["csv"], key="roster_csv_uploader")

        if uploaded_file is not None:
            try:
                uploaded_df = pd.read_csv(uploaded_file, dtype=str)
                st.markdown("#### Preview Uploaded Data:")
                st.dataframe(uploaded_df.head(), use_container_width=True)

                if st.button("Confirm & Overwrite Roster", type="primary"):
                    uploaded_df.columns = [c.strip() for c in uploaded_df.columns]

                    for col, default_val in [("Castle Level", "40"), ("Lord Level", "50"), ("Military Rank", ""), ("Alliance Rank", "Member"), ("Status", "Active")]:
                        if col not in uploaded_df.columns:
                            uploaded_df[col] = default_val

                    st.session_state.roster_df = uploaded_df[["Player Name", "Castle Level", "Lord Level", "Military Rank", "Alliance Rank", "Status"]]
                    save_roster()
                    st.success("Roster successfully replaced and saved!")
            except Exception as e:
                st.error(f"Error reading CSV file: {e}")

# ---------------------------------------------------------
# PAGE 5: UPLOAD ATTENDANCE CSV (PROTECTED)
# ---------------------------------------------------------
elif page == "📁 Upload Attendance CSV":
    if require_editor_access("Upload Attendance CSV"):
        st.subheader("📁 Attendance Records Import")
        st.markdown("Upload an attendance CSV file containing `Session ID`, `Event`, `Date`, `Player Name`, and `Status` (`Active`, `Zero Points`, or `Absent`).")

        uploaded_att_file = st.file_uploader("Choose Attendance CSV file", type=["csv"], key="attendance_csv_uploader")

        if uploaded_att_file is not None:
            try:
                raw_att_df = pd.read_csv(uploaded_att_file, dtype=str)
                normalized_df = normalize_attendance_df(raw_att_df)

                if normalized_df.empty:
                    st.warning("No valid attendance rows with a `Player Name` were found in the uploaded file.")
                else:
                    st.markdown("#### Preview Normalized Attendance Records:")
                    st.dataframe(normalized_df.head(15), use_container_width=True, hide_index=True)

                    import_mode = st.radio(
                        "Import Mode:",
                        ["Merge / Update matching Session IDs", "Overwrite All Attendance Logs"],
                        horizontal=True
                    )

                    if st.button("Confirm Attendance Import", type="primary"):
                        if import_mode == "Overwrite All Attendance Logs":
                            st.session_state.attendance_df = normalized_df
                        else:
                            existing_df = normalize_attendance_df(st.session_state.attendance_df) if not st.session_state.attendance_df.empty else pd.DataFrame(columns=["Session ID", "Event", "Date", "Player Name", "Status"])
                            imported_session_ids = normalized_df["Session ID"].unique().tolist()
                            filtered_existing = existing_df[~existing_df["Session ID"].isin(imported_session_ids)]
                            st.session_state.attendance_df = pd.concat([filtered_existing, normalized_df], ignore_index=True)

                        save_attendance()
                        st.success(f"Successfully imported **{len(normalized_df)}** attendance records across **{normalized_df['Session ID'].nunique()}** session(s)!")
            except Exception as e:
                st.error(f"Error reading attendance CSV file: {e}")

# ---------------------------------------------------------
# PAGE 6: DATA MANAGEMENT (PROTECTED)
# ---------------------------------------------------------
elif page == "⚙️ Data Management":
    if require_editor_access("Data Management"):
        st.subheader("⚙️ Data Management & Exports")

        c1, c2 = st.columns(2)

        with c1:
            st.markdown("### Export Data")
            st.download_button(
                "📥 Download Roster CSV",
                data=st.session_state.roster_df.to_csv(index=False).encode("utf-8"),
                file_name="roster_data.csv",
                mime="text/csv",
                use_container_width=True
            )
            st.download_button(
                "📥 Download Attendance Log CSV",
                data=st.session_state.attendance_df.to_csv(index=False).encode("utf-8"),
                file_name="attendance_matrix.csv",
                mime="text/csv",
                use_container_width=True
            )

        with c2:
            st.markdown("### Reset Data")
            if st.button("🚨 Clear All Attendance Logs"):
                st.session_state.attendance_df = pd.DataFrame(columns=["Session ID", "Event", "Date", "Player Name", "Status"])
                save_attendance()
                st.warning("All attendance records cleared!")
