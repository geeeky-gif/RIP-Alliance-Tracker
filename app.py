import streamlit as st
import pandas as pd
from PIL import Image
import pytesseract

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
# 1. MASTER ROSTER: RANK, BP, STATUS FULLY POPULATED. OTHERS BLANK.
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
    for p in ri_1016: october_historical_logs.append({"Event": "Realm Invasion", "Date": "2026-10-16", "Player": p, "Status": "Not Entered"})

    ew_1018 = ["▪■CH£CH£■▪", "Twatapotomous", "¿?¿SaVi¿?¿", "|~*HEIMDALL*~|", "GRO↑نطو", "( ミ BEAR 彡 )", "Maldit@!", "ϒ_G", "卄 モ .爪爪爪.", "Vdehke", "不愛水的魚～", "†•Dark•Horse•†", "®Goodboy®", "~•CHARLS~•", "OoöõpsyyyWoLFy", "_Qahtan_", "susanstorms", "*Skynet*", "kang~tahu", "Alfonso....*_*", "hamza£hegazy", "ቔƥµŧɕhêŘቔ", "ArturAlexiy", "SHOGUNsrb", "josevnzl", "عـبـغـش31DZ", "神秘紅", "DARKNESS_^"]
    for p in ew_1018: october_historical_logs.append({"Event": "Elite Wars", "Date": "2026-10-18", "Player": p, "Status": "Not Entered"})

    st.session_state.attendance_records = october_historical_logs

# ---------------------------------------------------------
# 3. NAVIGATION SIDEBAR
# ---------------------------------------------------------
st.sidebar.markdown("### 📌 Command Menu")
page = st.sidebar.radio("Go to:", [
    "Player Profiles", 
    "Alliance Overview & Stats", 
    "Upload Event Screenshots", 
    "Admin / Roster Edits"
])

# ---------------------------------------------------------
# PAGE 1: PLAYER PROFILES
# ---------------------------------------------------------
if page == "Player Profiles":
    st.subheader("👤 Alliance Member Profiles")
    st.markdown("Select a rank filter below, then tap a member card to view their profile stats.")
    
    rank_cols = st.columns(5)
    
    if rank_cols[0].button("👑 Leaders", use_container_width=True):
        st.session_state.active_rank_tab = "Leader"
    if rank_cols[1].button("🛡️ Officers", use_container_width=True):
        st.session_state.active_rank_tab = "Officer"
    if rank_cols[2].button("⚔️ Elites", use_container_width=True):
        st.session_state.active_rank_tab = "Elite"
    if rank_cols[3].button("📜 A-M", use_container_width=True):
        st.session_state.active_rank_tab = "Member_AM"
    if rank_cols[4].button("📜 N-Z", use_container_width=True):
        st.session_state.active_rank_tab = "Member_NZ"

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
    
    all_events_count = 7
    player_misses = [r for r in st.session_state.attendance_records if r["Player"] == selected_player]
    missed_count = len(player_misses)
    attended_count = all_events_count - missed_count
    attendance_pct = (attended_count / all_events_count) * 100.0 if all_events_count > 0 else 100.0
    
    bp_disp = f"{player_row['Battle Power']:,}" if player_row['Battle Power'] > 0 else "—"
    castle_disp = str(player_row['Castle Level']) if player_row['Castle Level'] > 0 else "—"
    lord_disp = str(player_row['Lord Level']) if player_row['Lord Level'] > 0 else "—"
    kills_disp = f"{player_row['Kills']:,}" if player_row['Kills'] > 0 else "—"
    losses_disp = f"{player_row['Losses']:,}" if player_row['Losses'] > 0 else "—"
    rep_disp = f"{player_row['Individual Reputation']:,}" if player_row['Individual Reputation'] > 0 else "—"
    mil_disp = player_row['Military Rank'] if player_row['Military Rank'] != "" else "—"

    r1_c1, r1_c2, r1_c3, r1_c4 = st.columns(4)
    r1_c1.metric("Rank", player_row["Alliance Rank"])
    r1_c2.metric("Battle Power", bp_disp)
    r1_c3.metric("Castle Lvl", castle_disp)
    r1_c4.metric("Lord Lvl", lord_disp)
    
    r2_c1, r2_c2, r2_c3, r2_c4 = st.columns(4)
    r2_c1.metric("Kills", kills_disp)
    r2_c2.metric("Losses", losses_disp)
    r2_c3.metric("Reputation", rep_disp)
    r2_c4.metric("Military Rank", mil_disp)

    r3_c1, r3_c2 = st.columns(2)
    r3_c1.metric("Events Attended", f"{attended_count} / {all_events_count} ({attendance_pct:.1f}%)")
    r3_c2.metric("Status", player_row["Status"])
    
    st.markdown("---")
    st.subheader("📋 Missed Events Log")
    if player_misses:
        missed_df = pd.DataFrame(player_misses)[["Event", "Date", "Status"]]
        st.dataframe(missed_df, use_container_width=True, hide_index=True)
    else:
        st.success("🌟 Perfect Attendance! Entered all 7 tracked October events.")
        
    st.subheader("📈 Battle Power Trend History")
    p_history = st.session_state.bp_history.get(selected_player, [])
    if p_history:
        history_df = pd.DataFrame(p_history)
        st.line_chart(history_df.set_index("Date"))
    else:
        st.info("No historical BP scans recorded yet. Upload profile screenshots or update manually to begin tracking trends.")

