# --------------------- RUNNING FORM ANALYSIS ---------------------#
elif app_mode == "Running Form Analysis":
st.header("Running Form Analysis")

st.markdown("""
    Running form plays a crucial role in performance, efficiency, and injury prevention.
    This tool helps analyze key aspects of running form and provides recommendations for improvement.

    While a comprehensive form analysis ideally includes video assessment by a coach or professional,
    this tool can help identify potential areas for improvement.

    **Scientific Validation**: The metrics and recommendations provided are based on research in biomechanics and running economy.

    **References**:
    - Moore, I. S. (2016). Is There an Economical Running Technique? A Review of Modifiable Biomechanical Factors Affecting Running Economy. *Sports Medicine, 46(6)*, 793-807.
    - Napier, C., Cochrane, C. K., Taunton, J. E., & Hunt, M. A. (2015). Gait modifications to change lower extremity gait biomechanics in runners: a systematic review. *British Journal of Sports Medicine, 49(21)*, 1382-1388.
    """)

analysis_type = st.radio(
    "Analysis Type:",
    ["Self-Assessment", "Metrics-Based Analysis", "Common Issues Troubleshooter"]
)

if analysis_type == "Self-Assessment":
    st.subheader("Running Form Self-Assessment")

    st.markdown("""
        This self-assessment helps identify potential form issues based on your observations and experiences.
        Answer each question to the best of your ability.
        """)

    # Cadence and stride
    st.markdown("### Cadence and Stride")
    cadence = st.radio(
        "What is your typical running cadence (steps per minute)?",
        ["I don't know", "Less than 160", "160-170", "170-180", "180-190", "More than 190"]
    )

    overstriding = st.radio(
        "Do you feel like you're reaching too far forward with each step?",
        ["Yes, I land well in front of my body", "Sometimes/Not sure", "No, I land under my body"]
    )

    # Foot strike and impact
    st.markdown("### Foot Strike and Impact")
    foot_strike = st.radio(
        "How do your feet typically contact the ground?",
        ["Heel first (heel strike)", "Midfoot (whole foot)", "Forefoot (ball of foot)", "Not sure"]
    )

    impact = st.radio(
        "How would you describe the sound/feeling of your footstrike?",
        ["Loud/heavy landing", "Moderate impact", "Quiet/light landing", "Not sure"]
    )

    # Upper body
    st.markdown("### Upper Body")
    arm_swing = st.radio(
        "How do your arms move when you run?",
        ["Cross in front of my body", "Swing forward and back alongside my body", "Barely move at all", "Not sure"]
    )

    posture = st.radio(
        "How would you describe your running posture?",
        ["Leaning forward from the waist", "Upright with slight forward lean", "Leaning backward slightly", "Not sure"]
    )

    # Injuries and discomfort
    st.markdown("### Injuries and Discomfort")
    injuries = st.multiselect(
        "Have you experienced any of these injuries in the past year?",
        ["Knee pain", "Shin splints", "IT band issues", "Plantar fasciitis", "Achilles tendinitis",
         "Hip pain", "Lower back pain", "Ankle sprains", "Stress fractures", "None of the above"]
    )

    fatigue = st.radio(
        "Where do you feel most fatigued during/after runs?",
        ["Calves/Achilles", "Quads/Knees", "Hips/Glutes", "Lower back", "Upper body/shoulders", "Generally all over",
         "Varies by run"]
    )

    # Performance and efficiency
    st.markdown("### Performance and Efficiency")
    breathing = st.radio(
        "How would you describe your breathing when running at conversation pace?",
        ["Labored/difficult even at easy pace", "Comfortable at easy pace, quickly labored when increasing pace",
         "Controlled and rhythmic at moderate paces", "Rarely a limiting factor"]
    )

    hills = st.radio(
        "How do you feel running uphill compared to flat terrain?",
        ["Much more difficult than seems normal", "Moderately more difficult (expected)",
         "Strong on hills compared to flat ground", "No significant difference"]
    )

    if st.button("Analyze Running Form"):
        # Calculate form score and identify issues
        issues = []
        recommendations = []

        # Assess cadence and stride
        if cadence == "Less than 160":
            issues.append("Low cadence (increased injury risk)")
            recommendations.append("""
                **Increase Cadence**:
                - Aim for 170-180 steps per minute
                - Use a metronome app or music with appropriate BPM
                - Start with 5% increase for 5 minutes, gradually extend
                """)

        if overstriding == "Yes, I land well in front of my body":
            issues.append("Overstriding (braking force and impact)")
            recommendations.append("""
                **Reduce Overstriding**:
                - Focus on landing with foot closer to center of mass
                - Slightly increase cadence to reduce stride length
                - Practice "running tall" with slight forward lean from ankles
                """)

        # Assess foot strike
        if foot_strike == "Heel first (heel strike)" and impact == "Loud/heavy landing":
            issues.append("Heavy heel striking (increased impact forces)")
            recommendations.append("""
                **Improve Foot Strike**:
                - Work on landing more lightly
                - Consider transitioning toward midfoot strike gradually
                - Focus on "quiet feet" during some training runs
                - Strengthen calves and feet for transition
                """)

        # Assess upper body
        if arm_swing == "Cross in front of my body":
            issues.append("Arms crossing midline (rotational inefficiency)")
            recommendations.append("""
                **Improve Arm Swing**:
                - Practice arms swinging forward and back, not across body
                - Maintain 90° bend at elbow
                - Relax shoulders and hands (hold "potato chips" lightly)
                - Imagine arms as pendulums pulling you forward
                """)

        if posture == "Leaning forward from the waist" or posture == "Leaning backward slightly":
            issues.append("Suboptimal posture (energy inefficiency)")
            recommendations.append("""
                **Improve Posture**:
                - Focus on "running tall" with good alignment
                - Slight forward lean should come from ankles, not waist
                - Engage core muscles throughout run
                - Regular core strengthening exercises
                """)

        # Assess based on injuries
        injury_recommendations = {
            "Knee pain": "- Evaluate stride length and foot strike\n- Check for hip drop or knee collapse\n- Consider shoe choice and potential orthotics",
            "Shin splints": "- Gradual progression in training load\n- Calf strengthening and stretching\n- Evaluate foot strike and impact forces",
            "IT band issues": "- Hip and glute strengthening\n- Address hip drop and knee movement\n- Cross-training and recovery",
            "Plantar fasciitis": "- Foot and calf strengthening\n- Proper recovery and stretching\n- Evaluate running shoes and surfaces",
            "Achilles tendinitis": "- Gradual progression with speedwork and hills\n- Calf strengthening and eccentric loading\n- Check for appropriate foot strike",
            "Hip pain": "- Core and hip stabilization exercises\n- Address potential leg length discrepancies\n- Evaluate running symmetry",
            "Lower back pain": "- Core strengthening focus\n- Evaluate posture during running\n- Address potential muscular imbalances",
            "Ankle sprains": "- Balance and proprioception training\n- Ankle strengthening exercises\n- Consider trail-specific training",
            "Stress fractures": "- Bone health (nutrition, vitamin D, calcium)\n- Gradual load progression\n- Impact management and recovery"
        }

        for injury in injuries:
            if injury != "None of the above" and injury in injury_recommendations:
                issues.append(f"{injury} (potential form contributing factor)")
                recommendations.append(f"""
                    **{injury} Recommendations**:
                    {injury_recommendations[injury]}
                    """)

        # Assess based on fatigue patterns
        fatigue_recommendations = {
            "Calves/Achilles": "- Evaluate foot strike (potential forefoot emphasis)\n- Check for sufficient hip extension\n- Address calf flexibility and strength",
            "Quads/Knees": "- Assess downhill running technique\n- Check for overstriding\n- Evaluate eccentric quad strength",
            "Hips/Glutes": "- Focus on hip mobility and strength\n- Check for hip drop during stance phase\n- Evaluate glute activation during running",
            "Lower back": "- Core strength and stability training\n- Assess posture during running\n- Check for anterior pelvic tilt",
            "Upper body/shoulders": "- Focus on relaxed shoulders and arms\n- Check for tension in neck and upper back\n- Assess arm swing efficiency"
        }

        if fatigue in fatigue_recommendations:
            issues.append(f"{fatigue} fatigue (potential form issue)")
            recommendations.append(f"""
                **Fatigue Pattern Recommendations**:
                {fatigue_recommendations[fatigue]}
                """)

        # Assess breathing and hills
        if breathing == "Labored/difficult even at easy pace":
            issues.append("Breathing difficulty (potential efficiency issue)")
            recommendations.append("""
                **Breathing Improvement**:
                - Practice rhythmic breathing (e.g., 3:3 or 2:2 inhale:exhale)
                - Ensure you're truly running at easy pace (heart rate zone 2)
                - Consider diaphragmatic breathing exercises
                - Check for excessive tension in shoulders and chest
                """)

        if hills == "Much more difficult than seems normal":
            issues.append("Hill difficulty (potential form/strength issue)")
            recommendations.append("""
                **Hill Running Improvement**:
                - Focus on shorter strides, increased cadence on hills
                - Practice arm drive and knee lift
                - Incorporate hill repeats progressively
                - Strengthen hip flexors and extensors
                """)

        # Calculate overall form score
        form_score = 100 - (len(issues) * 10)
        form_score = max(0, min(100, form_score))

        # Display results
        st.markdown("<div class='result-box'>", unsafe_allow_html=True)
        st.subheader("Running Form Analysis Results")

        # Form score
        score_category = ""
        if form_score >= 80:
            score_category = "Excellent"
        elif form_score >= 60:
            score_category = "Good"
        elif form_score >= 40:
            score_category = "Fair"
        else:
            score_category = "Needs Improvement"

        st.markdown(f"""
            <h3>Form Score: <span class="highlight">{form_score}/100</span> ({score_category})</h3>
            """, unsafe_allow_html=True)

        if issues:
            st.markdown("### Identified Form Issues:")
            for issue in issues:
                st.markdown(f"- {issue}")
        else:
            st.markdown("### No significant form issues identified!")

        st.markdown("</div>", unsafe_allow_html=True)

        # Display recommendations
        if recommendations:
            st.subheader("Recommendations for Improvement")

            for i, recommendation in enumerate(recommendations):
                with st.expander(f"Recommendation {i + 1}: {issues[i].split('(')[0].strip()}"):
                    st.markdown(recommendation)

            st.info("""
                **Implementation Tips:**
                - Focus on one form change at a time
                - Implement changes gradually during easy runs
                - Consider filming yourself before and after
                - Use shortened distances when first implementing changes
                - Be patient - form changes take time to become natural
                """)

        # Form drills and exercises
        st.subheader("Recommended Form Drills")

        st.markdown("""
            **Foundation Drills (for all runners):**

            1. **High Knees**: 2-3 × 30m
               - Exaggerated knee lift with proper posture
               - Develops hip flexor strength and knee drive

            2. **Butt Kicks**: 2-3 × 30m
               - Kick heels toward buttocks rhythmically
               - Improves hamstring recovery and turnover

            3. **A-Skip**: 2-3 × 30m
               - High knee lift with slight skip
               - Focuses on proper foot placement and posture

            4. **Straight-Leg Bounds**: 2-3 × 30m
               - Extended legs with forward movement
               - Develops hip extension power

            **Implement these drills 1-2 times weekly before quality sessions.**
            """)

        # Additional resources
        st.subheader("Additional Resources")

        st.markdown("""
            **Video Analysis Options:**
            - Self-filming (set up phone at side and back angles)
            - Run specialty store gait analysis (often free with shoe purchase)
            - Professional biomechanical assessment (sports medicine clinics)

            **Recommended Strengthening Exercises:**
            - Single-leg balance exercises
            - Hip bridges and variations
            - Planks and core stability work
            - Calf raises and eccentric heel drops
            - Lunges and split squats
            """)

