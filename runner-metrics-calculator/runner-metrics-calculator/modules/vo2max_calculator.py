# --------------------- VO2 MAX CALCULATOR ---------------------#
elif app_mode == "VO2 Max Calculator":
st.header("VO2 Max Calculator")

st.markdown("""
    VO2 Max represents your body's maximum capacity to transport and use oxygen during exercise. 
    It's measured in milliliters of oxygen per kilogram of body weight per minute (ml/kg/min).

    A higher VO2 Max generally indicates better cardiorespiratory fitness.
    """)

# Create tabs for different VO2 Max estimation methods
tabs = st.tabs(["Cooper Test", "Bruce Protocol", "1.5 Mile Run", "Rockport Walk Test", "Sub-maximal Test"])

with tabs[0]:
    st.subheader("Cooper Test")
    st.markdown("""
        The Cooper test involves running as far as possible in 12 minutes. It's a simple field test developed by Dr. Kenneth Cooper in 1968.

        **Scientific Validation**: This test has been validated in multiple studies and shows high correlation (r>0.90) with laboratory VO2 max measurements.

        **Reference**: Cooper, K. H. (1968). A means of assessing maximal oxygen intake: correlation between field and treadmill testing. *JAMA, 203(3)*, 201-204.
        """)

    distance = st.number_input("Distance covered in 12 minutes (meters):", min_value=0, value=2400)
    age = st.number_input("Age (years):", min_value=5, max_value=100, value=30)
    sex = st.radio("Sex:", ["Male", "Female"])

    if st.button("Calculate VO2 Max (Cooper Test)"):
        # Cooper formula (ml/kg/min)
        vo2max = (distance - 504.9) / 44.73

        # Age/sex adjusted (optional)
        if sex == "Female":
            vo2max = vo2max * 0.85  # Women typically 15% lower than men

        # Fitness category based on sex and age
        categories = []
        if sex == "Male":
            if age < 30:
                categories = ["Poor (<33)", "Fair (33-36)", "Good (37-48)", "Excellent (49-53)", "Superior (>53)"]
            elif age < 40:
                categories = ["Poor (<31)", "Fair (31-34)", "Good (35-45)", "Excellent (46-50)", "Superior (>50)"]
            elif age < 50:
                categories = ["Poor (<28)", "Fair (28-32)", "Good (33-42)", "Excellent (43-47)", "Superior (>47)"]
            else:
                categories = ["Poor (<25)", "Fair (25-29)", "Good (30-38)", "Excellent (39-43)", "Superior (>43)"]
        else:  # Female
            if age < 30:
                categories = ["Poor (<28)", "Fair (28-32)", "Good (33-42)", "Excellent (43-47)", "Superior (>47)"]
            elif age < 40:
                categories = ["Poor (<26)", "Fair (26-30)", "Good (31-38)", "Excellent (39-43)", "Superior (>43)"]
            elif age < 50:
                categories = ["Poor (<24)", "Fair (24-28)", "Good (29-36)", "Excellent (37-41)", "Superior (>41)"]
            else:
                categories = ["Poor (<22)", "Fair (22-26)", "Good (27-34)", "Excellent (35-39)", "Superior (>39)"]

        # Determine category
        category = ""
        for cat in categories:
            lower = float(cat.split("(")[1].split("-")[0].replace("<", "").replace(">", ""))
            if "<" in cat and vo2max < lower:
                category = cat.split("(")[0].strip()
                break
            elif ">" in cat and vo2max > lower:
                category = cat.split("(")[0].strip()
                break
            elif "-" in cat.split("(")[1]:
                upper = float(cat.split("-")[1].split(")")[0])
                if lower <= vo2max <= upper:
                    category = cat.split("(")[0].strip()
                    break

        # Display results
        st.markdown(f"""
            <div class="result-box">
                <h3>Your Estimated VO2 Max: <span class="highlight">{vo2max:.1f} ml/kg/min</span></h3>
                <p>Fitness Category: <strong>{category}</strong></p>
                <p>This places you in the {category} category for your age and sex.</p>
            </div>
            """, unsafe_allow_html=True)

        # Display recommendation based on the result
        st.subheader("What does this mean?")
        if category in ["Poor", "Fair"]:
            st.markdown("""
                Your VO2 Max indicates there's significant room for improvement in your aerobic fitness. 
                Consider incorporating:

                - Regular zone 2 training (conversational pace)
                - Gradually increasing weekly mileage
                - 1-2 interval sessions per week (after building base fitness)

                Consistent aerobic training can improve VO2 Max by 15-20% within 8-12 weeks.
                """)
        elif category == "Good":
            st.markdown("""
                You have a solid aerobic base. To further improve:

                - Include threshold training (tempo runs)
                - Add 1-2 interval sessions per week
                - Consider periodized training plans
                - Gradually increase volume before adding intensity

                At this level, improvements will be more gradual, with potential gains of 5-10% over several months.
                """)
        else:
            st.markdown("""
                You have excellent aerobic fitness. To maintain or make incremental improvements:

                - Focus on training specificity for your race goals
                - Incorporate polarized training (80% easy, 20% hard)
                - Consider advanced metrics like running economy
                - Include adequate recovery in your training cycle

                At this high level, gains will be small (1-3%) but can still impact performance significantly.
                """)

