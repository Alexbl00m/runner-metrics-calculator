# --------------------- RACE TIME PREDICTOR ---------------------#
elif app_mode == "Race Time Predictor":
st.header("Race Time Predictor")

st.markdown("""
    This calculator predicts your race times across different distances based on a recent performance.
    Multiple prediction models are available, as different formulas work better for different runners.

    **Scientific Validation**: These prediction methods are based on established research in exercise physiology and have been validated in peer-reviewed studies.

    **References**:
    - Riegel, P. S. (1981). Athletic records and human endurance. *American Scientist, 69(3)*, 285-290.
    - Daniels, J., & Gilbert, J. (1979). *Oxygen power: Performance tables for distance runners*. Tempe, AZ: John Daniels.
    - Vickers, A. J. (2016). What makes a good predictor of marathon time? *British Journal of Sports Medicine, 50(13)*, 777.
    """)

# Create columns for input and output
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("Enter Your Recent Race Data")

    prediction_method = st.radio(
        "Prediction Method:",
        ["Riegel Formula", "Daniels/Gilbert VDOT", "Cameron Formula", "Multiple Models Comparison"]
    )

    recent_distance = st.selectbox(
        "Recent Race Distance:",
        ["1 Mile", "5K", "10K", "15K", "10 Mile", "Half Marathon", "30K", "Marathon", "Custom"]
    )

    if recent_distance == "Custom":
        custom_distance = st.number_input("Enter distance (kilometers):", min_value=1.0, max_value=100.0, value=5.0,
                                          step=0.1)
        recent_distance_km = custom_distance
    else:
        # Convert selected distance to kilometers
        distance_map = {
            "1 Mile": 1.60934,
            "5K": 5,
            "10K": 10,
            "15K": 15,
            "10 Mile": 16.0934,
            "Half Marathon": 21.0975,
            "30K": 30,
            "Marathon": 42.195
        }
        recent_distance_km = distance_map[recent_distance]

    # Race time input
    hours = st.number_input("Hours:", min_value=0, max_value=24, value=0)
    minutes = st.number_input("Minutes:", min_value=0, max_value=59, value=20)
    seconds = st.number_input("Seconds:", min_value=0, max_value=59, value=0)

    # Convert to total seconds
    recent_time_seconds = (hours * 3600) + (minutes * 60) + seconds

    # Target race distances
    st.subheader("Target Race Distances")

    target_distances = []

    distance_options = ["1 Mile", "5K", "10K", "15K", "10 Mile", "Half Marathon", "30K", "Marathon"]

    # Create checkboxes for common distances
    cols = st.columns(4)  # 4 columns for checkboxes

    selected_distances = {}
    for i, distance in enumerate(distance_options):
        with cols[i % 4]:
            selected_distances[distance] = st.checkbox(distance, value=True)

    # Add custom distance option
    st.markdown("---")
    custom_enabled = st.checkbox("Add Custom Distance")
    if custom_enabled:
        custom_target = st.number_input("Custom Distance (kilometers):", min_value=1.0, max_value=100.0, value=25.0,
                                        step=0.1)
        selected_distances["Custom"] = True
    else:
        custom_target = 0
        selected_distances["Custom"] = False

    # Filter selected distances
    target_distances = []
    for distance, selected in selected_distances.items():
        if selected:
            if distance == "Custom":
                target_distances.append(("Custom", custom_target))
            else:
                target_distances.append((distance, distance_map[distance]))

    # Remove the distance that matches the recent race
    target_distances = [d for d in target_distances if abs(d[1] - recent_distance_km) > 0.01]

