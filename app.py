import streamlit as st
import pandas as pd
from PIL import Image
import pytesseract

st.set_page_config(page_title="RIP Alliance Attendance Tracker", layout="wide")

st.title("🛡️ RIP Alliance Attendance Tracker")
st.markdown("Automated Event Tracking & Leadership Dashboard")

# Navigation Sidebar
page = st.sidebar.selectbox("Navigation", ["Upload Event Screenshot", "Alliance Overview & Stats", "Master Roster"])

# Load Roster Data (Mock or connected to your Google Sheet / CSV)
@st.cache_data
def get_master_roster():
    # Placeholder for your 98 members
    return pd.DataFrame({
        "Player Name": ["•~SoulTaker~•", "Warbansteiger", "01*BAD*01", "MixMasterMike!", "•FÄLÇÖŅ•", "Mİ RⱭGЄ", "Compa_Gera"],
        "Alliance Rank": ["Alliance Leader", "Deputy", "Deputy", "Deputy", "Deputy", "Deputy", "Deputy"],
        "Battle Power": [114868760, 19755892, 46233787, 73798788, 27125931, 33185471, 14412624]
    })

roster_df = get_master_roster()

if page == "Upload Event Screenshot":
    st.header("📸 Event Non-Attendance Uploader")
    st.markdown("Upload the 'Not Entered' screenshot from your game event. The OCR will extract player names.")
    
    event_name = st.selectbox("Select Event", ["Elite Wars", "Fortress War", "Realm Invasion", "Void War"])
    event_date = st.date_input("Battle Date")
    
    uploaded_file = st.file_uploader("Choose a screenshot...", type=["png", "jpg", "jpeg"])
    
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Screenshot", use_column_width=True)
        
        if st.button("Run OCR & Process Non-Attendants"):
            with st.spinner("Extracting names from screenshot..."):
                # Run Tesseract OCR on the uploaded image
                extracted_text = pytesseract.image_to_string(image)
                
                st.subheader("📝 Extracted Text Preview:")
                st.text(extracted_text)
                
                st.success("Screenshot processed successfully! Ready to log to database.")

elif page == "Alliance Overview & Stats":
    st.header("📊 Alliance Attendance Dashboard")
    st.markdown("Review event turnout, participation rates, and historical trends.")
    
    # Quick metrics
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Roster Members", "98")
    col2.metric("Average Event Turnout", "71.4%")
    col3.metric("Tracked Events (October)", "7")
    
    st.subheader("Event Attendance Comparison")
    chart_data = pd.DataFrame({
        "Event": ["Elite Wars (10-04)", "Elite Wars (10-07)", "Fortress War", "Elite Wars (10-11 #1)", "Elite Wars (10-11 #2)", "Realm Invasion", "Elite Wars (10-18)"],
        "Turnout": [51, 75, 58, 57, 59, 76, 70]
    })
    st.bar_chart(chart_data.set_index("Event"))

elif page == "Master Roster":
    st.header("👥 RIP Master Roster")
    st.dataframe(roster_df, use_container_width=True)