elif analysis_type == "Metrics-Based Analysis":
    st.subheader("Metrics-Based Form Analysis")

    st.markdown("""
        This analysis uses specific running metrics to evaluate form efficiency and identify areas for improvement.
        Enter the values you have available from your running watch, tracking app, or running assessment.
        """)

    col1, col2 = st.columns(2)

    with col1:
        # Cadence metrics
        st.markdown("### Cadence Metrics")
        cadence_available = st.checkbox("I have cadence data")

        if cadence_available:
            cadence = st.number_input("Average Cadence (steps per minute):", min_value=120, max_value=220, value=170)
            height_cm = st.number_input("Your Height (cm):", min_value=120, max_value=220, value=170)

            # Convert height to determine optimal cadence range
            height_inches = height_cm / 2.54
            height_adjustment = (70 - height_inches) * 0.5
            optimal_cadence = 180 + height_adjustment
            lower_optimal = optimal_cadence - 5
            upper_optimal = optimal_cadence + 5

        # Vertical oscillation metrics
        st.markdown("### Vertical Oscillation")
        vo_available = st.checkbox("I have vertical oscillation data")

        if vo_available:
            vert_osc = st.number_input("Vertical Oscillation (cm):", min_value=4.0, max_value=15.0, value=9.5, step=0.1)
            vo_ratio = st.number_input("Vertical Ratio (oscillation:distance %):", min_value=1.0, max_value=15.0,
                                       value=7.0, step=0.1)

        # Ground contact metrics
        st.markdown("### Ground Contact Time")
        gct_available = st.checkbox("I have ground contact data")

        if gct_available:
            contact_time = st.number_input("Ground Contact Time (ms):", min_value=150, max_value=350, value=240)
            gct_balance = st.slider("GCT Balance (L/R %):", min_value=45, max_value=55, value=50)

    with col2:
        # Power metrics
        st.markdown("### Running Power")
        power_available = st.checkbox("I have running power data")

        if power_available:
            power = st.number_input("Running Power (watts):", min_value=100, max_value=500, value=250)
            weight = st.number_input("Body Weight (kg):", min_value=40.0, max_value=150.0, value=70.0, step=0.1)
            form_power = st.number_input("Form Power (watts):", min_value=20, max_value=100, value=50)
            leg_spring_stiffness = st.number_input("Leg Spring Stiffness (kN/m):", min_value=5.0, max_value=30.0,
                                                   value=12.0, step=0.1)

        # Efficiency metrics
        st.markdown("### Running Efficiency")
        efficiency_available = st.checkbox("I have efficiency data")

        if efficiency_available:
            efficiency_option = st.radio(
                "Efficiency Metric Type:",
                ["Running Economy (ml/kg/km)", "Energy Cost (kcal/kg/km)", "Other"]
            )

            if efficiency_option == "Running Economy (ml/kg/km)":
                running_economy = st.number_input("Running Economy (ml/kg/km):", min_value=150.0, max_value=300.0,
                                                  value=200.0, step=1.0)
            elif efficiency_option == "Energy Cost (kcal/kg/km)":
                energy_cost = st.number_input("Energy Cost (kcal/kg/km):", min_value=0.7, max_value=1.5, value=1.0,
                                              step=0.01)
            else:
                efficiency_other = st.text_input("Other Efficiency Metric:")
                efficiency_value = st.number_input("Value:", min_value=0.0, max_value=1000.0, value=0.0)

    if st.button("Analyze Form Based on Metrics"):
        # Create lists to store form insights and recommendations
        insights = []
        recommendations = []
        scores = {}

        # Analysis logic for each metric would go here...
        # Example for cadence:
        if cadence_available:
            if cadence < lower_optimal:
                cadence_score = 50 + ((cadence - 150) / (lower_optimal - 150)) * 30
                insights.append(
                    f"Cadence ({cadence} spm) is below optimal range for your height ({lower_optimal:.0f}-{upper_optimal:.0f} spm)")
                recommendations.append("""
                    **Cadence Improvement**:
                    - Gradually increase cadence by 5-10%
                    - Use metronome app during portions of runs
                    - Focus on shorter, quicker steps rather than longer strides
                    - Practice high-knee drills and fast feet exercises
                    """)
            elif cadence > upper_optimal:
                cadence_score = 80 + ((220 - cadence) / (220 - upper_optimal)) * 10
                insights.append(
                    f"Cadence ({cadence} spm) is above optimal range for your height ({lower_optimal:.0f}-{upper_optimal:.0f} spm)")
                recommendations.append("""
                    **Cadence Optimization**:
                    - Slightly higher cadence is generally fine if comfortable
                    - Ensure you're not sacrificing stride length unnecessarily
                    - Monitor for signs of excessive fatigue in calves/Achilles
                    - Focus on relaxed form at current cadence
                    """)
            else:
                cadence_score = 90
                insights.append(
                    f"Cadence ({cadence} spm) is within optimal range for your height ({lower_optimal:.0f}-{upper_optimal:.0f} spm)")

            scores["Cadence"] = min(100, max(0, cadence_score))

        # Similar analysis for other metrics would follow...

        # Display results with insights and recommendations
        st.markdown("<div class='result-box'>", unsafe_allow_html=True)
        st.subheader("Metrics-Based Form Analysis Results")

        if insights:
            st.markdown("### Key Insights:")
            for insight in insights:
                st.markdown(f"- {insight}")
        else:
            st.markdown("### No metrics available for analysis!")

        st.markdown("</div>", unsafe_allow_html=True)

        # Display recommendations
        if recommendations:
            st.subheader("Recommendations for Improvement")

            for i, recommendation in enumerate(recommendations):
                with st.expander(f"Recommendation {i + 1}"):
                    st.markdown(recommendation)

