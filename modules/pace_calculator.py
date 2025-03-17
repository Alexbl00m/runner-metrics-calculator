import streamlit as st
import pandas as pd
import numpy as np

def show_pace_calculator():
    """
    Display the pace calculator interface
    """
    st.title("Pace Calculator")
    
    st.markdown("""
    <div class="result-box">
    Convert between different pace metrics and calculate finish times for various distances.
    </div>
    """, unsafe_allow_html=True)
    
    # Create tabs for different calculators
    tab1, tab2, tab3 = st.tabs(["Pace Converter", "Race Time Predictor", "Split Calculator"])
    
    with tab1:
        show_pace_converter()
    
    with tab2:
        show_race_predictor()
    
    with tab3:
        show_split_calculator()

def show_pace_converter():
    """
    Display the pace converter calculator
    """
    st.header("Pace Converter")
    
    # Input method selection
    input_method = st.radio("Select input type:", 
                           ["Pace (min/km or min/mile)", "Speed (km/h or mph)"])
    
    if input_method == "Pace (min/km or min/mile)":
        col1, col2 = st.columns(2)
        
        with col1:
            pace_unit = st.selectbox("Pace unit:", ["min/km", "min/mile"])
            
            if pace_unit == "min/km":
                minutes = st.number_input("Minutes:", min_value=0, max_value=59, value=5)
                seconds = st.number_input("Seconds:", min_value=0, max_value=59, value=30)
                
                # Calculate pace in min/km
                pace_min_km = minutes + seconds/60
                pace_min_mile = pace_min_km * 1.60934
                speed_kmh = 60 / pace_min_km
                speed_mph = 60 / pace_min_mile
                
            else:  # min/mile
                minutes = st.number_input("Minutes:", min_value=0, max_value=59, value=8)
                seconds = st.number_input("Seconds:", min_value=0, max_value=59, value=45)
                
                # Calculate pace in min/mile
                pace_min_mile = minutes + seconds/60
                pace_min_km = pace_min_mile / 1.60934
                speed_mph = 60 / pace_min_mile
                speed_kmh = 60 / pace_min_km
    
    else:  # Speed input
        col1, col2 = st.columns(2)
        
        with col1:
            speed_unit = st.selectbox("Speed unit:", ["km/h", "mph"])
            
            if speed_unit == "km/h":
                speed = st.number_input("Speed:", min_value=0.1, max_value=50.0, value=10.5, step=0.1)
                
                # Calculate speeds
                speed_kmh = speed
                speed_mph = speed / 1.60934
                pace_min_km = 60 / speed
                pace_min_mile = 60 / speed_mph
                
            else:  # mph
                speed = st.number_input("Speed:", min_value=0.1, max_value=30.0, value=6.5, step=0.1)
                
                # Calculate speeds
                speed_mph = speed
                speed_kmh = speed * 1.60934
                pace_min_mile = 60 / speed
                pace_min_km = 60 / speed_kmh
    
    # Display results
    st.markdown("### Results")
    st.markdown("<div class='result-box'>", unsafe_allow_html=True)
    
    # Format pace values
    pace_min_km_formatted = f"{int(pace_min_km)}:{int((pace_min_km % 1) * 60):02d} min/km"
    pace_min_mile_formatted = f"{int(pace_min_mile)}:{int((pace_min_mile % 1) * 60):02d} min/mile"
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Pace (min/km)", pace_min_km_formatted)
        st.metric("Speed (km/h)", f"{speed_kmh:.2f} km/h")
    
    with col2:
        st.metric("Pace (min/mile)", pace_min_mile_formatted)
        st.metric("Speed (mph)", f"{speed_mph:.2f} mph")
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Show equivalent race times
    st.markdown("### Equivalent Race Times")
    distances = {
        "5K": 5,
        "10K": 10,
        "Half Marathon": 21.0975,
        "Marathon": 42.195
    }
    
    race_times = {}
    for race, distance in distances.items():
        time_hours = (pace_min_km * distance) / 60
        hours = int(time_hours)
        minutes = int((time_hours % 1) * 60)
        seconds = int(((time_hours % 1) * 60 % 1) * 60)
        
        race_times[race] = f"{hours}h {minutes}m {seconds}s" if hours > 0 else f"{minutes}m {seconds}s"
    
    st.dataframe(pd.DataFrame(list(race_times.items()), columns=["Race", "Estimated Time"]))

