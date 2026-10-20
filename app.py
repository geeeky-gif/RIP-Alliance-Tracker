import streamlit as st
import pandas as pd
from PIL import Image
import pytesseract
from difflib import SequenceMatcher

st.set_page_config(page_title="RIP Alliance Attendance Tracker", layout="wide")

# ---------------------------------------------------------
# CUSTOM WAR & ORDER / RIP ALLIANCE THEME CSS
# ---------------------------------------------------------
st.markdown(
    """
    <style>
        [data-testid="stSidebar"] {
            min-width: 200px;
            max-width: 240px;
            background-color: #121418;
        }
        .stApp {
            background-color: #0e1117;
            color: #e0e0e0;
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
            color: #ffd700;
            font-family: 'Cinzel', serif, sans-serif;
            text-transform: uppercase;
            letter-spacing: 2px;
            margin: 0;
            font-size: 24px;
        }
        .rip-header p {
            color: #a0a0a0;
            margin: 5px 0 0 0;
            font-size: 14px;
        }
        [data-testid="stMetric"] {
            background-color: #161a22;
            border: 1px solid #333842;
            padding: 8px;
            border-radius: 6px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.4);
        }
        [data-testid="stMetricLabel"] {
            color: #b0b8c4 !important;
            font-size: 12px !important;
        }
        [data-testid="stMetricValue"] {
            color: #ffd700 !important;
            font-size: 16px !important;
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
# FUZZY MATCHING HELPER FUNCTION
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

# ---------------------------------------------------------
# 1. MASTER ROSTER INITIALIZATION (RESTORED BATTLE POWERS)
# ---------------------------------------------------------
if 'roster_df' not in st.session_state:
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
        "Military Rank": [""] * 98,
        "Status": ["Active"] * 98
    })

if 'selected_player_name' not in st.session_state:
    st.session_state.selected_player_name = "•~SoulTaker~•"

if 'active_rank_tab' not in st.session_state:
    st.session_state.active_rank_tab = "Leader"

if 'bp_history' not in st.session_state:
    st.session_state.bp_history = {}

# ---------------------------------------------------------
# 2. RESTORE PRE-LOGGED OCTOBER EVENTS
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

    ew_1011_1 = ["Mİ RⱭGЄ", "•FÄLÇÖŅ•", "Twatapotomous", "M.PΣΠDЯΛGΘΠ.00", "Lisichka", "GRO↑نطو", "•••STYX•••", "SKELETOR", "( ミ BEAR 彡 )", "•REG!O•", "Maldit@!", "卄 モ .爪爪爪.", "Dominus™`", ":::MaxHook:::", "Ġñøşïş", "ϒ_G", "ቔƥµŧɕhêŘቔ", "JuanWolfSantz", "ArturAlexiy", "tsopanakos", "TOXXICBUNNY", "®Goodboy®", "kurt000", "josevnzl", "Madara.som3a", "°•WalterWhite•°", "Abdo0027", "susanstorms", "~•CHARLS~•", "002 سرراف", "_Qahtan_", "DiMPeR2.0", "«MAX»...", "hamza£hegazy", "VENOM", "Alfonso....*_*", "Vdehke", "Riad", "†•Dark•Horse•†", "kang~tahu", "عـبـغـش31DZ"]
    for p in ew_1011_1: october_historical_logs.append({"Event": "Elite Wars (Battle 1)", "Date": "2026-10-11", "Player": p, "Status": "Not Entered"})

    ew_1011_2 = ["GRO↑نطو", "xT_DEATH_Tx", "M.PΣΠDЯΛGΘΠ.00", "SKELETOR", "•••STYX•••", "( ミ BEAR 彡 )", "▪■CH£CH£■▪", "卄 モ .爪爪爪.", "MB", "ϒ_G", "•REG!O•", "Dominus™`", "Ġñøşïş", "_SţõŗmŔäïdēŗ_", ":::MaxHook:::", "josevnzl", "عـبـغـش31DZ", "ቔƥµŧɕhêŘቔ", "OoöõpsyyyWoLFy", "«MAX»...", "Vdehke", "badi_4", "#FATİHSULTAN#HAN", "~•CHARLS~•", "神秘紅", "hamza£hegazy", "DiMPeR2.0", "Riad", "ArturAlexiy", "®Goodboy®", "†•Dark•Horse•†", "tsopanakos", "kang~tahu", "Alfonso....*_*", "DARKNESS_^", "002 سرراف", "..Erik..", "SHOGUNsrb", "不愛水的魚～"]
    for p in ew_1011_2: october_historical_logs.append({"Event": "Elite Wars (Battle 2)", "Date": "2026-10-11", "Player": p, "Status": "Not Entered"})

    ri_1016 = ["( ミ BEAR 彡 )", "¿?¿SaVi¿?¿", "▪■CH£CH£■▪", "Twatapotomous", "GRO↑نطو", "AndresEled", "Δpredator®", "§Grutovsky§", "Ġñøşïş", ":::MaxHook:::", "Maldit@!", "Alfonso....*_*", "002 سرراف", "susanstorms", "*Skynet*", "عـبـغـش31DZ", "Adrián@Arg.", "神秘紅", "†•Dark•Horse•†", "_Qahtan_", "Riad", "tsopanakos"]
    for p in ri_1016: october_historical_logs.append({"Event": "Realm Invasion", "Date": "2026-10-1
