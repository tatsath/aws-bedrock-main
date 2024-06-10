import streamlit as st

## author: Yuxuan Zeng
## contact: yuxuanzeng220@gmail.com

# # Set the Streamlit layout to wide
# st.set_page_config(layout="wide") 

# Page configuration
st.set_page_config(
    page_title="compliease",
    page_icon="🤓 ",
    layout="wide",
    # initial_sidebar_state="expanded"
    )

# Load CSS
with open('style.css') as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Page header
st.markdown(
    """
    <div style=' top: 0;  left: 0; width: 100%; height: 110px; background-color: lightBlue; padding: 10px; text-align: center;'>
        <p></p>
        <h2 style='color: white; font-size: 3em; font-family: italic;'>CompliEase</h2>
        <p></p>
    </div>
    """,
    unsafe_allow_html=True
)



# Tabs
tabs = st.tabs([" 🔍 CompliCheck", " 🤖 Complibot ", " 🔄 ReguSync ", " 📰 ComplianceBrief ", " ℹ️ About ", " ❓ Help "])

# Import tab content
import tabs.complicheck as complicheck
import tabs.complibot as complibot
import tabs.regusync as regusync
import tabs.compliancebrief as compliancebrief
import tabs.about as about
import tabs.help as help

# Tab content
with tabs[0]:
    complicheck.display()

with tabs[1]:
    complibot.display()

with tabs[2]:
    regusync.display()

with tabs[3]:
    compliancebrief.display()

with tabs[4]:
    about.display()

with tabs[5]:
    help.display()

# Page footer
st.markdown(
    """
    <div style='position: fixed; bottom: 0; left: 0; width: 100%; background-color: lightBlue;  padding: 0px; text-align: left;'>
        <p style='color: white; font-size: 1em;'>&copy; 2024 Hackathon Team LLM</p>
    </div>
    """,
    unsafe_allow_html=True
)
