import streamlit as st
import pandas as pd
import os
from datetime import datetime

st.set_page_config(page_title="RIP Alliance Command Center", layout="wide")

# ---------------------------------------------------------
# HIGH-PERFORMANCE ANALYTICS COMMAND THEME (DARK GLOW & GLASSMORPHISM)
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

# ---------------------------------------------------------
# STATE INITIALIZATION
# ---------------------------------------------------------
if "roster_df" not in st.session_state:
    if os.path.exists(ROSTER_FILE):
        try:
            st.session_state.roster_df = pd.read_csv(ROSTER_FILE, dtype=str)
        except Exception:
            st.session_state.roster_df = pd.DataFrame(columns=["Player Name", "Castle Level", "Alliance Rank"])
    else:
        initial_roster = []
        for i in range(1, 101):
            initial_roster.append({
                "Player Name": f"Player_{i}",
                "Castle Level": "40" if i <= 10 else "35",
                "Alliance Rank": "Leader" if i == 1 else ("Officer" if i <= 5 else "Member")
            })
        st.session_state.roster_df = pd.DataFrame(initial_roster)
        st.session_state.roster_df.to_csv(ROSTER_FILE, index=False)

if "attendance_df" not in st.session_state:
    if os.path.exists(ATTENDANCE_FILE):
        try:
            st.session_state.attendance_df = pd.read_csv(ATTENDANCE_FILE)
            if not st.session_state.attendance_df.empty:
                # Migrate older boolean column data to string status format if needed
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

