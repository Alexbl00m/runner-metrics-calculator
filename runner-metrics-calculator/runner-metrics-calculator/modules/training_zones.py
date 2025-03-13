# --------------------- TRAINING ZONES ---------------------#
elif app_mode == "Training Zones":
st.header("Training Zones Calculator")

st.markdown("""
    Training zones help structure your workouts based on specific intensity levels. 
    These zones can be calculated using heart rate, pace, or power, and each zone targets different physiological adaptations.

    This calculator provides zones based on several established methods in exercise science.
    """)

# Create tabs for different zone calculation methods
zones_tabs = st.tabs(["Heart Rate Zones", "Pace Zones", "Power Zones"])

with zones_tabs[0]:
    st.subheader("Heart Rate Zones")

    zone_method = st.radio(
        "Heart Rate Zone Method:",
        ["% of Max HR", "Karvonen (Heart Rate Reserve)", "Lactate Threshold", "5-Zone System"]
    )

    col1, col2 = st.columns(2)

    with col1:
        if zone_method == "% of Max HR" or zone_method == "5-Zone System":
            max_hr = st.number_input("Maximum Heart Rate (bpm):", min_value=120, max_value=220, value=180)
            st.info(
                "If you don't know your maximum heart rate, you can estimate it as 220 - your age, though this formula can be inaccurate for some individuals.")

        if zone_method == "Karvonen (Heart Rate Reserve)":
            max_hr = st.number_input("Maximum Heart Rate (bpm):", min_value=120, max_value=220, value=180)
            resting_hr = st.number_input("Resting Heart Rate (bpm):", min_value=35, max_value=100, value=60)

        if zone_method == "Lactate Threshold":
            lthr = st.number_input("Lactate Threshold Heart Rate (bpm):", min_value=100, max_value=200, value=160)
            st.info(
                "Lactate threshold heart rate can be estimated from a 30-60 minute time trial, taking your average heart rate from the last 20 minutes.")

    with col2:
        st.markdown("""
            ### Zone Benefits

            **Zone 1 (Recovery)**: Enhances recovery, improves fat metabolism

            **Zone 2 (Aerobic)**: Builds aerobic endurance, improves fat utilization

            **Zone 3 (Tempo)**: Improves lactate clearance, aerobic capacity

            **Zone 4 (Threshold)**: Increases lactate threshold, VO2 max

            **Zone 5 (Anaerobic)**: Develops maximum power, speed, and anaerobic capacity
            """)

        st.markdown("""
            **Scientific Validation**: Heart rate zone training has been validated in numerous studies and is widely used in exercise physiology and endurance training.

            **Reference**: Seiler, S., & Tønnessen, E. (2009). Intervals, thresholds, and long slow distance: the role of intensity and duration in endurance training. *Sportscience, 13*, 32-53.
            """)

    if st.button("Calculate Heart Rate Zones"):
        if zone_method == "% of Max HR":
            # Calculate zones based on % of Max HR
            zones = {
                "Zone 1 (Recovery)": f"{int(max_hr * 0.5)} - {int(max_hr * 0.6)} bpm",
                "Zone 2 (Aerobic)": f"{int(max_hr * 0.6 + 1)} - {int(max_hr * 0.7)} bpm",
                "Zone 3 (Tempo)": f"{int(max_hr * 0.7 + 1)} - {int(max_hr * 0.8)} bpm",
                "Zone 4 (Threshold)": f"{int(max_hr * 0.8 + 1)} - {int(max_hr * 0.9)} bpm",
                "Zone 5 (Anaerobic)": f"{int(max_hr * 0.9 + 1)} - {int(max_hr)} bpm"
            }

        elif zone_method == "Karvonen (Heart Rate Reserve)":
            # Calculate Heart Rate Reserve (HRR)
            hrr = max_hr - resting_hr

            # Calculate zones based on HRR (Karvonen method)
            zones = {
                "Zone 1 (Recovery)": f"{int(resting_hr + (hrr * 0.5))} - {int(resting_hr + (hrr * 0.6))} bpm",
                "Zone 2 (Aerobic)": f"{int(resting_hr + (hrr * 0.6) + 1)} - {int(resting_hr + (hrr * 0.7))} bpm",
                "Zone 3 (Tempo)": f"{int(resting_hr + (hrr * 0.7) + 1)} - {int(resting_hr + (hrr * 0.8))} bpm",
                "Zone 4 (Threshold)": f"{int(resting_hr + (hrr * 0.8) + 1)} - {int(resting_hr + (hrr * 0.9))} bpm",
                "Zone 5 (Anaerobic)": f"{int(resting_hr + (hrr * 0.9) + 1)} - {int(max_hr)} bpm"
            }

        elif zone_method == "Lactate Threshold":
            # Calculate zones based on LTHR (Lactate Threshold Heart Rate)
            zones = {
                "Zone 1 (Recovery)": f"< {int(lthr * 0.85)} bpm",
                "Zone 2 (Aerobic)": f"{int(lthr * 0.85)} - {int(lthr * 0.89)} bpm",
                "Zone 3 (Tempo)": f"{int(lthr * 0.9)} - {int(lthr * 0.94)} bpm",
                "Zone 4 (Threshold)": f"{int(lthr * 0.95)} - {int(lthr * 0.99)} bpm",
                "Zone 5a (VO2 Intervals)": f"{int(lthr * 1.0)} - {int(lthr * 1.02)} bpm",
                "Zone 5b (Anaerobic)": f"{int(lthr * 1.03)} - {int(lthr * 1.06)} bpm",
                "Zone 5c (Neuromuscular)": f"> {int(lthr * 1.06)} bpm"
            }

        elif zone_method == "5-Zone System":
            # 5-Zone system (common in training platforms like TrainingPeaks)
            zones = {
                "Zone 1 (Active Recovery)": f"< {int(max_hr * 0.68)} bpm",
                "Zone 2 (Endurance)": f"{int(max_hr * 0.68)} - {int(max_hr * 0.83)} bpm",
                "Zone 3 (Tempo)": f"{int(max_hr * 0.84)} - {int(max_hr * 0.94)} bpm",
                "Zone 4 (Threshold)": f"{int(max_hr * 0.95)} - {int(max_hr * 1.0)} bpm",
                "Zone 5 (Anaerobic)": f"> {int(max_hr * 1.0)} bpm"
            }

        # Display results
        st.markdown("<div class='result-box'>", unsafe_allow_html=True)
        st.subheader(f"Your Heart Rate Training Zones ({zone_method})")

        # Create a DataFrame for better visualization
        zones_df = pd.DataFrame(list(zones.items()), columns=['Zone', 'Heart Rate Range'])
        st.table(zones_df)

        # Create a horizontal bar chart visualization of the zones
        zone_names = list(zones.keys())

        # Extract the lower and upper bounds from the ranges
        lower_bounds = []
        upper_bounds = []

        for zone_range in zones.values():
            if "<" in zone_range:
                # For ranges like "< 120 bpm"
                lower_bounds.append(0)
                upper_bounds.append(int(zone_range.split("<")[1].split(" ")[1]))
            elif ">" in zone_range:
                # For ranges like "> 180 bpm"
                if zone_method == "5-Zone System" and "Zone 5" in zone_range:
                    lower_bounds.append(int(zone_range.split(">")[1].split(" ")[1]))
                    upper_bounds.append(max_hr + 5)  # Add a small buffer for visualization
                else:
                    lower_bounds.append(int(zone_range.split(">")[1].split(" ")[1]))
                    upper_bounds.append(int(zone_range.split(">")[1].split(" ")[1]) + 10)  # Add a small buffer
            else:
                # For ranges like "120 - 140 bpm"
                range_parts = zone_range.split(" - ")
                lower_bounds.append(int(range_parts[0]))
                upper_bounds.append(int(range_parts[1].split(" ")[0]))

        # Create a DataFrame for the chart
        chart_data = pd.DataFrame({
            'Zone': zone_names,
            'Lower': lower_bounds,
            'Upper': upper_bounds,
            'Range': [upper - lower for upper, lower in zip(upper_bounds, lower_bounds)]
        })

        # Create a horizontal bar chart
        fig = px.bar(
            chart_data,
            y='Zone',
            x='Range',
            base='Lower',
            color='Zone',
            orientation='h',
            color_discrete_sequence=px.colors.sequential.Oranges_r,
            labels={'Range': 'Heart Rate (bpm)', 'Zone': ''},
            title='Heart Rate Zones Visualization'
        )

        # Add custom styling
        fig.update_layout(
            xaxis_title="Heart Rate (bpm)",
            showlegend=False,
            height=400,
            margin=dict(l=0, r=0, t=50, b=0)
        )

        st.plotly_chart(fig)

        # Add training recommendations based on zones
        st.markdown("</div>", unsafe_allow_html=True)
        st.subheader("Training Recommendations")
        st.markdown("""
            **Zone 1 (Recovery)**: Use for warm-up, cool-down, and recovery days. Should feel very easy, with no breathing discomfort.

            **Zone 2 (Aerobic/Endurance)**: The foundation of endurance training. Aim for 70-80% of weekly training volume in this zone. Conversational effort.

            **Zone 3 (Tempo)**: "Comfortably hard" effort. Useful for tempo runs and sustained efforts. Limited to 10-15% of weekly training volume.

            **Zone 4 (Threshold)**: Challenging effort at or near lactate threshold. Used for interval training to improve threshold. Limit to 5-10% of weekly volume.

            **Zone 5 (Anaerobic/VO2 Max)**: Very hard effort, used for short intervals to develop speed and power. Limit to 5% of weekly volume.
            """)

