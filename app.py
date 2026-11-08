import streamlit as st
import pandas as pd
import os
from datetime import datetime

st.set_page_config(page_title="RIP Alliance Command Center", layout="wide")

# ---------------------------------------------------------
# STYLING & HEADER
# ---------------------------------------------------------
st.markdown(
    """
    <style>
        .stApp, [data-testid="stAppViewContainer"], [data-testid="stHeader"] {
            background-color: #0e1117 !important;
            color: #e0e0e0 !important;
        }
        [data-testid="stSidebar"] {
            min-width: 220px;
            background-color: #121418 !important;
        }
        .rip-header {
            background: linear-gradient(90deg, #1a1c23 0%, #2c2f38 50%, #1a1c23 100%);
            border: 2px solid #ffd700;
            border-radius: 8px;
            padding: 15px;
            text-align: center;
            box-shadow: 0 4px 12px rgba(0,0,0,0.6);
            margin-bottom: 20px;
        }
        .rip-header h1 {
            color: #ffd700 !important;
            margin: 0;
            font-size: 24px;
        }
    </style>
    <div class="rip-header">
        <h1>🛡️ RIP Alliance Command Center</h1>
        <p>10x10 Matrix Grid & Direct Roster Manager</p>
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
        # Initial starter roster template
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
page = st.sidebar.radio("Navigation", [
    "📊 Attendance Dashboard",
    "📝 Quick Log Session (10x10 Grid)",
    "✏️ Edit Roster",
    "📁 Upload Roster CSV",
    "⚙️ Data Management"
])

# ---------------------------------------------------------
# PAGE 1: ATTENDANCE DASHBOARD
# ---------------------------------------------------------
if page == "📊 Attendance Dashboard":
    st.subheader("📊 Master Attendance Overview")
    
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
# PAGE 2: QUICK LOG SESSION (10x10 GRID VIEW)
# ---------------------------------------------------------
elif page == "📝 Quick Log Session (10x10 Grid)":
    st.subheader("📝 Record Event Attendance (10x10 Grid)")
    
    roster_df = st.session_state.roster_df
    roster_names = sorted(roster_df["Player Name"].tolist())
    
    if not roster_names:
        st.error("Roster is empty. Please add players first.")
    else:
        col1, col2, col3 = st.columns(3)
        selected_event = col1.selectbox("Event Type", EVENTS_LIST)
        event_date = col2.date_input("Event Date", datetime.now())
        session_label = col3.text_input("Session Identifier (Optional)", placeholder="e.g., Run 1, Match 2")
        
        unique_suffix = session_label.strip() if session_label.strip() else datetime.now().strftime("%H%M%S")
        session_id = f"{event_date}_{selected_event}_{unique_suffix}"
        
        st.markdown("---")
        st.markdown("### 📋 Member Attendance Grid")
        st.info("Everyone is checked **Present** by default. Uncheck any member who missed this event.")
        
        # Initialize session state tracking for checkboxes if not set
        grid_key = f"grid_{session_id}"
        if grid_key not in st.session_state:
            st.session_state[grid_key] = {name: True for name in roster_names}
            
        # Render in a 10-column layout grid
        cols_per_row = 10
        attendance_states = {}
        
        for i in range(0, len(roster_names), cols_per_row):
            row_players = roster_names[i:i + cols_per_row]
            row_cols = st.columns(len(row_players))
            for idx, p_name in enumerate(row_players):
                current_val = st.session_state[grid_key].get(p_name, True)
                attendance_states[p_name] = row_cols[idx].checkbox(p_name, value=current_val, key=f"chk_{session_id}_{p_name}")
        
        st.markdown("---")
        if st.button("💾 Save Event Session Matrix", type="primary"):
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
            # Remove existing session records if overwriting
            st.session_state.attendance_df = st.session_state.attendance_df[st.session_state.attendance_df["Session ID"] != session_id]
            st.session_state.attendance_df = pd.concat([st.session_state.attendance_df, new_df], ignore_index=True)
            save_attendance()
            st.success(f"Successfully saved session **{selected_event}** on **{event_date}**! (ID: `{session_id}`)")

# ---------------------------------------------------------
# PAGE 3: EDIT ROSTER (DIRECT EDIT TABLE + TOGGLE)
# ---------------------------------------------------------
elif page == "✏️ Edit Roster":
    st.subheader("✏️ Direct Roster Management")
    st.markdown("Modify player names, castle levels, or ranks directly on the table below.")
    
    enable_editing = st.toggle("🔓 Enable Table Editing Mode", value=False)
    
    if enable_editing:
        st.success("Editing mode active! Double click any cell in the table to modify names or stats, then click 'Save Roster Changes' below.")
        edited_df = st.data_editor(st.session_state.roster_df, num_rows="dynamic", use_container_width=True, hide_index=True)
        
        if st.button("💾 Save Roster Changes", type="primary"):
            st.session_state.roster_df = edited_df
            save_roster()
            st.success("Roster successfully updated and saved to disk!")
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
            
            if st.button("Confirm & Overwrite Roster"):
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