with tabs[1]:
    st.subheader("Bruce Protocol")
    st.markdown("""
        The Bruce Protocol is a maximal treadmill test that uses increasing speed and incline until exhaustion.

        **Scientific Validation**: The Bruce Protocol is widely used in clinical and research settings and has been validated against direct VO2 max measurements.

        **Reference**: Bruce, R. A., Kusumi, F., & Hosmer, D. (1973). Maximal oxygen intake and nomographic assessment of functional aerobic impairment in cardiovascular disease. *American Heart Journal, 85(4)*, 546-562.
        """)

    time_min = st.number_input("Time completed on test (minutes):", min_value=0.0, value=12.0, step=0.1)
    time_sec = st.number_input("Seconds (if any):", min_value=0, max_value=59, value=0)
    sex = st.radio("Sex (Bruce):", ["Male", "Female"])

    if st.button("Calculate VO2 Max (Bruce Protocol)"):
        total_time = time_min + (time_sec / 60)

        # Bruce Protocol equations
        if sex == "Male":
            vo2max = 14.8 - (1.379 * total_time) + (0.451 * total_time ** 2) - (0.012 * total_time ** 3)
        else:  # Female
            vo2max = 4.38 * total_time - 3.9

        # Display results
        st.markdown(f"""
            <div class="result-box">
                <h3>Your Estimated VO2 Max: <span class="highlight">{vo2max:.1f} ml/kg/min</span></h3>
            </div>
            """, unsafe_allow_html=True)

        # Display fitness category table
        st.subheader("VO2 Max Classifications")

        # Create VO2 Max classification table
        classification_data = {
            "Category": ["Very Poor", "Poor", "Fair", "Good", "Excellent", "Superior"],
            "Men 20-29": ["<33", "33-36", "37-41", "42-46", "47-51", ">51"],
            "Men 30-39": ["<31", "31-34", "35-39", "40-43", "44-48", ">48"],
            "Men 40-49": ["<28", "28-31", "32-35", "36-39", "40-43", ">43"],
            "Men 50-59": ["<25", "25-28", "29-31", "32-35", "36-38", ">38"],
            "Men 60+": ["<22", "22-25", "26-28", "29-31", "32-34", ">34"],
            "Women 20-29": ["<28", "28-32", "33-36", "37-40", "41-44", ">44"],
            "Women 30-39": ["<27", "27-30", "31-33", "34-37", "38-41", ">41"],
            "Women 40-49": ["<25", "25-27", "28-30", "31-34", "35-37", ">37"],
            "Women 50-59": ["<22", "22-24", "25-27", "28-30", "31-33", ">33"],
            "Women 60+": ["<20", "20-22", "23-25", "26-28", "29-30", ">30"]
        }

        classification_df = pd.DataFrame(classification_data)
        st.table(classification_df)

        st.info(
            "Note: The Bruce Protocol is a maximal test that should only be performed under medical supervision, especially for individuals with known cardiovascular issues or risk factors.")

