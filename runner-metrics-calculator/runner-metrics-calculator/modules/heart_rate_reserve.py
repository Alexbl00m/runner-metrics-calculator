# --------------------- HEART RATE RESERVE ---------------------#
elif app_mode == "Heart Rate Reserve":
st.header("Heart Rate Reserve (HRR) Calculator")

st.markdown("""
    Heart Rate Reserve (HRR) is the difference between your maximum heart rate and resting heart rate.
    The Karvonen Formula uses HRR to calculate more personalized training zones that account for individual fitness levels.

    Unlike percentage of maximum heart rate alone, HRR zones are more accurate across different individuals
    and fitness levels.

    **Scientific Validation**: The Karvonen method has been validated in research and is widely used by coaches and exercise physiologists.

    **Reference**: Karvonen, M. J., Kentala, E., & Mustala, O. (1957). The effects of training on heart rate: a longitudinal study. *Annales Medicinae Experimentalis et Biologiae Fenniae, 35(3)*, 307-315.
    """)

col1, col2 = st.columns([3, 2])

with col1:
    st.subheader("Calculate Heart Rate Reserve")

    max_hr_method = st.radio(
        "Maximum Heart Rate Method:",
        ["Age-predicted formula", "Measured maximum heart rate"]
    )

    if max_hr_method == "Age-predicted formula":
        age = st.number_input("Age:", min_value=12, max_value=100, value=35)
        formula = st.selectbox(
            "Formula:",
            ["Fox (220 - age)", "Tanaka (208 - 0.7 × age)", "Gellish (207 - 0.7 × age)", "Custom"]
        )

        if formula == "Fox (220 - age)":
            max_hr = 220 - age
        elif formula == "Tanaka (208 - 0.7 × age)":
            max_hr = 208 - (0.7 * age)
        elif formula == "Gellish (207 - 0.7 × age)":
            max_hr = 207 - (0.7 * age)
        else:  # Custom
            custom_a = st.number_input("Constant a:", min_value=150, max_value=230, value=220)
            custom_b = st.number_input("Coefficient b:", min_value=0.1, max_value=1.5, value=1.0, step=0.1)
            max_hr = custom_a - (custom_b * age)

        st.info(f"Estimated Maximum Heart Rate: {int(max_hr)} bpm")

    else:  # Measured
        max_hr = st.number_input("Maximum Heart Rate (bpm):", min_value=120, max_value=220, value=185)

        st.info("""
            **How to determine your true maximum heart rate:**

            1. Field test options:
               - After a thorough warm-up, run 3 × 3 minutes uphill at increasing effort
               - 30-minute time trial with final 5 minutes at maximum effort

            2. Laboratory options:
               - Maximal graded exercise test
               - VO2 max test with ECG monitoring

            Note: Always consult a physician before performing maximal tests, especially if you have any health concerns.
            """)

    resting_hr = st.number_input("Resting Heart Rate (bpm):", min_value=30, max_value=100, value=60)

    st.info("""
        **For accurate resting heart rate:**

        Measure your heart rate first thing in the morning while still lying in bed, 
        preferably for 3-5 consecutive days and take the average.
        """)

    # Zone calculation method
    zone_method = st.radio(
        "Zone Calculation Method:",
        ["5-Zone System", "7-Zone System", "3-Zone System (Polarized)"]
    )

with col2:
    st.markdown("""
        ### What is Heart Rate Reserve?

        Heart Rate Reserve (HRR) accounts for individual differences in resting heart rate, making it more precise than using just a percentage of maximum heart rate.

        **The formula is:**

        Target HR = Resting HR + (% intensity × (Max HR - Resting HR))

        **Benefits of using HRR:**

        - More individualized training zones
        - Better accounts for fitness level
        - More accurate across different age groups
        - Better for tracking changes in fitness over time
        """)

