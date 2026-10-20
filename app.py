import streamlit as st
import pandas as pd
from PIL import Image
import pytesseract

st.set_page_config(page_title="RIP Alliance Attendance Tracker", layout="wide")

st.title("🛡️ RIP Alliance Attendance Tracker")

# ---------------------------------------------------------
# 1. INITIALIZE MASTER ROSTER DATA
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
        "Battle Power": [114868760] + [20000000] * 97,
        "Status": ["Active"] * 98
    })

# ---------------------------------------------------------
# 2. INITIALIZE PRE-LOGGED OCTOBER EVENTS
# ---------------------------------------------------------
if 'events_list' not in st.session_state:
    st.session_state.events_list = ["Elite Wars", "Fortress War", "Realm Invasion", "Void War", "Territory Defense", "Elite Adventure"]

if 'attendance_records' not in st.session_state:
    # Pre-populate historical October records from processed screenshots
    october_historical_logs = []
    
    # Oct 04 - Elite Wars (47 missed)
    ew_1004_missed = [
        "Compa_Gera", "01*BAD*01", "Twatapotomous", "GRO↑نطو", "M.PΣΠDЯΛGΘΠ.00", "( ミ BEAR 彡 )", "SKELETOR", "AndresEled",
        "Ġñøşïş", ".JOOKER.", ":::MaxHook:::", "Gemlikli16", "Maldit@!", "Pøwer҉", "Δpredator®", "༄🏽BugsBunny•",
        "ArturAlexiy", "~•CHARLS~•", "zazouka ××ஒ", "eskanor.leon", "kadir3322", "Alfonso....*_*", "*Skynet*", "Mary@Chica",
        "DARKNESS_^", "G.aleman^*_*", "_Qahtan_", "SHOGUNsrb", "ቔƥµŧɕhêŘቔ", "XeNa.CheF.", "TOXXICBUNNY", "hamza£hegazy",
        "JuanWolfSantz", "Riad", "Adrián@Arg.", "002 سرراف", "Mrwakandaforever", "VENOM", "josevnzl", "Madara.som3a",
        "عـبـغـش31DZ", "†•Dark•Horse•†", "Vdehke", "«MAX»...", "Abdo0027", "ȼ₣ÐÐ¥LØ₦₲ÐÏĈҜ", "#FATİHSULTAN#HAN"
    ]
    for p in ew_1004_missed:
        october_historical_logs.append({"Event": "Elite Wars", "Date": "2026-10-04", "Player": p, "Status": "Not Entered"})

    # Oct 07 - Elite Wars (23 missed)
    ew_1007_missed = [
        "( ミ BEAR 彡 )", "M.PΣΠDЯΛGΘΠ.00", "•••STYX•••", "•John•○", "GRO↑نطو", "ϒ_G", "•Peresvet•", "ArturAlexiy",
        "عـبـغـش31DZ", "_Qahtan_", "~•CHARLS~•", "hamza£hegazy", "°•WalterWhite•°", "002 سرراف", "DARKNESS_^", "«MAX»...",
        "Vdehke", "Riad", "josevnzl", "kang~tahu", "†•Dark•Horse•†", "TOXXICBUNNY", "Alfonso....*_*"
    ]
    for p in ew_1007_missed:
        october_historical_logs.append({"Event": "Elite Wars", "Date": "2026-10-07", "Player": p, "Status": "Not Entered"})

    # Oct 08 - Fortress War (40 missed)
    fw_1008_missed = [
        "Twatapotomous", "GRO↑نطو", "( ミ BEAR 彡 )", "SKELETOR", "AndresEled", "•••STYX•••", "•Peresvet•", "ϒ_G",
        "Ġñøşïş", "_SţõŗmŔäïdēŗ_", "Maldit@!", ":::MaxHook:::", "•REG!O•", "eskanor.leon", "DiMPeR2.0", "ȼ₣ÐÐ¥LØ₦₲ÐÏĈҜ",
        "*Skynet*", "kang~tahu", "Alfonso....*_*", "Riad", "kadir3322", "JuanWolfSantz", "Wolf ᲼᲼forever", "..Erik..",
        "TOXXICBUNNY", "Vdehke", "OoöõpsyyyWoLFy", "josevnzl", "Abdo0027", "†•Dark•Horse•†", "Mrwakandaforever", "~•CHARLS~•",
        "Madara.som3a", "عـبـغـش31DZ", "ArturAlexiy", "_Qahtan_", "susanstorms", "VENOM", "002 سرراف", "#FATİHSULTAN#HAN"
    ]
    for p in fw_1008_missed:
        october_historical_logs.append({"Event": "Fortress War", "Date": "2026-10-08", "Player": p, "Status": "Not Entered"})

    # Oct 11 - Elite Wars Battle 1 (41 missed)
    ew_1011_1_missed = [
        "Mİ RⱭGЄ", "•FÄLÇÖŅ•", "Twatapotomous", "M.PΣΠDЯΛGΘΠ.00", "Lisichka", "GRO↑نطو", "•••STYX•••", "SKELETOR",
        "( ミ BEAR 彡 )", "•REG!O•", "Maldit@!", "卄 モ .爪爪爪.", "Dominus™`", ":::MaxHook:::", "Ġñøşïş", "ϒ_G",
        "ቔƥµŧɕhêŘቔ", "JuanWolfSantz", "ArturAlexiy", "tsopanakos", "TOXXICBUNNY", "®Goodboy®", "kurt000", "josevnzl",
        "Madara.som3a", "°•WalterWhite•°", "Abdo0027", "susanstorms", "~•CHARLS~•", "002 سرراف", "_Qahtan_", "DiMPeR2.0",
        "«MAX»...", "hamza£hegazy", "VENOM", "Alfonso....*_*", "Vdehke", "Riad", "†•Dark•Horse•†", "kang~tahu", "عـبـغـش31DZ"
    ]
    for p in ew_1011_1_missed:
        october_historical_logs.append({"Event": "Elite Wars (Battle 1)", "Date": "2026-10-11", "Player": p, "Status": "Not Entered"})

    # Oct 11 - Elite Wars Battle 2 (39 missed)
    ew_1011_2_missed = [
        "GRO↑نطو", "xT_DEATH_Tx", "M.PΣΠDЯΛGΘΠ.00", "SKELETOR", "•••STYX•••", "( ミ BEAR 彡 )", "▪■CH£CH£■▪",
        "卄 モ .爪爪爪.", "MB", "ϒ_G", "•REG!O•", "Dominus™`", "Ġñøşïş", "_SţõŗmŔäïdēŗ_", ":::MaxHook:::", "josevnzl",
        "عـبـغـش31DZ", "ቔƥµŧɕhêŘቔ", "OoöõpsyyyWoLFy", "«MAX»...", "Vdehke", "badi_4", "#FATİHSULTAN#HAN", "~•CHARLS~•",
        "神秘紅", "hamza£hegazy", "DiMPeR2.0", "Riad", "ArturAlexiy", "®Goodboy®", "†•Dark•Horse•†", "tsopanakos",
        "kang~tahu", "Alfonso....*_*", "DARKNESS_^", "002 سرراف", "..Erik..", "SHOGUNsrb", "不愛水的魚～"
    ]
    for p in ew_1011_2_missed:
        october_historical_logs.append({"Event": "Elite Wars (Battle 2)", "Date": "2026-10-11", "Player": p, "Status": "Not Entered"})

    # Oct 16 - Realm Invasion (22 missed)
    ri_1016_missed = [
        "( ミ BEAR 彡 )", "¿?¿SaVi¿?¿", "▪■CH£CH£■▪", "Twatapotomous", "GRO↑نطو", "AndresEled", "Δpredator®", "§Grutovsky§",
        "Ġñøşïş", ":::MaxHook:::", "Maldit@!", "Alfonso....*_*", "002 سرراف", "susanstorms", "*Skynet*", "عـبـغـش31DZ",
        "Adrián@Arg.", "神秘紅", "†•Dark•Horse•†", "_Qahtan_", "Riad", "tsopanakos"
    ]
    for p in ri_1016_missed:
        october_historical_logs.append({"Event": "Realm Invasion", "Date": "2026-10-16", "Player": p, "Status": "Not Entered"})

    # Oct 18 - Elite Wars (28 missed)
    ew_1018_missed = [
        "▪■CH£CH£■▪", "Twatapotomous", "¿?¿SaVi¿?¿", "|~*HEIMDALL*~|", "GRO↑نطو", "( ミ BEAR 彡 )", "Maldit@!", "ϒ_G",
        "卄 モ .爪爪爪.", "Vdehke", "不愛水的魚～", "†•Dark•Horse•†", "®Goodboy®", "~•CHARLS~•", "OoöõpsyyyWoLFy", "_Qahtan_",
        "susanstorms", "*Skynet*", "kang~tahu", "Alfonso....*_*", "hamza£hegazy", "ቔƥµŧɕhêŘቔ", "ArturAlexiy", "SHOGUNsrb",
        "josevnzl", "عـبـغـش31DZ", "神秘紅", "DARKNESS_^"
    ]
    for p in ew_1018_missed:
        october_historical_logs.append({"Event": "Elite Wars", "Date": "2026-10-18", "Player": p, "Status": "Not Entered"})

    st.session_state.attendance_records = october_historical_logs

