# --------------------- RUNNING POWER ---------------------#
elif app_mode == "Running Power":
st.header("Running Power Calculator")

st.markdown("""
    Running power is a measure of the work rate or energy expenditure during running, typically measured in watts.
    Unlike heart rate, power responds instantly to changes in effort and is not affected by factors such as 
    fatigue, temperature, or hydration status.

    This calculator estimates running power based on speed, incline, weight, and environmental factors.

    **Scientific Validation**: Running power has been validated in research as an effective training metric.

    **References**: 
    - Cerezuela-Espejo, V., Hernández-Belmonte, A., Courel-Ibáñez, J., Conesa-Ros, E., Mora-Rodriguez, R., & Pallarés, J. G. (2020). Running power meters and theoretical models based on laws of physics: A comparison study. *Scandinavian Journal of Medicine & Science in Sports, 30(11)*, 2113-2121.
    - Austin, C. L., Hokanson, J. F., McGinnis, P. M., & Patrick, S. (2018). The relationship between running power and running economy in well-trained distance runners. *Sports, 6(4)*, 142.
    """)

power_calculator_type = st.radio(
    "Calculator Type:",
    ["Power Estimation", "Power Zones", "Power Metrics Analysis"]
)

if power_calculator_type == "Power Estimation":
    st.subheader("Estimate Running Power")

    col1, col2 = st.columns(2)

    with col1:
        # Basic parameters
        weight = st.number_input("Body Weight (kg):", min_value=40.0, max_value=150.0, value=70.0, step=0.1)
        height = st.number_input("Height (cm):", min_value=140.0, max_value=220.0, value=175.0, step=0.1)
        speed = st.number_input("Running Speed (km/h):", min_value=5.0, max_value=25.0, value=12.0, step=0.1)

        # Additional parameters
        incline = st.slider("Incline/Grade (%):", min_value=-15.0, max_value=15.0, value=0.0, step=0.5)
        wind_speed = st.slider("Headwind/Tailwind (km/h):", min_value=-20.0, max_value=20.0, value=0.0, step=0.5,
                               help="Positive values indicate headwind, negative values indicate tailwind")

        terrain_factor = st.selectbox(
            "Running Surface:",
            ["Track/Road (firm)", "Grass (well maintained)", "Trail (packed dirt)", "Sand/Soft Surface", "Snow/Mud"]
        )

        # Map terrain to coefficient
        terrain_coefficients = {
            "Track/Road (firm)": 1.0,
            "Grass (well maintained)": 1.05,
            "Trail (packed dirt)": 1.1,
            "Sand/Soft Surface": 1.2,
            "Snow/Mud": 1.25
        }
        terrain_coef = terrain_coefficients[terrain_factor]

    with col2:
        st.markdown("""
            ### Factors Affecting Running Power

            - **Body Weight**: Heavier runners require more power
            - **Speed**: Power increases with speed (not linearly)
            - **Incline**: Uphill running dramatically increases power
            - **Wind**: Headwind increases power required, tailwind decreases it
            - **Surface**: Softer surfaces require more power
            - **Altitude**: Higher altitude slightly reduces air resistance
            """)

        st.info("""
            This calculator provides an estimate based on published models. 
            For precise power measurements, consider using a running power meter such as 
            Stryd, Garmin Running Power, or COROS running power.
            """)

        advanced_options = st.checkbox("Show Advanced Options")

        if advanced_options:
            altitude = st.number_input("Altitude (meters):", min_value=0, max_value=5000, value=0)
            temperature = st.number_input("Temperature (°C):", min_value=-20.0, max_value=50.0, value=20.0, step=0.5)
            humidity = st.slider("Relative Humidity (%):", min_value=0, max_value=100, value=50)
            footwear_weight = st.number_input("Shoe Weight (g per shoe):", min_value=100, max_value=500, value=250)
        else:
            altitude = 0
            temperature = 20.0
            humidity = 50
            footwear_weight = 250

    if st.button("Calculate Running Power"):
        # Convert speed to m/s
        speed_ms = speed / 3.6

        # Convert wind speed to m/s
        wind_ms = wind_speed / 3.6

        # Basic power calculation
        # Power (W) = Force (N) × Velocity (m/s)

        # Gravitational force component
        g = 9.81  # gravitational acceleration (m/s²)
        incline_rad = np.arctan(incline / 100)
        grav_force = weight * g * np.sin(incline_rad)

        # Air resistance
        # Adjust air density for altitude and temperature
        air_density_sl = 1.225  # kg/m³ at sea level, 15°C
        air_density = air_density_sl * np.exp(-altitude / 7000) * (273 / (273 + temperature))

        # Calculate frontal area (approximation based on height and weight)
        frontal_area = 0.266 * ((weight) ** 0.425) * ((height / 100) ** 0.725) / 10000  # m²

        # Drag coefficient
        cd = 0.9  # typical value for runner

        # Air resistance force
        rel_velocity = speed_ms + wind_ms  # relative velocity (headwind positive)
        air_resist = 0.5 * air_density * cd * frontal_area * rel_velocity ** 2

        # Rolling resistance
        rolling_coef = 0.01 * terrain_coef  # base coefficient adjusted for terrain
        rolling_resist = rolling_coef * weight * g * np.cos(incline_rad)

        # Total resistance force
        total_force = grav_force + air_resist + rolling_resist

        # Calculate power
        power = total_force * speed_ms

        # Add efficiency factor (running is not 100% efficient)
        efficiency = 0.25  # approximate mechanical efficiency of running
        power_output = power / efficiency

        # Add small adjustment for shoe weight
        shoe_effect = footwear_weight / 250  # normalize to typical shoe weight
        power_output *= (1 + (shoe_effect - 1) * 0.03)  # small adjustment based on shoe weight

        # Calculate power-to-weight ratio
        power_to_weight = power_output / weight

        # Display results
        st.markdown("<div class='result-box'>", unsafe_allow_html=True)
        st.subheader("Estimated Running Power")

        st.markdown(f"""
            <h3>Power Output: <span class="highlight">{power_output:.0f} watts</span></h3>

            **Power-to-Weight Ratio**: {power_to_weight:.2f} watts/kg

            **Running Conditions**:
            - Speed: {speed} km/h ({speed / 1.60934:.1f} mph)
            - Incline: {incline}%
            - Wind: {wind_speed} km/h ({wind_speed / 1.60934:.1f} mph)
            - Surface: {terrain_factor}
            """, unsafe_allow_html=True)

        # Display breakdown of power components
        st.markdown("### Power Component Breakdown")

        # Calculate component percentages
        grav_power = grav_force * speed_ms / efficiency
        air_power = air_resist * speed_ms / efficiency
        rolling_power = rolling_resist * speed_ms / efficiency

        # Ensure we don't have negative percentages
        grav_power = max(0, grav_power)
        air_power = max(0, air_power)
        rolling_power = max(0, rolling_power)

        total = grav_power + air_power + rolling_power

        # Create data for pie chart
        if incline == 0:
            labels = ['Air Resistance', 'Rolling Resistance']
            values = [air_power, rolling_power]
            colors = ['#E6754E', '#4E97E6']
        else:
            labels = ['Gravity (Incline)', 'Air Resistance', 'Rolling Resistance']
            values = [grav_power, air_power, rolling_power]
            colors = ['#E6754E', '#4E97E6', '#4EE6A5']

        # Remove components that are less than 1% of total
        cleaned_labels = []
        cleaned_values = []
        cleaned_colors = []

        for i, v in enumerate(values):
            if v > 0.01 * total:
                cleaned_labels.append(labels[i])
                cleaned_values.append(v)
                cleaned_colors.append(colors[i])

        # Create pie chart
        fig = go.Figure(data=[go.Pie(
            labels=cleaned_labels,
            values=cleaned_values,
            hole=.3,
            marker=dict(colors=cleaned_colors)
        )])

        fig.update_layout(
            title="Power Distribution",
            margin=dict(t=30, b=0, l=0, r=0)
        )

        st.plotly_chart(fig)
        st.markdown("</div>", unsafe_allow_html=True)

        # Add interpretations and recommendations
        st.subheader("Power Analysis & Training Recommendations")

        # Categorize power-to-weight ratio
        power_category = ""
        if power_to_weight < 2.5:
            power_category = "Beginner"
        elif power_to_weight < 3.0:
            power_category = "Recreational"
        elif power_to_weight < 3.5:
            power_category = "Intermediate"
        elif power_to_weight < 4.0:
            power_category = "Advanced"
        elif power_to_weight < 4.5:
            power_category = "Elite-Amateur"
        else:
            power_category = "Elite"

        st.markdown(f"""
            **Power-to-Weight Analysis**:

            Your power-to-weight ratio of {power_to_weight:.2f} watts/kg at {speed} km/h is in the **{power_category}** range.

            **Training with Power**:

            1. **For flat terrain running** ({power_output:.0f} watts at {speed} km/h):
               - Use this as a reference for maintaining consistent effort regardless of wind or fatigue
               - Target this power for tempo runs or threshold sessions

            2. **For hill training**:
               - On a {incline}% grade, maintain {power_output:.0f} watts for consistent effort
               - For hill repeats, target 110-120% of this power ({int(power_output * 1.15)} watts)

            3. **For race planning**:
               - Marathon: ~90-95% of threshold power
               - Half-Marathon: ~95-100% of threshold power
               - 10K: ~105-110% of threshold power
               - 5K: ~110-115% of threshold power
            """)

        # Display how this changes with different speeds
        st.subheader("Power at Different Speeds")

        # Calculate power at different speeds
        speeds = [speed * 0.8, speed * 0.9, speed, speed * 1.1, speed * 1.2]
        powers = []

        for s in speeds:
            s_ms = s / 3.6
            rel_v = s_ms + wind_ms
            air_r = 0.5 * air_density * cd * frontal_area * rel_v ** 2
            roll_r = rolling_coef * weight * g * np.cos(incline_rad)
            total_f = grav_force + air_r + roll_r
            p = total_f * s_ms / efficiency
            powers.append(int(p))

        # Create data for bar chart
        speed_labels = [f"{s:.1f} km/h" for s in speeds]

        fig = go.Figure(data=[
            go.Bar(x=speed_labels, y=powers, marker_color='#E6754E')
        ])

        fig.update_layout(
            title="Power Output at Different Speeds",
            xaxis_title="Running Speed",
            yaxis_title="Power (watts)",
        )

        st.plotly_chart(fig)

        # Add note about cubic relationship with speed
        st.info("""
            **Note**: Power increases non-linearly with speed. A 10% increase in speed typically requires a 15-20% increase in power output.
            This is mainly due to air resistance, which increases with the square of speed.
            """)

