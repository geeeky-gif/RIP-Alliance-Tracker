import streamlit as st
import pandas as pd
from PIL import Image
import pytesseract
from difflib import SequenceMatcher
import os
import re

st.set_page_config(page_title="RIP Alliance Attendance Tracker", layout="wide")

# ---------------------------------------------------------
# CUSTOM WAR & ORDER / RIP ALLIANCE THEME CSS (DAY & NIGHT)
# ---------------------------------------------------------
st.markdown(
    """
    <style>
        .stApp, [data-testid="stAppViewContainer"], [data-testid="stHeader"] {
            background-color: #0e1117 !important;
            color: #e0e0e0 !important;
        }
        [data-testid="stSidebar"] {
            min-width: 200px;
            max-width: 240px;
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
            font-family: 'Cinzel', serif, sans-serif;
            text-transform: uppercase;
            letter-spacing: 2px;
            margin: 0;
            font-size: 24px;
        }
        .rip-header p {
            color: #a0a0a0 !important;
            margin: 5px 0 0 0;
            font-size: 14px;
        }
        [data-testid="stMetric"] {
            background-color: #161a22 !important;
            border: 1px solid #333842 !important;
            padding: 10px !important;
            border-radius: 6px !important;
            box-shadow: 0 2px 5px rgba(0,0,0,0.4) !important;
        }
        [data-testid="stMetricLabel"] {
            color: #b0b8c4 !important;
            font-size: 13px !important;
        }
        [data-testid="stMetricValue"] {
            color: #ffd700 !important;
            font-size: 18px !important;
        }
        div[data-baseweb="input"], div[data-baseweb="select"], .stTextInput > div > div {
            background-color: #161a22 !important;
            color: #ffffff !important;
            border-color: #333842 !important;
        }
        input {
            color: #ffffff !important;
        }
        [data-testid="stDataFrame"] {
            background-color: #161a22 !important;
            border-radius: 6px;
        }
    </style>
    
    <div class="rip-header">
        <h1>🛡️ RIP Alliance Command Center</h1>
        <p>Raiders in Pajamas • Automated Event & Player Stats Tracking</p>
    </div>
    """,
    unsafe_allow_html=True
)

# ---------------------------------------------------------
# PERSISTENT STORAGE FILE PATHS & INITIALIZATION
# ---------------------------------------------------------
ROSTER_FILE = "roster_data.csv"
LOCKS_FILE = "field_locks.csv"
HISTORY_FILE = "bp_history.csv"

if 'roster_df' not in st.session_state:
    if os.path.exists(ROSTER_FILE):
        st.session_state.roster_df = pd.read_csv(ROSTER_FILE)
    else:
        st.session_state.roster_df = pd.DataFrame({
            "Player Name": ["•~SoulTaker~•", "Warbansteiger", "01*BAD*01"],
            "Alliance Rank": ["Alliance Leader", "Deputy", "Deputy"],
            "Battle Power": [114868760, 19755892, 46233787],
            "Kills": [0, 0, 0],
            "Losses": [0, 0, 0],
            "Castle Level": [40, 0, 0],
            "Lord Level": [0, 0, 0],
            "Individual Reputation": [0, 0, 0],
            "Power Ranking": [1, 0, 0],
            "Military Rank": ["", "", ""],
            "Status": ["Active", "Active", "Active"]
        })
        st.session_state.roster_df.to_csv(ROSTER_FILE, index=False)

def save_roster():
    st.session_state.roster_df.to_csv(ROSTER_FILE, index=False)

if 'locks_df' not in st.session_state:
    if os.path.exists(LOCKS_FILE):
        st.session_state.locks_df = pd.read_csv(LOCKS_FILE)
    else:
        st.session_state.locks_df = pd.DataFrame(columns=["Player Name", "Field", "Locked"])
        st.session_state.locks_df.to_csv(LOCKS_FILE, index=False)

def save_locks():
    st.session_state.locks_df.to_csv(LOCKS_FILE, index=False)

def is_locked(player, field):
    match = st.session_state.locks_df[(st.session_state.locks_df["Player Name"] == player) & (st.session_state.locks_df["Field"] == field)]
    if not match.empty:
        return bool(match.iloc[0]["Locked"])
    return False

def set_lock(player, field, locked_state):
    df = st.session_state.locks_df
    idx = df[(df["Player Name"] == player) & (df["Field"] == field)].index
    if not idx.empty:
        df.at[idx[0], "Locked"] = locked_state
    else:
        new_row = pd.DataFrame({"Player Name": [player], "Field": [field], "Locked": [locked_state]})
        st.session_state.locks_df = pd.concat([df, new_row], ignore_index=True)
    save_locks()