# ---------------------------------------------------------
# 3. NAVIGATION SIDEBAR
# ---------------------------------------------------------
page = st.sidebar.selectbox("Navigation", [
    "Player Profiles", 
    "Upload Event Screenshots", 
    "Master Roster & Status", 
    "Alliance Overview & Stats", 
    "Event Management"
])

# ---------------------------------------------------------
# PAGE 1: PLAYER PROFILES & INDIVIDUAL HISTORY
# ---------------------------------------------------------
if page == "Player Profiles":
    st.header("👤 Player Profile & Attendance History")
    
    player_list = sorted(st.session_state.roster_df["Player Name"].unique())
    selected_player = st.selectbox("Select Player", player_list, key="profile_select")
    
    player_row = st.session_state.roster_df[st.session_state.roster_df["Player Name"] == selected_player].iloc[0]
    
    # Calculate Attendance Metrics for this player
    all_events = [
        ("Elite Wars", "2026-10-04"),
        ("Elite Wars", "2026-10-07"),
        ("Fortress War", "2026-10-08"),
        ("Elite Wars (Battle 1)", "2026-10-11"),
        ("Elite Wars (Battle 2)", "2026-10-11"),
        ("Realm Invasion", "2026-10-16"),
        ("Elite Wars", "2026-10-18")
    ]
    total_tracked_events = len(all_events)
    
    # Filter logs for selected player
    player_misses = [r for r in st.session_state.attendance_records if r["Player"] == selected_player]
    missed_count = len(player_misses)
    attended_count = total_tracked_events - missed_count
    attendance_pct = (attended_count / total_tracked_events) * 100 if total_tracked_events > 0 else 100.0
    
    # High-Level Metrics
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Alliance Rank", player_row["Alliance Rank"])
    c2.metric("Events Attended", f"{attended_count} / {total_tracked_events}")
    c3.metric("Attendance Rate", f"{attendance_pct:.1f}%")
    c4.metric("Member Status", player_row["Status"])
    
    st.markdown("---")
    
    st.subheader("📋 Missed Events Log")
    if player_misses:
        missed_df = pd.DataFrame(player_misses)[["Event", "Date", "Status"]]
        st.dataframe(missed_df, use_container_width=True, hide_index=True)
    else:
        st.success("🌟 Perfect Attendance! This player entered all 7 tracked October events.")
        
    st.subheader("📈 Battle Power Trend")
    bp_data = pd.DataFrame({
        "Date": ["2026-10-01", "2026-10-08", "2026-10-15", "2026-10-18"],
        "Battle Power": [player_row["Battle Power"] * 0.96, player_row["Battle Power"] * 0.98, player_row["Battle Power"] * 0.99, player_row["Battle Power"]]
    })
    st.line_chart(bp_data.set_index("Date"))

