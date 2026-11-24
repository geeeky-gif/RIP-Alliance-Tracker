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
        active_summary_df = summary_df[summary_df["Member Status"] == "Active"]

        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Active Roster", len(active_summary_df))
        m2.metric("Tracked Events", total_sessions)
        avg_att = active_summary_df["Attendance Rate"].mean() if not active_summary_df.empty else 0
        m3.metric("Alliance Turnout", f"{avg_att:.1f}%")
        total_zero_pts = summary_df["Zero Points Count"].sum() if not summary_df.empty else 0
        m4.metric("Zero-Point Instances", total_zero_pts, delta=f"-{total_zero_pts} inactive" if total_zero_pts > 0 else "Optimal", delta_color="inverse")

        st.markdown("---")
        st.markdown("### 🎯 Minimum Attendance Threshold & Top Performers")

        f_col1, f_col2, f_col3 = st.columns([2, 1.5, 1.5])
        min_threshold = f_col1.slider(
            "Minimum Required Attendance (%)",
            min_value=0,
            max_value=100,
            value=70,
            step=5
        )
        roster_scope = f_col2.selectbox(
            "Member Scope",
            ["Active Only", "All Roster (Incl. Inactive)"]
        )
        threshold_view = f_col3.selectbox(
            "Threshold View",
            ["All in Scope", "Below Minimum Only", "Meeting Minimum Only"]
        )

        scoped_df = active_summary_df.copy() if roster_scope == "Active Only" else summary_df.copy()
        scoped_df["Meets Target"] = scoped_df["Attendance Rate"] >= min_threshold

        meets_count = int(scoped_df["Meets Target"].sum())
        below_count = int((~scoped_df["Meets Target"]).sum())
        total_scoped = len(scoped_df)

        k1, k2, k3 = st.columns(3)
        k1.metric(f"Meeting ≥ {min_threshold}%", f"{meets_count} / {total_scoped}")
        k2.metric(f"Below {min_threshold}% Target", below_count)
        pass_pct = (meets_count / total_scoped * 100) if total_scoped > 0 else 0.0
        k3.metric("Compliance Rate", f"{pass_pct:.1f}%")

        if threshold_view == "Below Minimum Only":
            filtered_chart_df = scoped_df[~scoped_df["Meets Target"]].sort_values(by="Attendance Rate", ascending=True)
        elif threshold_view == "Meeting Minimum Only":
            filtered_chart_df = scoped_df[scoped_df["Meets Target"]].sort_values(by="Attendance Rate", ascending=False)
        else:
            filtered_chart_df = scoped_df.sort_values(by="Attendance Rate", ascending=False)

        left_vis, right_vis = st.columns([3, 2])

        with left_vis:
            st.markdown(f"#### 📊 Attendance vs. {min_threshold}% Minimum")
            if filtered_chart_df.empty:
                st.info("No members match the selected threshold filter.")
            else:
                chart_plot_df = filtered_chart_df.set_index("Player Name")[["Attendance Rate"]].copy()
                chart_plot_df["Target %"] = float(min_threshold)
                st.line_chart(chart_plot_df, height=320)

        with right_vis:
            st.markdown("#### 🏆 Top Performers Leaderboard")
            top_lb = active_summary_df.sort_values(
                by=["Attendance Rate", "Active Count", "Total Logged"],
                ascending=[False, False, False]
            ).head(10).copy()

            if top_lb.empty:
                st.info("No active member data to rank yet.")
            else:
                top_lb.insert(0, "Rank", range(1, len(top_lb) + 1))
                top_lb["Turnout"] = (top_lb["Active Count"] + top_lb["Zero Points Count"]).astype(str) + "/" + top_lb["Total Logged"].astype(str)
                top_lb["Rate"] = top_lb["Attendance Rate"].astype(str) + "%"
                st.dataframe(
                    top_lb[["Rank", "Player Name", "Rate", "Turnout", "Zero Points Count"]].rename(
                        columns={"Zero Points Count": "0-Pt"}
                    ),
                    use_container_width=True,
                    hide_index=True,
                    height=320
                )

        st.markdown("---")
        st.markdown("#### 📋 Complete Member Performance Matrix")
        display_df = summary_df.copy()
        display_df["Turnout"] = (display_df["Active Count"] + display_df["Zero Points Count"]).astype(str) + " / " + display_df["Total Logged"].astype(str)
        display_df["Active Part."] = display_df["Active Count"].astype(str)
        display_df["Zero Points"] = display_df["Zero Points Count"].astype(str)
        display_df["Attendance %"] = display_df["Attendance Rate"].astype(str) + "%"

        st.dataframe(display_df[["Player Name", "Castle Level", "Lord Level", "Alliance Rank", "Member Status", "Turnout", "Active Part.", "Zero Points", "Attendance %"]], use_container_width=True, hide_index=True)

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