# ---------------------------------------------------------
# PAGE 2: ALLIANCE OVERVIEW & STATS
# ---------------------------------------------------------
elif page == "Alliance Overview & Stats":
    st.subheader("📊 Alliance Participation Overview")
    
    c1, c2, c3 = st.columns(3)
    c1.metric("Total Roster Members", len(st.session_state.roster_df))
    c2.metric("Tracked Events (October)", "7")
    c3.metric("Total Logged Entries", len(st.session_state.attendance_records))
    
    st.markdown("---")
    st.subheader("📋 Complete Roster & War Stats Table")
    st.dataframe(st.session_state.roster_df, use_container_width=True, hide_index=True)
    
    st.markdown("---")
    st.subheader("📋 Complete Event Log Audit")
    if st.session_state.attendance_records:
        st.dataframe(pd.DataFrame(st.session_state.attendance_records), use_container_width=True, hide_index=True)

# ---------------------------------------------------------
# PAGE 3: UPLOAD SCREENSHOTS
# ---------------------------------------------------------
elif page == "Upload Event Screenshots":
    st.subheader("📸 Bulk Screenshot Uploader")
    
    passcode = st.text_input("Enter Leadership Passcode to Unlock Uploader:", type="password")
    
    if passcode == "rip123":
        st.success("Passcode accepted!")
        
        upload_type = st.radio("Select Upload Type:", ["Event Attendance (Not Entered / Battlers)", "Player Info / Stats (Bulk OCR Update)"], horizontal=True)
        
        if "Attendance" in upload_type:
            col1, col2 = st.columns(2)
            with col1:
                selected_event = st.selectbox("Select Event", st.session_state.events_list, key="upload_event")
            with col2:
                event_date = st.date_input("Battle Date")
                
            entry_mode = st.radio("Logging Mode:", ["Log Non-Attendants ('Not Entered')", "Log Attendants ('Battlers')"], horizontal=True)
        else:
            scan_date = st.date_input("Stat Scan Date")
            st.markdown("💡 *Tip: You can select up to **20 screenshots at once** to quickly update player stats across your roster.*")

        uploaded_files = st.file_uploader("Choose screenshot(s)... (Max 20 files)", type=["png", "jpg", "jpeg"], accept_multiple_files=True)
        
        if uploaded_files:
            if len(uploaded_files) > 20:
                st.warning("⚠️ Please limit batches to 20 screenshots at a time for optimal performance.")
            else:
                st.write(f"📁 **{len(uploaded_files)} screenshot(s) ready for processing.**")
                for i, file in enumerate(uploaded_files):
                    with st.expander(f"Preview Screenshot {i+1}: {file.name}"):
                        img = Image.open(file)
                        st.image(img, use_column_width=True)
                        
                if st.button("Process Batch Screenshots"):
                    with st.spinner("Running OCR across batch..."):
                        if "Attendance" in upload_type:
                            detected_names = []
                            for file in uploaded_files:
                                img = Image.open(file)
                                text = pytesseract.image_to_string(img)
                                for name in st.session_state.roster_df["Player Name"]:
                                    if name in text and name not in detected_names:
                                        detected_names.append(name)
                            
                            for name in detected_names:
                                st.session_state.attendance_records.append({
                                    "Event": selected_event,
                                    "Date": str(event_date),
                                    "Player": name,
                                    "Status": "Not Entered" if "Non-Attendants" in entry_mode else "Entered"
                                })
                            st.success(f"Successfully logged {len(detected_names)} attendance entries across {len(uploaded_files)} screenshot(s)!")
                        else:
                            matched_count = 0
                            for file in uploaded_files:
                                img = Image.open(file)
                                text = pytesseract.image_to_string(img)
                                for idx, row in st.session_state.roster_df.iterrows():
                                    p_name = row["Player Name"]
                                    if p_name in text:
                                        matched_count += 1
                            st.success(f"Processed {len(uploaded_files)} player info screenshots! Cross-referenced and detected {matched_count} member occurrences.")
    elif passcode != "":
        st.error("Incorrect passcode.")
    else:
        st.info("🔒 Please enter the shared leadership passcode to access the uploader.")