# ---------------------------------------------------------
# SIDEBAR NAVIGATION
# ---------------------------------------------------------
st.sidebar.markdown("### 📊 NAVIGATION")
page = st.sidebar.radio("Select View:", [
    "📈 Analytics Dashboard",
    "📝 Quick Log / Edit Sessions",
    "✏️ Edit Roster",
    "📁 Upload Roster CSV",
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
            if total_sessions > 0 and not att_df.empty:
                p_logs = att_df[att_df["Player Name"] == p_name]
                active_cnt = len(p_logs[p_logs["Status"] == "Active"])
                zero_cnt = len(p_logs[p_logs["Status"] == "Zero Points"])
                absent_cnt = len(p_logs[p_logs["Status"] == "Absent"])
                
                # Showed up = Active + Zero Points
                showed_up_cnt = active_cnt + zero_cnt
                attendance_rate = (showed_up_cnt / total_sessions) * 100
            else:
                active_cnt, zero_cnt, absent_cnt = 0, 0, 0
                showed_up_cnt = 0
                attendance_rate = 100.0 if total_sessions == 0 else 0.0
                
            stats.append({
                "Player Name": p_name,
                "Castle Level": p_row.get("Castle Level", "—"),
                "Alliance Rank": p_row.get("Alliance Rank", "—"),
                "Active Count": active_cnt,
                "Zero Points Count": zero_cnt,
                "Total Sessions": total_sessions,
                "Attendance Rate": round(attendance_rate, 1)
            })
            
        summary_df = pd.DataFrame(stats)
        
        # Top KPI Metrics Row
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Active Roster", len(roster_df))
        m2.metric("Tracked Events", total_sessions)
        avg_att = summary_df["Attendance Rate"].mean() if not summary_df.empty else 0
        m3.metric("Alliance Turnout", f"{avg_att:.1f}%")
        total_zero_pts = summary_df["Zero Points Count"].sum() if not summary_df.empty else 0
        m4.metric("Zero-Point Instances", total_zero_pts, delta=f"-{total_zero_pts} inactive" if total_zero_pts > 0 else "Optimal", delta_color="inverse")
        
        st.markdown("---")
        
        # Visual Analytics Charts Row
        if total_sessions > 0 and not att_df.empty:
            c_chart1, c_chart2 = st.columns(2)
            with c_chart1:
                st.markdown("#### 📉 Overall Status Breakdown")
                status_counts = att_df["Status"].value_counts()
                st.bar_chart(status_counts, color="#38bdf8")
                
            with c_chart2:
                st.markdown("#### 🏆 Top Attendance Performers")
                top_performers = summary_df.sort_values(by="Attendance Rate", ascending=False).head(10)
                st.bar_chart(top_performers.set_index("Player Name")["Attendance Rate"], color="#818cf8")
            st.markdown("---")

        st.markdown("#### 📋 Complete Member Performance Matrix")
        display_df = summary_df.copy()
        display_df["Turnout"] = (display_df["Active Count"] + display_df["Zero Points Count"]).astype(str) + " / " + display_df["Total Sessions"].astype(str)
        display_df["Active Part."] = display_df["Active Count"].astype(str)
        display_df["Zero Points"] = display_df["Zero Points Count"].astype(str)
        display_df["Attendance %"] = display_df["Attendance Rate"].astype(str) + "%"
        
        st.dataframe(display_df[["Player Name", "Castle Level", "Alliance Rank", "Turnout", "Active Part.", "Zero Points", "Attendance %"]], use_container_width=True, hide_index=True)

# ---------------------------------------------------------
# PAGE 2: QUICK LOG / EDIT SESSIONS
# ---------------------------------------------------------
elif page == "📝 Quick Log / Edit Sessions":
    st.subheader("📝 Event Session Management")
    
    tab_new, tab_edit = st.tabs(["➕ Log New Session", "✏️ Edit Existing Session"])
    
    roster_df = st.session_state.roster_df
    roster_names = sorted(roster_df["Player Name"].tolist())
    
    with tab_new:
        if not roster_names:
            st.error("Roster is empty. Please add players first.")
        else:
            col1, col2, col3 = st.columns(3)
            selected_event = col1.selectbox("Event Type", EVENTS_LIST, key="new_ev")
            event_date = col2.date_input("Event Date", datetime.now(), key="new_dt")
            session_label = col3.text_input("Session Identifier (Optional)", placeholder="e.g., Run 1, Match 2", key="new_lbl")
            
            unique_suffix = session_label.strip() if session_label.strip() else datetime.now().strftime("%H%M%S")
            session_id = f"{event_date}_{selected_event}_{unique_suffix}"
            
            st.markdown("---")
            st.markdown("### 📋 Member Attendance Matrix")
            st.info("Assign each player's status for this session: **Active** (participated), **Zero Points** (showed up, no points), or **Absent** (missed).")
            
            grid_key = f"grid_new_{session_id}"
            if grid_key not in st.session_state:
                st.session_state[grid_key] = {name: "Active" for name in roster_names}
                
            session_statuses = {}
            for p_name in roster_names:
                default_status = st.session_state[grid_key].get(p_name, "Active")
                c_name, c_stat = st.columns([2, 3])
                c_name.markdown(f"**{p_name}**")
                session_statuses[p_name] = c_stat.selectbox(
                    f"Status for {p_name}", 
                    ["Active", "Zero Points", "Absent"], 
                    index=["Active", "Zero Points", "Absent"].index(default_status),
                    key=f"sel_new_{session_id}_{p_name}",
                    label_visibility="collapsed"
                )
            
            st.markdown("---")
            if st.button("💾 Save New Event Session", type="primary", use_container_width=True):
                new_records = []
                for p_name, status_val in session_statuses.items():
                    new_records.append({
                        "Session ID": session_id,
                        "Event": selected_event,
                        "Date": str(event_date),
                        "Player Name": p_name,
                        "Status": status_val
                    })
                
                new_df = pd.DataFrame(new_records)
                st.session_state.attendance_df = st.session_state.attendance_df[st.session_state.attendance_df["Session ID"] != session_id]
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
                
                st.markdown(f"### Editing Session: **{selected_session_to_edit['Event']}** ({selected_session_to_edit['Date']})")
                st.info("Update player statuses below and click **Update Session Matrix**.")
                
                updated_statuses = {}
                for p_name in roster_names:
                    default_stat = current_statuses.get(p_name, "Active")
                    if default_stat not in ["Active", "Zero Points", "Absent"]:
                        default_stat = "Active"
                    
                    c_name, c_stat = st.columns([2, 3])
                    c_name.markdown(f"**{p_name}**")
                    updated_statuses[p_name] = c_stat.selectbox(
                        f"Edit Status {p_name}",
                        ["Active", "Zero Points", "Absent"],
                        index=["Active", "Zero Points", "Absent"].index(default_stat),
                        key=f"sel_edit_{target_session_id}_{p_name}",
                        label_visibility="collapsed"
                    )
                
                st.markdown("---")
                col_save, col_del = st.columns([2, 1])
                
                if col_save.button("💾 Update Session Matrix", type="primary", use_container_width=True):
                    updated_records = []
                    for p_name, status_val in updated_statuses.items():
                        updated_records.append({
                            "Session ID": target_session_id,
                            "Event": selected_session_to_edit["Event"],
                            "Date": selected_session_to_edit["Date"],
                            "Player Name": p_name,
                            "Status": status_val
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
# PAGE 3: EDIT ROSTER
# ---------------------------------------------------------
elif page == "✏️ Edit Roster":
    st.subheader("✏️ Direct Roster Management")
    st.markdown("Modify player names, castle levels, or ranks directly on the interactive table.")
    
    enable_editing = st.toggle("🔓 Enable Table Editing Mode", value=False)
    
    if enable_editing:
        st.success("Editing mode active! Double click any cell to edit details, then click 'Save Roster Changes' below.")
        edited_df = st.data_editor(st.session_state.roster_df, num_rows="dynamic", use_container_width=True, hide_index=True)
        
        if st.button("💾 Save Roster Changes", type="primary"):
            st.session_state.roster_df = edited_df
            save_roster()
            st.success("Roster updated successfully!")
    else:
        st.info("Toggle the switch above to unlock table editing.")
        st.dataframe(st.session_state.roster_df, use_container_width=True, hide_index=True)

# ---------------------------------------------------------
# PAGE 4: UPLOAD ROSTER CSV
# ---------------------------------------------------------
elif page == "📁 Upload Roster CSV":
    st.subheader("📁 Simple Roster Import")
    st.markdown("Upload a CSV file containing columns: `Player Name`, `Castle Level`, `Alliance Rank`.")
    
    uploaded_file = st.file_uploader("Choose CSV file", type=["csv"])
    
    if uploaded_file is not None:
        try:
            uploaded_df = pd.read_csv(uploaded_file, dtype=str)
            st.markdown("#### Preview Uploaded Data:")
            st.dataframe(uploaded_df.head(), use_container_width=True)
            
            if st.button("Confirm & Overwrite Roster", type="primary"):
                uploaded_df.columns = [c.strip() for c in uploaded_df.columns]
                for col in ["Player Name", "Castle Level", "Alliance Rank"]:
                    if col not in uploaded_df.columns:
                        uploaded_df[col] = "—"
                
                st.session_state.roster_df = uploaded_df[["Player Name", "Castle Level", "Alliance Rank"]]
                save_roster()
                st.success("Roster successfully replaced and saved!")
        except Exception as e:
            st.error(f"Error reading CSV file: {e}")

# ---------------------------------------------------------
# PAGE 5: DATA MANAGEMENT
# ---------------------------------------------------------
elif page == "⚙️ Data Management":
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
