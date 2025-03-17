import streamlit as st
from modules import welcome, pace_calculator, metrics_analyzer

# Set up Streamlit configuration - must be the first Streamlit command
st.set_page_config(
    page_title="Runner Metrics Calculator",
    page_icon="🏃‍♂️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@300;400;500;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Montserrat', sans-serif;
}

.main {
    background-color: #FFFFFF;
}

h1, h2, h3, h4, h5, h6 {
    font-family: 'Montserrat', sans-serif;
    font-weight: 600;
    color: #E6754E;
}

.stButton>button {
    background-color: #E6754E;
    color: white;
    font-family: 'Montserrat', sans-serif;
    border: none;
    border-radius: 4px;
    padding: 8px 16px;
}

.stButton>button:hover {
    background-color: #c45d3a;
}

.highlight {
    color: #E6754E;
    font-weight: 600;
}

.result-box {
    background-color: #f8f8f8;
    padding: 20px;
    border-radius: 10px;
    border-left: 5px solid #E6754E;
}

footer {
    font-family: 'Montserrat', sans-serif;
    font-size: 12px;
    color: #888888;
    text-align: center;
    margin-top: 50px;
}
</style>
""", unsafe_allow_html=True)

# Sidebar navigation
st.sidebar.title("Runner Metrics Calculator")

page = st.sidebar.radio(
    "Navigation",
    ["Welcome", "Pace Calculator", "Metrics Analyzer", "About"]
)

# Display the selected page
if page == "Welcome":
    welcome.show_welcome()
elif page == "Pace Calculator":
    pace_calculator.show_pace_calculator()
elif page == "Metrics Analyzer":
    metrics_analyzer.show_metrics_analyzer()
elif page == "About":
    welcome.show_about()

# Footer
st.markdown("""
<footer>
© 2025 Runner Metrics Calculator | Developed with ❤️ for runners everywhere
</footer>
""", unsafe_allow_html=True)