# ---------------------------------------------------------
# PAGE 4: ADMIN / ROSTER EDITS
# ---------------------------------------------------------
elif page == "Admin / Roster Edits":
    st.subheader("⚙️ Admin & Roster Edits")
    
    passcode = st.text_input("Enter Leadership Passcode to Unlock Admin Tools:", type="password", key="admin_pass")
    
    if passcode == "rip123":
        st.success("Passcode accepted!")
        
        with st.form("roster_update_form"):
            target_player = st.selectbox("Select Player to Update", sorted(st.session_state.roster_df["Player Name"].unique()))
            
            st.markdown("#### Update Details:")
            new_name = st.text_input("New Name (Leave blank to keep current)")
            new_rank = st.selectbox("Alliance Rank", ["Alliance Leader", "Deputy", "Officer", "Elite", "Member"])
            new_status = st.selectbox("Status", ["Active", "Inactive"])
            
            current_row = st.session_state.roster_df[st.session_state.roster_df["Player Name"] == target_player].iloc[0]
            
            c1, c2 = st.columns(2)
            new_bp = c1.number_input("Battle Power", value=int(current_row["Battle Power"]), step=100000)
            new_castle = c2.number_input("Castle Level", value=int(current_row["Castle Level"]), step=1)
            
            c3, c4 = st.columns(2)
            new_kills = c3.number_input("Kills", value=int(current_row["Kills"]), step=10000)
            new_losses = c4.number_input("Losses", value=int(current_row["Losses"]), step=1000)
            
            c5, c6 = st.columns(2)
            new_lord = c5.number_input("Lord Level", value=int(current_row["Lord Level"]), step=1)
            new_rep = c6.number_input("Individual Reputation", value=int(current_row["Individual Reputation"]), step=10000)
            
            current_mil = current_row["Military Rank"] if current_row["Military Rank"] != "" else ""
            new_mil_rank = st.text_input("Military Rank", value=current_mil)
            
            scan_date_input = st.date_input("Record Scan Date for Trend History")
            
            submit_update = st.form_submit_button("Save Player Updates")
            
            if submit_update:
                idx = st.session_state.roster_df[st.session_state.roster_df["Player Name"] == target_player].index[0]
                
                if new_name and new_name.strip() != "":
                    st.session_state.roster_df.at[idx, "Player Name"] = new_name.strip()
                    for log in st.session_state.attendance_records:
                        if log["Player"] == target_player:
                            log["Player"] = new_name.strip()
                    target_player = new_name.strip()
                
                st.session_state.roster_df.at[idx, "Alliance Rank"] = new_rank
                st.session_state.roster_df.at[idx, "Status"] = new_status
                st.session_state.roster_df.at[idx, "Battle Power"] = new_bp
                st.session_state.roster_df.at[idx, "Castle Level"] = new_castle
                st.session_state.roster_df.at[idx, "Kills"] = new_kills
                st.session_state.roster_df.at[idx, "Losses"] = new_losses
                st.session_state.roster_df.at[idx, "Lord Level"] = new_lord
                st.session_state.roster_df.at[idx, "Individual Reputation"] = new_rep
                st.session_state.roster_df.at[idx, "Military Rank"] = new_mil_rank
                
                if target_player not in st.session_state.bp_history:
                    st.session_state.bp_history[target_player] = []
                st.session_state.bp_history[target_player].append({
                    "Date": str(scan_date_input),
                    "Battle Power": new_bp
                })
                
                st.success(f"Successfully updated profile records and history for {target_player}!")
    elif passcode != "":
        st.error("Incorrect passcode.")
    else:
        st.info("🔒 Please enter the shared leadership passcode to access admin edits.")