def show_race_predictor():
    """
    Display the race time predictor
    """
    st.header("Race Time Predictor")
    
    st.markdown("Use a previous race result to predict times for other distances.")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Previous race information
        race_type = st.selectbox("Previous race:", ["5K", "10K", "Half Marathon", "Marathon", "Custom"])
        
        if race_type == "Custom":
            distance = st.number_input("Distance (km):", min_value=0.1, max_value=100.0, value=5.0, step=0.1)
        else:
            distance_map = {"5K": 5, "10K": 10, "Half Marathon": 21.0975, "Marathon": 42.195}
            distance = distance_map[race_type]
        
        hours = st.number_input("Hours:", min_value=0, max_value=24, value=0)
        minutes = st.number_input("Minutes:", min_value=0, max_value=59, value=25)
        seconds = st.number_input("Seconds:", min_value=0, max_value=59, value=0)
        
        # Calculate total time in minutes
        total_time_min = hours * 60 + minutes + seconds / 60
        
        # Calculate pace
        pace_min_km = total_time_min / distance
        
        # Model selection
        prediction_model = st.selectbox("Prediction model:", 
                                       ["Riegel (standard)", "Cameron", "Purdy", "Daniels"])
        
        # Different models use different exponents
        exponents = {
            "Riegel (standard)": 1.06,
            "Cameron": 1.08,
            "Purdy": 1.07,
            "Daniels": 1.05
        }
        
        selected_exponent = exponents[prediction_model]
    
    # Display predictions
    st.markdown("### Predicted Race Times")
    
    # Common race distances
    target_distances = {
        "5K": 5,
        "10K": 10,
        "15K": 15,
        "10 Mile": 16.0934,
        "Half Marathon": 21.0975,
        "30K": 30,
        "Marathon": 42.195,
        "50K": 50,
        "50 Mile": 80.4672,
        "100K": 100
    }
    
    # Calculate predicted times using the selected model
    predictions = {}
    for race, target_dist in target_distances.items():
        # Skip the original race distance
        if abs(target_dist - distance) < 0.01:
            predicted_time = total_time_min
        else:
            # Riegel formula: T2 = T1 * (D2/D1)^exponent
            predicted_time = total_time_min * (target_dist/distance)**selected_exponent
        
        # Convert time to h:m:s format
        pred_hours = int(predicted_time / 60)
        pred_minutes = int(predicted_time % 60)
        pred_seconds = int((predicted_time * 60) % 60)
        
        if pred_hours > 0:
            predictions[race] = f"{pred_hours}h {pred_minutes}m {pred_seconds}s"
        else:
            predictions[race] = f"{pred_minutes}m {pred_seconds}s"
    
    # Create a dataframe for display
    predictions_df = pd.DataFrame(list(predictions.items()), columns=["Race", "Predicted Time"])
    
    st.dataframe(predictions_df)
    
    st.markdown("""
    **Note**: Predictions are most accurate for distances similar to your previous race.
    Longer distance predictions may not account for factors like fatigue and pacing strategy.
    """)