with tabs[2]:
    st.subheader("1.5 Mile Run Test")
    st.markdown("""
        The 1.5 Mile Run Test requires running 1.5 miles (2.4 km) as fast as possible, and using the time to estimate VO2 max.

        **Scientific Validation**: This test has been validated against laboratory measurements and is widely used in military and fitness assessments.

        **Reference**: George, J. D., Vehrs, P. R., Allsen, P. E., Fellingham, G. W., & Fisher, A. G. (1993). VO2max estimation from a submaximal 1-mile track jog for fit college-age individuals. *Medicine and Science in Sports and Exercise, 25(3)*, 401-406.
        """)

    run_min = st.number_input("1.5 Mile Run Time (minutes):", min_value=5, max_value=30, value=12)
    run_sec = st.number_input("Seconds:", min_value=0, max_value=59, value=30)
    age = st.number_input("Age (1.5 Mile Test):", min_value=18, max_value=65, value=30)
    weight = st.number_input("Weight (kg):", min_value=40.0, max_value=150.0, value=70.0, step=0.1)
    sex_1_5 = st.radio("Sex (1.5 Mile):", ["Male", "Female"])

    if st.button("Calculate VO2 Max (1.5 Mile Run)"):
        run_time_min = run_min + (run_sec / 60)

        # 1.5 Mile Run Test formula
        vo2max = 88.02 - (0.1656 * weight) - (2.76 * run_time_min) + (3.716 * (1 if sex_1_5 == "Male" else 0))

        # Display results
        st.markdown(f"""
            <div class="result-box">
                <h3>Your Estimated VO2 Max: <span class="highlight">{vo2max:.1f} ml/kg/min</span></h3>
            </div>
            """, unsafe_allow_html=True)

        # Compare to average for age and sex
        avg_vo2max = 0
        if sex_1_5 == "Male":
            if age < 30:
                avg_vo2max = 44
            elif age < 40:
                avg_vo2max = 42
            elif age < 50:
                avg_vo2max = 39
            else:
                avg_vo2max = 36
        else:  # Female
            if age < 30:
                avg_vo2max = 38
            elif age < 40:
                avg_vo2max = 36
            elif age < 50:
                avg_vo2max = 33
            else:
                avg_vo2max = 30

        diff = ((vo2max - avg_vo2max) / avg_vo2max) * 100

        st.markdown(f"""
            Your VO2 Max is {diff:.1f}% {'above' if diff >= 0 else 'below'} the average for your age and sex.
            """)

        # Visualization - where you stand compared to population
        st.subheader("How you compare to others")

        # Create data for normal distribution of VO2 max values
        x = np.linspace(avg_vo2max - 15, avg_vo2max + 15, 100)
        y = np.exp(-0.5 * ((x - avg_vo2max) / 5) ** 2) / (5 * np.sqrt(2 * np.pi))

        fig = go.Figure()

        # Add normal distribution curve
        fig.add_trace(go.Scatter(
            x=x,
            y=y,
            mode='lines',
            name='Population Distribution',
            line=dict(color='#E6754E', width=2)
        ))

        # Add vertical line for user's value
        fig.add_trace(go.Scatter(
            x=[vo2max, vo2max],
            y=[0, max(y) * 1.2],
            mode='lines',
            name='Your VO2 Max',
            line=dict(color='#4E97E6', width=2, dash='dash')
        ))

        fig.update_layout(
            title=f"Your VO2 Max Compared to {sex_1_5}s Age {age}",
            xaxis_title="VO2 Max (ml/kg/min)",
            yaxis_title="Probability Density",
            showlegend=True
        )

        st.plotly_chart(fig)

