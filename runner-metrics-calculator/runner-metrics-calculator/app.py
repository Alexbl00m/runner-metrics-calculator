import streamlit as st

# Import all modules
from modules import welcome
from modules import vo2max_calculator
from modules import training_zones
from modules import race_time_predictor
from modules import running_economy
from modules import vdot_calculator
from modules import running_power
from modules import heart_rate_reserve
from modules import training_load
from modules import running_form

# Set page configuration
st.set_page_config(
    page_title="Runner Performance Metrics Calculator",
    page_icon="🏃",
    layout="wide"
)

# Load custom CSS styles
with open("assets/styles.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Display logo and title
col1, col2 = st.columns([1, 5])
with col1:
    st.image("https://via.placeholder.com/100", width=80)  # Replace with your logo
with col2:
    st.title("Runner Performance Metrics Calculator")
    st.markdown("<p>Science-based metrics to enhance your running performance</p>", unsafe_allow_html=True)

# Create sidebar for navigation
st.sidebar.title("Navigation")
app_mode = st.sidebar.selectbox("Choose a calculator:",
    ["Welcome", "VO2 Max Calculator", "Training Zones", "Race Time Predictor",
     "Running Economy", "VDOT Calculator", "Running Power", "Heart Rate Reserve",
     "Training Load & Recovery", "Running Form Analysis"])

# User profile for personalized recommendations
st.sidebar.markdown("---")
st.sidebar.subheader("Runner Profile")
experience_level = st.sidebar.select_slider(
    "Experience Level:",
    options=["Beginner", "Intermediate", "Advanced", "Elite"],
    value="Intermediate"
)
training_frequency = st.sidebar.select_slider(
    "Training Frequency (days/week):",
    options=["1-2", "3-4", "5-6", "7+"],
    value="3-4"
)
primary_goal = st.sidebar.selectbox(
    "Primary Goal:",
    ["General Fitness", "Weight Management", "5K", "10K", "Half Marathon", "Marathon", "Ultra"]
)

st.sidebar.markdown("---")
st.sidebar.markdown("<footer>© 2025 Runner Performance Metrics Calculator. All metrics based on validated scientific research.</footer>", unsafe_allow_html=True)

# Store user profile in session state for module access
if 'user_profile' not in st.session_state:
    st.session_state.user_profile = {
        'experience_level': experience_level,
        'training_frequency': training_frequency,
        'primary_goal': primary_goal
    }
else:
    st.session_state.user_profile = {
        'experience_level': experience_level,
        'training_frequency': training_frequency,
        'primary_goal': primary_goal
    }

# Render the selected module
if app_mode == "Welcome":
    welcome.render()
elif app_mode == "VO2 Max Calculator":
    vo2max_calculator.render()
elif app_mode == "Training Zones":
    training_zones.render()
elif app_mode == "Race Time Predictor":
    race_time_predictor.render()
elif app_mode == "Running Economy":
    running_economy.render()
elif app_mode == "VDOT Calculator":
    vdot_calculator.render()
elif app_mode == "Running Power":
    running_power.render()
elif app_mode == "Heart Rate Reserve":
    heart_rate_reserve.render()
elif app_mode == "Training Load & Recovery":
    training_load.render()
elif app_mode == "Running Form Analysis":
    running_form.render()

# Footer with information
st.markdown("---")
st.markdown("""
<footer>
    <p>Runner Performance Metrics Calculator - Version 1.0</p>
    <p>© 2025 - All metrics based on validated scientific research in exercise physiology and biomechanics</p>
    <p>Created with Streamlit and Python</p>
</footer>
""", unsafe_allow_html=True)