if 'selected_player_name' not in st.session_state:
    st.session_state.selected_player_name = "•~SoulTaker~•"

if 'active_rank_tab' not in st.session_state:
    st.session_state.active_rank_tab = "Leader"

if 'admin_rank_tab' not in st.session_state:
    st.session_state.admin_rank_tab = "Leader"

if 'thresh_rank_tab' not in st.session_state:
    st.session_state.thresh_rank_tab = "Leader"

if 'bp_history' not in st.session_state:
    if os.path.exists(HISTORY_FILE):
        hist_df = pd.read_csv(HISTORY_FILE)
        st.session_state.bp_history = hist_df.groupby("Player").apply(lambda x: x[["Date", "Battle Power"]].to_dict('records')).to_dict()
    else:
        st.session_state.bp_history = {}

def save_history():
    rows = []
    for player, records in st.session_state.bp_history.items():
        for rec in records:
            rows.append({"Player": player, "Date": rec["Date"], "Battle Power": rec["Battle Power"]})
    if rows:
        pd.DataFrame(rows).to_csv(HISTORY_FILE, index=False)

if 'events_list' not in st.session_state:
    st.session_state.events_list = ["Elite Wars", "Fortress War", "Realm Invasion", "Void War", "Territory Defense", "Elite Adventure"]

if 'attendance_records' not in st.session_state:
    st.session_state.attendance_records = []

def get_player_attendance_stats(p_name):
    all_events_count = max(1, len(set(r["Event"] for r in st.session_state.attendance_records))) if st.session_state.attendance_records else 7
    p_misses = [r for r in st.session_state.attendance_records if r["Player"] == p_name]
    attended_count = max(0, all_events_count - len(p_misses))
    pct = (attended_count / all_events_count) * 100.0
    return attended_count, all_events_count, pct, len(p_misses)

# ---------------------------------------------------------
# OCR PARSER HELPERS
# ---------------------------------------------------------
def clean_text(text):
    return "".join(c for c in text if c.isalnum()).lower()

def find_best_roster_match(ocr_chunk, roster_names, cutoff=0.70):
    best_match = None
    highest_score = 0.0
    cleaned_chunk = clean_text(ocr_chunk)
    
    if len(cleaned_chunk) < 3:
        return None, 0.0
        
    for name in roster_names:
        cleaned_name = clean_text(name)
        if cleaned_name in cleaned_chunk or cleaned_chunk in cleaned_name:
            return name, 1.0
            
        score = SequenceMatcher(None, cleaned_chunk, cleaned_name).ratio()
        if score > highest_score:
            highest_score = score
            best_match = name
            
    if highest_score >= cutoff:
        return best_match, highest_score
    return None, 0.0

def extract_number(text):
    nums = re.findall(r'\d[\d,]*', text)
    if nums:
        return int(nums[0].replace(',', ''))
    return 0

def parse_player_info_screenshot(ocr_text, roster_names):
    lines = [line.strip() for line in ocr_text.split('\n') if line.strip()]
    parsed_data = {
        "Player Name": None, "Castle Level": 0, "Lord Level": 0,
        "Individual Reputation": 0, "Military Rank": "", "Power Ranking": 0,
        "Battle Power": 0, "Kills": 0, "Losses": 0
    }
    
    for line in lines[:6]:
        match, _ = find_best_roster_match(line, roster_names, cutoff=0.65)
        if match:
            parsed_data["Player Name"] = match
            break
            
    if not parsed_data["Player Name"]:
        for line in lines:
            match, _ = find_best_roster_match(line, roster_names, cutoff=0.75)
            if match:
                parsed_data["Player Name"] = match
                break

    for i, line in enumerate(lines):
        line_lower = line.lower()
        if "lv." in line_lower:
            num = extract_number(line)
            if num > 0:
                if parsed_data["Castle Level"] == 0 and "lord" not in line_lower:
                    parsed_data["Castle Level"] = num
                elif "lord" in line_lower or parsed_data["Castle Level"] > 0:
                    parsed_data["Lord Level"] = num
        if "castle" in line_lower:
            num = extract_number(line)
            if num > 0:
                parsed_data["Castle Level"] = num
        if "reputation" in line_lower or "individual" in line_lower:
            val = extract_number(line)
            parsed_data["Individual Reputation"] = val if val > 0 else (extract_number(lines[i+1]) if i + 1 < len(lines) else 0)
        if "military rank" in line_lower or ("rank" in line_lower and "power" not in line_lower):
            parts = line.split(":")
            parsed_data["Military Rank"] = parts[1].strip() if len(parts) > 1 and parts[1].strip() else (lines[i+1].strip() if i + 1 < len(lines) else "")
        if "power ranking" in line_lower or "power rank" in line_lower:
            val = extract_number(line)
            parsed_data["Power Ranking"] = val if val > 0 else (extract_number(lines[i+1]) if i + 1 < len(lines) else 0)
        if "battle power" in line_lower or (line_lower == "power" and "ranking" not in line_lower):
            val = extract_number(line)
            parsed_data["Battle Power"] = val if val > 0 else (extract_number(lines[i+1]) if i + 1 < len(lines) else 0)
        if "kills" in line_lower:
            parsed_data["Kills"] = extract_number(line) if extract_number(line) > 0 else (extract_number(lines[i+1]) if i + 1 < len(lines) else 0)
        if "losses" in line_lower:
            parsed_data["Losses"] = extract_number(line) if extract_number(line) > 0 else (extract_number(lines[i+1]) if i + 1 < len(lines) else 0)

    return parsed_data

