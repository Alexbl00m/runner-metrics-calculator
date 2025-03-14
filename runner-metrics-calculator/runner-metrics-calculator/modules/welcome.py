import streamlit as st

def render():
    st.markdown("""
    ## Welcome to the Runner Performance Metrics Calculator

    This application provides scientifically validated tools to assess and improve your running performance.
    Whether you're a beginner or an elite athlete, these metrics will help you understand your current 
    fitness level and guide your training effectively.

    ### Features:

    - **VO2 Max Calculation**: Estimate your maximal oxygen uptake using various protocols
    - **Training Zones**: Determine your personalized heart rate and pace zones
    - **Race Time Prediction**: Predict race times across different distances
    - **Running Economy**: Calculate how efficiently you use oxygen while running
    - **VDOT Calculator**: Use Jack Daniels' VDOT system to evaluate performance
    - **Running Power**: Estimate your running power output
    - **Heart Rate Reserve**: Calculate and apply the Karvonen formula
    - **Training Load & Recovery**: Track your training stress and recovery
    - **Running Form Analysis**: Evaluate key running form metrics

    ### How to use:

    1. Select a calculator from the sidebar
    2. Input your running data
    3. Get your results and recommendations
    4. Track your metrics over time to monitor progress

    Each calculator includes scientific background information and references to help you understand 
    the metrics and how to use them effectively in your training.
    """)

    st.info("Select your experience level and training frequency in the sidebar to get personalized recommendations.")

    # Du kan lägga till logik baserat på användarens profil om det behövs
    # Exempel:
    # if st.session_state.get('experience_level') == "Beginner":
    #     st.markdown("### Beginner Recommendations: ...")

        # Display appropriate guidance based on user's experience level
        if experience_level == "Beginner":
            st.markdown("""
                ### Beginner Recommendations:
        
                As a beginner runner, focus on these key metrics:
                - **Heart Rate Reserve**: Understand your training zones
                - **Training Zones**: Learn appropriate effort levels
                - **Race Time Predictor**: Set realistic goals
        
                Start by establishing consistent running habits and gradually build your endurance before 
                focusing on performance metrics.
                """)
        
            # Add beginner-focused tips
            with st.expander("Tips for Beginners"):
                st.markdown("""
                    **Getting Started with Running Metrics**:
        
                    1. **Focus on consistency over intensity**
                       - Regular easy runs are the foundation of improvement
                       - Aim for 3-4 runs per week before adding speed work
        
                    2. **Use heart rate as your primary intensity guide**
                       - Learn your zones using the Heart Rate Reserve calculator
                       - Keep most runs in Zone 1-2 (easy/conversational pace)
        
                    3. **Progression guidelines**
                       - Increase weekly volume by no more than 10% per week
                       - Add one "quality" session per week after building a base
                       - Include rest days between harder efforts
        
                    4. **Key metrics to track**
                       - Resting heart rate (sign of improving fitness when it decreases)
                       - Easy pace (should gradually get faster at the same heart rate)
                       - Distance of longest run (build gradually)
                    """)
        
            # Add beginner training plan example
            with st.expander("Sample Beginner Training Plan"):
                st.markdown("""
                    **4-Week Beginner Plan**:
        
                    **Week 1:**
                    - Monday: Rest or cross-train
                    - Tuesday: 20 min easy run (Zone 2)
                    - Wednesday: Rest or cross-train
                    - Thursday: 20 min easy run (Zone 2)
                    - Friday: Rest
                    - Saturday: 25 min easy run (Zone 2)
                    - Sunday: Rest
        
                    **Week 2:**
                    - Monday: Rest or cross-train
                    - Tuesday: 25 min easy run (Zone 2)
                    - Wednesday: Rest or cross-train
                    - Thursday: 25 min easy run with 5×30 sec pickups
                    - Friday: Rest
                    - Saturday: 30 min easy run (Zone 2)
                    - Sunday: Rest
        
                    **Weeks 3-4:**
                    - Continue pattern with gradual increases in duration
                    - Add one additional 5-minute block each week to longest run
                    - Incorporate brief pickups (15-30 seconds) within easy runs
        
                    Use the calculators in this app to determine your appropriate heart rate zones and paces.
                    """)
        
        elif experience_level == "Intermediate":
            st.markdown("""
                ### Intermediate Recommendations:
        
                As an intermediate runner, these metrics will be most valuable:
                - **VO2 Max Calculator**: Track your cardiorespiratory fitness
                - **VDOT Calculator**: Determine appropriate training paces
                - **Training Load & Recovery**: Balance training stress with recovery
        
                Begin incorporating structured workouts based on your metrics to improve performance.
                """)
        
            # Add intermediate-focused tips
            with st.expander("Tips for Intermediate Runners"):
                st.markdown("""
                    **Advancing Your Training with Metrics**:
        
                    1. **Structured training approach**
                       - Follow an 80/20 approach (80% easy, 20% hard)
                       - Include 2-3 quality sessions per week
                       - Utilize specific paces from VDOT calculator
        
                    2. **Monitoring training load**
                       - Track weekly mileage/time and intensity
                       - Watch for signs of excessive fatigue
                       - Plan recovery weeks every 3-4 weeks
        
                    3. **Race-specific preparation**
                       - Use the Race Time Predictor to set realistic goals
                       - Incorporate race-pace work in training
                       - Practice nutrition and hydration strategies
        
                    4. **Key metrics to track**
                       - VO2 Max or VDOT (improvement over time)
                       - Training load (weekly and 4-week average)
                       - Race times at different distances
                    """)
        
            # Add intermediate training plan example
            with st.expander("Sample Intermediate Training Plan"):
                st.markdown("""
                    **Weekly Intermediate Plan Structure**:
        
                    **Monday:** Recovery run (30-40 min, Zone 1-2)
        
                    **Tuesday:** Quality Session - Example: Threshold Training
                    - 15 min warm-up
                    - 4-6 × 5 minutes at threshold pace (from VDOT calculator)
                    - 1-2 min recovery between intervals
                    - 10 min cool-down
        
                    **Wednesday:** Easy run (40-50 min, Zone 2)
        
                    **Thursday:** Quality Session - Example: VO2 Max Intervals
                    - 15 min warm-up
                    - 5-8 × 3 minutes at interval pace (from VDOT calculator)
                    - 3 min recovery between intervals
                    - 10 min cool-down
        
                    **Friday:** Rest or very easy recovery run
        
                    **Saturday:** Long run (70-90 min at easy pace)
        
                    **Sunday:** Recovery run or cross-training
        
                    Use the calculators in this app to determine your appropriate heart rate zones, paces, and monitor your training load.
                    """)
        
        elif experience_level == "Advanced" or experience_level == "Elite":
            st.markdown("""
                ### Advanced/Elite Recommendations:
        
                At your level, focus on these sophisticated metrics:
                - **Running Economy**: Optimize your efficiency
                - **Running Power**: Understand your output in various conditions
                - **Running Form Analysis**: Fine-tune your biomechanics
        
                These metrics can help you identify small improvements that lead to significant performance gains.
                """)
        
            # Add advanced-focused tips
            with st.expander("Tips for Advanced/Elite Runners"):
                st.markdown("""
                    **Optimizing Performance with Advanced Metrics**:
        
                    1. **Precision in training**
                       - Use power-based training for consistent stimulus
                       - Monitor running economy for efficiency improvements
                       - Implement periodization with targeted blocks
        
                    2. **Recovery optimization**
                       - Track HRV (heart rate variability) for recovery status
                       - Use metrics to identify early signs of overtraining
                       - Implement recovery protocols based on fatigue metrics
        
                    3. **Marginal gains approach**
                       - Use Running Form Analysis to identify mechanical inefficiencies
                       - Monitor biomechanical metrics (ground contact time, vertical oscillation)
                       - Track running power:weight ratio improvements
        
                    4. **Race optimization**
                       - Develop precise pacing strategies based on power and critical velocity
                       - Consider environmental conditions in race planning
                       - Create detailed race nutrition plans based on metabolic requirements
                    """)
        
            # Add advanced training approach
            with st.expander("Advanced Training Approaches"):
                st.markdown("""
                    **Advanced Training Methodologies**:
        
                    **Polarized Training Model**
                    - 80-85% of training at low intensity (below ventilatory threshold)
                    - 15-20% at high intensity (above respiratory compensation threshold)
                    - Minimal time spent in the "moderate" zone
                    - Scientific research indicates this approach optimizes adaptations
        
                    **Critical Power/Velocity Approach**
                    - Determine Critical Power (CP) or Critical Velocity (CV)
                    - Train below CP for endurance development
                    - Train at CP for threshold improvement
                    - Train above CP for VO2max and anaerobic capacity
                    - Use the Running Power calculator to identify your zones
        
                    **Block Periodization**
                    - Concentrated blocks focusing on specific abilities
                    - Example: 3-week blocks alternating between:
                      - Threshold/tempo focus
                      - VO2max/interval focus
                      - Specific endurance/race pace focus
                    - Monitor with Training Load calculator to prevent overtraining
        
                    **Advanced Recovery Protocols**
                    - Implement HRV-guided training decisions
                    - Utilize strategic nutrition timing
                    - Incorporate altitude or heat training when appropriate
                    - Monitor sleep quality metrics
                    """)
        
        # General Resources section for all experience levels
        st.subheader("Resources and References")
        
        with st.expander("Scientific References"):
            st.markdown("""
                **Key Research in Running Science**:
        
                **VO2 Max & Performance Prediction**
                - Daniels, J., & Gilbert, J. (1979). *Oxygen power: Performance tables for distance runners*.
                - Midgley, A. W., et al. (2007). "Impact of the number of treadmill familiarization sessions on VO2max in untrained adults." *Journal of Sports Science* 25(14): 1519-1525.
        
                **Training Intensity Distribution**
                - Seiler, S., & Tønnessen, E. (2009). "Intervals, thresholds, and long slow distance: the role of intensity and duration in endurance training." *Sportscience* 13: 32-53.
                - Stöggl, T. L., & Sperlich, B. (2015). "Polarized training has greater impact on key endurance variables than threshold, high intensity, or high volume training." *Frontiers in Physiology* 6: 295.
        
                **Running Economy & Biomechanics**
                - Moore, I. S. (2016). "Is There an Economical Running Technique? A Review of Modifiable Biomechanical Factors Affecting Running Economy." *Sports Medicine* 46(6): 793-807.
                - Barnes, K. R., & Kilding, A. E. (2015). "Running economy: measurement, norms, and determining factors." *Sports Medicine - Open* 1(1): 8.
        
                **Training Load & Recovery**
                - Banister, E. W. (1991). "Modeling elite athletic performance." *Physiological testing of elite athletes*: 403-424.
                - Bellenger, C. R., et al. (2016). "Monitoring athletic training status through autonomic heart rate regulation: a systematic review and meta-analysis." *Sports Medicine* 46(10): 1461-1486.
                """)
        
        with st.expander("Recommended Books"):
            st.markdown("""
                **Essential Running Books**:
        
                **Training Science & Methodology**
                - *Daniels' Running Formula* by Jack Daniels
                - *Training for the Uphill Athlete* by Kilian Jornet, Scott Johnston & Steve House
                - *Science of Running* by Steve Magness
                - *Advanced Marathoning* by Pete Pfitzinger & Scott Douglas
        
                **Running Form & Biomechanics**
                - *Running Form* by Owen Anderson
                - *Running Rewired* by Jay Dicharry
                - *Running Science* by Owen Anderson
        
                **Mental Aspects & Racing**
                - *Endure* by Alex Hutchinson
                - *Let Your Mind Run* by Deena Kastor
                - *How Bad Do You Want It?* by Matt Fitzgerald
                """)
        
        # Quick Start Guide
        st.subheader("Quick Start Guide")
        
        st.markdown("""
            **Start using the app in 3 easy steps:**
        
            1. **Set your profile**
               - Use the sidebar to set your experience level
               - This customizes recommendations for your specific needs
        
            2. **Choose your calculator**
               - Select a calculator from the sidebar navigation menu
               - Start with the calculators recommended for your experience level
        
            3. **Enter your data and get results**
               - Each calculator will prompt you for relevant information
               - After calculation, review your results and personalized recommendations
               - Use these insights to optimize your training
            """)