else:  # Common Issues Troubleshooter
    st.subheader("Common Running Form Issues Troubleshooter")

    st.markdown("""
        This tool helps identify and address common running form issues based on symptoms or concerns.
        Select the issues you're experiencing to receive targeted recommendations.
        """)

    # Create categories of common form issues
    form_categories = [
        "Impact & Pain Issues",
        "Efficiency & Performance Issues",
        "Stride & Gait Issues",
        "Upper Body Issues",
        "Biomechanical Issues"
    ]

    selected_category = st.selectbox("Select Issue Category:", form_categories)

    # Define issues for each category
    issues_by_category = {
        "Impact & Pain Issues": [
            "Shin splints/lower leg pain",
            "Knee pain during/after running",
            "IT band issues",
            "Plantar fasciitis/foot pain",
            "Hip/lower back pain",
            "Excessive soreness after runs",
            "Joint pain on hard surfaces"
        ],
        "Efficiency & Performance Issues": [
            "Feeling slow despite high effort",
            "Tiring quickly during runs",
            "Poor uphill running performance",
            "Limited finishing kick/sprint",
            "Breathing difficulties at pace",
            "High heart rate at easy pace",
            "Bonking/hitting the wall regularly"
        ],
        "Stride & Gait Issues": [
            "Overstriding/reaching forward",
            "Heavy foot strikes/loud running",
            "Short/choppy stride",
            "Inconsistent pacing",
            "Toe running/minimal heel contact",
            "Excessive heel striking",
            "Asymmetrical stride/limp"
        ],
        "Upper Body Issues": [
            "Shoulder/neck tension while running",
            "Arms crossing body midline",
            "Excessive upper body rotation",
            "Arm swing issues/limited arm motion",
            "Forward head posture",
            "Hunched shoulders/rounded back",
            "Hand/wrist tension"
        ],
        "Biomechanical Issues": [
            "Foot pronation (collapsing inward)",
            "Supination (rigid/high arches)",
            "Knee valgus (inward collapse)",
            "Hip drop during stance phase",
            "Limited hip extension",
            "Bouncy/vertical running style",
            "Pelvic tilt issues"
        ]
    }

    # Display issues for selected category
    selected_issues = st.multiselect(
        "Select the issues you're experiencing:",
        issues_by_category[selected_category]
    )

    if st.button("Get Recommendations"):
        if not selected_issues:
            st.warning("Please select at least one issue to receive recommendations.")
        else:
            # For each selected issue, display targeted recommendations
            for issue in selected_issues:
                st.markdown(f"<div class='result-box'>", unsafe_allow_html=True)
                st.subheader(f"Analysis: {issue}")

                # Recommendations would be displayed here based on the specific issue
                st.markdown("""
                    **Likely Causes**:
                    Various biomechanical and training factors that contribute to this issue

                    **Form Recommendations**:
                    Specific technique adjustments to address the issue

                    **Supportive Exercises**:
                    Strengthening and mobility exercises to support form changes

                    **Additional Advice**:
                    Training modifications, equipment considerations, and recovery strategies
                    """)

                st.markdown("</div>", unsafe_allow_html=True)

            # General implementation advice
            st.subheader("Implementation Strategy")

            st.markdown("""
                **How to address multiple form issues:**

                1. **Prioritize** - Focus on one primary form change at a time
                2. **Integration** - Begin with short form-focused segments (5-10 minutes)
                3. **Progression** - Gradually extend duration of form focus
                4. **Feedback** - Use video, mirrors, or coaching for regular assessment
                5. **Consistency** - Practice new movement patterns regularly

                **Timeline expectations:**
                - Initial awareness: 1-2 weeks
                - Conscious competence: 2-4 weeks
                - Unconscious integration: 4-8+ weeks

                **Remember**: Form changes require patience and consistent practice!
                """)