# ---------------------------------------------------------
# NAVIGATION SIDEBAR
# ---------------------------------------------------------
st.sidebar.markdown("### 📌 Command Menu")
page = st.sidebar.radio("Go to:", [
    "Player Profiles", 
    "Attendance Thresholds",
    "Alliance Overview & Stats", 
    "Upload Event Screenshots", 
    "Admin / Roster Edits"
])

# ---------------------------------------------------------
# PAGE 1: PLAYER PROFILES
# ---------------------------------------------------------
if page == "Player Profiles":
    st.subheader("👤 Alliance Member Profiles")
    rank_cols = st.columns(5)
    if rank_cols[0].button("👑 Leaders", use_container_width=True): st.session_state.active_rank_tab = "Leader"
    if rank_cols[1].button("🛡️ Officers", use_container_width=True): st.session_state.active_rank_tab = "Officer"
    if rank_cols[2].button("⚔️ Elites", use_container_width=True): st.session_state.active_rank_tab = "Elite"
    if rank_cols[3].button("📜 A-M", use_container_width=True): st.session_state.active_rank_tab = "Member_AM"
    if rank_cols[4].button("📜 N-Z", use_container_width=True): st.session_state.active_rank_tab = "Member_NZ"

    active_tab = st.session_state.active_rank_tab
    if active_tab == "Leader":
        filtered_df = st.session_state.roster_df[st.session_state.roster_df["Alliance Rank"].isin(["Alliance Leader", "Deputy"])]
    elif active_tab == "Officer":
        filtered_df = st.session_state.roster_df[st.session_state.roster_df["Alliance Rank"] == "Officer"]
    elif active_tab == "Elite":
        filtered_df = st.session_state.roster_df[st.session_state.roster_df["Alliance Rank"] == "Elite"]
    elif active_tab == "Member_AM":
        all_df = st.session_state.roster_df[st.session_state.roster_df["Alliance Rank"] == "Member"]
        filtered_df = all_df[all_df["Player Name"].apply(lambda x: x[0].upper() <= 'M' or not x[0].isalpha())]
    else:
        all_df = st.session_state.roster_df[st.session_state.roster_df["Alliance Rank"] == "Member"]
        filtered_df = all_df[all_df["Player Name"].apply(lambda x: x[0].upper() > 'M' and x[0].isalpha())]

    st.markdown("#### Select Player Card:")
    grid_cols = st.columns(2)
    for idx, row in filtered_df.reset_index().iterrows():
        p_name = row["Player Name"]
        p_bp = row["Battle Power"]
        bp_label = f"{p_bp / 1_000_000:.1f}M" if p_bp > 0 else "0"
        if grid_cols[idx % 2].button(f"🛡️ {p_name}\n⚔️ {bp_label} BP", key=f"card_{p_name}", use_container_width=True):
            st.session_state.selected_player_name = p_name

    selected_player = st.session_state.selected_player_name
    st.markdown("---")
    st.markdown(f"### ⚔️ Active Profile: **{selected_player}**")
    
    player_row = st.session_state.roster_df[st.session_state.roster_df["Player Name"] == selected_player].iloc[0]
    attended_count, all_events_count, attendance_pct, _ = get_player_attendance_stats(selected_player)
    player_misses = [r for r in st.session_state.attendance_records if r["Player"] == selected_player]
    
    r1_c1, r1_c2, r1_c3, r1_c4 = st.columns(4)
    r1_c1.metric("Rank", player_row["Alliance Rank"])
    r1_c2.metric("Battle Power", f"{player_row['Battle Power']:,}" if player_row['Battle Power'] > 0 else "—")
    r1_c3.metric("Castle Lvl", str(player_row['Castle Level']) if player_row['Castle Level'] > 0 else "—")
    r1_c4.metric("Lord Lvl", str(player_row['Lord Level']) if player_row['Lord Level'] > 0 else "—")
    
    r2_c1, r2_c2, r2_c3, r2_c4 = st.columns(4)
    r2_c1.metric("Kills", f"{player_row['Kills']:,}" if player_row['Kills'] > 0 else "—")
    r2_c2.metric("Losses", f"{player_row['Losses']:,}" if player_row['Losses'] > 0 else "—")
    r2_c3.metric("Power Ranking", f"{player_row['Power Ranking']:,}" if player_row['Power Ranking'] > 0 else "—")
    r2_c4.metric("Military Rank", player_row['Military Rank'] if pd.notna(player_row['Military Rank']) and player_row['Military Rank'] != "" else "—")

    r3_c1, r3_c2, r3_c3 = st.columns(3)
    r3_c1.metric("Reputation", f"{player_row['Individual Reputation']:,}" if player_row['Individual Reputation'] > 0 else "—")
    r3_c2.metric("Events Attended", f"{attended_count} / {all_events_count} ({attendance_pct:.1f}%)")
    r3_c3.metric("Status", player_row["Status"])
    
    st.markdown("---")
    st.subheader("📋 Missed Events Log")
    if player_misses:
        st.dataframe(pd.DataFrame(player_misses)[["Event", "Date", "Status"]], use_container_width=True, hide_index=True)
    else:
        st.success("🌟 Perfect Attendance!")