# Calculate predictions when button is clicked
if st.button("Calculate Race Predictions"):
    with col2:
        st.subheader("Predicted Race Times")


        # Function to format time in HH:MM:SS
        def format_time(seconds):
            hours = int(seconds // 3600)
            minutes = int((seconds % 3600) // 60)
            secs = int(seconds % 60)

            if hours > 0:
                return f"{hours}:{minutes:02d}:{secs:02d}"
            else:
                return f"{minutes}:{secs:02d}"


        # Riegel formula
        def riegel_prediction(base_distance, base_time, target_distance, fatigue_factor=1.06):
            return base_time * (target_distance / base_distance) ** fatigue_factor


        # Cameron formula (variation of Riegel with adjusted fatigue factor)
        def cameron_prediction(base_distance, base_time, target_distance):
            # Cameron's formula adjusts the fatigue factor based on distance
            fatigue = 1.07 if base_distance <= 10 else 1.05
            return base_time * (target_distance / base_distance) ** fatigue


        # Daniels VDOT method
        def daniels_prediction(base_distance, base_time, target_distance):
            # Calculate velocity in meters per minute
            velocity = (base_distance * 1000) / (base_time / 60)

            # Calculate percent VO2 max for given race
            percent_vo2 = 0.8 + 0.1894393 * exp(-0.012778 * (base_time / 60)) + 0.2989558 * exp(
                -0.1932605 * (base_time / 60))

            # Calculate VO2 max
            vo2 = -4.60 + 0.182258 * velocity + 0.000104 * velocity * velocity

            # Calculate VDOT
            vdot = vo2 / percent_vo2

            # Predict time for target distance (in km)
            # Convert to meters
            target_distance_m = target_distance * 1000

            # Calculate percent VO2 max for target distance (estimated)
            # For this, we need to estimate the time first
            # Start with Riegel estimate
            estimated_time = riegel_prediction(base_distance, base_time, target_distance)

            # Iterate to refine the estimate
            for _ in range(3):  # 3 iterations should be enough
                percent_vo2_target = 0.8 + 0.1894393 * exp(-0.012778 * (estimated_time / 60)) + 0.2989558 * exp(
                    -0.1932605 * (estimated_time / 60))

                # Calculate required velocity
                vo2_target = vdot * percent_vo2_target

                # Convert VO2 to velocity (solving the formula: vo2 = -4.60 + 0.182258 * velocity + 0.000104 * velocity * velocity)
                # Quadratic formula: velocity = (-b ± sqrt(b^2 - 4ac))/2a where a=0.000104, b=0.182258, c=(-4.60-vo2_target)
                a = 0.000104
                b = 0.182258
                c = -4.60 - vo2_target

                # We want the positive solution
                velocity_target = (-b + (b ** 2 - 4 * a * c) ** 0.5) / (2 * a)

                # Calculate new estimated time
                estimated_time = (target_distance_m / velocity_target) * 60

            return estimated_time


        # Create results DataFrame
        predictions = []

        for distance_name, distance_km in target_distances:
            riegel_time = riegel_prediction(recent_distance_km, recent_time_seconds, distance_km)
            cameron_time = cameron_prediction(recent_distance_km, recent_time_seconds, distance_km)
            daniels_time = daniels_prediction(recent_distance_km, recent_time_seconds, distance_km)

            # Select which prediction to display based on method chosen
            if prediction_method == "Riegel Formula":
                display_time = riegel_time
                method_name = "Riegel"
            elif prediction_method == "Daniels/Gilbert VDOT":
                display_time = daniels_time
                method_name = "Daniels/VDOT"
            elif prediction_method == "Cameron Formula":
                display_time = cameron_time
                method_name = "Cameron"
            else:  # Multiple models
                predictions.append({
                    "Distance": distance_name,
                    "Riegel Formula": format_time(riegel_time),
                    "Daniels/VDOT": format_time(daniels_time),
                    "Cameron Formula": format_time(cameron_time)
                })
                continue

            # Add single method prediction
            predictions.append({
                "Distance": distance_name,
                "Predicted Time": format_time(display_time),
                "Method": method_name
            })

        # Display the predictions
        if prediction_method == "Multiple Models Comparison":
            # Display multi-model comparison
            multi_df = pd.DataFrame(predictions)
            st.markdown("<div class='result-box'>", unsafe_allow_html=True)
            st.table(multi_df)
            st.markdown("</div>", unsafe_allow_html=True)

            st.info("""
                **Model Differences:**
                - **Riegel Formula** tends to be most accurate for similar distances to your base race.
                - **Daniels/VDOT** often provides better predictions for very different distances.
                - **Cameron Formula** adjusts the fatigue factor based on race distance, which can be more accurate for longer races.
                """)
        else:
            # Display single model prediction
            pred_df = pd.DataFrame(predictions)
            st.markdown("<div class='result-box'>", unsafe_allow_html=True)
            st.table(pred_df)
            st.markdown("</div>", unsafe_allow_html=True)

        # Create a pace comparison chart
        st.subheader("Pace Comparison")

        pace_data = []

        # Calculate base race pace
        base_pace_min_km = recent_time_seconds / (recent_distance_km * 60)
        base_pace_min_mile = recent_time_seconds / (recent_distance_km / 1.60934 * 60)

        pace_data.append({
            "Distance": f"{recent_distance} (Base)",
            "Min/Km": f"{int(base_pace_min_km)}:{int((base_pace_min_km % 1) * 60):02d}",
            "Min/Mile": f"{int(base_pace_min_mile)}:{int((base_pace_min_mile % 1) * 60):02d}",
            "Pace Change": "0%"
        })

        # Calculate target race paces
        for distance_name, distance_km in target_distances:
            if prediction_method == "Riegel Formula":
                pred_time = riegel_prediction(recent_distance_km, recent_time_seconds, distance_km)
            elif prediction_method == "Daniels/Gilbert VDOT":
                pred_time = daniels_prediction(recent_distance_km, recent_time_seconds, distance_km)
            elif prediction_method == "Cameron Formula":
                pred_time = cameron_prediction(recent_distance_km, recent_time_seconds, distance_km)
            else:  # Multiple models - use average
                riegel_time = riegel_prediction(recent_distance_km, recent_time_seconds, distance_km)
                cameron_time = cameron_prediction(recent_distance_km, recent_time_seconds, distance_km)
                daniels_time = daniels_prediction(recent_distance_km, recent_time_seconds, distance_km)
                pred_time = (riegel_time + cameron_time + daniels_time) / 3

            # Calculate pace
            pred_pace_min_km = pred_time / (distance_km * 60)
            pred_pace_min_mile = pred_time / (distance_km / 1.60934 * 60)

            # Calculate pace change percentage
            pace_change = ((pred_pace_min_km / base_pace_min_km) - 1) * 100

            pace_data.append({
                "Distance": distance_name,
                "Min/Km": f"{int(pred_pace_min_km)}:{int((pred_pace_min_km % 1) * 60):02d}",
                "Min/Mile": f"{int(pred_pace_min_mile)}:{int((pred_pace_min_mile % 1) * 60):02d}",
                "Pace Change": f"{pace_change:+.1f}%"
            })

        # Display pace comparison table
        pace_df = pd.DataFrame(pace_data)
        st.table(pace_df)

        # Create a visualization of the pace differences
        fig = go.Figure()

        # Extract pace values for visualization (convert MM:SS to seconds)
        distances = [item["Distance"] for item in pace_data]
        paces_km = []

        for item in pace_data:
            pace_str = item["Min/Km"]
            minutes, seconds = map(int, pace_str.split(':'))
            paces_km.append(minutes * 60 + seconds)

        # Add bar chart for paces
        fig.add_trace(go.Bar(
            x=distances,
            y=paces_km,
            marker_color=['#E6754E' if "Base" in d else '#4E97E6' for d in distances],
            text=[item["Min/Km"] for item in pace_data],
            textposition='auto'
        ))

        fig.update_layout(
            title='Race Pace Comparison',
            xaxis_title='Race Distance',
            yaxis_title='Pace (seconds per km)',
            height=400
        )

        st.plotly_chart(fig)

        # Training pace recommendations
        st.subheader("Training Pace Recommendations")

        # Calculate training paces based on recent performance
        # Calculate VDOT first
        base_velocity = (recent_distance_km * 1000) / (recent_time_seconds / 60)
        percent_vo2 = 0.8 + 0.1894393 * exp(-0.012778 * (recent_time_seconds / 60)) + 0.2989558 * exp(
            -0.1932605 * (recent_time_seconds / 60))
        vo2 = -4.60 + 0.182258 * base_velocity + 0.000104 * base_velocity * base_velocity
        vdot = vo2 / percent_vo2

        # Calculate training paces
        easy_pace = format_time((1000 / 60) * (150 * (vdot ** -0.75)))  # seconds per km
        marathon_pace = format_time((1000 / 60) * (120 * (vdot ** -0.73)))
        threshold_pace = format_time((1000 / 60) * (100 * (vdot ** -0.71)))
        interval_pace = format_time((1000 / 60) * (77 * (vdot ** -0.67)))
        repetition_pace = format_time((1000 / 60) * (64 * (vdot ** -0.65)))

        st.markdown(f"""
            Based on your recent {recent_distance} performance, here are recommended training paces:

            - **Easy/Recovery Runs**: {easy_pace} min/km
            - **Marathon Pace**: {marathon_pace} min/km
            - **Threshold/Tempo Runs**: {threshold_pace} min/km
            - **Interval Training (VO2max)**: {interval_pace} min/km
            - **Repetition/Speed Work**: {repetition_pace} min/km

            These paces are designed to target specific physiological adaptations in your training.
            """)

        # Race strategy tips
        st.subheader("Race Strategy Tips")

        # Different tips based on selected target races
        target_names = [d[0] for d in target_distances]

        if "Marathon" in target_names:
            st.markdown("""
                **Marathon Strategy:**

                - **Pacing**: Start slightly slower than goal pace (5-10 seconds/mile) for the first 2-3 miles
                - **Fueling**: Consume 30-60g of carbohydrates per hour starting around mile 5
                - **Hydration**: Drink to thirst at every aid station (typically 4-6 oz)
                - **Race Execution**: Aim for even or slightly negative splits (running the second half at the same pace or slightly faster than the first half)

                **Pre-race**: Carbohydrate loading for 2-3 days before, with emphasis on the day before the race.
                """)

        if "Half Marathon" in target_names:
            st.markdown("""
                **Half Marathon Strategy:**

                - **Pacing**: Even effort throughout, with potential to pick up pace in the final 5K if feeling strong
                - **Fueling**: 30-45g of carbohydrates during the race (typically 1-2 gels or equivalent)
                - **Hydration**: Water or sports drink every 15-20 minutes
                - **Race Execution**: The first 5K should feel comfortable; the middle 10K steady and focused; final 5K increasing effort
                """)

        if "10K" in target_names or "5K" in target_names:
            st.markdown("""
                **5K/10K Strategy:**

                - **Pacing**: Slight negative split recommended (run the second half 1-2% faster than the first half)
                - **Start**: Don't go out too fast in the first kilometer - a common mistake
                - **Middle**: Maintain effort when it starts to get uncomfortable
                - **Finish**: Begin your finishing kick with 1K (5K) or 2K (10K) remaining

                **Mental approach**: Break the race into segments and focus on running each segment well.
                """)