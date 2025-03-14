#--------------------- TRAINING LOAD & RECOVERY ---------------------#
elif app_mode == "Training Load & Recovery":
    st.header("Training Load & Recovery Calculator")
    
    st.markdown("""
    Training load quantifies the stress placed on your body through running, while recovery metrics help
    assess your body's response to that stress. Balancing these factors is crucial for optimal performance
    and injury prevention.
    
    This calculator provides various methods to track training load and estimate recovery needs.
    
    **Scientific Validation**: These training load and recovery metrics are based on established research in exercise physiology and sports science.
    
    **References**:
    - Banister, E. W. (1991). Modeling elite athletic performance. *Physiological testing of elite athletes*, 403-424.
    - Foster, C. (1998). Monitoring training in athletes with reference to overtraining syndrome. *Medicine and Science in Sports and Exercise, 30(7)*, 1164-1168.
    - Hulin, B. T., Gabbett, T. J., Lawson, D. W., Caputi, P., & Sampson, J. A. (2016). The acute:chronic workload ratio predicts injury: high chronic workload may decrease injury risk in elite rugby league players. *British Journal of Sports Medicine, 50(4)*, 231-236.
    """)
    
    load_mode = st.radio(
        "Calculator Type:",
        ["RPE-Based Load", "Heart Rate-Based Load", "ACWR (Acute:Chronic Workload Ratio)", "Recovery Metrics"]
    )
    
    if load_mode == "RPE-Based Load":
        st.subheader("RPE-Based Training Load")
        
        st.markdown("""
        Session RPE (sRPE) is a simple yet effective method to quantify training load by multiplying the session
        duration by the Rating of Perceived Exertion (RPE).
        
        sRPE Load = Duration (minutes) × RPE (1-10 scale)
        """)
        
        col1, col2 = st.columns([3, 2])
        
        with col1:
            # Option to enter multiple sessions or just one session
            calculation_type = st.radio(
                "Calculation Type:",
                ["Single Session", "Weekly Training Load"]
            )
            
            if calculation_type == "Single Session":
                # Single session input
                duration = st.number_input("Session Duration (minutes):", min_value=10, max_value=300, value=60)
                rpe = st.slider("Session RPE (1-10):", min_value=1, max_value=10, value=6)
                
                # Description of RPE values
                st.markdown("""
                **RPE Scale Guide**:
                1. Very, very easy (rest)
                2. Easy (recovery run)
                3. Moderate (easy run)
                4. Somewhat hard (steady run)
                5. Hard (tempo run)
                6. Hard+ (threshold run)
                7. Very hard (interval session)
                8. Very, very hard (hard intervals)
                9. Near maximal (race effort)
                10. Maximal (sprint/all-out effort)
                """)
            
            else:  # Weekly Training Load
                st.markdown("### Enter your training sessions for the week:")
                
                # Create inputs for each day of the week
                days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
                durations = {}
                rpes = {}
                
                for day in days:
                    st.markdown(f"**{day}**")
                    col1a, col1b = st.columns(2)
                    with col1a:
                        durations[day] = st.number_input(f"Duration (min):", min_value=0, max_value=300, value=0, key=f"dur_{day}")
                    with col1b:
                        rpes[day] = st.slider(f"RPE (1-10):", min_value=1, max_value=10, value=5, key=f"rpe_{day}", disabled=(durations[day] == 0))
                    
                    # Add spacer
                    st.markdown("---")
        
        with col2:
            if calculation_type == "Single Session":
                st.markdown("""
                ### Benefits of RPE-Based Load
                
                - **Simplicity**: Easy to implement without special equipment
                - **Subjective Feedback**: Captures individual perception of effort
                - **Comprehensive**: Accounts for both physical and psychological stress
                - **Adaptable**: Works across different training modalities
                
                ### Interpreting Session Load
                
                - **<150**: Very light training session
                - **150-300**: Light to moderate session
                - **300-450**: Moderate to hard session
                - **450-600**: Hard session
                - **>600**: Very hard/high load session
                """)
            else:
                st.markdown("""
                ### Weekly Training Load Guidelines
                
                **By Experience Level**:
                - **Beginners**: 1000-1500 units
                - **Intermediate**: 1500-2500 units
                - **Advanced**: 2500-3500 units
                - **Elite**: 3500+ units
                
                **Load Distribution**:
                - Hard days (RPE 7-10): 30-40% of weekly load
                - Moderate days (RPE 4-6): 30-40% of weekly load
                - Easy days (RPE 1-3): 20-40% of weekly load
                
                **Signs of Excessive Load**:
                - Elevated resting heart rate
                - Persistent fatigue
                - Decreasing performance
                - Sleep disturbances
                - Mood changes
                """)
        
        if st.button("Calculate RPE-Based Load"):
            if calculation_type == "Single Session":
                # Calculate load for single session
                session_load = duration * rpe
                
                # Display result
                st.markdown("<div class='result-box'>", unsafe_allow_html=True)
                st.subheader("Training Load Result")
                
                st.markdown(f"""
                <h3>Session RPE Load: <span class="highlight">{session_load}</span> arbitrary units</h3>
                """, unsafe_allow_html=True)
                
                # Categorize the load
                load_category = ""
                if session_load < 150:
                    load_category = "Very Light"
                elif session_load < 300:
                    load_category = "Light to Moderate"
                elif session_load < 450:
                    load_category = "Moderate to Hard"
                elif session_load < 600:
                    load_category = "Hard"
                else:
                    load_category = "Very Hard"
                
                st.markdown(f"**Session Intensity**: {load_category}")
                
                # Fatigue impact estimate
                fatigue_impact = session_load / 100
                recovery_estimate = 0
                
                if session_load < 200:
                    recovery_estimate = "Minimal (ready for quality training next day)"
                elif session_load < 350:
                    recovery_estimate = "Low (easy training possible next day)"
                elif session_load < 500:
                    recovery_estimate = "Moderate (24 hours for full recovery)"
                elif session_load < 650:
                    recovery_estimate = "High (36-48 hours for full recovery)"
                else:
                    recovery_estimate = "Very High (48+ hours for full recovery)"
                
                st.markdown(f"""
                **Fatigue Impact**: {fatigue_impact:.1f}/10
                
                **Recovery Needs**: {recovery_estimate}
                """)
                
                st.markdown("</div>", unsafe_allow_html=True)
                
                # Recovery recommendations
                st.subheader("Recovery Recommendations")
                
                st.markdown(f"""
                Based on your session load of {session_load} units:
                
                **Nutrition**:
                - Consume carbohydrates within 30 minutes post-session ({int(0.5 * duration)} g recommended)
                - Ensure adequate protein intake ({int(0.25 * duration)} g recommended)
                - Hydrate with {int(0.5 * duration)} oz of fluid
                
                **Recovery Activities**:
                - {'Active recovery (20-30 min easy activity)' if session_load > 350 else 'Light mobility work'}
                - {'Foam rolling and targeted stretching' if session_load > 300 else 'Brief stretching for major muscle groups'}
                - {'Consider cold therapy for larger muscle groups' if session_load > 500 else ''}
                
                **Next Training Session**:
                - {'Allow 48 hours before next high-intensity session' if session_load > 500 else 'Allow 24 hours before next high-intensity session' if session_load > 300 else 'Next day training can include quality work'}
                """)
            
            else:  # Weekly Training Load
                # Calculate load for each day and total weekly load
                daily_loads = {}
                total_weekly_load = 0
                training_days = 0
                
                for day in days:
                    if durations[day] > 0:
                        daily_loads[day] = durations[day] * rpes[day]
                        total_weekly_load += daily_loads[day]
                        training_days += 1
                    else:
                        daily_loads[day] = 0
                
                # Calculate average daily load and monotony
                if training_days > 0:
                    avg_daily_load = total_weekly_load / 7  # Use 7 for all days of the week
                    
                    # Calculate standard deviation of daily loads
                    squared_diffs = [(daily_loads[day] - avg_daily_load)**2 for day in days]
                    variance = sum(squared_diffs) / 7
                    std_dev = variance**0.5
                    
                    # Training monotony (average load / standard deviation)
                    training_monotony = avg_daily_load / std_dev if std_dev > 0 else 0
                    
                    # Training strain (total load × monotony)
                    training_strain = total_weekly_load * training_monotony
                else:
                    avg_daily_load = 0
                    training_monotony = 0
                    training_strain = 0
                
                # Display result
                st.markdown("<div class='result-box'>", unsafe_allow_html=True)
                st.subheader("Weekly Training Load Analysis")
                
                st.markdown(f"""
                <h3>Total Weekly Load: <span class="highlight">{total_weekly_load}</span> arbitrary units</h3>
                
                **Average Daily Load**: {avg_daily_load:.1f} units
                
                **Training Monotony**: {training_monotony:.2f} (variability index)
                
                **Training Strain**: {training_strain:.1f} units
                """, unsafe_allow_html=True)
                
                # Categorize the weekly load
                load_category = ""
                if total_weekly_load < 1000:
                    load_category = "Low (Beginner/Recovery)"
                elif total_weekly_load < 2000:
                    load_category = "Moderate (Intermediate)"
                elif total_weekly_load < 3000:
                    load_category = "High (Advanced)"
                else:
                    load_category = "Very High (Elite/Potential Overload)"
                
                st.markdown(f"**Weekly Load Category**: {load_category}")
                
                # Monotony assessment
                monotony_assessment = ""
                if training_monotony < 1.0:
                    monotony_assessment = "Good (well-balanced week with appropriate variation)"
                elif training_monotony < 1.5:
                    monotony_assessment = "Moderate (some variation, but could be improved)"
                else:
                    monotony_assessment = "High (insufficient variation, risk of overtraining)"
                
                st.markdown(f"**Monotony Assessment**: {monotony_assessment}")
                
                # Strain assessment
                strain_assessment = ""
                if training_strain < 2000:
                    strain_assessment = "Low (sustainable training stress)"
                elif training_strain < 3500:
                    strain_assessment = "Moderate (significant but manageable stress)"
                elif training_strain < 5000:
                    strain_assessment = "High (substantial stress, ensure adequate recovery)"
                else:
                    strain_assessment = "Very High (potential for overreaching, monitor closely)"
                
                st.markdown(f"**Training Strain Assessment**: {strain_assessment}")
                
                st.markdown("</div>", unsafe_allow_html=True)
                
                # Create visualization
                st.subheader("Weekly Training Load Distribution")
                
                # Bar chart of daily loads
                fig = go.Figure()
                
                # Add bars for each day
                fig.add_trace(go.Bar(
                    x=days,
                    y=[daily_loads[day] for day in days],
                    marker_color='#E6754E',
                    text=[f"RPE: {rpes[day]}" if durations[day] > 0 else "Rest" for day in days],
                    textposition='auto'
                ))
                
                # Add line for average daily load
                fig.add_trace(go.Scatter(
                    x=days,
                    y=[avg_daily_load] * len(days),
                    mode='lines',
                    name='Average Daily Load',
                    line=dict(color='rgba(78, 151, 230, 0.7)', width=2, dash='dash')
                ))
                
                fig.update_layout(
                    title='Daily Training Loads',
                    xaxis_title='Day of Week',
                    yaxis_title='Training Load (arbitrary units)',
                    showlegend=True
                )
                
                st.plotly_chart(fig)
                
                # Training distribution analysis
                easy_load = sum(daily_loads[day] for day in days if rpes[day] <= 3)
                moderate_load = sum(daily_loads[day] for day in days if 4 <= rpes[day] <= 6)
                hard_load = sum(daily_loads[day] for day in days if rpes[day] >= 7)
                
                # Calculate percentages
                easy_percent = (easy_load / total_weekly_load * 100) if total_weekly_load > 0 else 0
                moderate_percent = (moderate_load / total_weekly_load * 100) if total_weekly_load > 0 else 0
                hard_percent = (hard_load / total_weekly_load * 100) if total_weekly_load > 0 else 0
                
                # Create pie chart for intensity distribution
                labels = ['Easy (RPE 1-3)', 'Moderate (RPE 4-6)', 'Hard (RPE 7-10)']
                values = [easy_percent, moderate_percent, hard_percent]
                
                fig2 = go.Figure(data=[go.Pie(
                    labels=labels,
                    values=values,
                    hole=.3,
                    marker=dict(colors=['#4EE6A5', '#4E97E6', '#E6754E'])
                )])
                
                fig2.update_layout(
                    title='Training Intensity Distribution',
                    margin=dict(t=30, b=0, l=0, r=0)
                )
                
                st.plotly_chart(fig2)
                
                # Recommendations based on analysis
                st.subheader("Training Recommendations")
                
                # Based on monotony
                if training_monotony > 1.5:
                    st.warning("""
                    **High Training Monotony Detected**
                    
                    Your training shows insufficient variation between hard and easy days, which increases injury and overtraining risk.
                    
                    **Recommendations**:
                    - Incorporate more distinct easy days (RPE 2-3)
                    - Ensure hard days are followed by easy recovery days
                    - Consider adding a complete rest day if none exists
                    """)
                
                # Based on weekly load distribution
                if hard_percent > 40:
                    st.warning(f"""
                    **High-Intensity Load Warning**
                    
                    Your high-intensity training ({hard_percent:.1f}% of total load) exceeds recommended limits (20-25%).
                    
                    **Recommendations**:
                    - Reduce volume of high-intensity work
                    - Replace some hard sessions with moderate endurance work
                    - Ensure adequate recovery after hard sessions
                    """)
                
                if easy_percent < 20 and total_weekly_load > 1500:
                    st.warning(f"""
                    **Insufficient Easy Training**
                    
                    Your easy training ({easy_percent:.1f}% of total load) is below recommended levels (30-40% for most runners).
                    
                    **Recommendations**:
                    - Increase proportion of easy running
                    - Consider converting 1-2 moderate sessions to easy
                    - Ensure proper recovery between hard sessions
                    """)
                
                # Overall load recommendations
                st.markdown("### Overall Training Load Assessment")
                
                if training_strain > 4000:
                    st.markdown("""
                    **High Strain Week Detected**
                    
                    Your training strain indicates a very stressful week. This level may be appropriate for peak training but is not sustainable long-term.
                    
                    **Actions to Consider**:
                    - Plan a recovery week in the next 1-2 weeks
                    - Monitor sleep quality and resting heart rate closely
                    - Consider reducing total load by 30-40% next week
                    - Prioritize recovery modalities (sleep, nutrition, active recovery)
                    """)
                elif total_weekly_load > 3000 and training_monotony > 1.3:
                    st.markdown("""
                    **Elevated Risk Profile**
                    
                    The combination of high load and moderate monotony increases overtraining risk.
                    
                    **Actions to Consider**:
                    - Increase variation between hard and easy days
                    - Maintain total load but redistribute more effectively
                    - Consider adding an additional recovery day
                    """)
                elif total_weekly_load < 1000 and training_days >= 4:
                    st.markdown("""
                    **Low Training Stimulus**
                    
                    Your current training load may be insufficient for significant adaptation if you're beyond beginner level.
                    
                    **Actions to Consider**:
                    - Gradually increase volume on easy/moderate days
                    - Add one quality session per week
                    - Focus on consistency before adding intensity
                    """)
                else:
                    st.markdown("""
                    **Balanced Training Approach**
                    
                    Your current training structure appears well-balanced with appropriate load and variation.
                    
                    **Maintenance Recommendations**:
                    - Continue with current approach
                    - Monitor for signs of fatigue or staleness
                    - Consider small progressive increases (5-10% weekly) if building
                    """)
    
    elif load_mode == "Heart Rate-Based Load":
        st.subheader("Heart Rate-Based Training Load")
        
        st.markdown("""
        Training Impulse (TRIMP) is a method to quantify training load based on heart rate response,
        duration, and intensity relative to heart rate reserve.
        
        This calculator provides both Banister TRIMP and Edwards TRIMP methods.
        """)
        
        col1, col2 = st.columns([3, 2])
        
        with col1:
            trimp_method = st.radio(
                "TRIMP Method:",
                ["Banister TRIMP", "Edwards TRIMP"]
            )
            
            # Basic parameters needed for both methods
            max_hr = st.number_input("Maximum Heart Rate (bpm):", min_value=120, max_value=220, value=185)
            resting_hr = st.number_input("Resting Heart Rate (bpm):", min_value=30, max_value=100, value=60)
            
            if trimp_method == "Banister TRIMP":
                # Banister TRIMP only needs average HR
                duration = st.number_input("Session Duration (minutes):", min_value=10, max_value=300, value=60)
                avg_hr = st.number_input("Average Heart Rate during session (bpm):", min_value=60, max_value=200, value=145)
                gender = st.radio("Gender:", ["Male", "Female"])
                
            else:  # Edwards TRIMP
                st.markdown("### Time Spent in Different Heart Rate Zones:")
                
                # Calculate heart rate zones based on max HR
                zone1_lower = int(max_hr * 0.5)
                zone1_upper = int(max_hr * 0.6)
                zone2_lower = zone1_upper + 1
                zone2_upper = int(max_hr * 0.7)
                zone3_lower = zone2_upper + 1
                zone3_upper = int(max_hr * 0.8)
                zone4_lower = zone3_upper + 1
                zone4_upper = int(max_hr * 0.9)
                zone5_lower = zone4_upper + 1
                
                # Input for time in each zone
                st.markdown(f"**Zone 1** ({zone1_lower}-{zone1_upper} bpm)")
                zone1_min = st.number_input("Minutes in Zone 1:", min_value=0, max_value=300, value=10)
                
                st.markdown(f"**Zone 2** ({zone2_lower}-{zone2_upper} bpm)")
                zone2_min = st.number_input("Minutes in Zone 2:", min_value=0, max_value=300, value=15)
                
                st.markdown(f"**Zone 3** ({zone3_lower}-{zone3_upper} bpm)")
                zone3_min = st.number_input("Minutes in Zone 3:", min_value=0, max_value=300, value=20)
                
                st.markdown(f"**Zone 4** ({zone4_lower}-{zone4_upper} bpm)")
                zone4_min = st.number_input("Minutes in Zone 4:", min_value=0, max_value=300, value=10)
                
                st.markdown(f"**Zone 5** (>{zone5_lower} bpm)")
                zone5_min = st.number_input("Minutes in Zone 5:", min_value=0, max_value=300, value=5)
        
        with col2:
            st.markdown("""
            ### Heart Rate-Based Training Load
            
            Using heart rate data provides a more objective measure of internal training load compared to RPE.
            
            **Benefits**:
            - Accounts for individual physiological response
            - Reflects cardiovascular stress more accurately
            - Useful for comparing different workout types
            - Enables precise quantification of training sessions
            """)
            
            if trimp_method == "Banister TRIMP":
                st.markdown("""
                **Banister TRIMP Formula**:
                
                TRIMP = Duration × HRR × Intensity factor
                
                Where:
                - Duration is in minutes
                - HRR is Heart Rate Reserve ratio during exercise
                - Intensity factor is a weighting based on gender
                
                The intensity weighting emphasizes higher intensities, recognizing that working at higher percentages of HRR creates disproportionately greater training stress.
                """)
            else:
                st.markdown("""
                **Edwards TRIMP Formula**:
                
                TRIMP = (Zone1 min × 1) + (Zone2 min × 2) + (Zone3 min × 3) + (Zone4 min × 4) + (Zone5 min × 5)
                
                This method applies different weightings to each heart rate zone, recognizing that time spent in higher zones creates greater training stress.
                
                Edwards TRIMP is particularly useful for interval training where heart rate fluctuates between zones.
                """)
        
        if st.button("Calculate Heart Rate-Based Load"):
            # Heart Rate Reserve
            hrr = max_hr - resting_hr
            
            if trimp_method == "Banister TRIMP":
                # Calculate HR ratio
                hr_ratio = (avg_hr - resting_hr) / hrr
                
                # Gender-specific weighting factor
                if gender == "Male":
                    intensity_factor = 0.64 * exp(1.92 * hr_ratio)
                else:  # Female
                    intensity_factor = 0.86 * exp(1.67 * hr_ratio)
                
                # Calculate TRIMP
                trimp = duration * hr_ratio * intensity_factor
                
                # Display result
                st.markdown("<div class='result-box'>", unsafe_allow_html=True)
                st.subheader("Banister TRIMP Result")
                
                st.markdown(f"""
                <h3>Training Load (TRIMP): <span class="highlight">{trimp:.1f}</span> units</h3>
                
                **Heart Rate Reserve Ratio**: {hr_ratio:.2f}
                
                **Intensity Factor**: {intensity_factor:.2f}
                """, unsafe_allow_html=True)
                
                # Categorize the TRIMP score
                category = ""
                if trimp < 50:
                    category = "Very Light (Recovery session)"
                elif trimp < 100:
                    category = "Light (Easy aerobic session)"
                elif trimp < 150:
                    category = "Moderate (Steady aerobic session)"
                elif trimp < 200:
                    category = "Moderately Hard (Tempo/threshold session)"
                elif trimp < 300:
                    category = "Hard (Interval/high-intensity session)"
                else:
                    category = "Very Hard (Extended high-intensity session)"
                
                st.markdown(f"**Session Category**: {category}")
                st.markdown("</div>", unsafe_allow_html=True)
                
                # Additional analysis and recommendations
                avg_hr_percent = (avg_hr / max_hr) * 100
                
                st.subheader("Session Analysis")
                
                st.markdown(f"""
                **Average HR**: {avg_hr} bpm ({avg_hr_percent:.1f}% of maximum)
                
                **Average HR Zone**: {
                    "Zone 5 (Anaerobic)" if avg_hr > 0.9 * max_hr else
                    "Zone 4 (Threshold)" if avg_hr > 0.8 * max_hr else
                    "Zone 3 (Tempo)" if avg_hr > 0.7 * max_hr else
                    "Zone 2 (Aerobic)" if avg_hr > 0.6 * max_hr else
                    "Zone 1 (Recovery)"
                }
                
                **Estimated Carbohydrate Usage**: {
                    "Very High" if avg_hr > 0.85 * max_hr else
                    "High" if avg_hr > 0.75 * max_hr else
                    "Moderate" if avg_hr > 0.65 * max_hr else
                    "Low"
                }
                
                **Estimated Fat Utilization**: {
                    "Low" if avg_hr > 0.85 * max_hr else
                    "Moderate" if avg_hr > 0.75 * max_hr else
                    "High" if avg_hr > 0.65 * max_hr else
                    "Very High"
                }
                """)
                
                # Weekly guideline based on TRIMP
                st.subheader("Weekly TRIMP Guidelines")
                
                weekly_estimate = trimp * 5  # Rough estimate for 5 sessions per week
                
                st.markdown(f"""
                Based on this session TRIMP of {trimp:.1f}, a typical weekly training load might be around {weekly_estimate:.0f} TRIMP units.
                
                **Weekly TRIMP Guidelines by Runner Level**:
                - **Beginner**: 200-300 TRIMP units/week
                - **Intermediate**: 300-500 TRIMP units/week  
                - **Advanced**: 500-750 TRIMP units/week
                - **Elite**: 750-1000+ TRIMP units/week
                
                **Recovery Recommendations**:
                - {'Low-intensity recovery session recommended for next day' if trimp > 150 else 'Normal training can resume next day'}
                - {'Consider extra recovery techniques (compression, massage)' if trimp > 200 else ''}
                - {'Monitor sleep quality and duration' if trimp > 150 else ''}
                - {'Ensure adequate carbohydrate replenishment' if avg_hr > 0.75 * max_hr else ''}
                """)
                
                # Training zone visualization
                st.subheader("Training Zones and Session Analysis")
                
                # Create data for heart rate zone visualization
                zones = ["Zone 1", "Zone 2", "Zone 3", "Zone 4", "Zone 5"]
                zone_ranges = [
                    f"{int(max_hr * 0.5)}-{int(max_hr * 0.6)} bpm",
                    f"{int(max_hr * 0.6 + 1)}-{int(max_hr * 0.7)} bpm",
                    f"{int(max_hr * 0.7 + 1)}-{int(max_hr * 0.8)} bpm",
                    f"{int(max_hr * 0.8 + 1)}-{int(max_hr * 0.9)} bpm",
                    f"{int(max_hr * 0.9 + 1)}+ bpm"
                ]
                
                # Highlight the zone containing the average HR
                zone_colors = ['lightgray', 'lightgray', 'lightgray', 'lightgray', 'lightgray']
                if avg_hr <= max_hr * 0.6:
                    zone_colors[0] = '#E6754E'
                elif avg_hr <= max_hr * 0.7:
                    zone_colors[1] = '#E6754E'
                elif avg_hr <= max_hr * 0.8:
                    zone_colors[2] = '#E6754E'
                elif avg_hr <= max_hr * 0.9:
                    zone_colors[3] = '#E6754E'
                else:
                    zone_colors[4] = '#E6754E'
                
                # Create bar chart
                fig = go.Figure(data=[
                    go.Bar(
                        x=zones,
                        y=[1, 2, 3, 4, 5],  # Arbitrary values for visualization
                        text=zone_ranges,
                        marker_color=zone_colors,
                        textposition='auto'
                    )
                ])
                
                # Add marker for average HR
                fig.add_trace(go.Scatter(
                    x=[zones[0] if avg_hr <= max_hr * 0.6 else
                       zones[1] if avg_hr <= max_hr * 0.7 else
                       zones[2] if avg_hr <= max_hr * 0.8 else
                       zones[3] if avg_hr <= max_hr * 0.9 else
                       zones[4]],
                    y=[1 if avg_hr <= max_hr * 0.6 else
                       2 if avg_hr <= max_hr * 0.7 else
                       3 if avg_hr <= max_hr * 0.8 else
                       4 if avg_hr <= max_hr * 0.9 else
                       5],
                    mode='markers+text',
                    marker=dict(size=15, color='blue', symbol='star'),
                    text=[f"Avg HR: {avg_hr} bpm"],
                    textposition="top center",
                    showlegend=False
                ))
                
                fig.update_layout(
                    title=f"Session Average Heart Rate: {avg_hr} bpm ({avg_hr_percent:.1f}% of max)",
                    yaxis_title="Intensity Multiplier",
                    showlegend=False
                )
                
                st.plotly_chart(fig)
            
            else:  # Edwards TRIMP
                # Calculate Edwards TRIMP
                edwards_trimp = (zone1_min * 1) + (zone2_min * 2) + (zone3_min * 3) + (zone4_min * 4) + (zone5_min * 5)
                
                # Total duration
                total_duration = zone1_min + zone2_min + zone3_min + zone4_min + zone5_min
                
                # Display result
                st.markdown("<div class='result-box'>", unsafe_allow_html=True)
                st.subheader("Edwards TRIMP Result")
                
                st.markdown(f"""
                <h3>Training Load (Edwards TRIMP): <span class="highlight">{edwards_trimp}</span> units</h3>
                
                **Total Duration**: {total_duration} minutes
                
                **Average Intensity Factor**: {edwards_trimp / total_duration if total_duration > 0 else 0:.2f}
                """, unsafe_allow_html=True)
                
                # Categorize the load
                category = ""
                if edwards_trimp < 60:
                    category = "Very Light (Recovery session)"
                elif edwards_trimp < 120:
                    category = "Light (Easy aerobic session)"
                elif edwards_trimp < 180:
                    category = "Moderate (Steady aerobic session)"
                elif edwards_trimp < 240:
                    category = "Moderately Hard (Mixed session)"
                elif edwards_trimp < 300:
                    category = "Hard (Interval/high-intensity session)"
                else:
                    category = "Very Hard (Extended high-intensity session)"
                
                st.markdown(f"**Session Category**: {category}")
                st.markdown("</div>", unsafe_allow_html=True)
                
                # Create visualization of time in each zone
                st.subheader("Time in Heart Rate Zones")
                
                # Calculate zone percentages
                if total_duration > 0:
                    zone1_pct = (zone1_min / total_duration) * 100
                    zone2_pct = (zone2_min / total_duration) * 100
                    zone3_pct = (zone3_min / total_duration) * 100
                    zone4_pct = (zone4_min / total_duration) * 100
                    zone5_pct = (zone5_min / total_duration) * 100
                else:
                    zone1_pct = zone2_pct = zone3_pct = zone4_pct = zone5_pct = 0
                
                # Create bar chart
                fig = go.Figure()
                
                # Add bars for minutes in each zone
                fig.add_trace(go.Bar(
                    x=["Zone 1", "Zone 2", "Zone 3", "Zone 4", "Zone 5"],
                    y=[zone1_min, zone2_min, zone3_min, zone4_min, zone5_min],
                    marker_color=['#4EE6A5', '#4EBDE6', '#4E97E6', '#E69A4E', '#E6754E'],
                    text=[f"{zone1_pct:.1f}%", f"{zone2_pct:.1f}%", f"{zone3_pct:.1f}%", f"{zone4_pct:.1f}%", f"{zone5_pct:.1f}%"],
                    textposition='auto'
                ))
                
                fig.update_layout(
                    title='Time Spent in Each Heart Rate Zone',
                    xaxis_title='Heart Rate Zone',
                    yaxis_title='Minutes',
                    showlegend=False
                )
                
                st.plotly_chart(fig)
                
                # Create pie chart of TRIMP contribution by zone
                zone1_contribution = zone1_min * 1
                zone2_contribution = zone2_min * 2
                zone3_contribution = zone3_min * 3
                zone4_contribution = zone4_min * 4
                zone5_contribution = zone5_min * 5
                
                labels = [f'Zone 1 ({zone1_contribution} TRIMP)', 
                          f'Zone 2 ({zone2_contribution} TRIMP)', 
                          f'Zone 3 ({zone3_contribution} TRIMP)', 
                          f'Zone 4 ({zone4_contribution} TRIMP)', 
                          f'Zone 5 ({zone5_contribution} TRIMP)']
                
                values = [zone1_contribution, zone2_contribution, zone3_contribution, zone4_contribution, zone5_contribution]
                
                fig2 = go.Figure(data=[go.Pie(
                    labels=labels,
                    values=values,
                    hole=.3,
                    marker=dict(colors=['#4EE6A5', '#4EBDE6', '#4E97E6', '#E69A4E', '#E6754E'])
                )])
                
                fig2.update_layout(
                    title='TRIMP Contribution by Zone',
                    margin=dict(t=30, b=0, l=0, r=0)
                )
                
                st.plotly_chart(fig2)
                
                # Session analysis and recommendations
                st.subheader("Session Analysis and Recommendations")
                
                # Determine session type based on zone distribution
                session_type = ""
                if zone1_pct + zone2_pct > 70:
                    session_type = "Recovery/Easy Aerobic"
                elif zone3_pct > 50:
                    session_type = "Steady/Tempo"
                elif zone4_pct + zone5_pct > 30:
                    session_type = "High Intensity/Interval"
                else:
                    session_type = "Mixed/Moderate Intensity"
                
                st.markdown(f"""
                **Session Type**: {session_type}
                
                **Training Effect**:
                - **Aerobic Development**: {"High" if zone1_pct + zone2_pct + zone3_pct > 70 else "Moderate" if zone1_pct + zone2_pct + zone3_pct > 40 else "Low"}
                - **Anaerobic Development**: {"High" if zone4_pct + zone5_pct > 30 else "Moderate" if zone4_pct + zone5_pct > 15 else "Low"}
                - **Recovery Impact**: {"High" if edwards_trimp > 200 else "Moderate" if edwards_trimp > 120 else "Low"}
                
                **Weekly Guidelines**:
                - Sessions of this type per week: {
                    "1-2" if session_type == "High Intensity/Interval" else 
                    "1-2" if session_type == "Steady/Tempo" else
                    "3-5" if session_type == "Recovery/Easy Aerobic" else
                    "2-3"
                }
                - Recommended recovery before next hard session: {
                    "48-72 hours" if edwards_trimp > 200 else
                    "24-48 hours" if edwards_trimp > 120 else
                    "None required"
                }
                """)
                
                # Optimal zone distribution for different training goals
                st.markdown("""
                ### Optimal Zone Distribution by Training Goal
                
                **Base Building**:
                - Zone 1-2: 70-80%
                - Zone 3: 10-20%
                - Zone 4-5: 5-10%
                
                **Threshold Development**:
                - Zone 1-2: 60-70%
                - Zone 3-4: 25-35%
                - Zone 5: 5%
                
                **Race Preparation**:
                - Zone 1-2: 60-65%
                - Zone 3: 15-20%
                - Zone 4-5: 15-25%
                """)
    
    elif load_mode == "ACWR (Acute:Chronic Workload Ratio)":
        st.subheader("Acute:Chronic Workload Ratio Calculator")
        
        st.markdown("""
        The Acute:Chronic Workload Ratio (ACWR) compares your recent training load (acute, typically 
        last 7 days) with your longer-term load (chronic, typically last 28 days).
        
        This metric helps monitor training progression and identify injury risk when the ratio gets too high
        (training spike) or too low (detraining).
        
        **Scientific Validation**: Research has shown that maintaining the ACWR in the "sweet spot" (typically 0.8-1.3) 
        is associated with lower injury risk in athletes.
        
        **Reference**: Gabbett, T. J. (2016). The training-injury prevention paradox: should athletes be training smarter and harder? *British Journal of Sports Medicine, 50(5)*, 273-280.
        """)
        
        col1, col2 = st.columns([3, 2])
        
        with col1:
            load_unit = st.radio(
                "Load Measurement Unit:",
                ["Distance (km/miles)", "Duration (minutes)", "Training Load (TRIMP/RPE)"]
            )
            
            st.markdown("### Enter your training loads for the past 4 weeks:")
            
            # Create 4 columns for the past 4 weeks
            weeks = ["Week -4", "Week -3", "Week -2", "Last Week"]
            week_loads = {}
            
            for i, week in enumerate(weeks):
                if i == 3:  # Last week (acute period)
                    st.markdown(f"**{week} (Acute Period)**")
                else:
                    st.markdown(f"**{week}**")
                
                if load_unit == "Distance (km/miles)":
                    week_loads[week] = st.number_input(f"Distance:", min_value=0.0, max_value=300.0, value=40.0, step=5.0, key=f"dist_{i}")
                elif load_unit == "Duration (minutes)":
                    week_loads[week] = st.number_input(f"Duration (min):", min_value=0, max_value=2000, value=300, step=30, key=f"dur_{i}")
                else:  # Training Load
                    week_loads[week] = st.number_input(f"Training Load:", min_value=0, max_value=5000, value=400, step=50, key=f"load_{i}")
                
                # Add a spacer between weeks
                st.markdown("---")
            
            # Optional: Allow changing the acute/chronic period definitions
            custom_periods = st.checkbox("Customize acute/chronic periods")
            
            if custom_periods:
                acute_period = st.slider("Acute period (days):", min_value=3, max_value=14, value=7)
                chronic_period = st.slider("Chronic period (days):", min_value=14, max_value=42, value=28)
            else:
                acute_period = 7
                chronic_period = 28
        
        with col2:
            st.markdown("""
            ### Understanding ACWR
            
            The Acute:Chronic Workload Ratio is calculated as:
            
            ACWR = Acute Workload / Chronic Workload
            
            Where:
            - **Acute workload** is typically the last 7 days
            - **Chronic workload** is typically the last 28 days (including the acute period)
            
            **Interpretation**:
            - **<0.8**: Undertraining (potential detraining effects)
            - **0.8-1.3**: "Sweet spot" (optimal training progression)
            - **1.3-1.5**: Potential injury risk (caution zone)
            - **>1.5**: High injury risk (danger zone)
            
            The concept is based on the idea that the body can handle high workloads if they are built up gradually, but sudden spikes in training load relative to what you're prepared for increase injury risk.
            """)
            
            st.info("""
            **Note**: Different types of training load metrics can be used with ACWR:
            
            - External load (distance, time)
            - Internal load (RPE-based, TRIMP)
            - Combined metrics
            
            For best results, use the same metric consistently.
            """)
        
        if st.button("Calculate ACWR"):
            # Calculate acute workload (last week)
            acute_workload = week_loads["Last Week"]
            
            # Calculate chronic workload (average of last 4 weeks)
            total_load = sum(week_loads.values())
            chronic_workload = total_load / 4
            
            # Calculate ACWR
            acwr = acute_workload / chronic_workload if chronic_workload > 0 else 0
            
            # Display result
            st.markdown("<div class='result-box'>", unsafe_allow_html=True)
            st.subheader("Acute:Chronic Workload Ratio Analysis")
            
            st.markdown(f"""
            <h3>ACWR: <span class="highlight">{acwr:.2f}</span></h3>
            
            **Acute Workload (Last Week)**: {acute_workload} {load_unit.split(" ")[0]}
            
            **Chronic Workload (4-Week Average)**: {chronic_workload:.1f} {load_unit.split(" ")[0]}
            """, unsafe_allow_html=True)
            
            # Categorize the ACWR value
            category = ""
            color = ""
            if acwr < 0.8:
                category = "Undertraining"
                color = "blue"
            elif acwr <= 1.3:
                category = "Optimal Loading (Sweet Spot)"
                color = "green"
            elif acwr <= 1.5:
                category = "Potential Injury Risk (Caution)"
                color = "orange"
            else:
                category = "High Injury Risk (Danger)"
                color = "red"
            
            st.markdown(f"""
            **Status**: <span style="color:{color}; font-weight:bold">{category}</span>
            """, unsafe_allow_html=True)
            
            # Training progression analysis
            weekly_changes = []
            for i in range(1, len(weeks)):
                previous = week_loads[weeks[i-1]]
                current = week_loads[weeks[i]]
                if previous > 0:
                    change_percent = ((current - previous) / previous) * 100
                    weekly_changes.append(change_percent)
                else:
                    weekly_changes.append(0)
            
            # Calculate average weekly change
            avg_weekly_change = sum(weekly_changes) / len(weekly_changes) if weekly_changes else 0
            
            st.markdown(f"""
            **Weekly Progression Rate**: {avg_weekly_change:.1f}% (Recommended: 5-10%)
            
            **4-Week Load Trend**: {"Increasing" if avg_weekly_change > 2 else "Decreasing" if avg_weekly_change < -2 else "Stable"}
            """)
            
            st.markdown("</div>", unsafe_allow_html=True)
            
            # Create visualization of weekly loads and ACWR
            st.subheader("Weekly Load Progression")
            
            # Bar chart of weekly loads
            fig = go.Figure()
            
            # Add bars for each week
            fig.add_trace(go.Bar(
                x=weeks,
                y=[week_loads[week] for week in weeks],
                marker_color=['#4E97E6', '#4E97E6', '#4E97E6', 
                             '#E6754E' if acwr > 1.3 else '#4EE6A5' if acwr >= 0.8 else '#4E97E6'],
                text=[f"{week_loads[week]}" for week in weeks],
                textposition='auto'
            ))
            
            # Add line for chronic workload
            fig.add_trace(go.Scatter(
                x=weeks,
                y=[chronic_workload] * len(weeks),
                mode='lines',
                name='Chronic Workload',
                line=dict(color='rgba(0, 0, 0, 0.7)', width=2, dash='dash')
            ))
            
            fig.update_layout(
                title=f'Weekly {load_unit.split(" ")[0]} Progression',
                xaxis_title='Week',
                yaxis_title=f'{load_unit.split(" ")[0]}',
                showlegend=True
            )
            
            st.plotly_chart(fig)
            
            # ACWR risk zones visualization
            st.subheader("ACWR Risk Zones")
            
            # Create visualization of ACWR risk zones
            fig2 = go.Figure()
            
            # Add colored regions for different risk zones
            fig2.add_trace(go.Scatter(
                x=[0, 0.8, 0.8, 0, 0],
                y=[0, 0, chronic_workload * 1.5, chronic_workload * 1.5, 0],
                fill='toself',
                fillcolor='rgba(173, 216, 230, 0.5)',
                line=dict(width=0),
                name='Undertraining Zone',
                showlegend=True
            ))
            
            fig2.add_trace(go.Scatter(
                x=[0.8, 1.3, 1.3, 0.8, 0.8],
                y=[0, 0, chronic_workload * 1.5, chronic_workload * 1.5, 0],
                fill='toself',
                fillcolor='rgba(144, 238, 144, 0.5)',
                line=dict(width=0),
                name='Sweet Spot',
                showlegend=True
            ))
            
            fig2.add_trace(go.Scatter(
                x=[1.3, 1.5, 1.5, 1.3, 1.3],
                y=[0, 0, chronic_workload * 1.5, chronic_workload * 1.5, 0],
                fill='toself',
                fillcolor='rgba(255, 165, 0, 0.5)',
                line=dict(width=0),
                name='Caution Zone',
                showlegend=True
            ))
            
            fig2.add_trace(go.Scatter(
                x=[1.5, 2.5, 2.5, 1.5, 1.5],
                y=[0, 0, chronic_workload * 1.5, chronic_workload * 1.5, 0],
                fill='toself',
                fillcolor='rgba(255, 0, 0, 0.5)',
                line=dict(width=0),
                name='Danger Zone',
                showlegend=True
            ))
            
            # Add point for current ACWR
            fig2.add_trace(go.Scatter(
                x=[acwr],
                y=[acute_workload],
                mode='markers',
                marker=dict(
                    size=15,
                    color='black',
                    symbol='circle'
                ),
                name='Current ACWR',
                showlegend=True
            ))
            
            fig2.update_layout(
                title='ACWR Risk Zones',
                xaxis_title='Acute:Chronic Workload Ratio',
                yaxis_title=f'Acute Workload ({load_unit.split(" ")[0]})',
                xaxis=dict(range=[0, 2.5]),
                yaxis=dict(range=[0, chronic_workload * 1.5 if chronic_workload > 0 else 100])
            )
            
            st.plotly_chart(fig2)
            
            # Recommendations based on ACWR value
            st.subheader("Recommendations")
            
            if acwr < 0.8:
                st.markdown("""
                **Undertraining Zone Recommendations**:
                
                Your acute workload is lower than your chronic workload, which may lead to detraining effects.
                
                **Actions to Consider**:
                - Gradually increase training volume
                - Add 1-2 quality sessions per week
                - Aim for 5-10% weekly increases in load
                - Consider whether this is an intentional recovery week
                
                **Note**: If this is a planned recovery week, this lower ACWR is appropriate. Otherwise, consider increasing load gradually in the coming week.
                """)
            elif acwr <= 1.3:
                st.markdown("""
                **Sweet Spot Recommendations**:
                
                Your acute:chronic workload ratio is in the optimal range for safe progression.
                
                **Actions to Consider**:
                - Continue with current training progression
                - Maintain similar load in the coming week
                - Monitor for any signs of fatigue or staleness
                - Consider small incremental increases (5-10%) if building fitness
                
                **Note**: This is the ideal zone for balancing training progression with injury risk. Maintaining your ACWR in this range over time is associated with lower injury risk.
                """)
            elif acwr <= 1.5:
                st.markdown("""
                **Caution Zone Recommendations**:
                
                Your acute workload is considerably higher than your chronic workload, putting you at increased injury risk.
                
                **Actions to Consider**:
                - Reduce next week's training load by 10-15%
                - Focus on recovery (sleep, nutrition, hydration)
                - Monitor for early signs of overtraining or injury
                - Consider adding an extra recovery day
                
                **Note**: While this zone doesn't guarantee injury, research shows increased risk. Be particularly attentive to recovery and any early warning signs like persistent soreness or minor niggles.
                """)
            else:
                st.markdown("""
                **Danger Zone Recommendations**:
                
                Your acute workload is significantly higher than your chronic workload, indicating a training spike and high injury risk.
                
                **Actions to Consider**:
                - Reduce next week's training load by 20-30%
                - Implement an immediate recovery week
                - Avoid high-intensity training for 5-7 days
                - Pay close attention to any pain or discomfort
                
                **Note**: This level of ACWR has been strongly associated with injury risk in research. Even if you feel fine now, the accumulated fatigue may manifest as injury in the coming days or weeks if load isn't reduced.
                """)
            
            # Future planning
            st.subheader("Planning Your Next Week")
            
            # Calculate recommended load for next week
            if acwr < 0.8:
                min_recommended = chronic_workload * 0.85
                max_recommended = chronic_workload * 1.1
                recommendation = "increase"
            elif acwr <= 1.3:
                min_recommended = chronic_workload * 0.8
                max_recommended = chronic_workload * 1.1
                recommendation = "maintain"
            elif acwr <= 1.5:
                min_recommended = chronic_workload * 0.7
                max_recommended = chronic_workload * 0.9
                recommendation = "decrease slightly"
            else:
                min_recommended = chronic_workload * 0.6
                max_recommended = chronic_workload * 0.8
                recommendation = "decrease significantly"
            
            st.markdown(f"""
            Based on your current ACWR of {acwr:.2f}, it's recommended to **{recommendation}** your load next week.
            
            **Recommended load range for next week**:
            - Minimum: {min_recommended:.1f} {load_unit.split(" ")[0]}
            - Maximum: {max_recommended:.1f} {load_unit.split(" ")[0]}
            
            This range should help maintain your ACWR in the optimal zone while allowing appropriate training progression.
            """)
    
    else:  # Recovery Metrics
        st.subheader("Recovery Metrics Calculator")
        
        st.markdown("""
        Recovery metrics help assess your body's response to training load and readiness for subsequent training.
        This calculator provides several methods to quantify recovery status.
        
        Monitoring recovery is as important as tracking training load for optimizing performance and preventing overtraining.
        """)
        
        recovery_method = st.radio(
            "Recovery Assessment Method:",
            ["Heart Rate Variability (HRV)", "Resting Heart Rate", "Perceived Recovery (Subjective)", "Combined Metrics"]
        )
        
        if recovery_method == "Heart Rate Variability (HRV)":
            col1, col2 = st.columns([3, 2])
            
            with col1:
                st.markdown("""
                ### Heart Rate Variability (HRV) Assessment
                
                HRV is a measure of the variation in time between consecutive heartbeats. Higher variability generally 
                indicates better recovery and parasympathetic nervous system activity.
                """)
                
                measurement_type = st.radio(
                    "Measurement Type:",
                    ["Single Measurement", "Weekly Trend"]
                )
                
                if measurement_type == "Single Measurement":
                    hrv_value = st.number_input("HRV Value (RMSSD or ln RMSSD):", min_value=0.0, max_value=120.0, value=65.0, step=0.5)
                    hrv_type = st.radio("HRV Metric Type:", ["RMSSD (ms)", "ln RMSSD"])
                    
                    if hrv_type == "RMSSD (ms)" and hrv_value > 20:
                        ln_rmssd = np.log(hrv_value)
                    else:
                        ln_rmssd = hrv_value
                    
                    age = st.number_input("Age:", min_value=18, max_value=80, value=35)
                    gender = st.radio("Gender:", ["Male", "Female"])
                    fitness_level = st.select_slider(
                        "Fitness Level:",
                        options=["Beginner", "Recreational", "Trained", "Elite"],
                        value="Trained"
                    )
                
                else:  # Weekly Trend
                    st.markdown("### Enter HRV values for the past 7 days:")
                    
                    hrv_values = []
                    for i in range(7):
                        hrv_values.append(st.number_input(f"Day {i+1} HRV:", min_value=0.0, max_value=120.0, value=65.0, step=0.5, key=f"hrv_{i}"))
                    
                    hrv_type = st.radio("HRV Metric Type (Weekly):", ["RMSSD (ms)", "ln RMSSD"])
                    
                    if hrv_type == "RMSSD (ms)":
                        ln_rmssd_values = [np.log(v) if v > 0 else 0 for v in hrv_values]
                    else:
                        ln_rmssd_values = hrv_values
            
            with col2:
                st.markdown("""
                ### Understanding HRV
                
                **Benefits of HRV Monitoring**:
                
                - Objective measure of recovery status
                - Reflects autonomic nervous system balance
                - Early indicator of overtraining
                - Helps optimize training timing
                
                **Interpretation Factors**:
                
                - Individual baseline is most important
                - Trend matters more than absolute values
                - Higher is generally better (but excessive values can indicate parasympathetic overtraining)
                - Context matters (sleep, stress, nutrition)
                
                **Measurement Best Practices**:
                
                - Measure first thing in the morning
                - Consistent conditions (lying down, after waking)
                - Use same measurement method consistently
                - Track 7-day rolling average for best results
                """)
            
            if st.button("Calculate Recovery Status"):
                if measurement_type == "Single Measurement":
                    # Create reference ranges based on age, gender, fitness level
                    # Note: These are approximations based on research literature
                    base_value = 0
                    
                    if gender == "Male":
                        base_value = 65 - (age * 0.2)
                    else:  # Female
                        base_value = 70 - (age * 0.2)
                    
                    # Adjust for fitness level
                    fitness_adjustments = {
                        "Beginner": -10,
                        "Recreational": 0,
                        "Trained": 10,
                        "Elite": 20
                    }
                    
                    reference_value = base_value + fitness_adjustments[fitness_level]
                    reference_ln = np.log(reference_value) if reference_value > 0 else 0
                    
                    # Calculate recovery status percentage
                    if hrv_type == "RMSSD (ms)":
                        recovery_percentage = (hrv_value / reference_value) * 100
                    else:  # ln RMSSD
                        recovery_percentage = (hrv_value / reference_ln) * 100
                    
                    # Display result
                    st.markdown("<div class='result-box'>", unsafe_allow_html=True)
                    st.subheader("Recovery Status Assessment")
                    
                    # Original HRV value and converted value
                    if hrv_type == "RMSSD (ms)":
                        st.markdown(f"""
                        **HRV (RMSSD)**: {hrv_value} ms
                        
                        **ln RMSSD**: {ln_rmssd:.2f}
                        """)
                    else:
                        st.markdown(f"""
                        **HRV (ln RMSSD)**: {hrv_value}
                        
                        **RMSSD**: {np.exp(hrv_value):.1f} ms
                        """)
                    
                    # Recovery status
                    recovery_status = ""
                    color = ""
                    if recovery_percentage < 80:
                        recovery_status = "Low (Significant Fatigue)"
                        color = "red"
                    elif recovery_percentage < 90:
                        recovery_status = "Below Average (Moderate Fatigue)"
                        color = "orange"
                    elif recovery_percentage < 110:
                        recovery_status = "Normal (Recovered)"
                        color = "green"
                    elif recovery_percentage < 130:
                        recovery_status = "Above Average (Well Recovered)"
                        color = "lightgreen"
                    else:
                        recovery_status = "Very High (Potential Parasympathetic Overtraining)"
                        color = "blue"
                    
                    st.markdown(f"""
                    <h3>Recovery Status: <span style="color:{color}">{recovery_status}</span></h3>
                    
                    **Recovery Percentage**: {recovery_percentage:.1f}% of reference value
                    """, unsafe_allow_html=True)
                    
                    st.markdown("</div>", unsafe_allow_html=True)
                    
                    # Training recommendations
                    st.subheader("Training Recommendations")
                    
                    if recovery_percentage < 80:
                        st.markdown("""
                        **Low Recovery Status Recommendations**:
                        
                        Your HRV indicates significant fatigue and incomplete recovery.
                        
                        **Training Approach**:
                        - Take a recovery day or very light session
                        - Focus on active recovery (walking, light movement)
                        - Prioritize sleep and nutrition
                        - Consider reducing training load for next 2-3 days
                        - Avoid high-intensity work until HRV improves
                        """)
                    elif recovery_percentage < 90:
                        st.markdown("""
                        **Below Average Recovery Recommendations**:
                        
                        Your HRV indicates some residual fatigue.
                        
                        **Training Approach**:
                        - Moderate training volume (70-80% of normal)
                        - Avoid high-intensity work
                        - Focus on technique and easy aerobic training
                        - Implement additional recovery strategies (hydration, nutrition, sleep)
                        - Monitor HRV trend over next few days
                        """)
                    elif recovery_percentage < 110:
                        st.markdown("""
                        **Normal Recovery Recommendations**:
                        
                        Your HRV indicates normal recovery status.
                        
                        **Training Approach**:
                        - Proceed with planned training
                        - No special modifications needed
                        - Good day for moderate intensity or volume
                        - Continue with normal recovery practices
                        """)
                    elif recovery_percentage < 130:
                        st.markdown("""
                        **Above Average Recovery Recommendations**:
                        
                        Your HRV indicates excellent recovery status.
                        
                        **Training Approach**:
                        - Optimal day for high-intensity training
                        - Consider a breakthrough session or key workout
                        - Good time for testing or racing
                        - Can handle increased training load if desired
                        """)
                    else:
                        st.markdown("""
                        **Very High HRV Recommendations**:
                        
                        Your HRV is unusually high, which might indicate parasympathetic overtraining or might simply be a good recovery day.
                        
                        **Training Approach**:
                        - If feeling good: Proceed with quality training
                        - If feeling flat or fatigued despite high HRV: Take an easy day
                        - Monitor other recovery metrics (sleep quality, RPE, general feeling)
                        - Watch for continued very high HRV with poor performance (potential parasympathetic overtraining)
                        """)
                
                else:  # Weekly Trend
                    # Calculate 7-day rolling average and coefficient of variation
                    avg_hrv = sum(hrv_values) / len(hrv_values)
                    rolling_avg = avg_hrv
                    
                    # Calculate standard deviation
                    squared_diffs = [(v - avg_hrv)**2 for v in hrv_values]
                    variance = sum(squared_diffs) / len(hrv_values)
                    std_dev = variance**0.5
                    
                    # Coefficient of variation
                    cv = (std_dev / avg_hrv) * 100 if avg_hrv > 0 else 0
                    
                    # Calculate day-to-day change (last day compared to 7-day average)
                    today_vs_avg = ((hrv_values[-1] - rolling_avg) / rolling_avg) * 100 if rolling_avg > 0 else 0
                    
                    # Calculate smallest worthwhile change (SWC = 0.5 × CV)
                    swc = 0.5 * cv
                    
                    # Display result
                    st.markdown("<div class='result-box'>", unsafe_allow_html=True)
                    st.subheader("HRV Trend Analysis")
                    
                    st.markdown(f"""
                    **7-Day Average HRV**: {rolling_avg:.1f} {hrv_type}
                    
                    **Coefficient of Variation**: {cv:.1f}% (stability of measurements)
                    
                    **Today vs. Average**: {today_vs_avg:+.1f}% (positive is better)
                    
                    **Smallest Worthwhile Change**: {swc:.1f}% (threshold for meaningful change)
                    """)
                    
                    # Determine trend status
                    trend_status = ""
                    if abs(today_vs_avg) < swc:
                        trend_status = "Stable (No Significant Change)"
                    elif today_vs_avg > 0:
                        trend_status = "Improving (Enhanced Recovery)"
                    else:
                        trend_status = "Declining (Increasing Fatigue)"
                    
                    st.markdown(f"""
                    <h3>HRV Trend: {trend_status}</h3>
                    """, unsafe_allow_html=True)
                    
                    st.markdown("</div>", unsafe_allow_html=True)
                    
                    # Create visualization of HRV trend
                    fig = go.Figure()
                    
                    # Add line for daily HRV values
                    fig.add_trace(go.Scatter(
                        x=list(range(1, 8)),
                        y=hrv_values,
                        mode='lines+markers',
                        name='Daily HRV',
                        line=dict(color='#E6754E', width=2)
                    ))
                    
                    # Add line for rolling average
                    fig.add_trace(go.Scatter(
                        x=list(range(1, 8)),
                        y=[rolling_avg] * 7,
                        mode='lines',
                        name='7-Day Average',
                        line=dict(color='rgba(0, 0, 0, 0.7)', width=2, dash='dash')
                    ))
                    
                    # Add bands for smallest worthwhile change
                    fig.add_trace(go.Scatter(
                        x=list(range(1, 8)),
                        y=[rolling_avg * (1 + swc/100)] * 7,
                        mode='lines',
                        name=f'SWC (+{swc:.1f}%)',
                        line=dict(color='rgba(0, 255, 0, 0.3)', width=1)
                    ))
                    
                    fig.add_trace(go.Scatter(
                        x=list(range(1, 8)),
                        y=[rolling_avg * (1 - swc/100)] * 7,
                        mode='lines',
                        name=f'SWC (-{swc:.1f}%)',
                        line=dict(color='rgba(255, 0, 0, 0.3)', width=1),
                        fill='tonexty',
                        fillcolor='rgba(200, 200, 200, 0.2)'
                    ))
                    
                    fig.update_layout(
                        title='7-Day HRV Trend',
                        xaxis_title='Day',
                        yaxis_title=f'HRV ({hrv_type})',
                        showlegend=True
                    )
                    
                    st.plotly_chart(fig)
                    
                    # Training recommendations based on trend
                    st.subheader("Training Recommendations")
                    
                    if trend_status == "Stable (No Significant Change)":
                        st.markdown("""
                        **Stable HRV Trend Recommendations**:
                        
                        Your HRV is showing good stability, indicating balanced training load and recovery.
                        
                        **Training Approach**:
                        - Continue with planned training program
                        - Maintain current balance of intensity and volume
                        - No specific modifications needed
                        - Good status for progressive training
                        """)
                    elif trend_status == "Improving (Enhanced Recovery)":
                        st.markdown("""
                        **Improving HRV Trend Recommendations**:
                        
                        Your HRV is showing an upward trend, indicating good recovery and adaptation.
                        
                        **Training Approach**:
                        - Good time to include high-intensity training
                        - Could slightly increase training load if desired
                        - Optimal time for key workouts or testing
                        - Your body is responding well to current training
                        """)
                    else:  # Declining trend
                        st.markdown("""
                        **Declining HRV Trend Recommendations**:
                        
                        Your HRV is showing a downward trend, indicating accumulating fatigue or stress.
                        
                        **Training Approach**:
                        - Reduce training load temporarily (10-20%)
                        - Emphasize recovery techniques
                        - Avoid high-intensity training until trend stabilizes
                        - Monitor other markers (sleep quality, mood, motivation)
                        - Consider non-training stressors that may be affecting recovery
                        """)
        
        elif recovery_method == "Resting Heart Rate":
            col1, col2 = st.columns([3, 2])
            
            with col1:
                st.markdown("""
                ### Resting Heart Rate (RHR) Assessment
                
                Resting heart rate is a simple yet effective indicator of recovery status and overall fitness.
                Increases in RHR often indicate incomplete recovery or increased stress.
                """)
                
                rhr_tracking = st.radio(
                    "Assessment Method:",
                    ["Daily Measurement", "Weekly Trend"]
                )
                
                if rhr_tracking == "Daily Measurement":
                    today_rhr = st.number_input("Today's Resting Heart Rate (bpm):", min_value=30, max_value=100, value=55)
                    baseline_rhr = st.number_input("Baseline/Normal Resting Heart Rate (bpm):", min_value=30, max_value=100, value=52)
                    
                    # Additional context
                    sleep_quality = st.select_slider(
                        "Sleep Quality Last Night:",
                        options=["Very Poor", "Poor", "Fair", "Good", "Very Good"],
                        value="Good"
                    )
                    
                    stress_level = st.select_slider(
                        "Current Stress Level:",
                        options=["Very Low", "Low", "Moderate", "High", "Very High"],
                        value="Low"
                    )
                
                else:  # Weekly Trend
                    st.markdown("### Enter resting heart rate values for the past 7 days:")
                    
                    rhr_values = []
                    for i in range(7):
                        rhr_values.append(st.number_input(f"Day {i+1} RHR (bpm):", min_value=30, max_value=100, value=53, key=f"rhr_{i}"))
            
            with col2:
                st.markdown("""
                ### Understanding Resting Heart Rate
                
                **Benefits of RHR Monitoring**:
                
                - Simple to measure
                - Reflects autonomic nervous system balance
                - Indicator of cardiovascular fitness
                - Sensitive to recovery status
                
                **Interpretation Guidelines**:
                
                - 3-5 bpm increase: Minor fatigue
                - 5-10 bpm increase: Significant fatigue
                - >10 bpm increase: Excessive fatigue or illness
                
                **Influencing Factors**:
                
                - Sleep quality and duration
                - Hydration status
                - Psychological stress
                - Ambient temperature
                - Caffeine or alcohol
                - Illness or infection
                
                **Measurement Best Practices**:
                
                - Measure upon waking
                - Before consuming caffeine
                - After using the bathroom
                - While lying still
                - Same time each day
                """)
            
            if st.button("Calculate Recovery Status (RHR)"):
                if rhr_tracking == "Daily Measurement":
                    # Calculate the difference between today's RHR and baseline
                    rhr_difference = today_rhr - baseline_rhr
                    
                    # Calculate recovery percentage
                    # This is a simple algorithm - elevated RHR means lower recovery percentage
                    recovery_percentage = 100 - (rhr_difference * 5)
                    recovery_percentage = max(0, min(110, recovery_percentage))  # Limit to 0-110%
                    
                    # Adjust based on sleep quality
                    sleep_adjustment = {
                        "Very Poor": -15,
                        "Poor": -10,
                        "Fair": 0,
                        "Good": 5,
                        "Very Good": 10
                    }
                    
                    # Adjust based on stress level
                    stress_adjustment = {
                        "Very Low": 10,
                        "Low": 5,
                        "Moderate": 0,
                        "High": -10,
                        "Very High": -15
                    }
                    
                    # Apply adjustments
                    adjusted_recovery = recovery_percentage + sleep_adjustment[sleep_quality] + stress_adjustment[stress_level]
                    adjusted_recovery = max(0, min(100, adjusted_recovery))  # Limit to 0-100%
                    
                    # Display result
                    st.markdown("<div class='result-box'>", unsafe_allow_html=True)
                    st.subheader("Resting Heart Rate Analysis")
                    
                    st.markdown(f"""
                    **Today's RHR**: {today_rhr} bpm
                    
                    **Baseline RHR**: {baseline_rhr} bpm
                    
                    **Difference**: {rhr_difference:+d} bpm
                    """)
                    
                    # Recovery status
                    recovery_status = ""
                    color = ""
                    if adjusted_recovery < 40:
                        recovery_status = "Very Poor (Significant Fatigue)"
                        color = "red"
                    elif adjusted_recovery < 60:
                        recovery_status = "Poor (Moderate Fatigue)"
                        color = "orange"
                    elif adjusted_recovery < 80:
                        recovery_status = "Moderate (Some Fatigue)"
                        color = "yellow"
                    else:
                        recovery_status = "Good (Well Recovered)"
                        color = "green"
                    
                    st.markdown(f"""
                    <h3>Recovery Status: <span style="color:{color}">{recovery_status}</span></h3>
                    
                    **Recovery Score**: {adjusted_recovery:.0f}%
                    
                    **Influencing Factors**:
                    - Sleep Quality: {sleep_quality} ({sleep_adjustment[sleep_quality]:+d}%)
                    - Stress Level: {stress_level} ({stress_adjustment[stress_level]:+d}%)
                    """, unsafe_allow_html=True)
                    
                    st.markdown("</div>", unsafe_allow_html=True)
                    
                    # Training recommendations
                    st.subheader("Training Recommendations")
                    
                    if adjusted_recovery < 40:
                        st.markdown("""
                        **Very Poor Recovery Recommendations**:
                        
                        Your RHR indicates significant fatigue or possible illness.
                        
                        **Training Approach**:
                        - Consider a rest day or active recovery only
                        - Focus on hydration and nutrition
                        - Prioritize sleep (aim for 8-9 hours)
                        - Monitor for signs of illness
                        - Avoid high-intensity or long-duration training
                        """)
                    elif adjusted_recovery < 60:
                        st.markdown("""
                        **Poor Recovery Recommendations**:
                        
                        Your RHR indicates moderate fatigue and incomplete recovery.
                        
                        **Training Approach**:
                        - Light aerobic training only (30-60% of normal volume)
                        - Keep intensity low (RPE 3-4/10)
                        - Focus on technique or mobility work
                        - Implement additional recovery strategies
                        - Consider adjusting tomorrow's session if still elevated
                        """)
                    elif adjusted_recovery < 80:
                        st.markdown("""
                        **Moderate Recovery Recommendations**:
                        
                        Your RHR indicates some fatigue but adequate recovery for moderate training.
                        
                        **Training Approach**:
                        - Proceed with moderate training (70-90% of planned volume)
                        - Avoid maximum efforts
                        - Focus on steady-state or tempo work
                        - Monitor how you feel during the session
                        - Be prepared to cut the session short if needed
                        """)
                    else:
                        st.markdown("""
                        **Good Recovery Recommendations**:
                        
                        Your RHR indicates good recovery status.
                        
                        **Training Approach**:
                        - Proceed with planned training as scheduled
                        - Suitable for high-intensity or key sessions
                        - No specific modifications needed
                        - Good day for breakthrough workouts or testing
                        """)
                    
                    # Additional insights based on RHR difference
                    st.subheader("Additional Insights")
                    
                    if rhr_difference >= 10:
                        st.warning("""
                        **Warning**: Your RHR is elevated by 10+ bpm, which may indicate:
                        - Significant fatigue from previous training
                        - Possible illness or infection
                        - Severe dehydration
                        - High psychological stress
                        
                        Consider monitoring your temperature and other symptoms, and prioritize recovery strategies.
                        """)
                    elif rhr_difference <= -5:
                        st.success("""
                        **Positive Sign**: Your RHR is significantly lower than baseline, which often indicates:
                        - Improved cardiovascular fitness
                        - Excellent recovery status
                        - Positive adaptation to training
                        - Good parasympathetic tone
                        
                        This is a good indicator that your training is producing the desired adaptations.
                        """)
                
                else:  # Weekly Trend
                    # Calculate 7-day average
                    avg_rhr = sum(rhr_values) / len(rhr_values)
                    
                    # Calculate standard deviation
                    squared_diffs = [(v - avg_rhr)**2 for v in rhr_values]
                    variance = sum(squared_diffs) / len(rhr_values)
                    std_dev = variance**0.5
                    
                    # Calculate trend (simple linear regression)
                    x = list(range(1, 8))
                    y = rhr_values
                    
                    # Calculate slope and intercept
                    n = len(x)
                    sum_x = sum(x)
                    sum_y = sum(y)
                    sum_xy = sum(x_i * y_i for x_i, y_i in zip(x, y))
                    sum_xx = sum(x_i * x_i for x_i in x)
                    
                    slope = (n * sum_xy - sum_x * sum_y) / (n * sum_xx - sum_x * sum_x)
                    intercept = (sum_y - slope * sum_x) / n
                    
                    # Project values based on trend line
                    trend_values = [intercept + slope * x_i for x_i in x]
                    
                    # Calculate day-to-day variability (average absolute difference between consecutive days)
                    day_to_day = []
                    for i in range(1, len(rhr_values)):
                        day_to_day.append(abs(rhr_values[i] - rhr_values[i-1]))
                    
                    avg_day_to_day = sum(day_to_day) / len(day_to_day) if day_to_day else 0
                    
                    # Display result
                    st.markdown("<div class='result-box'>", unsafe_allow_html=True)
                    st.subheader("Resting Heart Rate Trend Analysis")
                    
                    st.markdown(f"""
                    **7-Day Average RHR**: {avg_rhr:.1f} bpm
                    
                    **RHR Variability**: ±{std_dev:.1f} bpm (lower is better)
                    
                    **Day-to-Day Change**: {avg_day_to_day:.1f} bpm (average)
                    
                    **Weekly Trend**: {slope:.2f} bpm/day ({
                        "Increasing (negative)" if slope > 0.5 else
                        "Slightly Increasing" if slope > 0.2 else
                        "Stable" if abs(slope) <= 0.2 else
                        "Slightly Decreasing" if slope > -0.5 else
                        "Decreasing (positive)"
                    })
                    """)
                    
                    # Overall status assessment
                    status = ""
                    color = ""
                    if slope > 0.5:
                        status = "Increasing Fatigue (Recovery Needed)"
                        color = "red"
                    elif slope > 0.2:
                        status = "Slight Fatigue Accumulation (Caution)"
                        color = "orange"
                    elif abs(slope) <= 0.2 and std_dev < 3:
                        status = "Stable (Good Recovery Balance)"
                        color = "green"
                    elif slope < -0.2:
                        status = "Improving Recovery (Positive Adaptation)"
                        color = "lightgreen"
                    else:
                        status = "Mixed Signals (Monitor Closely)"
                        color = "yellow"
                    
                    st.markdown(f"""
                    <h3>Recovery Status: <span style="color:{color}">{status}</span></h3>
                    """, unsafe_allow_html=True)
                    
                    st.markdown("</div>", unsafe_allow_html=True)
                    
                    # Create visualization of RHR trend
                    fig = go.Figure()
                    
                    # Add line for daily RHR values
                    fig.add_trace(go.Scatter(
                        x=list(range(1, 8)),
                        y=rhr_values,
                        mode='lines+markers',
                        name='Daily RHR',
                        line=dict(color='#E6754E', width=2)
                    ))
                    
                    # Add line for trend
                    fig.add_trace(go.Scatter(
                        x=list(range(1, 8)),
                        y=trend_values,
                        mode='lines',
                        name='Trend Line',
                        line=dict(color='rgba(0, 0, 0, 0.7)', width=2, dash='dash')
                    ))
                    
                    fig.update_layout(
                        title='7-Day RHR Trend',
                        xaxis_title='Day',
                        yaxis_title='Resting Heart Rate (bpm)',
                        showlegend=True
                    )
                    
                    st.plotly_chart(fig)
                    
                    # Training recommendations based on trend
                    st.subheader("Training Recommendations")
                    
                    if slope > 0.5:
                        st.markdown("""
                        **Increasing RHR Trend Recommendations**:
                        
                        Your RHR is increasing steadily, indicating fatigue accumulation or incomplete recovery.
                        
                        **Training Approach**:
                        - Reduce training load by 30-50% for 3-5 days
                        - Implement a recovery week
                        - Focus on sleep quality and duration
                        - Emphasize nutrition and hydration
                        - Consider non-training stressors that may be affecting recovery
                        """)
                    elif slope > 0.2:
                        st.markdown("""
                        **Slightly Increasing RHR Trend Recommendations**:
                        
                        Your RHR is showing a slight upward trend, suggesting mild fatigue accumulation.
                        
                        **Training Approach**:
                        - Reduce training intensity (keep volume if desired)
                        - Add an additional easy/recovery day
                        - Emphasize post-workout recovery strategies
                        - Monitor trend closely over next 3-4 days
                        - Be prepared to reduce load further if trend continues
                        """)
                    elif abs(slope) <= 0.2 and std_dev < 3:
                        st.markdown("""
                        **Stable RHR Trend Recommendations**:
                        
                        Your RHR is showing good stability, indicating balanced training load and recovery.
                        
                        **Training Approach**:
                        - Continue with planned training program
                        - Maintain current balance of intensity and volume
                        - Suitable for progressive overload
                        - Good status for key workouts or testing
                        """)
                    elif slope < -0.2:
                        st.markdown("""
                        **Improving RHR Trend Recommendations**:
                        
                        Your RHR is decreasing, indicating improving fitness or enhanced recovery.
                        
                        **Training Approach**:
                        - Good time to introduce progressive overload
                        - Can include challenging workouts
                        - Consider testing performance
                        - Your body is responding well to current training
                        """)
                    else:
                        st.markdown("""
                        **Mixed Signals Recommendations**:
                        
                        Your RHR is showing inconsistent patterns, which may indicate varied recovery or external stressors.
                        
                        **Training Approach**:
                        - Proceed with moderate training
                        - Adjust based on how you feel day-to-day
                        - Monitor other recovery metrics
                        - Pay attention to sleep consistency and quality
                        - Track external stressors
                        """)
        
        elif recovery_method == "Perceived Recovery (Subjective)":
            col1, col2 = st.columns([3, 2])
            
            with col1:
                st.markdown("""
                ### Perceived Recovery Assessment
                
                Subjective measures of recovery are powerful predictors of readiness to train and can often 
                detect changes in recovery status earlier than objective measures.
                
                This assessment combines several validated subjective metrics to quantify recovery status.
                """)
                
                # Sleep quality
                sleep_quality = st.slider("Sleep Quality:", min_value=1, max_value=5, value=3, 
                                         help="1 = Very poor, 5 = Very good")
                
                # Muscle soreness
                muscle_soreness = st.slider("Muscle Soreness:", min_value=1, max_value=5, value=3,
                                           help="1 = Very sore, 5 = No soreness")
                
                # Fatigue level
                fatigue = st.slider("Fatigue Level:", min_value=1, max_value=5, value=3,
                                   help="1 = Very fatigued, 5 = Very fresh")
                
                # Mood state
                mood = st.slider("Mood State:", min_value=1, max_value=5, value=4,
                               help="1 = Very negative, 5 = Very positive")
                
                # Stress level
                stress = st.slider("Stress Level:", min_value=1, max_value=5, value=3,
                                 help="1 = Very stressed, 5 = Very relaxed")
                
                # Additional inputs
                recent_training = st.select_slider(
                    "Recent Training Load:",
                    options=["Very Light", "Light", "Moderate", "Heavy", "Very Heavy"],
                    value="Moderate"
                )
                
                motivation = st.select_slider(
                    "Motivation to Train:",
                    options=["Very Low", "Low", "Moderate", "High", "Very High"],
                    value="High"
                )
            
            with col2:
                st.markdown("""
                ### Importance of Subjective Monitoring
                
                Research has shown that subjective measures are often **more sensitive** than objective measures for detecting changes in athlete recovery status.
                
                **Benefits of Subjective Monitoring**:
                
                - Captures psychological and physiological status
                - Often detects changes before objective measures
                - Simple to implement without equipment
                - Provides holistic view of recovery
                
                **Key Components**:
                
                - **Sleep Quality**: Foundation of recovery
                - **Muscle Soreness**: Indicator of muscle damage
                - **Fatigue**: Overall energy status
                - **Mood**: Psychological readiness
                - **Stress**: External and internal pressure
                
                **Interpreting Scores**:
                - Regular monitoring establishes your baseline
                - Sudden changes are more important than absolute values
                - Consider context (training phase, goals, etc.)
                """)
        
            if st.button("Calculate Recovery Status (Subjective)"):
                # Calculate Total Quality Recovery (TQR) score
                # Base calculation: sum of all factors, max 25 points
                base_score = sleep_quality + muscle_soreness + fatigue + mood + stress
                
                # Convert to percentage
                recovery_percentage = (base_score / 25) * 100
                
                # Adjust for training load
                training_adjustment = {
                    "Very Light": 5,
                    "Light": 2.5,
                    "Moderate": 0,
                    "Heavy": -5,
                    "Very Heavy": -10
                }
                
                # Adjust for motivation (indicator of central nervous system status)
                motivation_adjustment = {
                    "Very Low": -10,
                    "Low": -5,
                    "Moderate": 0,
                    "High": 2.5,
                    "Very High": 5
                }
                
                # Apply adjustments
                adjusted_recovery = recovery_percentage + training_adjustment[recent_training] + motivation_adjustment[motivation]
                adjusted_recovery = max(0, min(100, adjusted_recovery))  # Limit to 0-100%
                
                # Display result
                st.markdown("<div class='result-box'>", unsafe_allow_html=True)
                st.subheader("Perceived Recovery Analysis")
                
                st.markdown(f"""
                **Base Recovery Score**: {base_score}/25 ({recovery_percentage:.1f}%)
                
                **Adjustments**:
                - Recent Training: {recent_training} ({training_adjustment[recent_training]:+.1f}%)
                - Motivation: {motivation} ({motivation_adjustment[motivation]:+.1f}%)
                """)
                
                # Recovery status
                recovery_status = ""
                color = ""
                if adjusted_recovery < 40:
                    recovery_status = "Poor (Not Recovered)"
                    color = "red"
                elif adjusted_recovery < 60:
                    recovery_status = "Low (Partially Recovered)"
                    color = "orange"
                elif adjusted_recovery < 80:
                    recovery_status = "Moderate (Adequately Recovered)"
                    color = "yellow"
                else:
                    recovery_status = "High (Well Recovered)"
                    color = "green"
                
                st.markdown(f"""
                <h3>Recovery Status: <span style="color:{color}">{recovery_status}</span></h3>
                
                **Adjusted Recovery Score**: {adjusted_recovery:.1f}%
                """, unsafe_allow_html=True)
                
                st.markdown("</div>", unsafe_allow_html=True)
                
                # Create visual representation of component scores
                st.subheader("Recovery Component Analysis")
                
                # Radar chart of recovery components
                categories = ['Sleep Quality', 'Muscle Soreness', 'Fatigue Level', 'Mood State', 'Stress Level']