with tabs[3]:
    st.subheader("Rockport Walking Test")
    st.markdown("""
        The Rockport Walking Test is a submaximal test that involves walking 1 mile (1.6 km) as quickly as possible.
        It's suitable for individuals who cannot perform running tests due to fitness or health limitations.

        **Scientific Validation**: This test was validated in the original Rockport Walking Institute study and has been confirmed in subsequent research.

        **Reference**: Kline, G. M., Porcari, J. P., Hintermeister, R., Freedson, P. S., Ward, A., McCarron, R. F., ... & Rippe, J. M. (1987). Estimation of VO2max from a one-mile track walk, gender, age, and body weight. *Medicine and Science in Sports and Exercise, 19(3)*, 253-259.
        """)

    walk_min = st.number_input("1 Mile Walk Time (minutes):", min_value=10, max_value=30, value=15)
    walk_sec = st.number_input("Seconds (Walk Test):", min_value=0, max_value=59, value=0)
    heart_rate = st.number_input("Heart Rate at End of Walk (bpm):", min_value=60, max_value=200, value=120)
    age_walk = st.number_input("Age (Rockport Test):", min_value=18, max_value=80, value=35)
    weight_lb = st.number_input("Weight (lbs):", min_value=80.0, max_value=330.0, value=154.0, step=0.1)
    sex_walk = st.radio("Sex (Rockport):", ["Male", "Female"])

    if st.button("Calculate VO2 Max (Rockport Walking Test)"):
        walk_time_min = walk_min + (walk_sec / 60)

        # Rockport Walking Test formula
        gender_factor = 1 if sex_walk == "Male" else 0
        vo2max = 132.853 - (0.0769 * weight_lb) - (0.3877 * age_walk) + (6.315 * gender_factor) - (
                    3.2649 * walk_time_min) - (0.1565 * heart_rate)

        # Display results
        st.markdown(f"""
            <div class="result-box">
                <h3>Your Estimated VO2 Max: <span class="highlight">{vo2max:.1f} ml/kg/min</span></h3>
            </div>
            """, unsafe_allow_html=True)

        st.info(
            "The Rockport Walking Test is particularly useful for beginners, older individuals, or those returning from injury who cannot safely perform running tests.")

        # Guidelines based on the result
        if vo2max < 30:
            st.markdown("""
                **Recommended Training Focus:**
                - Begin with consistent walking, gradually increasing duration
                - Introduce walk-jog intervals as fitness improves
                - Focus on building consistency rather than intensity
                - Aim for 3-4 sessions per week, 20-30 minutes each
                """)
        elif vo2max < 40:
            st.markdown("""
                **Recommended Training Focus:**
                - Progress to continuous jogging at conversational pace
                - Gradually increase duration before increasing intensity
                - Add 1 day per week of hill walking or light intervals
                - Consider strength training to support running development
                """)
        else:
            st.markdown("""
                **Recommended Training Focus:**
                - Transition to a running-focused program if desired
                - Consider training plans appropriate for your goals
                - Include a mix of easy runs and structured workouts
                - Use the other calculators to determine appropriate training paces
                """)

with tabs[4]:
    st.subheader("Submaximal Test (Astrand-Rhyming)")
    st.markdown("""
        The Astrand-Rhyming submaximal test estimates VO2 max using heart rate response to a standardized workload.
        This method is useful when maximal testing is not appropriate or possible.

        **Scientific Validation**: The Astrand-Rhyming test has been validated in numerous studies and shows good correlation with direct measurements in most populations.

        **Reference**: Astrand, P. O., & Ryhming, I. (1954). A nomogram for calculation of aerobic capacity (physical fitness) from pulse rate during submaximal work. *Journal of Applied Physiology, 7(2)*, 218-221.
        """)

    workload = st.number_input("Workload (Watts):", min_value=50, max_value=300, value=100)
    hr_steady = st.number_input("Steady-State Heart Rate (bpm):", min_value=80, max_value=180, value=130)
    age_sub = st.number_input("Age (Submaximal Test):", min_value=18, max_value=65, value=40)
    weight_sub = st.number_input("Weight (kg, Submaximal):", min_value=40.0, max_value=150.0, value=70.0, step=0.1)
    sex_sub = st.radio("Sex (Submaximal):", ["Male", "Female"])

    if st.button("Calculate VO2 Max (Submaximal Test)"):
        # Convert workload from watts to kgm/min (1 watt = 6.12 kgm/min)
        workload_kgm = workload * 6.12

        # Oxygen uptake during test (L/min)
        if sex_sub == "Male":
            if hr_steady <= 120:
                vo2_test = (workload_kgm + 300) / 200
            else:
                vo2_test = workload_kgm / 200
        else:  # Female
            if hr_steady <= 120:
                vo2_test = (workload_kgm + 300) / 170
            else:
                vo2_test = workload_kgm / 170

        # Predicted maximal heart rate
        hr_max = 220 - age_sub

        # VO2 max calculation
        vo2max_l = vo2_test * hr_max / hr_steady

        # Age correction factor
        age_factor = 1.0
        if age_sub >= 25:
            age_factor = (0.01 * (age_sub - 25))
            age_factor = 1.0 - age_factor

        # Apply age correction
        vo2max_l = vo2max_l * age_factor

        # Convert to ml/kg/min
        vo2max = vo2max_l * 1000 / weight_sub

        # Display results
        st.markdown(f"""
            <div class="result-box">
                <h3>Your Estimated VO2 Max: <span class="highlight">{vo2max:.1f} ml/kg/min</span></h3>
                <p>Absolute VO2 Max: {vo2max_l:.2f} L/min</p>
            </div>
            """, unsafe_allow_html=True)

        st.info(
            "Submaximal tests are less accurate than maximal tests but are safer for untrained individuals or those with health concerns. For most accurate results, ensure you reach a true steady-state heart rate during the test.")