# ---------------------------------------------------------
# PAGE 2: UPLOAD EVENT SCREENSHOTS
# ---------------------------------------------------------
elif page == "Upload Event Screenshots":
    st.header("📸 Multi-Screenshot Attendance Uploader")
    st.markdown("Upload event screenshots. OCR will automatically extract player names and log attendance.")
    
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
# PAGE 3: MASTER ROSTER & PROTECTED MANAGEMENT
# ---------------------------------------------------------
elif page == "Master Roster & Status":
    st.header("👥 RIP Master Roster (Read-Only View)")
    st.markdown("This list is locked for viewing to prevent accidental modifications.")
    
    # Display non-editable table
    st.dataframe(st.session_state.roster_df, use_container_width=True, hide_index=True)
    
    st.markdown("---")
    st.subheader("⚙️ Roster Updates & Corrections")
    st.info("Use this form to rename a player or change their active status. This prevents accidental edits.")
    
    with st.form("roster_update_form"):
        target_player = st.selectbox("Select Player to Update", sorted(st.session_state.roster_df["Player Name"].unique()))
        new_name = st.text_input("New Name (Leave blank if keeping current name)")
        new_status = st.selectbox("Status", ["Active", "Inactive"])
        
        submit_update = st.form_submit_button("Confirm Roster Update")
        
        if submit_update:
            idx = st.session_state.roster_df[st.session_state.roster_df["Player Name"] == target_player].index[0]
            
            # Update name if provided
            if new_name and new_name.strip() != "":
                st.session_state.roster_df.at[idx, "Player Name"] = new_name.strip()
                # Update name in historical logs
                for log in st.session_state.attendance_records:
                    if log["Player"] == target_player:
                        log["Player"] = new_name.strip()
                st.success(f"Renamed '{target_player}' to '{new_name.strip()}' across roster and event logs!")
            
            # Update status
            st.session_state.roster_df.at[idx, "Status"] = new_status
            st.success(f"Updated status for '{target_player}' to {new_status}.")

# ---------------------------------------------------------
# PAGE 4: OVERVIEW & AUDIT LOGS
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
# PAGE 5: EVENT TYPES MANAGEMENT
# ---------------------------------------------------------
elif page == "Event Management":
    st.header("⚙️ Custom Event Management")
    new_ev = st.text_input("Add New Event Type (e.g. Sanguine Siege)")
    if st.button("Add Event"):
        if new_ev and new_ev not in st.session_state.events_list:
            st.session_state.events_list.append(new_ev)
            st.success(f"Added '{new_ev}' to event list!")
    st.write("Active Events:", st.session_state.events_list)
