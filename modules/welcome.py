import streamlit as st

def show_welcome():
    """
    Display the welcome page for the Runner Metrics Calculator app.
    """
    st.title("Runner Metrics Calculator")
    
    st.markdown("""
    <div class="result-box">
    Welcome to the Runner Metrics Calculator - your go-to tool for analyzing your running performance!
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### What can you do here?")
    
    st.markdown("""
    - **Calculate Pace**: Convert between different pace metrics (min/km, min/mile, km/h, mph)
    - **Analyze Performance**: Upload your running data and get detailed analytics
    - **Race Predictions**: Predict your finish time for different race distances
    - **Training Zones**: Calculate your heart rate training zones
    """)
    
    st.markdown("### How to use")
    st.markdown("Navigate through the different sections using the sidebar menu to access the various calculators and tools.")
    
    st.image("https://via.placeholder.com/600x300?text=Runner+Metrics+Calculator", 
             caption="Track your progress and improve your performance!")

def show_about():
    """
    Display the about page with information about the application.
    """
    st.title("About Runner Metrics Calculator")
    
    st.markdown("""
    <div class="result-box">
    The Runner Metrics Calculator was created to help runners of all levels track, analyze, 
    and improve their performance through data-driven insights.
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### Features")
    st.markdown("""
    - Easy pace calculations and conversions
    - Performance analysis based on your running data
    - Race time predictions using various models
    - Heart rate zone calculations
    - Running efficiency metrics
    """)
    
    st.markdown("### Contact")
    st.markdown("For support or feedback, please reach out to us at support@runnermetrics.com")