# ---------------------------------------------------------
# PAGE 2: ATTENDANCE THRESHOLDS
# ---------------------------------------------------------
elif page == "Attendance Thresholds":
    st.subheader("🎯 Low Attendance Audit & Rank Minimums")
    threshold = st.slider("Select Participation Benchmark (%):", min_value=0, max_value=100, value=70, step=5)
    
    low_att_list = []
    for _, row in st.session_state.roster_df.iterrows():
        p_name = row["Player Name"]
        att_cnt, total_cnt, pct, _ = get_player_attendance_stats(p_name)
        if pct < threshold:
            low_att_list.append({"Player Name": p_name, "Alliance Rank": row["Alliance Rank"], "Battle Power": row["Battle Power"], "Events Attended": f"{att_cnt} / {total_cnt}", "Attendance %": f"{pct:.1f}%", "Status": row["Status"]})
            
    low_att_df = pd.DataFrame(low_att_list)
    st.markdown(f"### ⚠️ Accounts Below **{threshold}%** Participation ({len(low_att_df)} Total)")
    
    t_rank_cols = st.columns(5)
    if t_rank_cols[0].button("👑 Leaders", use_container_width=True, key="t_btn_lead"): st.session_state.thresh_rank_tab = "Leader"
    if t_rank_cols[1].button("🛡️ Officers", use_container_width=True, key="t_btn_off"): st.session_state.thresh_rank_tab = "Officer"
    if t_rank_cols[2].button("⚔️ Elites", use_container_width=True, key="t_btn_elite"): st.session_state.thresh_rank_tab = "Elite"
    if t_rank_cols[3].button("📜 Members A-M", use_container_width=True, key="t_btn_am"): st.session_state.thresh_rank_tab = "Member_AM"
    if t_rank_cols[4].button("📜 Members N-Z", use_container_width=True, key="t_btn_nz"): st.session_state.thresh_rank_tab = "Member_NZ"

    t_tab = st.session_state.thresh_rank_tab
    if not low_att_df.empty:
        if t_tab == "Leader": t_filtered = low_att_df[low_att_df["Alliance Rank"].isin(["Alliance Leader", "Deputy"])]
        elif t_tab == "Officer": t_filtered = low_att_df[low_att_df["Alliance Rank"] == "Officer"]
        elif t_tab == "Elite": t_filtered = low_att_df[low_att_df["Alliance Rank"] == "Elite"]
        elif t_tab == "Member_AM": t_filtered = low_att_df[(low_att_df["Alliance Rank"] == "Member") & low_att_df["Player Name"].apply(lambda x: x[0].upper() <= 'M' or not x[0].isalpha())]
        else: t_filtered = low_att_df[(low_att_df["Alliance Rank"] == "Member") & low_att_df["Player Name"].apply(lambda x: x[0].upper() > 'M' and x[0].isalpha())]

        if not t_filtered.empty:
            st.dataframe(t_filtered[["Player Name", "Alliance Rank", "Battle Power", "Events Attended", "Attendance %", "Status"]], use_container_width=True, hide_index=True)
        else:
            st.success(f"🎉 No accounts in the **{t_tab}** category fall below {threshold}% attendance!")
    else:
        st.success(f"🎉 Zero accounts fall below {threshold}% attendance.")