def show_split_calculator():
    """
    Display the split calculator
    """
    st.header("Split Calculator")
    
    st.markdown("Calculate even or negative splits for your race")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Race information
        race_type = st.selectbox("Race distance:", ["5K", "10K", "Half Marathon", "Marathon", "Custom"], key="split_race")
        
        if race_type == "Custom":
            distance = st.number_input("Distance (km):", min_value=0.1, max_value=100.0, value=5.0, step=0.1, key="split_distance")
        else:
            distance_map = {"5K": 5, "10K": 10, "Half Marathon": 21.0975, "Marathon": 42.195}
            distance = distance_map[race_type]
        
        # Target time
        hours = st.number_input("Target Hours:", min_value=0, max_value=24, value=0, key="split_hours")
        minutes = st.number_input("Target Minutes:", min_value=0, max_value=59, value=25, key="split_minutes")
        seconds = st.number_input("Target Seconds:", min_value=0, max_value=59, value=0, key="split_seconds")
        
        # Calculate total time in minutes
        total_time_min = hours * 60 + minutes + seconds / 60
        
        # Split type
        split_type = st.selectbox("Split type:", ["Even splits", "Negative splits (5% faster at end)", 
                                                "Negative splits (10% faster at end)", "Custom progression"])
        
        if split_type == "Custom progression":
            start_percent = st.slider("Starting pace (% slower than average):", 
                                     min_value=0, max_value=20, value=5)
            end_percent = st.slider("Finishing pace (% faster than average):", 
                                   min_value=0, max_value=20, value=5)
        
        # Number of splits
        num_splits = st.number_input("Number of splits:", min_value=1, max_value=50, value=5)
    
    # Calculate splits
    split_distance = distance / num_splits
    
    if split_type == "Even splits":
        # All splits are the same
        split_times = [total_time_min / num_splits] * num_splits
    elif split_type == "Negative splits (5% faster at end)":
        # Linear progression from 2.5% slower to 2.5% faster
        progression = np.linspace(1.025, 0.975, num_splits)
        avg_split_time = total_time_min / num_splits
        split_times = [avg_split_time * factor for factor in progression]
    elif split_type == "Negative splits (10% faster at end)":
        # Linear progression from 5% slower to 5% faster
        progression = np.linspace(1.05, 0.95, num_splits)
        avg_split_time = total_time_min / num_splits
        split_times = [avg_split_time * factor for factor in progression]
    else:  # Custom progression
        # Linear progression from specified start to end percentages
        start_factor = 1 + (start_percent / 100)
        end_factor = 1 - (end_percent / 100)
        progression = np.linspace(start_factor, end_factor, num_splits)
        avg_split_time = total_time_min / num_splits
        split_times = [avg_split_time * factor for factor in progression]
    
    # Create splits dataframe
    splits_data = []
    cumulative_time = 0
    cumulative_distance = 0
    
    for i in range(num_splits):
        split_time_min = split_times[i]
        cumulative_time += split_time_min
        cumulative_distance += split_distance
        
        # Format times
        split_time_formatted = f"{int(split_time_min)}:{int((split_time_min % 1) * 60):02d}"
        cumulative_time_formatted = f"{int(cumulative_time/60)}:{int(cumulative_time%60):02d}:{int((cumulative_time*60)%60):02d}" if cumulative_time >= 60 else f"{int(cumulative_time)}:{int((cumulative_time % 1) * 60):02d}"
        
        # Calculate pace
        pace_min_km = split_time_min / split_distance
        pace_formatted = f"{int(pace_min_km)}:{int((pace_min_km % 1) * 60):02d}"
        
        splits_data.append({
            "Split": i+1,
            "Distance": f"{cumulative_distance:.2f} km",
            "Split Time": split_time_formatted,
            "Cumulative Time": cumulative_time_formatted,
            "Pace (min/km)": pace_formatted
        })
    
    # Display splits
    st.markdown("### Your Race Splits")
    splits_df = pd.DataFrame(splits_data)
    st.dataframe(splits_df)
    
    # Download link for splits
    csv = splits_df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="Download Splits as CSV",
        data=csv,
        file_name=f"{race_type}_splits.csv",
        mime="text/csv",
    )