elif power_calculator_type == "Power Zones":
    st.subheader("Power Zones Calculator")

    col1, col2 = st.columns(2)

    with col1:
        # Reference power input
        reference_method = st.radio(
            "Reference Method:",
            ["Critical Power (CP)", "Functional Threshold Power (FTP)", "Critical Velocity (CV)"]
        )

        if reference_method == "Critical Power (CP)":
            cp = st.number_input("Critical Power (watts):", min_value=100, max_value=500, value=280)
            reference_power = cp

        elif reference_method == "Functional Threshold Power (FTP)":
            ftp = st.number_input("FTP (watts):", min_value=100, max_value=500, value=270)
            reference_power = ftp

        else:  # Critical Velocity (CV)
            cv = st.number_input("Critical Velocity (m/s):", min_value=2.5, max_value=7.0, value=4.0, step=0.1)
            weight = st.number_input("Body Weight (kg, CV):", min_value=40.0, max_value=150.0, value=70.0, step=0.1)

            # Estimate CP from CV (this is an approximation)
            # Formula based on the relationship between running speed and power
            speed_kph = cv * 3.6  # convert to km/h

            # Estimate power using simplified formula for flat terrain
            g = 9.81  # gravitational acceleration
            air_density = 1.225  # kg/m³
            cd = 0.9  # drag coefficient
            frontal_area = 0.266 * ((weight) ** 0.425) * ((175 / 100) ** 0.725) / 10000  # m²

            air_resist = 0.5 * air_density * cd * frontal_area * cv ** 2
            rolling_resist = 0.01 * weight * g

            total_force = air_resist + rolling_resist
            power = total_force * cv

            # Apply efficiency factor
            efficiency = 0.25
            reference_power = power / efficiency

            st.info(f"Estimated Power from CV: {reference_power:.0f} watts")

        # Body weight for power-to-weight calculations
        if reference_method != "Critical Velocity (CV)":
            weight = st.number_input("Body Weight (kg):", min_value=40.0, max_value=150.0, value=70.0, step=0.1)

        # Zone model selection
        zone_model = st.selectbox(
            "Zone Model:",
            ["5-Zone Model", "7-Zone Model", "3-Zone Model (Polarized)"]
        )

    with col2:
        st.markdown("""
            ### Power Zone Training Benefits

            Power-based training offers several advantages over heart rate or pace-based training:

            - **Immediate Feedback**: Power responds instantly to changes in effort
            - **Consistent Metric**: Not affected by fatigue, heat, or hydration
            - **Precise Intensity**: Exact workout prescription
            - **Effective Pacing**: Valuable for hilly courses and varied terrain

            **Reference Values**:
            - **Critical Power (CP)**: Highest sustainable power over ~30-40 minutes
            - **FTP**: Similar to CP, often measured with 20-minute test × 0.95
            - **Critical Velocity (CV)**: Running equivalent of critical power, measured in m/s
            """)

    if st.button("Calculate Power Zones"):
        # Calculate power-to-weight ratio
        power_to_weight = reference_power / weight

        # Calculate power zones based on selected model
        if zone_model == "7-Zone Model":
            power_zones = {
                "Zone 1 (Recovery)": f"< {int(reference_power * 0.55)} watts",
                "Zone 2 (Endurance)": f"{int(reference_power * 0.55)} - {int(reference_power * 0.75)} watts",
                "Zone 3 (Tempo)": f"{int(reference_power * 0.76)} - {int(reference_power * 0.9)} watts",
                "Zone 4 (Threshold)": f"{int(reference_power * 0.91)} - {int(reference_power * 1.05)} watts",
                "Zone 5 (VO2max)": f"{int(reference_power * 1.06)} - {int(reference_power * 1.2)} watts",
                "Zone 6 (Anaerobic)": f"{int(reference_power * 1.21)} - {int(reference_power * 1.5)} watts",
                "Zone 7 (Neuromuscular)": f"> {int(reference_power * 1.5)} watts"
            }
        elif zone_model == "5-Zone Model":
            power_zones = {
                "Zone 1 (Recovery)": f"< {int(reference_power * 0.75)} watts",
                "Zone 2 (Endurance)": f"{int(reference_power * 0.75)} - {int(reference_power * 0.9)} watts",
                "Zone 3 (Tempo)": f"{int(reference_power * 0.9)} - {int(reference_power * 1.0)} watts",
                "Zone 4 (Threshold)": f"{int(reference_power * 1.0)} - {int(reference_power * 1.1)} watts",
                "Zone 5 (Anaerobic)": f"> {int(reference_power * 1.1)} watts"
            }
        else:  # 3-Zone Model (Polarized)
            power_zones = {
                "Zone 1 (Easy)": f"< {int(reference_power * 0.85)} watts",
                "Zone 2 (Moderate)": f"{int(reference_power * 0.85)} - {int(reference_power * 1.05)} watts",
                "Zone 3 (Hard)": f"> {int(reference_power * 1.05)} watts"
            }

        # Display results
        st.markdown("<div class='result-box'>", unsafe_allow_html=True)
        st.subheader(f"Your Running Power Zones (Based on {reference_method}: {int(reference_power)} watts)")

        # Create a DataFrame for better visualization
        power_df = pd.DataFrame(list(power_zones.items()), columns=['Zone', 'Power Range'])
        st.table(power_df)

        # Display power-to-weight ratio
        st.markdown(f"""
            **Power-to-Weight Ratio**: {power_to_weight:.2f} watts/kg
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

        # Training recommendations
        st.subheader("Training Recommendations")

        if zone_model == "7-Zone Model":
            st.markdown(f"""
                **7-Zone Training Model**

                1. **Zone 1 (Recovery)** - <{int(reference_power * 0.55)} watts
                   - Purpose: Active recovery, warm-up, cool-down
                   - Sessions: Recovery runs, 30-45 minutes
                   - Perceived Effort: Very easy, conversational

                2. **Zone 2 (Endurance)** - {int(reference_power * 0.55)}-{int(reference_power * 0.75)} watts
                   - Purpose: Aerobic development, fat utilization
                   - Sessions: Long runs, 45-150 minutes
                   - Perceived Effort: Easy, comfortable conversation possible

                3. **Zone 3 (Tempo)** - {int(reference_power * 0.76)}-{int(reference_power * 0.9)} watts
                   - Purpose: Improved lactate clearance and sustainable power
                   - Sessions: Tempo runs, 20-40 minutes
                   - Perceived Effort: Moderately hard, limited conversation

                4. **Zone 4 (Threshold)** - {int(reference_power * 0.91)}-{int(reference_power * 1.05)} watts
                   - Purpose: Increased lactate threshold
                   - Sessions: Threshold intervals, 4-6 × 5-8 minutes, 1:1 recovery
                   - Perceived Effort: Hard but sustainable

                5. **Zone 5 (VO2max)** - {int(reference_power * 1.06)}-{int(reference_power * 1.2)} watts
                   - Purpose: Maximum aerobic capacity development
                   - Sessions: VO2max intervals, 6-10 × 2-4 minutes, 1:1 recovery
                   - Perceived Effort: Very hard, breathing labored

                6. **Zone 6 (Anaerobic)** - {int(reference_power * 1.21)}-{int(reference_power * 1.5)} watts
                   - Purpose: Anaerobic capacity development
                   - Sessions: Hard intervals, 6-10 × 30-90 seconds, 2:1 or 3:1 recovery
                   - Perceived Effort: Extremely hard, near maximum

                7. **Zone 7 (Neuromuscular)** - >{int(reference_power * 1.5)} watts
                   - Purpose: Power and speed development
                   - Sessions: Short sprints, 10-15 × 10-20 seconds, full recovery
                   - Perceived Effort: Maximum, all-out effort
                """)

            st.info("""
                **Recommended Zone Distribution**: For endurance running, aim for approximately:
                - 75-80% in Zones 1-2
                - 10-15% in Zones 3-4
                - 5-10% in Zones 5-7
                """)

        elif zone_model == "5-Zone Model":
            st.markdown(f"""
                **5-Zone Training Model**

                1. **Zone 1 (Recovery)** - <{int(reference_power * 0.75)} watts
                   - Purpose: Active recovery, warm-up, cool-down
                   - Sessions: Recovery runs, 30-45 minutes
                   - Example: Post-hard workout recovery, pre-race day

                2. **Zone 2 (Endurance)** - {int(reference_power * 0.75)}-{int(reference_power * 0.9)} watts
                   - Purpose: Aerobic development, fat utilization
                   - Sessions: Long runs, daily training runs
                   - Example: Weekend long run, easy runs

                3. **Zone 3 (Tempo)** - {int(reference_power * 0.9)}-{int(reference_power * 1.0)} watts
                   - Purpose: Lactate threshold development
                   - Sessions: Steady tempo runs, marathon pace work
                   - Example: 20-30 minute tempo run, cruise intervals

                4. **Zone 4 (Threshold)** - {int(reference_power * 1.0)}-{int(reference_power * 1.1)} watts
                   - Purpose: VO2 max development, race-specific fitness
                   - Sessions: Intervals at 5K-10K pace
                   - Example: 5 × 1000m at 5K pace, 3 × 1 mile at 10K pace

                5. **Zone 5 (Anaerobic)** - >{int(reference_power * 1.1)} watts
                   - Purpose: Speed development, neuromuscular power
                   - Sessions: Short, fast intervals, hill sprints
                   - Example: 10 × 200m at mile pace, 8 × 30-second hill sprints
                """)

            st.info("""
                **Recommended Zone Distribution**: For endurance running, aim for approximately:
                - 80% in Zones 1-2
                - 10% in Zone 3
                - 10% in Zones 4-5
                """)

        else:  # 3-Zone Model (Polarized)
            st.markdown(f"""
                **3-Zone (Polarized) Training Model**

                1. **Zone 1 (Easy)** - <{int(reference_power * 0.85)} watts
                   - Purpose: Aerobic development with minimal stress
                   - Sessions: Long runs, recovery runs, easy runs
                   - Volume: 80-85% of total training time
                   - Example: All easy running, morning runs, recovery days

                2. **Zone 2 (Moderate)** - {int(reference_power * 0.85)}-{int(reference_power * 1.05)} watts
                   - Purpose: Threshold development
                   - Sessions: Tempo runs, marathon pace work
                   - Volume: 0-10% of total training time
                   - Note: Often minimized in a truly polarized approach

                3. **Zone 3 (Hard)** - >{int(reference_power * 1.05)} watts
                   - Purpose: VO2 max, anaerobic capacity, neuromuscular power
                   - Sessions: High-intensity intervals, hill repeats, track workouts
                   - Volume: 15-20% of total training time
                   - Example: 8 × 400m at mile pace, 5 × 3 minutes at 5K pace
                """)

            st.success("""
                **Polarized Training Approach**: Research suggests that elite endurance athletes often follow a polarized distribution:
                - ~80% Low intensity (Zone 1)
                - ~0-5% Moderate intensity (Zone 2) 
                - ~15-20% High intensity (Zone 3)

                This approach may provide better adaptations with less risk of overtraining compared to a traditional pyramid approach.
                """)

else:  # Power Metrics Analysis
    st.subheader("Running Power Metrics Analysis")

    st.markdown("""
        This tool helps analyze various power-related metrics that provide insights into your running efficiency
        and performance characteristics.
        """)

    col1, col2 = st.columns(2)

    with col1:
        # Basic inputs
        weight = st.number_input("Body Weight (kg):", min_value=40.0, max_value=150.0, value=70.0, step=0.1)

        # Test interval inputs
        cp = st.number_input("Critical Power (watts):", min_value=100, max_value=500, value=280)
        max_power = st.number_input("Maximum/Sprint Power (watts):", min_value=200, max_value=1000, value=650)

        # Race power inputs
        st.subheader("Race Power Data (Optional)")
        race_power_5k = st.number_input("5K Average Power (watts):", min_value=0, max_value=800, value=320)
        race_power_10k = st.number_input("10K Average Power (watts):", min_value=0, max_value=800, value=300)
        race_power_hm = st.number_input("Half Marathon Average Power (watts):", min_value=0, max_value=800, value=275)

        # Advanced metrics
        include_advanced = st.checkbox("Include Advanced Metrics")

        if include_advanced:
            leg_spring_stiffness = st.number_input("Leg Spring Stiffness (kN/m):", min_value=5.0, max_value=40.0,
                                                   value=12.0, step=0.5)
            ground_contact_time = st.number_input("Ground Contact Time (ms):", min_value=150, max_value=350, value=220)
            form_power = st.number_input("Form Power (watts):", min_value=30, max_value=150, value=55)
        else:
            # Default values if not provided
            leg_spring_stiffness = 12.0
            ground_contact_time = 220
            form_power = 55

    with col2:
        st.markdown("""
            ### Power Metrics Explained

            **Basic Power Metrics**:
            - **Critical Power (CP)**: Highest power sustainable for ~30-40 minutes
            - **Max Power**: Highest power output over 5-10 seconds (sprint)
            - **Power-to-Weight Ratio**: Power output divided by body weight

            **Advanced Metrics**:
            - **Form Power**: Power used for "vertical oscillation" (bouncing)
            - **Leg Spring Stiffness**: Measure of leg's ability to store/return energy
            - **Ground Contact Time**: Time foot spends on ground each stride

            **How to Measure**:
            - **Critical Power**: 30-minute time trial (average power)
            - **Max Power**: Short sprint (5-10 seconds) at maximum effort
            - **Advanced Metrics**: Measured by some running power meters
            """)

    if st.button("Analyze Power Metrics"):
        # Calculate basic power metrics
        power_to_weight = cp / weight
        max_power_to_weight = max_power / weight

        # Calculate power reserve (anaerobic work capacity)
        power_reserve = max_power - cp
        power_reserve_percentage = (power_reserve / cp) * 100

        # Calculate power duration relationship
        # Simplified version of critical power model (P = AWC/t + CP)
        # where AWC (anaerobic work capacity) is estimated from power reserve
        awc = power_reserve * 90  # rough estimate, typically in joules

        # Calculate fatigue resistance
        fatigue_resistance = cp / max_power

        # Power duration curve data
        durations = [1, 2, 5, 10, 30, 60, 120, 300, 600, 1200, 2400, 3600, 7200, 10800]  # seconds
        powers = [min(max_power, cp + (awc / t if t > 0 else 0)) for t in durations]

        # Display results
        st.markdown("<div class='result-box'>", unsafe_allow_html=True)
        st.subheader("Power Metrics Analysis")

        # Create columns for metrics display
        metric_col1, metric_col2 = st.columns(2)

        with metric_col1:
            st.markdown(f"""
                **Basic Power Metrics**:

                Critical Power: {cp} watts

                Max Power: {max_power} watts

                Power-to-Weight: {power_to_weight:.2f} watts/kg

                Max Power-to-Weight: {max_power_to_weight:.2f} watts/kg
                """)

        with metric_col2:
            st.markdown(f"""
                **Performance Characteristics**:

                Power Reserve: {power_reserve} watts ({power_reserve_percentage:.1f}%)

                Fatigue Resistance: {fatigue_resistance:.2f}

                Anaerobic Work Capacity: ~{awc:.0f} joules
                """)

        # Interpretation
        st.subheader("Interpretation")

        # Power-to-weight assessment
        ptw_category = ""
        if power_to_weight < 3.0:
            ptw_category = "Beginner/Recreational"
            ptw_description = "typical for new or recreational runners"
        elif power_to_weight < 3.5:
            ptw_category = "Intermediate"
            ptw_description = "competitive at local level"
        elif power_to_weight < 4.0:
            ptw_category = "Advanced"
            ptw_description = "competitive at regional level"
        elif power_to_weight < 4.5:
            ptw_category = "Elite-Amateur"
            ptw_description = "high level club runner"
        else:
            ptw_category = "Elite"
            ptw_description = "professional/elite level"

        # Fatigue resistance assessment
        if fatigue_resistance < 0.35:
            fr_category = "Sprint Specialist"
            fr_description = "excellent sprint capability but may struggle with endurance events"
        elif fatigue_resistance < 0.45:
            fr_category = "Speed-Endurance"
            fr_description = "good balance of speed and endurance, suited for middle distances"
        else:
            fr_category = "Endurance Specialist"
            fr_description = "excellent endurance but may lack top-end speed"

        st.markdown(f"""
            **Power-to-Weight Ratio**: {power_to_weight:.2f} watts/kg is classified as **{ptw_category}** - {ptw_description}

            **Fatigue Profile**: Your fatigue resistance of {fatigue_resistance:.2f} suggests you are a **{fr_category}** - {fr_description}
            """)

        # Create power duration curve
        time_labels = ["1s", "2s", "5s", "10s", "30s", "1min", "2min", "5min", "10min", "20min", "40min", "1hr", "2hr",
                       "3hr"]

        fig = go.Figure()

        # Add power duration curve
        fig.add_trace(go.Scatter(
            x=durations,
            y=powers,
            mode='lines',
            name='Predicted Power',
            line=dict(color='#E6754E', width=3)
        ))

        # Add race points if provided
        race_points_x = []
        race_points_y = []
        race_labels = []

        if race_power_5k > 0:
            # Approximate 5K time based on power-to-weight
            approx_5k_min = 30 / power_to_weight
            race_points_x.append(approx_5k_min * 60)
            race_points_y.append(race_power_5k)
            race_labels.append("5K")

        if race_power_10k > 0:
            approx_10k_min = 65 / power_to_weight
            race_points_x.append(approx_10k_min * 60)
            race_points_y.append(race_power_10k)
            race_labels.append("10K")

        if race_power_hm > 0:
            approx_hm_min = 150 / power_to_weight
            race_points_x.append(approx_hm_min * 60)
            race_points_y.append(race_power_hm)
            race_labels.append("HM")

        if race_points_x:
            fig.add_trace(go.Scatter(
                x=race_points_x,
                y=race_points_y,
                mode='markers+text',
                marker=dict(size=10, color='#4E97E6'),
                text=race_labels,
                textposition="top center",
                name='Race Data'
            ))

        # Add logarithmic x-axis
        fig.update_layout(
            title="Power-Duration Curve",
            xaxis_title="Duration (seconds, log scale)",
            yaxis_title="Power (watts)",
            xaxis_type="log",
            xaxis=dict(
                tickvals=durations,
                ticktext=time_labels
            ),
            showlegend=True
        )

        st.plotly_chart(fig)

        # If advanced metrics included, show those too
        if include_advanced:
            st.subheader("Advanced Metrics Analysis")

            # Calculate efficiency metrics
            form_power_percentage = (form_power / cp) * 100
            running_effectiveness = 100 - form_power_percentage

            # Leg spring stiffness assessment
            if leg_spring_stiffness < 10:
                stiffness_category = "Low"
                stiffness_description = "typical of recreational runners or heavier runners"
            elif leg_spring_stiffness < 15:
                stiffness_category = "Moderate"
                stiffness_description = "average for trained runners"
            else:
                stiffness_category = "High"
                stiffness_description = "typical of elite/efficient runners"

            # Ground contact time assessment
            if ground_contact_time > 250:
                gct_category = "Long"
                gct_description = "typical of recreational runners or longer distance specialists"
            elif ground_contact_time > 200:
                gct_category = "Moderate"
                gct_description = "average for trained runners"
            else:
                gct_category = "Short"
                gct_description = "typical of efficient/elite runners or sprinters"

            st.markdown(f"""
                **Running Efficiency Metrics**:

                Form Power: {form_power} watts ({form_power_percentage:.1f}% of CP)

                Running Effectiveness: {running_effectiveness:.1f}%

                Leg Spring Stiffness: {leg_spring_stiffness} kN/m (**{stiffness_category}** - {stiffness_description})

                Ground Contact Time: {ground_contact_time} ms (**{gct_category}** - {gct_description})
                """)

            # Recommendations based on advanced metrics
            st.subheader("Recommendations")

            if form_power_percentage > 25:
                st.markdown("""
                    **Running Form**: Your form power is relatively high, suggesting significant vertical oscillation. Consider:
                    - Focusing on form drills to reduce bouncing
                    - Increasing cadence slightly
                    - Core and hip stability exercises
                    """)

            if leg_spring_stiffness < 10:
                st.markdown("""
                    **Leg Stiffness**: Your leg spring stiffness is relatively low. Consider:
                    - Plyometric exercises (box jumps, depth jumps)
                    - Heavy strength training (squats, deadlifts)
                    - Hill sprints and bounds
                    """)

            if ground_contact_time > 250:
                st.markdown("""
                    **Ground Contact Time**: Your ground contact time is relatively long. Consider:
                    - Strides and short sprints to develop faster foot turnover
                    - Running drills emphasizing quick ground contact
                    - Ankle/calf strengthening exercises
                    """)

        st.markdown("</div>", unsafe_allow_html=True)

        # Training recommendations
        st.subheader("Training Recommendations")

        # Different recommendations based on fatigue profile
        if fatigue_resistance < 0.35:  # Sprint specialist
            st.markdown(f"""
                **Recommended Training for Sprint Specialists**:

                1. **Endurance Development**:
                   - Gradually increase aerobic volume
                   - Zone 2 runs: 3-4 × 30-60 minutes per week at {int(cp * 0.7)}-{int(cp * 0.8)} watts
                   - Tempo runs: 1 × 20-30 minutes per week at {int(cp * 0.85)}-{int(cp * 0.95)} watts

                2. **Maintain Strengths**:
                   - Short power intervals: 8-10 × 10-30 seconds at {int(max_power * 0.85)}-{int(max_power * 0.95)} watts
                   - Hill sprints: 8-10 × 10-15 seconds at maximum effort

                3. **Race Strategy**:
                   - For 5K-10K: Slightly negative split recommended (second half faster)
                   - For longer races: Conservative early pace crucial
                """)

        elif fatigue_resistance < 0.45:  # Speed-endurance
            st.markdown(f"""
                **Recommended Training for Speed-Endurance Athletes**:

                1. **Balanced Approach**:
                   - Maintain 80/20 polarized training (80% easy, 20% hard)
                   - Threshold work: 2 × 20-30 minutes per week at {int(cp * 0.95)}-{int(cp * 1.0)} watts
                   - VO2max intervals: 1 × 5-6 × 3 minutes at {int(cp * 1.1)}-{int(cp * 1.15)} watts

                2. **Race-Specific Work**:
                   - 5K: 8-10 × 400m at {int(cp * 1.1)}-{int(cp * 1.15)} watts
                   - 10K: 5-6 × 1000m at {int(cp * 1.05)}-{int(cp * 1.1)} watts
                   - Half-Marathon: 3-4 × 2 miles at {int(cp * 0.95)}-{int(cp * 1.0)} watts

                3. **Race Strategy**:
                   - Even pacing recommended for most distances
                   - Final push in last 10-15% of race
                """)

        else:  # Endurance specialist
            st.markdown(f"""
                **Recommended Training for Endurance Specialists**:

                1. **Speed Development**:
                   - Strides: 8-10 × 20 seconds, 2-3 times per week
                   - Hill sprints: 6-8 × 10 seconds at maximum effort
                   - Plyometric exercises: 2 × per week

                2. **Maintain Strengths**:
                   - Long runs: Weekly run of 90-120 minutes at {int(cp * 0.7)}-{int(cp * 0.8)} watts
                   - Tempo runs: 1-2 × 30-40 minutes at {int(cp * 0.85)}-{int(cp * 0.95)} watts
                   - Sweet spot training: 2 × 20 minutes at {int(cp * 0.88)}-{int(cp * 0.94)} watts

                3. **Race Strategy**:
                   - Leverage endurance by maintaining steady pace
                   - For shorter races (5K-10K): Progressive effort approach
                   - For longer races: Slight negative split recommended
                """)