# ---------------------------------------------------------
# PAGE 3: ALLIANCE OVERVIEW & STATS
# ---------------------------------------------------------
elif page == "Alliance Overview & Stats":
    st.subheader("📊 Alliance Participation Overview")
    c1, c2, c3 = st.columns(3)
    c1.metric("Total Roster Members", len(st.session_state.roster_df))
    c2.metric("Tracked Events", len(set(r["Event"] for r in st.session_state.attendance_records)) if st.session_state.attendance_records else 0)
    c3.metric("Total Logged Entries", len(st.session_state.attendance_records))
    st.markdown("---")
    st.dataframe(st.session_state.roster_df, use_container_width=True, hide_index=True)

# ---------------------------------------------------------
# PAGE 4: UPLOAD SCREENSHOTS
# ---------------------------------------------------------
elif page == "Upload Event Screenshots":
    st.subheader("📸 Bulk Screenshot Uploader")
    passcode = st.text_input("Enter Leadership Passcode to Unlock Uploader:", type="password")
    if passcode == "rip123":
        st.success("Passcode accepted!")
        upload_type = st.radio("Select Upload Type:", ["Event Attendance", "Player Info / Stats"], horizontal=True)
        if "Attendance" in upload_type:
            c1, c2 = st.columns(2)
            selected_event = c1.selectbox("Select Event", st.session_state.events_list)
            event_date = c2.date_input("Battle Date")
            entry_mode = st.radio("Logging Mode:", ["Log Non-Attendants ('Not Entered')", "Log Attendants ('Battlers')"], horizontal=True)
        else:
            scan_date = st.date_input("Stat Scan Date")

        uploaded_files = st.file_uploader("Choose screenshot(s)...", type=["png", "jpg", "jpeg"], accept_multiple_files=True)
        if uploaded_files and st.button("Process Batch Screenshots"):
            with st.spinner("Running OCR Parser..."):
                roster_names = st.session_state.roster_df["Player Name"].tolist()
                success_count = 0
                for file in uploaded_files:
                    text = pytesseract.image_to_string(Image.open(file))
                    if "Attendance" in upload_type:
                        for name in roster_names:
                            if name in text:
                                st.session_state.attendance_records.append({"Event": selected_event, "Date": str(event_date), "Player": name, "Status": "Not Entered" if "Non-Attendants" in entry_mode else "Entered"})
                                success_count += 1
                    else:
                        p_data = parse_player_info_screenshot(text, roster_names)
                        p_name = p_data["Player Name"]
                        if p_name:
                            idx = st.session_state.roster_df[st.session_state.roster_df["Player Name"] == p_name].index[0]
                            for field, key in [("Battle Power", "Battle Power"), ("Castle Level", "Castle Level"), ("Lord Level", "Lord Level"), ("Individual Reputation", "Individual Reputation"), ("Power Ranking", "Power Ranking"), ("Military Rank", "Military Rank"), ("Kills", "Kills"), ("Losses", "Losses")]:
                                if p_data[field] and not is_locked(p_name, field):
                                    st.session_state.roster_df.at[idx, field] = p_data[field]
                            save_roster()
                            success_count += 1
                st.success(f"Successfully updated {success_count} record(s).")
    elif passcode != "":
        st.error("Incorrect passcode.")

# ---------------------------------------------------------
# PAGE 5: ADMIN / ROSTER EDITS
# ---------------------------------------------------------
elif page == "Admin / Roster Edits":
    st.subheader("⚙️ Admin & Roster Edits")
    passcode = st.text_input("Enter Leadership Passcode to Unlock Admin Tools:", type="password", key="admin_pass")
    if passcode == "rip123":
        st.success("Passcode accepted!")
        with st.expander("💾 CSV Backup & Instant Restore Tools"):
            c1, c2 = st.columns(2)
            c1.download_button("📥 Download Roster CSV Backup", data=st.session_state.roster_df.to_csv(index=False).encode('utf-8'), file_name="roster_data_backup.csv", mime="text/csv", use_container_width=True)
            uploaded_backup = c2.file_uploader("📤 Upload
