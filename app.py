import streamlit as st
import pandas as pd
from PIL import Image
import pytesseract

st.set_page_config(page_title="RIP Alliance Attendance Tracker", layout="wide")

# Custom CSS to make the sidebar narrower for landscape mode
st.markdown(
    """
    <style>
        [data-testid="stSidebar"] {
            min-width: 200px;
            max-width: 240px;
        }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("🛡️ RIP Alliance Attendance Tracker")

# ---------------------------------------------------------
# 1. INITIALIZE MASTER ROSTER DATA WITH EXACT BATTLE POWERS
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
        "Status": ["Active"] * 98
    })

if 'selected_player_name' not in st.session_state:
    st.session_state.selected_player_name = "•~SoulTaker~•"

if 'active_rank_tab' not in st.session_state:
    st.session_state.active_rank_tab = "Leader"

# ---------------------------------------------------------
# 2. INITIALIZE PRE-LOGGED OCTOBER EVENTS
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
# 3. NAVIGATION SIDEBAR (REDUCED PAGES)
# ---------------------------------------------------------
st.sidebar.markdown("### 📌 Navigation")
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
    st.header("👤 Player Profile & Attendance History")
    st.markdown("Tap any rank button below to list members, then tap a member to view their profile.")
    
    # Touch Pills for Rank Selection
    rank_cols = st.columns(5)
    
    if rank_cols[0].button("👑 Leaders", use_container_width=True):
        st.session_state.active_rank_tab = "Leader"
    if rank_cols[1].button("🛡️ Officers", use_container_width=True):
        st.session_state.active_rank_tab = "Officer"
    if rank_cols[2].button("⚔️ Elites", use_container_width=True):
        st.session_state.active_rank_tab = "Elite"
    if rank_cols[3].button("📜 Members A-M", use_container_width=True):
        st.session_state.active_rank_tab = "Member_AM"
    if rank_cols[4].button("📜 Members N-Z", use_container_width=True):
        st.session_state.active_rank_tab = "Member_NZ"

    # Filter members based on selected Touch Pill
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

    # Render Member Selection Cards with individual Battle Power
    st.markdown("#### Select Player Card:")
    grid_cols = st.columns(2)
    for idx, row in filtered_df.reset_index().iterrows():
        p_name = row["Player Name"]
        p_bp = row["Battle Power"]
        bp_label = f"{p_bp / 1_000_000:.1f}M" if p_bp > 0 else "0"
        
        if grid_cols[idx % 2].button(f"👤 {p_name}\n⚔️ {bp_label} BP", key=f"card_{p_name}", use_container_width=True):
            st.session_state.selected_player_name = p_name

    selected_player = st.session_state.selected_player_name
    st.markdown("---")
    st.markdown(f"## 📊 Selected Profile: **{selected_player}**")
    
    player_row = st.session_state.roster_df[st.session_state.roster_df["Player Name"] == selected_player].iloc[0]
    
    all_events_count = 7
    player_misses = [r for r in st.session_state.attendance_records if r["Player"] == selected_player]
    missed_count = len(player_misses)
    attended_count = all_events_count - missed_count
    attendance_pct = (attended_count / all_events_count) * 100.0 if all_events_count > 0 else 100.0
    
    # Read-Only Metrics with exact individual Battle Power
    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric("Rank", player_row["Alliance Rank"])
    c2.metric("Battle Power", f"{player_row['Battle Power']:,}")
    c3.metric("Attended", f"{attended_count} / {all_events_count}")
    c4.metric("Rate", f"{attendance_pct:.1f}%")
    c5.metric("Status", player_row["Status"])
    
    st.subheader("📋 Missed Events Log")
    if player_misses:
        missed_df = pd.DataFrame(player_misses)[["Event", "Date", "Status"]]
        st.dataframe(missed_df, use_container_width=True, hide_index=True)
    else:
        st.success("🌟 Perfect Attendance! Entered all 7 tracked October events.")
        
    st.subheader("📈 Battle Power Trend")
    bp_val = player_row["Battle Power"]
    bp_data = pd.DataFrame({
        "Date": ["2026-10-01", "2026-10-08", "2026-10-15", "2026-10-18"],
        "Battle Power": [bp_val * 0.96, bp_val * 0.98, bp_val * 0.99, bp_val]
    })
    st.line_chart(bp_data.set_index("Date"))

# ---------------------------------------------------------
# PAGE 2: ALLIANCE OVERVIEW & STATS (READ-ONLY)
# ---------------------------------------------------------
elif page == "Alliance Overview & Stats":
    st.header("📊 Alliance Participation Overview")
    
    c1, c2, c3 = st.columns(3)
    c1.metric("Total Roster Members", len(st.session_state.roster_df))
    c2.metric("Tracked Events (October)", "7")
    c3.metric("Total Logged Entries", len(st.session_state.attendance_records))
    
    st.markdown("---")
    st.subheader("📋 Complete Event Log Audit")
    if st.session_state.attendance_records:
        st.dataframe(pd.DataFrame(st.session_state.attendance_records), use_container_width=True, hide_index=True)

# ---------------------------------------------------------
# PAGE 3: UPLOAD SCREENSHOTS (FOR DEPUTIES)
# ---------------------------------------------------------
elif page == "Upload Event Screenshots":
    st.header("📸 Screenshot Attendance Uploader")
    
    col1, col2 = st.columns(2)
    with col1:
        selected_event = st.selectbox("Select Event", st.session_state.events_list, key="upload_event")
    with col2:
        event_date = st.date_input("Battle Date")
        
    entry_mode = st.radio("Logging Mode:", ["Log Non-Attendants ('Not Entered')", "Log Attendants ('Battlers')"], horizontal=True)
    
    uploaded_files = st.file_uploader("Choose screenshot(s)...", type=["png", "jpg", "jpeg"], accept_multiple_files=True)
    
    if uploaded_files:
        st.write(f"📁 **{len(uploaded_files)} screenshot(s) uploaded.**")
        for i, file in enumerate(uploaded_files):
            with st.expander(f"Preview Screenshot {i+1}: {file.name}"):
                img = Image.open(file)
                st.image(img, use_column_width=True)
                
        if st.button("Process Screenshots & Save Records"):
            with st.spinner("Running OCR..."):
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
                st.success(f"Logged {len(detected_names)} entries for {selected_event} ({event_date})!")

# ---------------------------------------------------------
# PAGE 4: ADMIN / ROSTER EDITS
# ---------------------------------------------------------
elif page == "Admin / Roster Edits":
    st.header("⚙️ Admin & Roster Edits")
    st.info("Form fields requiring typing are strictly contained to this admin page.")
    
    with st.form("roster_update_form"):
        target_player = st.selectbox("Select Player to Update", sorted(st.session_state.roster_df["Player Name"].unique()))
        new_name = st.text_input("New Name (Leave blank to keep current)")
        new_status = st.selectbox("Status", ["Active", "Inactive"])
        
        submit_update = st.form_submit_button("Confirm Roster Update")
        
        if submit_update:
            idx = st.session_state.roster_df[st.session_state.roster_df["Player Name"] == target_player].index[0]
            if new_name and new_name.strip() != "":
                st.session_state.roster_df.at[idx, "Player Name"] = new_name.strip()
                for log in st.session_state.attendance_records:
                    if log["Player"] == target_player:
                        log["Player"] = new_name.strip()
                st.success(f"Renamed '{target_player}' to '{new_name.strip()}'!")
            
            st.session_state.roster_df.at[idx, "Status"] = new_status
            st.success(f"Updated status for '{target_player}' to {new_status}.")