if st.button("Calculate HRR Zones"):
    # Calculate Heart Rate Reserve
    hrr = max_hr - resting_hr

    # Calculate zones based on selected method
    if zone_method == "5-Zone System":
        zones = {
            "Zone 1 (Recovery)": f"{int(resting_hr + (hrr * 0.5))} - {int(resting_hr + (hrr * 0.6))} bpm",
            "Zone 2 (Aerobic)": f"{int(resting_hr + (hrr * 0.6) + 1)} - {int(resting_hr + (hrr * 0.7))} bpm",
            "Zone 3 (Tempo)": f"{int(resting_hr + (hrr * 0.7) + 1)} - {int(resting_hr + (hrr * 0.8))} bpm",
            "Zone 4 (Threshold)": f"{int(resting_hr + (hrr * 0.8) + 1)} - {int(resting_hr + (hrr * 0.9))} bpm",
            "Zone 5 (Anaerobic)": f"{int(resting_hr + (hrr * 0.9) + 1)} - {int(max_hr)} bpm"
        }

        # Percentages of HRR for each zone (for chart)
        zone_lower_percentages = [50, 60, 70, 80, 90]
        zone_upper_percentages = [60, 70, 80, 90, 100]

        # Zone descriptions
        zone_descriptions = {
            "Zone 1 (Recovery)": "Very easy intensity for recovery, warm-up, and cool-down.",
            "Zone 2 (Aerobic)": "Aerobic development zone, builds endurance and fat burning capacity.",
            "Zone 3 (Tempo)": "Tempo pace, improves efficiency and lactate clearance.",
            "Zone 4 (Threshold)": "Threshold training, increases lactate threshold.",
            "Zone 5 (Anaerobic)": "High intensity for developing VO2 Max and anaerobic capacity."
        }

    elif zone_method == "7-Zone System":
        zones = {
            "Zone 1 (Recovery)": f"{int(resting_hr + (hrr * 0.5))} - {int(resting_hr + (hrr * 0.55))} bpm",
            "Zone 2 (Easy)": f"{int(resting_hr + (hrr * 0.55) + 1)} - {int(resting_hr + (hrr * 0.65))} bpm",
            "Zone 3 (Aerobic)": f"{int(resting_hr + (hrr * 0.65) + 1)} - {int(resting_hr + (hrr * 0.75))} bpm",
            "Zone 4 (Tempo)": f"{int(resting_hr + (hrr * 0.75) + 1)} - {int(resting_hr + (hrr * 0.82))} bpm",
            "Zone 5 (Threshold)": f"{int(resting_hr + (hrr * 0.82) + 1)} - {int(resting_hr + (hrr * 0.89))} bpm",
            "Zone 6 (VO2 Max)": f"{int(resting_hr + (hrr * 0.89) + 1)} - {int(resting_hr + (hrr * 0.94))} bpm",
            "Zone 7 (Anaerobic)": f"{int(resting_hr + (hrr * 0.94) + 1)} - {int(max_hr)} bpm"
        }

        # Percentages of HRR for each zone (for chart)
        zone_lower_percentages = [50, 55, 65, 75, 82, 89, 94]
        zone_upper_percentages = [55, 65, 75, 82, 89, 94, 100]

        # Zone descriptions
        zone_descriptions = {
            "Zone 1 (Recovery)": "Active recovery, promotes blood flow and recovery.",
            "Zone 2 (Easy)": "Base endurance training, improves fat utilization.",
            "Zone 3 (Aerobic)": "Builds aerobic capacity and endurance.",
            "Zone 4 (Tempo)": "Improves lactate clearance and sustained efforts.",
            "Zone 5 (Threshold)": "Increases lactate threshold and time to exhaustion.",
            "Zone 6 (VO2 Max)": "Develops maximum aerobic capacity.",
            "Zone 7 (Anaerobic)": "Anaerobic capacity development and neuromuscular power."
        }

    else:  # 3-Zone System (Polarized)
        zones = {
            "Zone 1 (Easy)": f"{int(resting_hr + (hrr * 0.5))} - {int(resting_hr + (hrr * 0.77))} bpm",
            "Zone 2 (Moderate)": f"{int(resting_hr + (hrr * 0.77) + 1)} - {int(resting_hr + (hrr * 0.87))} bpm",
            "Zone 3 (Hard)": f"{int(resting_hr + (hrr * 0.87) + 1)} - {int(max_hr)} bpm"
        }

        # Percentages of HRR for each zone (for chart)
        zone_lower_percentages = [50, 77, 87]
        zone_upper_percentages = [77, 87, 100]

        # Zone descriptions
        zone_descriptions = {
            "Zone 1 (Easy)": "Below ventilatory threshold, conversational pace.",
            "Zone 2 (Moderate)": "Between ventilatory and respiratory compensation thresholds.",
            "Zone 3 (Hard)": "Above respiratory compensation threshold, high intensity."
        }

    # Create zone colors for chart
    zone_colors = px.colors.sequential.Oranges_r[:len(zones)]

    # Display results
    st.markdown("<div class='result-box'>", unsafe_allow_html=True)
    st.subheader("Your Heart Rate Reserve Zones (Karvonen Method)")

    st.markdown(f"""
        **Maximum Heart Rate**: {int(max_hr)} bpm

        **Resting Heart Rate**: {resting_hr} bpm

        **Heart Rate Reserve (HRR)**: {hrr} bpm
        """)

    # Create a DataFrame for better visualization
    zones_df = pd.DataFrame(list(zones.items()), columns=['Zone', 'Heart Rate Range'])
    st.table(zones_df)

    # Create a visual representation of the zones
    st.subheader("Heart Rate Zones Visualization")

    # Create data for the chart
    zone_names = list(zones.keys())

    # Calculate lower and upper values in bpm
    lower_values = [resting_hr + (hrr * p / 100) for p in zone_lower_percentages]
    upper_values = [resting_hr + (hrr * p / 100) for p in zone_upper_percentages]

    # Create a horizontal stacked bar chart for zones
    fig = go.Figure()

    # Add segments for each zone
    for i, zone in enumerate(zone_names):
        fig.add_trace(go.Bar(
            name=zone,
            y=[zone],
            x=[upper_values[i] - lower_values[i]],  # Width of segment
            base=lower_values[i],  # Starting point
            orientation='h',
            marker=dict(color=zone_colors[i])
        ))

    # Add a marker for current resting HR
    fig.add_trace(go.Scatter(
        x=[resting_hr],
        y=[zone_names[0]],
        mode='markers+text',
        marker=dict(symbol='triangle-left', size=15, color='green'),
        text=['RHR'],
        textposition='top right',
        showlegend=False
    ))

    # Add a marker for max HR
    fig.add_trace(go.Scatter(
        x=[max_hr],
        y=[zone_names[-1]],
        mode='markers+text',
        marker=dict(symbol='triangle-right', size=15, color='red'),
        text=['Max HR'],
        textposition='top left',
        showlegend=False
    ))

    # Update layout
    fig.update_layout(
        title='Heart Rate Zones (Karvonen Method)',
        barmode='stack',
        xaxis=dict(
            title='Heart Rate (bpm)',
            range=[resting_hr - 10, max_hr + 10]
        ),
        yaxis=dict(title=''),
        showlegend=False,
        height=300,
        margin=dict(l=0, r=0, t=50, b=0)
    )

    st.plotly_chart(fig)
    st.markdown("</div>", unsafe_allow_html=True)

    # Zone descriptions and training recommendations
    st.subheader("Zone Descriptions and Training Recommendations")

    # Display each zone with description and training recommendations
    for zone, hr_range in zones.items():
        with st.expander(f"{zone}: {hr_range}"):
            st.markdown(f"""
                **Description**: {zone_descriptions[zone]}

                **Recommended Training**:
                """)

            if "Recovery" in zone:
                st.markdown("""
                    - Recovery runs after hard workouts
                    - Warm-up and cool-down segments
                    - Active recovery between intervals
                    - Typical duration: 20-40 minutes
                    """)
            elif "Easy" in zone or ("Aerobic" in zone and "2" in zone):
                st.markdown("""
                    - Long, slow distance runs
                    - Base building runs
                    - Easy/conversational runs
                    - Foundation of endurance training
                    - Typical duration: 30-120 minutes
                    """)
            elif "Aerobic" in zone and "3" in zone:
                st.markdown("""
                    - Steady state aerobic runs
                    - Medium-long runs
                    - Foundation for marathon training
                    - Typical duration: 40-90 minutes
                    """)
            elif "Tempo" in zone:
                st.markdown("""
                    - Tempo runs
                    - Marathon pace work
                    - Cruise intervals (e.g., 4 × 8 minutes)
                    - Typical duration: 20-40 minutes total
                    """)
            elif "Threshold" in zone:
                st.markdown("""
                    - Lactate threshold intervals
                    - Half marathon pace work
                    - Shorter tempo runs
                    - Examples: 4 × 5 minutes, 2 × 10 minutes
                    - Typical duration: 15-30 minutes total
                    """)
            elif "VO2" in zone:
                st.markdown("""
                    - VO2 Max intervals
                    - 5K race pace work
                    - Examples: 5 × 3 minutes, 6-8 × 800m
                    - Typical duration: 12-20 minutes total
                    """)
            elif "Anaerobic" in zone:
                st.markdown("""
                    - Short, high-intensity intervals
                    - Speed development
                    - Examples: 10-12 × 400m, 6-8 × 30-second hill sprints
                    - Typical duration: 5-12 minutes total
                    """)
            elif "Easy" in zone and "1" in zone:  # Polarized Zone 1
                st.markdown("""
                    - Most of your training volume (80-85%)
                    - All easy runs, recovery runs, long runs
                    - Comfortable, conversational pace
                    - Foundation of polarized training approach
                    """)
            elif "Moderate" in zone:  # Polarized Zone 2
                st.markdown("""
                    - Limited volume in polarized training (0-10%)
                    - Threshold runs, marathon pace work
                    - Often minimized in true polarized approach
                    - "No man's land" - neither easy enough for volume nor hard enough for intensity
                    """)
            elif "Hard" in zone:  # Polarized Zone 3
                st.markdown("""
                    - High intensity work (15-20% of training)
                    - Interval training, hill repeats
                    - Race-specific workouts
                    - Key quality sessions in polarized training
                    """)

    # Display percentage guidelines
    st.subheader("Recommended Training Distribution")

    if zone_method == "3-Zone System (Polarized)":
        # Create data for polarized distribution
        labels = ['Zone 1 (Easy)', 'Zone 2 (Moderate)', 'Zone 3 (Hard)']
        polarized = [80, 5, 15]
        traditional = [50, 40, 10]

        # Create grouped bar chart
        fig = go.Figure()

        fig.add_trace(go.Bar(
            x=labels,
            y=polarized,
            name='Polarized Approach',
            marker_color='#E6754E'
        ))

        fig.add_trace(go.Bar(
            x=labels,
            y=traditional,
            name='Traditional Approach',
            marker_color='#4E97E6'
        ))

        fig.update_layout(
            title='Training Distribution Comparison',
            xaxis_title='Training Zone',
            yaxis_title='Percentage of Training Volume',
            barmode='group',
            margin=dict(l=0, r=0, t=50, b=0)
        )

        st.plotly_chart(fig)

        st.markdown("""
            **Polarized Training Approach**:

            Research with elite endurance athletes suggests a polarized distribution (80/5/15) may be more effective than a traditional pyramidal approach (50/40/10).

            **Key Benefits**:
            - Reduced risk of overtraining
            - Better recovery between hard sessions
            - More sustainable long-term approach
            - Potentially greater performance improvements

            **Implementation**:
            - Ensure easy runs are truly easy (HR strictly in Zone 1)
            - Make hard sessions genuinely challenging (Zone 3)
            - Minimize "moderate" intensity work (Zone 2)
            """)

    else:
        # Create data for standard zone distribution
        if zone_method == "5-Zone System":
            labels = ['Zone 1', 'Zone 2', 'Zone 3', 'Zone 4', 'Zone 5']
            values = [20, 50, 15, 10, 5]
        else:  # 7-Zone System
            labels = ['Zone 1', 'Zone 2', 'Zone 3', 'Zone 4', 'Zone 5', 'Zone 6', 'Zone 7']
            values = [10, 25, 30, 15, 10, 7, 3]

        # Create pie chart
        fig = go.Figure(data=[go.Pie(
            labels=labels,
            values=values,
            hole=.3,
            marker=dict(colors=zone_colors)
        )])

        fig.update_layout(
            title='Recommended Training Distribution',
            margin=dict(t=50, b=0, l=0, r=0)
        )

        st.plotly_chart(fig)

        st.markdown("""
            **General Guidelines for Training Distribution**:

            - **Base/Foundation Phase**: 80-90% low intensity (Zones 1-2), 10-20% moderate-high intensity
            - **Build Phase**: 70-80% low intensity, 20-30% moderate-high intensity
            - **Peak/Race Phase**: 65-75% low intensity, 25-35% moderate-high intensity

            **Weekly Structure Example**:
            - 1-2 high-intensity sessions (Zones 4-5/7)
            - 1 moderate-intensity session (Zone 3)
            - Remaining sessions at low intensity (Zones 1-2)

            Monitoring your training using heart rate zones helps ensure you're training at the right intensity for each session, optimizing adaptations while reducing injury risk.
            """)