import streamlit as st
import pandas as pd
from PIL import Image
import pytesseract
from difflib import SequenceMatcher
import os
import re
from datetime import datetime

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
# PREDEFINED DROPDOWN OPTIONS (OFFICIAL GAME CONSTRAINTS)
# ---------------------------------------------------------
CASTLE_LEVEL_OPTIONS = [str(i) for i in range(1, 41)] + ["S1", "S2", "S3"]
LORD_LEVEL_OPTIONS = list(range(0, 81))
POWER_RANK_OPTIONS = list(range(0, 501))
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

# ---------------------------------------------------------
# PERSISTENT STORAGE FILE PATHS & INITIALIZATION
# ---------------------------------------------------------
ROSTER_FILE = "roster_data.csv"
LOCKS_FILE = "field_locks.csv"
ATTENDANCE_FILE = "attendance_data.csv"

if 'roster_df' not in st.session_state:
    if os.path.exists(ROSTER_FILE):
        try:
            st.session_state.roster_df = pd.read_csv(ROSTER_FILE)
            st.session_state.roster_df["Military Rank"] = st.session_state.roster_df["Military Rank"].astype(str)
            st.session_state.roster_df["Player Name"] = st.session_state.roster_df["Player Name"].astype(str)
            st.session_state.roster_df["Alliance Rank"] = st.session_state.roster_df["Alliance Rank"].astype(str)
            st.session_state.roster_df["Status"] = st.session_state.roster_df["Status"].astype(str)
            st.session_state.roster_df["Castle Level"] = st.session_state.roster_df["Castle Level"].astype(str)
        except Exception:
            st.session_state.roster_df = pd.DataFrame()
    if 'roster_df' not in st.session_state or st.session_state.roster_df.empty:
        st.session_state.roster_df = pd.DataFrame({
            "Player Name": ["•~SoulTaker~•", "Warbansteiger", "01*BAD*01"],
            "Alliance Rank": ["Alliance Leader", "Deputy", "Deputy"],
            "Battle Power": [114868760, 19755892, 46233787],
            "Kills": [0, 0, 0],
            "Losses": [0, 0, 0],
            "Castle Level": ["40", "1", "1"],
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
        try:
            st.session_state.locks_df = pd.read_csv(LOCKS_FILE)
        except Exception:
            st.session_state.locks_df = pd.DataFrame(columns=["Player Name", "Field", "Locked"])
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

if 'events_list' not in st.session_state:
    st.session_state.events_list = [
        "Elite Wars", 
        "Fortress War", 
        "Realm Conquest", 
        "Realm Invasion", 
        "Territory Defense", 
        "Territory Expulsion", 
        "Alliance Conquest", 
        "Frenzy", 
        "Void", 
        "Elite Adventures"
    ]

if 'uploader_key_counter' not in st.session_state:
    st.session_state.uploader_key_counter = 0

if 'attendance_records' not in st.session_state:
    if os.path.exists(ATTENDANCE_FILE):
        try:
            att_df = pd.read_csv(ATTENDANCE_FILE)
            if not att_df.empty:
                if "Session ID" not in att_df.columns:
                    att_df["Session ID"] = att_df["Date"].astype(str) + "_" + att_df["Event"].astype(str)
                st.session_state.attendance_records = att_df.to_dict('records')
            else:
                st.session_state.attendance_records = []
        except Exception:
            st.session_state.attendance_records = []
    else:
        st.session_state.attendance_records = []

def save_attendance():
    if st.session_state.attendance_records:
        df = pd.DataFrame(st.session_state.attendance_records)
        if "Session ID" not in df.columns:
            df["Session ID"] = df["Date"].astype(str) + "_" + df["Event"].astype(str)
        df.to_csv(ATTENDANCE_FILE, index=False)
    else:
        pd.DataFrame(columns=["Event", "Date", "Status", "Player", "Session ID"]).to_csv(ATTENDANCE_FILE, index=False)

def get_tracked_sessions_count():
    if not st.session_state.attendance_records:
        return 0
    att_df = pd.DataFrame(st.session_state.attendance_records)
    if att_df.empty:
        return 0
    if "Session ID" in att_df.columns:
        return att_df["Session ID"].nunique()
    elif "Date" in att_df.columns and "Event" in att_df.columns:
        return len(att_df[["Event", "Date"]].drop_duplicates())
    return len(att_df)

def get_player_attendance_stats(p_name):
    """
    Calculates attendance correctly based on uploaded 'Not Entered' absence lists.
    Everyone on the roster is assumed PRESENT ('Entered') by default for every session, 
    unless explicitly logged as 'Not Entered' in that session.
    """
    if not st.session_state.attendance_records:
        return 0, 0, 0.0, 0
        
    att_df = pd.DataFrame(st.session_state.attendance_records)
    if att_df.empty or "Session ID" not in att_df.columns:
        return 0, 0, 0.0, 0
        
    unique_sessions = att_df["Session ID"].unique()
    total_sessions_count = len(unique_sessions)
    if total_sessions_count == 0:
        return 0, 0, 0.0, 0
        
    absent_sessions = att_df[(att_df["Player"] == p_name) & (att_df["Status"] == "Not Entered")]["Session ID"].nunique()
    p_attended_sessions = max(0, total_sessions_count - absent_sessions)
    p_misses = att_df[(att_df["Player"] == p_name) & (att_df["Status"] == "Not Entered")].to_dict('records')
    
    pct = (p_attended_sessions / total_sessions_count) * 100.0 if total_sessions_count > 0 else 0.0
    return p_attended_sessions, total_sessions_count, pct, len(p_misses)

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

def extract_screenshot_date(ocr_text):
    lines = [line.strip() for line in ocr_text.split('\n') if line.strip()]
    current_year = "2026"
    
    for line in lines[:10]:
        line_lower = line.lower()
        if any(keyword in line_lower for keyword in ["time", "battle", "period", "date"]):
            full_match = re.search(r'\b(20\d{2}[./-]\d{1,2}[./-]\d{1,2})\b', line)
            if full_match:
                return full_match.group(0).replace('.', '-').replace('/', '-')
            
            short_match = re.search(r'\b(\d{1,2}[./-]\d{1,2})\b', line)
            if short_match:
                parts = re.split(r'[./-]', short_match.group(0))
                if len(parts) == 2:
                    return f"{current_year}-{parts[0].zfill(2)}-{parts[1].zfill(2)}"

    general_short = re.search(r'\b(\d{1,2}[./-]\d{1,2})\b', ocr_text)
    if general_short:
        parts = re.split(r'[./-]', general_short.group(0))
        if len(parts) == 2 and 1 <= int(parts[0]) <= 12 and 1 <= int(parts[1]) <= 31:
            return f"{current_year}-{parts[0].zfill(2)}-{parts[1].zfill(2)}"

    return "Unknown Date"

def parse_attendance_screenshot_auto(ocr_text, roster_names, events_list):
    text_lower = ocr_text.lower()
    cleaned_ocr = clean_text(ocr_text)
    
    detected_event = "Elite Wars"
    if "fortress" in text_lower or "fortress" in cleaned_ocr:
        detected_event = "Fortress War"
    elif "expulsion" in text_lower or "expulsion" in cleaned_ocr:
        detected_event = "Territory Expulsion"
    elif "territory" in text_lower or "defense" in text_lower:
        detected_event = "Territory Defense"
    elif "realm" in text_lower and "conquest" in text_lower:
        detected_event = "Realm Conquest"
    elif "realm" in text_lower or "invasion" in text_lower:
        detected_event = "Realm Invasion"
    elif "alliance" in text_lower and "conquest" in text_lower:
        detected_event = "Alliance Conquest"
    elif "frenzy" in text_lower or "frenzy" in cleaned_ocr:
        detected_event = "Frenzy"
    elif "void" in text_lower or "void" in cleaned_ocr:
        detected_event = "Void"
    elif "adventure" in text_lower or "adventures" in text_lower:
        detected_event = "Elite Adventures"
    elif "elite" in text_lower or "wars" in text_lower:
        detected_event = "Elite Wars"
    else:
        sorted_events = sorted(events_list, key=len, reverse=True)
        for ev in sorted_events:
            if ev.lower() in text_lower or clean_text(ev) in cleaned_ocr:
                detected_event = ev
                break

    detected_date = extract_screenshot_date(ocr_text)

    matched_players = []
    for name in roster_names:
        cleaned_name = clean_text(name)
        if len(cleaned_name) >= 3 and (cleaned_name in cleaned_ocr or name.lower() in text_lower):
            matched_players.append(name)

    return detected_event, detected_date, matched_players

def parse_player_info_screenshot(ocr_text, roster_names):
    lines = [line.strip() for line in ocr_text.split('\n') if line.strip()]
    parsed_data = {
        "Player Name": None, "Castle Level": "1", "Lord Level": 0,
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
        if "s1" in line_lower: parsed_data["Castle Level"] = "S1"
        elif "s2" in line_lower: parsed_data["Castle Level"] = "S2"
        elif "s3" in line_lower: parsed_data["Castle Level"] = "S3"
        elif "lv." in line_lower or "castle" in line_lower:
            num = extract_number(line)
            if 1 <= num <= 40:
                parsed_data["Castle Level"] = str(num)
        if "lord" in line_lower:
            num = extract_number(line)
            if 0 <= num <= 80:
                parsed_data["Lord Level"] = num
        if "reputation" in line_lower or "individual" in line_lower:
            val = extract_number(line)
            parsed_data["Individual Reputation"] = val if val > 0 else (extract_number(lines[i+1]) if i + 1 < len(lines) else 0)
        if "power ranking" in line_lower or "power rank" in line_lower:
            val = extract_number(line)
            if 0 <= val <= 500:
                parsed_data["Power Ranking"] = val
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
    "Events Dashboard",
    "Player Activity Dashboard",
    "Alliance Overview & Stats", 
    "Admin & Operations Hub"
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
    player_misses = [r for r in st.session_state.attendance_records if isinstance(r, dict) and r.get("Player") == selected_player and r.get("Status") == "Not Entered"]
    
    r1_c1, r1_c2, r1_c3, r1_c4 = st.columns(4)
    r1_c1.metric("Rank", player_row["Alliance Rank"])
    r1_c2.metric("Battle Power", f"{int(player_row['Battle Power']):,}" if player_row['Battle Power'] > 0 else "—")
    r1_c3.metric("Castle Lvl", str(player_row['Castle Level']))
    r1_c4.metric("Lord Lvl", str(int(player_row['Lord Level'])) if int(player_row['Lord Level']) > 0 else "—")
    
    r2_c1, r2_c2, r2_c3, r2_c4 = st.columns(4)
    r2_c1.metric("Kills", f"{int(player_row['Kills']):,}" if int(player_row['Kills']) > 0 else "—")
    r2_c2.metric("Losses", f"{int(player_row['Losses']):,}" if int(player_row['Losses']) > 0 else "—")
    r2_c3.metric("Power Ranking", f"{int(player_row['Power Ranking']):,}" if int(player_row['Power Ranking']) > 0 else "—")
    r2_c4.metric("Military Rank", player_row['Military Rank'] if pd.notna(player_row['Military Rank']) and player_row['Military Rank'] != "" else "—")

    r3_c1, r3_c2, r3_c3 = st.columns(3)
    r3_c1.metric("Reputation", f"{int(player_row['Individual Reputation']):,}" if int(player_row['Individual Reputation']) > 0 else "—")
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
            low_
