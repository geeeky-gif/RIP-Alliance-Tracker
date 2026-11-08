import streamlit as st
import pandas as pd
import os
from datetime import datetime

st.set_page_config(page_title="RIP Alliance Command Center", layout="wide")

# ---------------------------------------------------------
# MODERN, ELEGANT & BRIGHT THEME (CLEAN LIGHT MODE)
# ---------------------------------------------------------
st.markdown(
    """
    <style>
        /* Main background & global text */
        .stApp, [data-testid="stAppViewContainer"], [data-testid="stHeader"] {
            background-color: #f8fafc !important;
            color: #1e293b !important;
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
        }
        
        /* Sidebar styling */
        [data-testid="stSidebar"] {
            background-color: #ffffff !important;
            border-right: 1px solid #e2e8f0;
        }
        [data-testid="stSidebar"] .stRadio label {
            color: #334155 !important;
            font-weight: 500;
        }

        /* Header card */
        .command-header {
            background: linear-gradient(135deg, #ffffff 0%, #f1f5f9 100%);
            border: 1px solid #cbd5e1;
            border-radius: 12px;
            padding: 24px;
            text-align: center;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 2px 4px -1px rgba(0, 0, 0, 0.03);
            margin-bottom: 25px;
        }
        .command-header h1 {
            color: #0f172a !important;
            margin: 0;
            font-size: 28px;
            letter-spacing: -0.5px;
            font-weight: 700;
        }
        .command-header p {
            color: #64748b !important;
            margin: 6px 0 0 0;
            font-size: 15px;
        }

        /* Metrics cards */
        [data-testid="stMetric"] {
            background-color: #ffffff !important;
            border: 1px solid #e2e8f0 !important;
            padding: 16px !important;
            border-radius: 10px !important;
            box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.05) !important;
        }
        [data-testid="stMetricLabel"] {
            color: #64748b !important;
            font-size: 13px !important;
            font-weight: 500;
        }
        [data-testid="stMetricValue"] {
            color: #0f172a !important;
            font-size: 24px !important;
            font-weight: 700;
        }

        /* Dataframe tables */
        [data-testid="stDataFrame"] {
            background-color: #ffffff !important;
            border-radius: 10px;
            border: 1px solid #e2e8f0;
            box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.02);
        }

        /* Buttons */
        .stButton button {
            background-color: #ffffff;
            color: #334155;
            border: 1px solid #cbd5e1;
            border-radius: 8px;
            font-weight: 600;
            transition: all 0.2s ease;
        }
        .stButton button:hover {
            background-color: #f1f5f9;
            color: #0f172a;
            border-color: #94a3b8;
        }
        
        /* Primary buttons */
        button[kind="primary"] {
            background-color: #2563eb !important;
            color: #ffffff !important;
            border: none !important;
        }
        button[kind="primary"]:hover {
            background-color: #1d4ed8 !important;
        }
    </style>
    <div class="command-header">
        <h1>🛡️ RIP ALLIANCE COMMAND CENTER</h1>
        <p>Operational Command & Master Matrix Tracking</p>
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
            if not st.session_state.attendance_df.empty and "Attended" in st.session_state.attendance_df.columns:
                st.session_state.attendance_df["Attended"] = st.session_state.attendance_df["Attended"].astype(str).str.lower() == "true"
        except Exception:
            st.session_state.attendance_df = pd.DataFrame(columns=["Session ID", "Event", "Date", "Player Name", "Attended"])
    else:
        st.session_state.attendance_df = pd.DataFrame(columns=["Session ID", "Event", "Date", "Player Name", "Attended"])

def save_roster():
    st.session_state.roster_df.to_csv(ROSTER_FILE, index=False)

def save_attendance():
    st.session_state.attendance_df.to_csv(ATTENDANCE_FILE, index=False)

# ---------------------------------------------------------
# SIDEBAR NAVIGATION
# ---------------------------------------------------------
st.sidebar.markdown("### 📌 Navigation Menu")
page = st.sidebar.radio("Select View:", [
    "📊 Attendance Dashboard",
    "📝 Quick Log / Edit Sessions",
    "✏️ Edit Roster",
    "📁 Upload Roster CSV",
    "⚙️ Data Management"
])

# ---------------------------------------------------------
# PAGE 1: ATTENDANCE DASHBOARD
# ---------------------------------------------------------
if page == "📊 Attendance Dashboard":
    st.subheader("📊 Master Alliance Attendance Overview")
    
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
                attended_cnt = len(p_logs[p_logs["Attended"] == True])
                pct = (attended_cnt / total_sessions) * 100
            else:
                attended_cnt = 0
                pct = 100.0 if total_sessions == 0 else 0.0
                
            stats.append({
                "Player Name": p_name,
                "Castle Level": p_row.get("Castle Level", "—"),
                "Alliance Rank": p_row.get("Alliance Rank", "—"),
                "Attended": f"{attended_cnt} / {total_sessions}",
                "Attendance %": f"{pct:.1f}%"
            })
            
        summary_df = pd.DataFrame(stats)
        
        m1, m2, m3 = st.columns(3)
        m1.metric("Total Roster Members", len(roster_df))
        m2.metric("Total Tracked Sessions", total_sessions)
        avg_att = summary_df["Attendance %"].str.rstrip('%').astype(float).mean() if not summary_df.empty else 0
        m3.metric("Avg Alliance Attendance", f"{avg_att:.1f}%")
        
        st.markdown("---")
        st.dataframe(summary_df, use_container_width=True, hide_index=True)

# ---------------------------------------------------------
# PAGE 2: QUICK LOG / EDIT SESSIONS (10x10 GRID & EDIT HUB)
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
            st.markdown("### 📋 Member Attendance Grid (10 Columns)")
            st.info("Everyone starts checked as **Present**. Uncheck any member who missed this event.")
            
            grid_key = f"grid_new_{session_id}"
            if grid_key not in st.session_state:
                st.session_state[grid_key] = {name: True for name in roster_names}
                
            cols_per_row = 10
            attendance_states = {}
            
            for i in range(0, len(roster_names), cols_per_row):
                row_players = roster_names[i:i + cols_per_row]
                row_cols = st.columns(len(row_players))
                for idx, p_name in enumerate(row_players):
                    current_val = st.session_state[grid_key].get(p_name, True)
                    attendance_states[p_name] = row_cols[idx].checkbox(p_name, value=current_val, key=f"chk_new_{session_id}_{p_name}")
            
            st.markdown("---")
            if st.button("💾 Save New Event Session", type="primary", use_container_width=True):
                new_records = []
                for p_name, attended_status in attendance_states.items():
                    new_records.append({
                        "Session ID": session_id,
                        "Event": selected_event,
                        "Date": str(event_date),
                        "Player Name": p_name,
                        "Attended": attended_status
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
                
                current_statuses = {row["Player Name"]: bool(row["Attended"]) for _, row in session_logs.iterrows()}
                
                st.markdown(f"### Editing Session: **{selected_session_to_edit['Event']}** ({selected_session_to_edit['Date']})")
                st.info("Adjust the attendance checkboxes below and click **Update Session Matrix** to save your changes.")
                
                cols_per_row = 10
                updated_states = {}
                
                for i in range(0, len(roster_names), cols_per_row):
                    row_players = roster_names[i:i + cols_per_row]
                    row_cols = st.columns(len(row_players))
                    for idx, p_name in enumerate(row_players):
                        default_val = current_statuses.get(p_name, True)
                        updated_states[p_name] = row_cols[idx].checkbox(p_name, value=default_val, key=f"chk_edit_{target_session_id}_{p_name}")
                
                st.markdown("---")
                col_save, col_del = st.columns([2, 1])
                
                if col_save.button("💾 Update Session Matrix", type="primary", use_container_width=True):
                    updated_records = []
                    for p_name, attended_status in updated_states.items():
                        updated_records.append({
                            "Session ID": target_session_id,
                            "Event": selected_session_to_edit["Event"],
                            "Date": selected_session_to_edit["Date"],
                            "Player Name": p_name,
                            "Attended": attended_status
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
            st.session_state.attendance_df = pd.DataFrame(columns=["Session ID", "Event", "Date", "Player Name", "Attended"])
            save_attendance()
            st.warning("All attendance records cleared!")
