import streamlit as st
import pandas as pd
from PIL import Image
import pytesseract

st.set_page_config(page_title="RIP Alliance Attendance Tracker", layout="wide")

st.title("🛡️ RIP Alliance Attendance Tracker")

# Initialize Session State
if 'events_list' not in st.session_state:
    st.session_state.events_list = ["Elite Wars", "Fortress War", "Realm Invasion", "Void War", "Territory Defense", "Elite Adventure"]

if 'attendance_records' not in st.session_state:
    st.session_state.attendance_records = []

# Initialize Roster in Session State so edits (Name changes, Inactive status) persist
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
        "Battle Power": [114868760] + [20000000] * 97,  # Default baseline BP for demo
        "Status": ["Active"] * 98
    })

# Navigation Sidebar
page = st.sidebar.selectbox("Navigation", [
    "Upload Event Screenshots", 
    "Player Profiles", 
    "Master Roster & Management", 
    "Alliance Overview & Stats", 
    "Event Management"
])

if page == "Upload Event Screenshots":
    st.header("📸 Multi-Screenshot Attendance Uploader")
    
    col1, col2 = st.columns(2)
    with col1:
        selected_event = st.selectbox("Select Event", st.session_state.events_list)
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
                
                # Save to session records
                for name in detected_names:
                    st.session_state.attendance_records.append({
                        "Event": selected_event,
                        "Date": str(event_date),
                        "Player": name,
                        "Type": entry_mode
                    })
                st.success(f"Successfully logged {len(detected_names)} attendance entries for {selected_event} ({event_date})!")

elif page == "Player Profiles":
    st.header("👤 Individual Player Profile & Trends")
    
    player_list = sorted(st.session_state.roster_df["Player Name"].unique())
    selected_player = st.selectbox("Select Player", player_list)
    
    player_row = st.session_state.roster_df[st.session_state.roster_df["Player Name"] == selected_player].iloc[0]
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Alliance Rank", player_row["Alliance Rank"])
    col2.metric("Current Battle Power", f"{player_row['Battle Power']:,}")
    col3.metric("Status", player_row["Status"])
    
    st.subheader("📈 Battle Power Trend Over Time")
    # Mock historical BP data for demonstration
    bp_trend_data = pd.DataFrame({
        "Date": ["2026-10-01", "2026-10-08", "2026-10-15", "2026-10-18"],
        "Battle Power": [player_row["Battle Power"] * 0.95, player_row["Battle Power"] * 0.97, player_row["Battle Power"] * 0.99, player_row["Battle Power"]]
    })
    st.line_chart(bp_trend_data.set_index("Date"))
    
    st.subheader("📋 Event Participation History")
    player_records = [r for r in st.session_state.attendance_records if r["Player"] == selected_player]
    if player_records:
        st.dataframe(pd.DataFrame(player_records), use_container_width=True)
    else:
        st.info("No event records logged for this player yet.")

elif page == "Master Roster & Management":
    st.header("👥 Master Roster & Member Management")
    st.markdown("Update player avatar names or toggle members between **Active** and **Inactive**.")
    
    # Editable Roster Table
    edited_roster = st.data_editor(
        st.session_state.roster_df, 
        num_rows="dynamic",
        use_container_width=True,
        key="roster_editor"
    )
    st.session_state.roster_df = edited_roster
    st.success("Changes to roster saved automatically.")

elif page == "Alliance Overview & Stats":
    st.header("📊 Alliance Overview & Logs")
    st.metric("Total Members in Roster", len(st.session_state.roster_df))
    st.metric("Total Logged Attendance Records", len(st.session_state.attendance_records))
    
    if st.session_state.attendance_records:
        st.subheader("All Logged Records")
        st.dataframe(pd.DataFrame(st.session_state.attendance_records), use_container_width=True)
    else:
        st.info("Upload screenshots in the upload tab to start populating records.")

elif page == "Event Management":
    st.header("⚙️ Event Management")
    new_ev = st.text_input("New Event Name")
    if st.button("Add Event"):
        if new_ev and new_ev not in st.session_state.events_list:
            st.session_state.events_list.append(new_ev)
            st.success(f"Added {new_ev}!")
    st.write("Active Events:", st.session_state.events_list)