with zones_tabs[1]:
    st.subheader("Pace Zones")

    st.markdown("""
        Pace zones help structure your training based on running speeds for different workout types.
        These can be calculated based on a recent race time or time trial.

        **Scientific Validation**: Pace-based training zones have been validated in coaching and scientific literature, particularly through Jack Daniels' VDOT system and research on race equivalency.

        **Reference**: Daniels, J. (2013). *Daniels' running formula*. Human Kinetics.
        """)

    pace_method = st.radio(
        "Pace Zone Calculation Method:",
        ["Recent Race Time", "Time Trial", "Current VDOT"]
    )

    col1, col2 = st.columns(2)

    with col1:
        if pace_method == "Recent Race Time":
            race_distance = st.selectbox(
                "Race Distance:",
                ["5K", "10K", "Half Marathon", "Marathon"]
            )

            hours = st.number_input("Hours:", min_value=0, max_value=24, value=0)
            minutes = st.number_input("Minutes:", min_value=0, max_value=59, value=20 if race_distance == "5K" else 40)
            seconds = st.number_input("Seconds:", min_value=0, max_value=59, value=0)

        elif pace_method == "Time Trial":
            tt_distance = st.number_input("Time Trial Distance (meters):", min_value=1000, max_value=10000, value=3000,
                                          step=1000)

            tt_min = st.number_input("Minutes:", min_value=0, max_value=59, value=12)
            tt_sec = st.number_input("Seconds:", min_value=0, max_value=59, value=0)

        elif pace_method == "Current VDOT":
            vdot = st.number_input("Current VDOT value:", min_value=30.0, max_value=85.0, value=50.0, step=0.1)

    with col2:
        st.markdown("""
            ### Pace Zone Descriptions

            **Easy/Recovery**: Very comfortable pace for recovery runs and warm-ups

            **Endurance**: Aerobic development pace for long runs and base building

            **Marathon Pace**: Specific pace for marathon training and long tempo runs

            **Threshold**: "Comfortably hard" pace that improves lactate threshold

            **Interval**: VO2 max development pace for interval training

            **Repetition**: Speed development for shorter, faster repetitions
            """)

    if st.button("Calculate Pace Zones"):
        # Calculate VDOT first
        race_time_seconds = 0
        vdot_value = 0

        if pace_method == "Recent Race Time":
            race_time_seconds = (hours * 3600) + (minutes * 60) + seconds

            # Convert race distance to meters
            if race_distance == "5K":
                distance_m = 5000
            elif race_distance == "10K":
                distance_m = 10000
            elif race_distance == "Half Marathon":
                distance_m = 21097.5
            else:  # Marathon
                distance_m = 42195

            # Calculate velocity in meters per minute
            velocity = distance_m / (race_time_seconds / 60)

            # Calculate percent VO2 max for given race distance
            percent_vo2 = 0.8 + 0.1894393 * exp(-0.012778 * (race_time_seconds / 60)) + 0.2989558 * exp(
                -0.1932605 * (race_time_seconds / 60))

            # Calculate VO2 max
            vo2 = -4.60 + 0.182258 * velocity + 0.000104 * velocity * velocity

            # Calculate VDOT
            vdot_value = vo2 / percent_vo2

        elif pace_method == "Time Trial":
            race_time_seconds = (tt_min * 60) + tt_sec

            # Calculate velocity in meters per minute
            velocity = tt_distance / (race_time_seconds / 60)

            # Calculate percent VO2 max for given race distance
            percent_vo2 = 0.8 + 0.1894393 * exp(-0.012778 * (race_time_seconds / 60)) + 0.2989558 * exp(
                -0.1932605 * (race_time_seconds / 60))

            # Calculate VO2 max
            vo2 = -4.60 + 0.182258 * velocity + 0.000104 * velocity * velocity

            # Calculate VDOT
            vdot_value = vo2 / percent_vo2

        elif pace_method == "Current VDOT":
            vdot_value = vdot


        # Function to format pace (seconds) to min:sec format
        def format_pace(pace_seconds):
            minutes = int(pace_seconds // 60)
            seconds = int(pace_seconds % 60)
            return f"{minutes}:{seconds:02d}"


        # Calculate training paces based on VDOT value
        # These formulas are derived from Daniels' Running Formula

        # Easy pace (min/km)
        easy_pace_lower = (180 * (vdot_value ** -0.79)) * (60 / 1000)
        easy_pace_upper = (150 * (vdot_value ** -0.75)) * (60 / 1000)

        # Marathon pace (min/km)
        marathon_pace = (120 * (vdot_value ** -0.73)) * (60 / 1000)

        # Threshold pace (min/km)
        threshold_pace = (100 * (vdot_value ** -0.71)) * (60 / 1000)

        # Interval pace (min/km)
        interval_pace = (77 * (vdot_value ** -0.67)) * (60 / 1000)

        # Repetition pace (min/km)
        repetition_pace = (64 * (vdot_value ** -0.65)) * (60 / 1000)

        # Create a dictionary of pace zones
        pace_zones = {
            "Easy/Recovery": f"{format_pace(easy_pace_upper)} - {format_pace(easy_pace_lower)} min/km",
            "Endurance": f"{format_pace(easy_pace_lower)} - {format_pace((easy_pace_lower + marathon_pace) / 2)} min/km",
            "Marathon Pace": f"{format_pace(marathon_pace)} min/km",
            "Threshold": f"{format_pace(threshold_pace)} min/km",
            "Interval (VO2 max)": f"{format_pace(interval_pace)} min/km",
            "Repetition (Speed)": f"{format_pace(repetition_pace)} min/km"
        }

        # Display results
        st.markdown("<div class='result-box'>", unsafe_allow_html=True)
        st.subheader(f"Your Pace Training Zones (VDOT: {vdot_value:.1f})")

        # Create a DataFrame for better visualization
        pace_df = pd.DataFrame(list(pace_zones.items()), columns=['Zone', 'Pace (min/km)'])
        st.table(pace_df)

        # Add a pace conversion table (km to miles)
        st.subheader("Pace Conversion")

        conversion_data = {
            "Min/Km": [format_pace(easy_pace_upper), format_pace(easy_pace_lower),
                       format_pace(marathon_pace), format_pace(threshold_pace),
                       format_pace(interval_pace), format_pace(repetition_pace)],
            "Min/Mile": [format_pace(easy_pace_upper * 1.60934), format_pace(easy_pace_lower * 1.60934),
                         format_pace(marathon_pace * 1.60934), format_pace(threshold_pace * 1.60934),
                         format_pace(interval_pace * 1.60934), format_pace(repetition_pace * 1.60934)]
        }

        conversion_df = pd.DataFrame(conversion_data, index=["Easy (Upper)", "Easy (Lower)",
                                                             "Marathon", "Threshold",
                                                             "Interval", "Repetition"])
        st.dataframe(conversion_df)

        # Create a pace zones visualization
        pace_values = [
            easy_pace_upper,
            easy_pace_lower,
            (easy_pace_lower + marathon_pace) / 2,
            marathon_pace,
            threshold_pace,
            interval_pace,
            repetition_pace
        ]

        zone_labels = [
            "Recovery",
            "Easy",
            "Endurance",
            "Marathon",
            "Threshold",
            "Interval",
            "Repetition"
        ]

        fig = go.Figure()

        # Add lines for each pace boundary
        for i, pace in enumerate(pace_values):
            fig.add_trace(go.Scatter(
                x=[pace, pace],
                y=[0, 1],
                mode='lines',
                name=zone_labels[i],
                line=dict(color='rgba(230, 117, 78, 0.7)', width=2)
            ))

            # Add labels
            fig.add_annotation(
                x=pace,
                y=1.1,
                text=zone_labels[i],
                showarrow=False,
                font=dict(size=10)
            )

            # Add pace values
            fig.add_annotation(
                x=pace,
                y=-0.1,
                text=format_pace(pace),
                showarrow=False,
                font=dict(size=10)
            )

        fig.update_layout(
            title="Pace Zones Visualization",
            xaxis_title="Pace (min/km)",
            showlegend=False,
            height=300,
            margin=dict(l=0, r=0, t=50, b=50),
            xaxis=dict(
                range=[min(pace_values) - 10, max(pace_values) + 10],
                showticklabels=False
            ),
            yaxis=dict(
                range=[-0.2, 1.2],
                showticklabels=False,
                showgrid=False
            )
        )

        st.plotly_chart(fig)
        st.markdown("</div>", unsafe_allow_html=True)

        # Training recommendations
        st.subheader("Training Recommendations")
        st.markdown("""
            **Weekly Training Structure Based on Your VDOT:**

            1. **Easy/Recovery Runs (70-80% of volume)**
               - Keep these truly easy to aid recovery and build aerobic base
               - Example: 40-60 minute runs at easy pace

            2. **Threshold Workouts (10-15% of volume)**
               - Tempo runs: 20-40 minutes continuous at threshold pace
               - Cruise intervals: 5-10 minutes at threshold with 1-minute recovery
               - One session per week

            3. **VO2 Max/Interval Training (5-8% of volume)**
               - 3-5 minute intervals at interval pace with equal recovery
               - Total work time: 15-25 minutes
               - One session per week or every other week

            4. **Speed/Repetition Work (0-5% of volume)**
               - 200-400m repeats at repetition pace with full recovery
               - Include only if specifically training for shorter races

            5. **Long Runs (20-30% of weekly volume)**
               - At easy to endurance pace
               - Optional: Include some marathon pace segments for race-specific training
            """)

        # Race predictions based on VDOT
        st.subheader("Race Predictions Based on Current Fitness")

        # Calculate predicted race times based on VDOT
        # These formulas are approximations based on Daniels' tables

        # 5K prediction (seconds)
        time_5k = (5000 / 1000) * 60 * (29.87 * (vdot_value ** -0.29))

        # 10K prediction
        time_10k = (10000 / 1000) * 60 * (31.72 * (vdot_value ** -0.294))

        # Half marathon prediction
        time_half = (21097.5 / 1000) * 60 * (33.71 * (vdot_value ** -0.298))

        # Marathon prediction
        time_marathon = (42195 / 1000) * 60 * (35.66 * (vdot_value ** -0.3))


        # Format times
        def format_time(seconds):
            hours = int(seconds // 3600)
            minutes = int((seconds % 3600) // 60)
            secs = int(seconds % 60)

            if hours > 0:
                return f"{hours}:{minutes:02d}:{secs:02d}"
            else:
                return f"{minutes}:{secs:02d}"


        prediction_data = {
            "Distance": ["5K", "10K", "Half Marathon", "Marathon"],
            "Predicted Time": [
                format_time(time_5k),
                format_time(time_10k),
                format_time(time_half),
                format_time(time_marathon)
            ]
        }

        prediction_df = pd.DataFrame(prediction_data)
        st.table(prediction_df)

with zones_tabs[2]:
    st.subheader("Power Zones")

    st.markdown("""
        Running power is a relatively new metric that measures the actual work rate (in watts) while running.
        Unlike heart rate, power responds immediately to changes in effort and is not affected by factors like
        fatigue, temperature, or hydration status.

        **Scientific Validation**: While newer than heart rate or pace-based training, power has been validated in research studies as an effective training metric.

        **References**: 
        - Cerezuela-Espejo, V., Hernández-Belmonte, A., Courel-Ibáñez, J., Conesa-Ros, E., Mora-Rodriguez, R., & Pallarés, J. G. (2020). Running power meters and theoretical models based on laws of physics: A comparison study. *Scandinavian Journal of Medicine & Science in Sports, 30(11)*, 2113-2121.
        - Austin, C. L., Hokanson, J. F., McGinnis, P. M., & Patrick, S. (2018). The relationship between running power and running economy in well-trained distance runners. *Sports, 6(4)*, 142.
        """)

    st.info(
        "Note: Running power is typically measured using devices like Stryd, Garmin Running Power, or COROS running power.")

    power_method = st.radio(
        "Power Zone Calculation Method:",
        ["Critical Power (CP)", "Functional Threshold Power (FTP)", "Race Power"]
    )

    col1, col2 = st.columns(2)

    with col1:
        if power_method == "Critical Power (CP)":
            cp = st.number_input("Critical Power (watts):", min_value=100, max_value=500, value=280)

            st.info("""
                Critical Power can be estimated from a 30-minute time trial or through special test protocols.
                It represents the highest power you can maintain in a metabolic steady state.
                """)

        elif power_method == "Functional Threshold Power (FTP)":
            ftp = st.number_input("FTP (watts):", min_value=100, max_value=500, value=270)

            st.info("""
                FTP can be estimated from a 20-minute time trial (95% of average power) or a recent race.
                """)

        elif power_method == "Race Power":
            race_power = st.number_input("Recent Race Average Power (watts):", min_value=100, max_value=500, value=300)
            race_duration = st.number_input("Race Duration (minutes):", min_value=5, max_value=300, value=40)

            st.info("""
                Using recent race data allows for more customized power zones based on your actual performance.
                """)

        weight = st.number_input("Body Weight (kg):", min_value=40.0, max_value=150.0, value=70.0, step=0.1)

    with col2:
        st.markdown("""
            ### Power Zone Benefits

            **Zone 1 (Recovery)**: Active recovery, promotes blood flow and recovery

            **Zone 2 (Endurance)**: Aerobic development, fat utilization, mitochondrial development

            **Zone 3 (Tempo)**: Improved lactate clearance and sustainable power

            **Zone 4 (Threshold)**: Increased lactate threshold and time to exhaustion

            **Zone 5 (VO2max)**: Maximum aerobic capacity development

            **Zone 6 (Anaerobic)**: Anaerobic capacity development

            **Zone 7 (Neuromuscular)**: Pure speed and power development
            """)

    if st.button("Calculate Power Zones"):
        # Calculate reference power value (CP or FTP)
        reference_power = 0

        if power_method == "Critical Power (CP)":
            reference_power = cp
            ref_type = "CP"
        elif power_method == "Functional Threshold Power (FTP)":
            reference_power = ftp
            ref_type = "FTP"
        else:  # Race Power
            # Estimate CP or FTP from race power and duration
            # This is an approximation based on the relationship between race duration and sustainable power
            # Formula based on power-duration relationship
            if race_duration <= 20:
                # For shorter races, assume FTP is ~85-90% of race power
                reference_power = race_power * 0.88
            elif race_duration <= 60:
                # For medium duration, closer to FTP
                reference_power = race_power * 0.95
            else:
                # For longer races, power is typically below FTP
                reference_power = race_power * 1.05

            ref_type = "Estimated FTP"

        # Calculate power-to-weight ratio
        power_to_weight = reference_power / weight

        # Calculate 7-zone power ranges based on reference power
        power_zones = {
            "Zone 1 (Recovery)": f"< {int(reference_power * 0.55)} watts",
            "Zone 2 (Endurance)": f"{int(reference_power * 0.55)} - {int(reference_power * 0.75)} watts",
            "Zone 3 (Tempo)": f"{int(reference_power * 0.76)} - {int(reference_power * 0.9)} watts",
            "Zone 4 (Threshold)": f"{int(reference_power * 0.91)} - {int(reference_power * 1.05)} watts",
            "Zone 5 (VO2max)": f"{int(reference_power * 1.06)} - {int(reference_power * 1.2)} watts",
            "Zone 6 (Anaerobic)": f"{int(reference_power * 1.21)} - {int(reference_power * 1.5)} watts",
            "Zone 7 (Neuromuscular)": f"> {int(reference_power * 1.5)} watts"
        }

        # Display results
        st.markdown("<div class='result-box'>", unsafe_allow_html=True)
        st.subheader(f"Your Running Power Zones ({ref_type}: {reference_power} watts)")

        # Create a DataFrame for better visualization
        power_df = pd.DataFrame(list(power_zones.items()), columns=['Zone', 'Power Range'])
        st.table(power_df)

        # Display power-to-weight ratio
        st.markdown(f"""
            **Power-to-Weight Ratio**: {power_to_weight:.2f} watts/kg

            This power-to-weight ratio is an important performance indicator for running, especially on hills and varied terrain.
            """)

        # Create a visualization of power zones
        zone_labels = list(power_zones.keys())

        # Extract the lower and upper bounds from the ranges
        lower_bounds = []
        upper_bounds = []

        for zone_range in power_zones.values():
            if "<" in zone_range:
                # For ranges like "< 120 watts"
                lower_bounds.append(0)
                upper_bounds.append(int(zone_range.split("<")[1].split(" ")[1]))
            elif ">" in zone_range:
                # For ranges like "> 180 watts"
                lower_bounds.append(int(zone_range.split(">")[1].split(" ")[1]))
                upper_bounds.append(int(zone_range.split(">")[1].split(" ")[1]) + 50)  # Add a buffer for visualization
            else:
                # For ranges like "120 - 140 watts"
                range_parts = zone_range.split(" - ")
                lower_bounds.append(int(range_parts[0]))
                upper_bounds.append(int(range_parts[1].split(" ")[0]))

        # Create a DataFrame for the chart
        chart_data = pd.DataFrame({
            'Zone': zone_labels,
            'Lower': lower_bounds,
            'Upper': upper_bounds,
            'Range': [upper - lower for upper, lower in zip(upper_bounds, lower_bounds)]
        })

        # Create a horizontal bar chart
        fig = px.bar(
            chart_data,
            y='Zone',
            x='Range',
            base='Lower',
            color='Zone',
            orientation='h',
            color_discrete_sequence=px.colors.sequential.Oranges_r,
            labels={'Range': 'Power (watts)', 'Zone': ''},
            title='Power Zones Visualization'
        )

        # Add custom styling
        fig.update_layout(
            xaxis_title="Power (watts)",
            showlegend=False,
            height=400,
            margin=dict(l=0, r=0, t=50, b=0)
        )

        st.plotly_chart(fig)
        st.markdown("</div>", unsafe_allow_html=True)

        # Add training recommendations based on power zones
        st.subheader("Training With Power")
        st.markdown(f"""
            **Benefits of Power-Based Training:**

            - **Immediate feedback**: Unlike heart rate, power responds instantly to changes in effort
            - **Consistent metric**: Not affected by fatigue, heat, or hydration like heart rate
            - **Precise intensity control**: Allows for exact workout prescription and execution
            - **Effective pacing**: Particularly valuable for hilly courses and varied terrain

            **Example Power Workouts:**

            1. **Zone 2 Endurance**: 40-90 minutes at {int(reference_power * 0.65)}-{int(reference_power * 0.75)} watts

            2. **Sweet Spot Training**: 2-3 sets of 10-20 minutes at {int(reference_power * 0.88)}-{int(reference_power * 0.94)} watts

            3. **Threshold Intervals**: 3-5 sets of 5-8 minutes at {int(reference_power * 0.95)}-{int(reference_power * 1.05)} watts

            4. **VO2max Development**: 5-8 sets of 2-4 minutes at {int(reference_power * 1.1)}-{int(reference_power * 1.2)} watts

            5. **Anaerobic Capacity**: 6-10 sets of 30-60 seconds at {int(reference_power * 1.3)}-{int(reference_power * 1.5)} watts
            """)

        # Performance level assessment
        level_assessment = ""
        if power_to_weight < 2.5:
            level_assessment = "Beginner level. Focus on building consistent training and aerobic base."
        elif power_to_weight < 3.0:
            level_assessment = "Recreational runner level. Good foundation to build upon."
        elif power_to_weight < 3.5:
            level_assessment = "Intermediate level. Competitive in local races."
        elif power_to_weight < 4.0:
            level_assessment = "Advanced level. Competitive at regional level."
        elif power_to_weight < 4.5:
            level_assessment = "Elite-amateur level. Potential for high placement in competitive races."
        else:
            level_assessment = "Elite/professional level. Excellent power-to-weight ratio."

        st.info(f"Performance Assessment: {level_assessment}")

        st.success("""
            **Note**: Power data is most valuable when tracked over time. Monitor changes in your power output 
            at different intensities to gauge improvements in fitness and performance.
            """)