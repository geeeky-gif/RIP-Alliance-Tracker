import streamlit as st
import pandas as pd
from PIL import Image
import pytesseract
from difflib import SequenceMatcher
import os
import re

st.set_page_config(page_title="RIP Alliance Attendance Tracker", layout="wide")

# ---------------------------------------------------------
# FORCE DARK WAR & ORDER / RIP ALLIANCE THEME CSS (DAY & NIGHT)
# ---------------------------------------------------------
st.markdown(
    """
    <style>
        /* Force app dark background even in light mode */
        .stApp, [data-testid="stAppViewContainer"], [data-testid="stHeader"] {
            background-color: #0e1117 !important;
            color: #e0e0e0 !important;
        }
        
        /* Sidebar styling */
        [data-testid="stSidebar"] {
            min-width: 200px;
            max-width: 240px;
            background-color: #121418 !important;
        }
        
        /* RIP Gold Header */
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
        
        /* Metric Box Dark Containers */
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

        /* Force dark background on input fields, dropdowns, & text boxes */
        div[data-baseweb="input"], div[data-baseweb="select"], .stTextInput > div > div {
            background-color: #161a22 !important;
            color: #ffffff !important;
            border-color: #333842 !important;
        }
        input {
            color: #ffffff !important;
        }
        
        /* Dark Table Overrides */
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

# Load or Initialize Master Roster
if 'roster_df' not in st.session_state:
    if os.path.exists(ROSTER_FILE):
        st.session_state.roster_df = pd.read_csv(ROSTER_FILE)
    else:
        st.session_state.roster_df = pd.DataFrame({
            "Player Name": [
                "•~SoulTaker~•", "Warbansteiger", "01*BAD*01", "MixMasterMike!", "•FÄLÇÖŅ•", "Mİ RⱭGЄ", "Compa_Gera",
                "ALİ_DEMİR", "SKELETOR", "KÏṪṪŸ", "|~*HEIMDALL*~|", "( ミ BEAR 彡 )", "MikeB1973", "•John•○", "Lisichka",
                "M.PΣΠDЯΛGΘΠ.00", "xT_DEATH_Tx", "triXXter2304", "¿?¿SaVi¿?¿", "•••STYX•••", "GRO↑نطو", "₩E₮_ÐRƸAɱƵ",
                "Twatapotomous", "VillageWarrior", "▪■CH£CH£■▪", "AndresEled", "Minion.B", "Ġñøşïş", "•REG!O•", "MB",
                "Gemlikli16", "༄🏽BugsBunny•", "_SţõŗmŔäïdēŗ_", "*|~BebePanda~|*", "Pøwer҉", "卄 モ .爪爪爪.", "Edelvejs",
                "№ C r a z y №", "Dominus™`", "Cosmonaut®", "Δpredator®", ".JOOKER.", "•Peresvet•", "___Lazy___",
                "§Grutovsky§", "Maldit@!", "ϒ_G", ":::MaxHook:::", "..Erik..", "神秘紅", "kadir3322", "OoöõpsyyyWoLFy",
                "JuanWolfSantz", "*Skynet*", "ȼ₣ÐÐ¥LØ₦₲ÐÏĈҜ", "«1»ABDO", "°¶~iS~¶°", "ቔƥµŧɕhêŘቔ", "Mrwakandaforever",
                "豬頭瓶子", "Riad", "badi_4", "~•CHARLS~•", "Marihuna.Vnzl™", "Abdo0027", "#FATİHSULTAN#HAN", "josevnzl",
                "Mary@Chica", "«MAX»...", "Wolf ᲼᲼forever", "不愛水的魚～", "°•WalterWhite•°", "VENOM", "XeNa.CheF.",
                "hamza£hegazy", "TOXXICBUNNY", "DiMPeR2.0", "®Goodboy®", "_Qahtan_", "Madara.som3a", "DARKNESS_^",
                "HorusRun", "Alfonso....*_*", "ArturAlexiy", "G.aleman^*_*", "SHOGUNsrb", "BONSEK", "kang~tahu",
                "tsopanakos", "002 سرراف", "kurt000", "zazouka ××ஒ", "عـبـغـش31DZ", "Vdehke", "eskanor.leon", "susanstorms",
                "Adrián@Arg.", "†•Dark•Horse•†"
            ],
            "Alliance Rank": [
                "Alliance Leader", "Deputy", "Deputy", "Deputy", "Deputy", "Deputy", "Deputy",
                "Officer", "Officer", "Officer", "Officer", "Officer", "Officer", "Officer", "Officer",
                "Officer", "Officer", "Officer", "Officer", "Officer", "Officer", "Officer",
                "Officer", "Officer", "Officer", "Officer", "Elite", "Elite", "Elite", "Elite",
                "Elite", "Elite", "Elite", "Elite", "Elite", "Elite", "Elite",
                "Elite", "Elite", "Elite", "Elite", "Elite", "Elite", "Elite",
                "Elite", "Elite", "Elite", "Elite", "Member", "Member", "Member", "Member",
                "Member", "Member", "Member", "Member", "Member", "Member", "Member",
                "Member", "Member", "Member", "Member", "Member", "Member", "Member", "Member",
                "Member", "Member", "Member", "Member", "Member", "Member", "Member", "Member",
                "Member", "Member", "Member", "Member", "Member", "Member", "Member",
                "Member", "Member", "Member", "Member", "Member", "Member", "Member", "Member",
                "Member", "Member", "Member", "Member", "Member", "Member", "Member", "Member"
            ],
            "Battle Power": [
                114868760, 19755892, 46233787, 73798788, 27125931, 33185471, 14412624,
                41320177, 30311814, 27592265, 53629229, 14484362, 29558050, 64213255, 12870792,
                24504174, 32362970, 13481429, 20718008, 41983374, 14223374, 29167177,
                13214323, 28068481, 17422525, 32072931, 22049897, 17153913, 22959795, 13353616,
                16340322, 17826745, 16798028, 0, 17597305, 20851556, 23351759,
                22416721, 16595288, 16987720, 18864239, 25294936, 17687980, 20048433,
                16493289, 21199760, 26577988, 15101687, 17835737, 20452615, 11007546, 10329042,
                20292626, 13949713, 22701921, 22615040, 10044142, 28685097, 16881537,
                17039949, 12238796, 12710750, 8655503, 12561949, 0, 29729176, 11624664,
                20266930, 9329853, 10820403, 17063715, 46720961, 20773665, 0,
                9351327, 17047386, 13851926, 18706825, 12153728, 21693287, 22976112,
                13134740, 11073114, 6968217, 12849922, 8767112, 9780074, 16478082,
                16008706, 18590299, 15498491, 20010237, 18409578, 22880798, 16406189, 29270139,
                12223807, 18231946
            ],
            "Kills": [0] * 98,
            "Losses": [0] * 98,
            "Castle Level": [0] * 98,
            "Lord Level": [0] * 98,
            "Individual Reputation": [0] * 98,
            "Power Ranking": [0] * 98,
            "Military Rank": [""] * 98,
            "Status": ["Active"] * 98
        })
        st.session_state.roster_df.to_csv(ROSTER_FILE, index=False)

def save_roster():
    st.session_state.roster_df.to_csv(ROSTER_FILE, index=False)

# Load or Initialize Field Locks
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

# Load or Initialize BP History
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

# ---------------------------------------------------------
# FUZZY MATCHING & OCR PARSER HELPERS
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
        "Player Name": None,
        "Castle Level": 0,
        "Lord Level": 0,
        "Individual Reputation": 0,
        "Military Rank": "",
        "Power Ranking": 0,
        "Battle Power": 0,
        "Kills": 0,
        "Losses": 0
    }
    
    for line in lines[:6]:
        match, score = find_best_roster_match(line, roster_names, cutoff=0.65)
        if match:
            parsed_data["Player Name"] = match
            break
            
    if not parsed_data["Player Name"]:
        for line in lines:
            match, score = find_best_roster_match(line, roster_names, cutoff=0.75)
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
            if val > 0:
                parsed_data["Individual Reputation"] = val
            elif i + 1 < len(lines):
                parsed_data["Individual Reputation"] = extract_number(lines[i+1])

        if "military rank" in line_lower or ("rank" in line_lower and "power" not in line_lower and "position" not in line_lower):
            parts = line.split(":")
            if len(parts) > 1 and parts[1].strip():
                parsed_data["Military Rank"] = parts[1].strip()
            elif i + 1 < len(lines):
                parsed_data["Military Rank"] = lines[i+1].strip()

        if "power ranking" in line_lower or "power rank" in line_lower:
            val = extract_number(line)
            if val > 0:
                parsed_data["Power Ranking"] = val
            elif i + 1 < len(lines):
                parsed_data["Power Ranking"] = extract_number(lines[i+1])

        if "battle power" in line_lower or (line_lower == "power" and "ranking" not in line_lower):
            val = extract_number(line)
            if val > 0:
                parsed_data["Battle Power"] = val
            elif i + 1 < len(lines):
                parsed_data["Battle Power"] = extract_number(lines[i+1])

        if "kills" in line_lower:
            parsed_data["Kills"] = extract_number(line)
            if parsed_data["Kills"] == 0 and i + 1 < len(lines):
                parsed_data["Kills"] = extract_number(lines[i+1])
                
        if "losses" in line_lower:
            parsed_data["Losses"] = extract_number(line)
            if parsed_data["Losses"] == 0 and i + 1 < len(lines):
                parsed_data["Losses"] = extract_number(lines[i+1])

    return parsed_data

# ---------------------------------------------------------
# RESTORE PRE-LOGGED OCTOBER EVENTS
# ---------------------------------------------------------
if 'events_list' not in st.session_state:
    st.session_state.events_list = ["Elite Wars", "Fortress War", "Realm Invasion", "Void War", "Territory Defense", "Elite Adventure"]

if 'attendance_records' not in st.session_state:
    october_historical_logs = []
    ew_1004 = ["Compa_Gera", "01*BAD*01", "Twatapotomous", "GRO↑نطو", "M.PΣΠDЯΛGΘΠ.00", "( ミ BEAR 彡 )", "SKELETOR", "AndresEled", "Ġñøşïş", ".JOOKER.", ":::MaxHook:::", "Gemlikli16", "Maldit@!", "Pøwer҉", "Δpredator®", "༄🏽BugsBunny•", "ArturAlexiy", "~•CHARLS~•", "zazouka ××ஒ", "eskanor.leon", "kadir3322", "Alfonso....*_*", "*Skynet*", "Mary@Chica", "DARKNESS_^", "G.aleman^*_*", "_Qahtan_", "SHOGUNsrb", "ቔƥµŧɕhêŘቔ", "XeNa.CheF.", "TOXXICBUNNY", "hamza£hegazy", "JuanWolfSantz", "Riad", "Adrián@Arg.", "002 سرراف", "Mrwakandaforever", "VENOM", "josevnzl", "Madara.som3a", "عـبـغـش31DZ", "†•Dark•Horse•†", "Vdehke", "«MAX»...", "Abdo0027", "ȼ₣ÐÐ¥LØ₦₲ÐÏĈҜ", "#FATİHSULTAN#HAN"]
    for p in ew_1004: october_historical_logs.append({"Event": "Elite Wars", "Date": "2026-10-04", "Player": p, "Status": "Not Entered"})

    ew_1007 = ["( ミ BEAR 彡 )", "M.PΣΠDЯΛGΘΠ.00", "•••STYX•••", "•John•○", "GRO↑نطو", "ϒ_G", "•Peresvet•", "ArturAlexiy", "عـبـغـش31DZ", "_Qahtan_", "~•CHARLS~•", "hamza£hegazy", "°•WalterWhite•°", "002 سرراف", "DARKNESS_^", "«MAX»...", "Vdehke", "Riad", "josevnzl", "kang~tahu", "†•Dark•Horse•†", "TOXXICBUNNY", "Alfonso....*_*"]
    for p in ew_1007: october_historical_logs.append({"Event": "Elite Wars", "Date": "2026-10-07", "Player": p, "Status": "Not Entered"})

    fw_1008 = ["Twatapotomous", "GRO↑نطو", "( ミ BEAR 彡 )", "SKELETOR", "AndresEled", "•••STYX•••", "•Peresvet•", "ϒ_G", "Ġñøşïş", "_SţõŗmŔäïdēŗ_", "Maldit@!", ":::MaxHook:::", "•REG!O•", "eskanor.leon", "DiMPeR2.0", "ȼ₣ÐÐ¥LØ₦₲ÐÏĈҜ", "*Skynet*", "kang~tahu", "Alfonso....*_*", "Riad", "kadir3322", "JuanWolfSantz", "Wolf ᲼᲼forever", "..Erik..", "TOXXICBUNNY", "Vdehke", "OoöõpsyyyWoLFy", "josevnzl", "Abdo0027", "†•Dark•Horse•†", "Mrwakandaforever", "~•CHARLS~•", "Madara.som3a", "عـبـغـش31DZ", "ArturAlexiy", "_Qahtan_", "susanstorms", "VENOM", "002 سرراف", "#FATİHSULTAN#HAN"]
    for p in fw_1008: october_historical_logs.append({"Event": "Fortress War", "Date": "2026-10-08", "Player": p, "Status": "Not Entered"})

    ew_1011_1 = ["Mİ RⱭGЄ", "•FÄLÇÖŅ•", "Twatapotomous", "M.PΣΠDЯΛGΘΠ.00", "Lisichka", "GRO↑نطو", "•••STYX•••", "SKELETOR", "( ミ BEAR 彡 )", "•REG!O•", "Maldit@!", "卄 モ .爪爪爪.", "Domin
