import streamlit as st
import pandas as pd
from PIL import Image
import pytesseract

st.set_page_config(page_title="RIP Alliance Attendance Tracker", layout="wide")

st.title("🛡️ RIP Alliance Attendance Tracker")

# Navigation Sidebar
page = st.sidebar.selectbox("Navigation", ["Upload Event Screenshots", "Alliance Overview & Stats", "Master Roster", "Event Management"])

# Initialize Session State for Custom Events and Event Logs
if 'events_list' not in st.session_state:
    st.session_state.events_list = ["Elite Wars", "Fortress War", "Realm Invasion", "Void War", "Territory Defense", "Elite Adventure"]

if 'attendance_records' not in st.session_state:
    st.session_state.attendance_records = []

# Master Roster DataFrame (All 98 Members)
@st.cache_data
def get_master_roster():
    return pd.DataFrame({
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
        ]
    })

roster_df = get_master_roster()

if page == "Upload Event Screenshots":
    st.header("📸 Multi-Screenshot Attendance Uploader")
    st.markdown("Upload one or multiple screenshots from your game event. Select whether you are capturing **Non-Attendants** or **Attendants**.")
    
    col1, col2 = st.columns(2)
    with col1:
        selected_event = st.selectbox("Select Event", st.session_state.events_list)
    with col2:
        event_date = st.date_input("Battle Date")
        
    entry_mode = st.radio("Logging Mode:", ["Log Non-Attendants ('Not Entered')", "Log Attendants ('Battlers')"], horizontal=True)
    
    uploaded_files = st.file_uploader("Choose screenshot(s)...", type=["png", "jpg", "jpeg"], accept_multiple_files=True)
    
    if uploaded_files:
        st.write(f"📁 **{len(uploaded_files)} screenshot(s) uploaded successfully.**")
        
        for i, file in enumerate(uploaded_files):
            with st.expander(f"Preview Screenshot {i+1}: {file.name}"):
                img = Image.open(file)
                st.image(img, use_column_width=True)
                
        if st.button("Process All Screenshots & Log Attendance"):
            with st.spinner("Running OCR across all uploaded images..."):
                extracted_names = []
                for file in uploaded_files:
                    img = Image.open(file)
                    text = pytesseract.image_to_string(img)
                    for name in roster_df["Player Name"]:
                        if name in text and name not in extracted_names:
                            extracted_names.append(name)
                
                st.success(f"Processed {len(uploaded_files)} screenshot(s)! Detected {len(extracted_names)} player names.")
                st.write(f"**Mode:** {entry_mode}")
                st.write("Detected Players:", extracted_names)

elif page == "Event Management":
    st.header("⚙️ Event Management")
    st.markdown("Add new event types to the dropdown list so you can track custom or new game events.")
    
    new_event_name = st.text_input("New Event Name (e.g. Sanguine Siege, Alliance Championship)")
    if st.button("Add Event"):
        if new_event_name and new_event_name not in st.session_state.events_list:
            st.session_state.events_list.append(new_event_name)
            st.success(f"Added '{new_event_name}' to the event list!")
        else:
            st.warning("Please enter a valid, unique event name.")
            
    st.subheader("Current Active Events")
    for ev in st.session_state.events_list:
        st.write(f"- {ev}")

elif page == "Alliance Overview & Stats":
    st.header("📊 Alliance Attendance Dashboard")
    st.metric("Total Roster Members", len(roster_df))
    st.markdown("Dashboard statistics and historical trends will appear here as events are logged.")

elif page == "Master Roster":
    st.header("👥 RIP Master Roster (98 Members)")
    st.dataframe(roster_df, use_container_width=True)
