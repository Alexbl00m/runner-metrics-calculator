import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import io

def show_metrics_analyzer():
    """
    Display the metrics analyzer interface for uploading and analyzing running data
    """
    st.title("Running Metrics Analyzer")
    
    st.markdown("""
    <div class="result-box">
    Upload your running data to get insights and visualizations of your performance metrics.
    </div>
    """, unsafe_allow_html=True)
    
    # File uploader
    uploaded_file = st.file_uploader("Upload your running data (CSV or Excel file)", 
                                     type=["csv", "xlsx", "xls"])
    
    if uploaded_file is not None:
        try:
            # Determine file type and read accordingly
            if uploaded_file.name.endswith('.csv'):
                df = pd.read_csv(uploaded_file)
            else:
                df = pd.read_excel(uploaded_file)
            
            # Display preview of the data
            st.markdown("### Data Preview")
            st.dataframe(df.head())
            
            # Try to determine data format and extract key metrics
            data_format = detect_data_format(df)
            
            if data_format == "unknown":
                st.warning("Unable to automatically detect your data format. Please specify the columns manually.")
                df_processed = manually_map_columns(df)
            else:
                st.success(f"Detected data format: {data_format}")
                df_processed = process_data(df, data_format)
            
            if df_processed is not None:
                analyze_metrics(df_processed)
        
        except Exception as e:
            st.error(f"Error processing the file: {str(e)}")
            st.markdown("Please make sure the file contains valid running data with columns for distance, time/pace, and date.")

def detect_data_format(df):
    """
    Try to automatically detect the format of the uploaded running data
    """
    columns = [col.lower() for col in df.columns]
    
    # Check for common formats
    if all(col in columns for col in ['date', 'distance', 'time']):
        return "standard"
    elif all(col in columns for col in ['activity date', 'distance', 'moving time']):
        return "strava"
    elif all(col in columns for col in ['start_time', 'distance', 'duration']):
        return "garmin"
    elif all(col in columns for col in ['date', 'km', 'pace']):
        return "simple"
    else:
        return "unknown"

def manually_map_columns(df):
    """
    Allow the user to manually map columns when format can't be detected
    """
    st.markdown("### Map Your Data Columns")
    st.markdown("Please select which columns correspond to each metric:")
    
    date_col = st.selectbox("Date column:", ["None"] + list(df.columns))
    distance_col = st.selectbox("Distance column:", ["None"] + list(df.columns))
    time_col = st.selectbox("Time/Duration column:", ["None"] + list(df.columns))
    pace_col = st.selectbox("Pace column (if available, otherwise select None):", 
                           ["None"] + list(df.columns))
    hr_col = st.selectbox("Heart rate column (if available, otherwise select None):", 
                         ["None"] + list(df.columns))
    
    if date_col == "None" or distance_col == "None" or (time_col == "None" and pace_col == "None"):
        st.warning("Please select at least date, distance, and either time or pace columns.")
        return None
    
    # Create a new dataframe with standardized column names
    df_processed = df.copy()
    df_processed['Date'] = df[date_col] if date_col != "None" else None
    df_processed['Distance'] = df[distance_col] if distance_col != "None" else None
    
    if time_col != "None":
        df_processed['Time'] = df[time_col]
    
    if pace_col != "None":
        df_processed['Pace'] = df[pace_col]
    
    if hr_col != "None":
        df_processed['HeartRate'] = df[hr_col]
    
    # Ensure Date is in datetime format
    try:
        df_processed['Date'] = pd.to_datetime(df_processed['Date'])
    except:
        st.warning("Unable to convert date column to datetime format. Please ensure it's in a valid date format.")
    
    # Ensure Distance is numeric
    try:
        df_processed['Distance'] = pd.to_numeric(df_processed['Distance'])
    except:
        st.warning("Unable to convert distance column to numeric format.")
    
    # If we have Time but not Pace, calculate Pace
    if 'Time' in df_processed.columns and 'Pace' not in df_processed.columns:
        try:
            # Convert time strings (HH:MM:SS) to minutes
            if df_processed['Time'].dtype == object:
                df_processed['TimeMinutes'] = df_processed['Time'].apply(convert_time_to_minutes)
            else:
                df_processed['TimeMinutes'] = df_processed['Time']
                
            # Calculate pace as minutes per kilometer
            df_processed['Pace'] = df_processed['TimeMinutes'] / df_processed['Distance']
        except:
            st.warning("Unable to calculate pace from time and distance.")
    
    return df_processed

def process_data(df, data_format):
    """
    Process data based on detected format
    """
    df_processed = df.copy()
    
    if data_format == "standard":
        # Standard format with date, distance, time columns
        df_processed['Date'] = pd.to_datetime(df['date'])
        df_processed['Distance'] = pd.to_numeric(df['distance'])
        
        if df['time'].dtype == object:
            df_processed['TimeMinutes'] = df['time'].apply(convert_time_to_minutes)
        else:
            df_processed['TimeMinutes'] = df['time']
        
        df_processed['Pace'] = df_processed['TimeMinutes'] / df_processed['Distance']
        
        if 'heart_rate' in df.columns:
            df_processed['HeartRate'] = pd.to_numeric(df['heart_rate'])
    
    elif data_format == "strava":
        # Strava export format
        df_processed['Date'] = pd.to_datetime(df['Activity Date'])
        df_processed['Distance'] = pd.to_numeric(df['Distance'])
        
        if 'Moving Time' in df.columns:
            df_processed['TimeMinutes'] = df['Moving Time'].apply(convert_time_to_minutes)
        elif 'Elapsed Time' in df.columns:
            df_processed['TimeMinutes'] = df['Elapsed Time'].apply(convert_time_to_minutes)
        
        df_processed['Pace'] = df_processed['TimeMinutes'] / df_processed['Distance']
        
        if 'Average Heart Rate' in df.columns:
            df_processed['HeartRate'] = pd.to_numeric(df['Average Heart Rate'])
    
    elif data_format == "garmin":
        # Garmin export format
        df_processed['Date'] = pd.to_datetime(df['start_time'])
        df_processed['Distance'] = pd.to_numeric(df['distance']) / 1000  # Convert meters to kilometers
        
        if 'duration' in df.columns:
            # Convert seconds to minutes
            df_processed['TimeMinutes'] = pd.to_numeric(df['duration']) / 60
        
        df_processed['Pace'] = df_processed['TimeMinutes'] / df_processed['Distance']
        
        if 'average_heart_rate' in df.columns:
            df_processed['HeartRate'] = pd.to_numeric(df['average_heart_rate'])
    
    elif data_format == "simple":
        # Simple format with date, km, pace
        df_processed['Date'] = pd.to_datetime(df['date'])
        df_processed['Distance'] = pd.to_numeric(df['km'])
        
        if 'pace' in df.columns:
            if df['pace'].dtype == object:
                # Convert pace in format MM:SS to minutes
                df_processed['Pace'] = df['pace'].apply(convert_pace_to_minutes)
            else:
                df_processed['Pace'] = df['pace']
        
        # Calculate time from pace and distance
        df_processed['TimeMinutes'] = df_processed['Pace'] * df_processed['Distance']
        
        if 'heart_rate' in df.columns or 'hr' in df.columns:
            hr_col = 'heart_rate' if 'heart_rate' in df.columns else 'hr'
            df_processed['HeartRate'] = pd.to_numeric(df[hr_col])
    
    # Sort by date
    df_processed = df_processed.sort_values('Date')
    
    return df_processed

def convert_time_to_minutes(time_str):
    """
    Convert time string (HH:MM:SS or MM:SS) to minutes
    """
    if pd.isnull(time_str):
        return np.nan
    
    if isinstance(time_str, (int, float)):
        return time_str
    
    parts = time_str.split(':')
    
    if len(parts) == 3:  # HH:MM:SS
        return int(parts[0]) * 60 + int(parts[1]) + int(parts[2]) / 60
    elif len(parts) == 2:  # MM:SS
        return int(parts[0]) + int(parts[1]) / 60
    else:
        try:
            return float(time_str)
        except:
            return np.nan

def convert_pace_to_minutes(pace_str):
    """
    Convert pace string (MM:SS per km) to minutes per km
    """
    if pd.isnull(pace_str):
        return np.nan
    
    if isinstance(pace_str, (int, float)):
        return pace_str
    
    parts = pace_str.split(':')
    
    if len(parts) == 2:  # MM:SS
        return int(parts[0]) + int(parts[1]) / 60
    else:
        try:
            return float(pace_str)
        except:
            return np.nan

def analyze_metrics(df):
    """
    Analyze the processed running data and display insights
    """
    # Create tabs for different analyses
    tab1, tab2, tab3, tab4 = st.tabs(["Overview", "Distance Analysis", "Pace Analysis", "Progress Over Time"])
    
    with tab1:
        show_overview(df)
    
    with tab2:
        show_distance_analysis(df)
    
    with tab3:
        show_pace_analysis(df)
    
    with tab4:
        show_progress_analysis(df)

def show_overview(df):
    """
    Display overview of running metrics
    """
    st.header("Running Overview")
    
    # Calculate summary statistics
    total_runs = len(df)
    total_distance = df['Distance'].sum()
    avg_distance = df['Distance'].mean()
    
    if 'TimeMinutes' in df.columns:
        total_time_min = df['TimeMinutes'].sum()
        avg_time_min = df['TimeMinutes'].mean()
        time_hours = int(total_time_min // 60)
        time_mins = int(total_time_min % 60)
        time_str = f"{time_hours}h {time_mins}m"
    else:
        time_str = "N/A"
        
    if 'Pace' in df.columns:
        avg_pace = df['Pace'].mean()
        pace_min = int(avg_pace)
        pace_sec = int((avg_pace % 1) * 60)
        pace_str = f"{pace_min}:{pace_sec:02d} min/km"
    else:
        pace_str = "N/A"
    
    # Date range
    start_date = df['Date'].min().strftime('%Y-%m-%d')
    end_date = df['Date'].max().strftime('%Y-%m-%d')
    date_range = f"{start_date} to {end_date}"
    
    # Display summary metrics
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total Runs", f"{total_runs}")
        st.metric("Total Distance", f"{total_distance:.2f} km")
    
    with col2:
        st.metric("Total Running Time", time_str)
        st.metric("Average Pace", pace_str)
    
    with col3:
        st.metric("Average Distance", f"{avg_distance:.2f} km")
        st.metric("Date Range", date_range)
    
    # Recent runs
    st.markdown("### Recent Runs")
    recent_runs = df.sort_values('Date', ascending=False).head(5)
    
    # Format for display
    display_df = recent_runs[['Date', 'Distance']].copy()
    display_df['Date'] = display_df['Date'].dt.strftime('%Y-%m-%d')
    
    if 'TimeMinutes' in recent_runs.columns:
        display_df['Duration'] = recent_runs['TimeMinutes'].apply(
            lambda x: f"{int(x // 60)}h {int(x % 60)}m" if x >= 60 else f"{int(x)}m {int((x % 1) * 60)}s"
        )
    
    if 'Pace' in recent_runs.columns:
        display_df['Pace'] = recent_runs['Pace'].apply(
            lambda x: f"{int(x)}:{int((x % 1) * 60):02d} min/km"
        )
    
    st.dataframe(display_df)
    
    # Monthly distance chart
    st.markdown("### Monthly Distance")
    
    # Group by month and sum distances
    df['YearMonth'] = df['Date'].dt.to_period('M')
    monthly_distance = df.groupby('YearMonth')['Distance'].sum().reset_index()
    monthly_distance['YearMonth'] = monthly_distance['YearMonth'].astype(str)
    
    fig = px.bar(
        monthly_distance, 
        x='YearMonth', 
        y='Distance',
        labels={'YearMonth': 'Month', 'Distance': 'Distance (km)'},
        title='Monthly Running Distance'
    )
    
    st.plotly_chart(fig, use_container_width=True)

def show_distance_analysis(df):
    """
    Display distance analysis
    """
    st.header("Distance Analysis")
    
    # Calculate distance metrics
    max_distance = df['Distance'].max()
    min_distance = df['Distance'].min()
    median_distance = df['Distance'].median()
    
    # Longest run
    longest_run = df.loc[df['Distance'].idxmax()]
    longest_date = longest_run['Date'].strftime('%Y-%m-%d')
    
    # Distance distribution
    st.markdown("### Distance Distribution")
    
    fig = px.histogram(
        df, 
        x='Distance',
        nbins=20,
        labels={'Distance': 'Distance (km)'},
        title='Distribution of Run Distances'
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Distance metrics
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Longest Run", f"{max_distance:.2f} km")
        st.markdown(f"**Date:** {longest_date}")
    
    with col2:
        st.metric("Shortest Run", f"{min_distance:.2f} km")
    
    with col3:
        st.metric("Median Distance", f"{median_distance:.2f} km")
    
    # Distance by day of week
    st.markdown("### Distance by Day of Week")
    
    df['DayOfWeek'] = df['Date'].dt.day_name()
    day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    
    day_distance = df.groupby('DayOfWeek')['Distance'].agg(['sum', 'mean', 'count']).reset_index()
    day_distance['sum'] = day_distance['sum'].round(2)
    day_distance['mean'] = day_distance['mean'].round(2)
    
    # Reorder days
    day_distance['DayOfWeek'] = pd.Categorical(day_distance['DayOfWeek'], categories=day_order, ordered=True)
    day_distance = day_distance.sort_values('DayOfWeek')
    
    fig = px.bar(
        day_distance,
        x='DayOfWeek',
        y='sum',
        title='Total Distance by Day of Week',
        labels={'DayOfWeek': 'Day', 'sum': 'Total Distance (km)'}
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Average distance by day of week
    fig = px.bar(
        day_distance,
        x='DayOfWeek',
        y='mean',
        title='Average Distance by Day of Week',
        labels={'DayOfWeek': 'Day', 'mean': 'Average Distance (km)'}
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Number of runs by day of week
    fig = px.bar(
        day_distance,
        x='DayOfWeek',
        y='count',
        title='Number of Runs by Day of Week',
        labels={'DayOfWeek': 'Day', 'count': 'Number of Runs'}
    )
    
    st.plotly_chart(fig, use_container_width=True)

def show_pace_analysis(df):
    """
    Display pace analysis
    """
    st.header("Pace Analysis")
    
    if 'Pace' not in df.columns:
        st.warning("Pace data not available for analysis.")
        return
    
    # Calculate pace metrics
    fastest_pace = df['Pace'].min()
    slowest_pace = df['Pace'].max()
    avg_pace = df['Pace'].mean()
    
    # Format pace values
    fastest_pace_str = f"{int(fastest_pace)}:{int((fastest_pace % 1) * 60):02d} min/km"
    slowest_pace_str = f"{int(slowest_pace)}:{int((slowest_pace % 1) * 60):02d} min/km"
    avg_pace_str = f"{int(avg_pace)}:{int((avg_pace % 1) * 60):02d} min/km"
    
    # Fastest run
    fastest_run = df.loc[df['Pace'].idxmin()]
    fastest_date = fastest_run['Date'].strftime('%Y-%m-%d')
    fastest_distance = fastest_run['Distance']
    
    # Display pace metrics
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Fastest Pace", fastest_pace_str)
        st.markdown(f"**Date:** {fastest_date}")
        st.markdown(f"**Distance:** {fastest_distance:.2f} km")
    
    with col2:
        st.metric("Slowest Pace", slowest_pace_str)
    
    with col3:
        st.metric("Average Pace", avg_pace_str)
    
    # Pace distribution
    st.markdown("### Pace Distribution")
    
    fig = px.histogram(
        df, 
        x='Pace',
        nbins=20,
        labels={'Pace': 'Pace (min/km)'},
        title='Distribution of Running Paces'
    )
    
    # Format x-axis labels to show minutes:seconds
    fig.update_xaxes(
        tickvals=[i for i in range(int(fastest_pace), int(slowest_pace)+1)],
        ticktext=[f"{i}:00" for i in range(int(fastest_pace), int(slowest_pace)+1)]
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Pace vs Distance scatter plot
    st.markdown("### Pace vs Distance")
    
    fig = px.scatter(
        df,
        x='Distance',
        y='Pace',
        title='Pace vs Distance',
        labels={'Distance': 'Distance (km)', 'Pace': 'Pace (min/km)'},
        trendline='lowess'  # Add a smoothed trendline
    )
    
    # Format y-axis labels to show minutes:seconds
    pace_min = int(fastest_pace)
    pace_max = int(slowest_pace) + 1
    
    fig.update_yaxes(
        tickvals=[i for i in range(pace_min, pace_max)],
        ticktext=[f"{i}:00" for i in range(pace_min, pace_max)]
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Pace over time
    st.markdown("### Pace Over Time")
    
    fig = px.scatter(
        df,
        x='Date',
        y='Pace',
        size='Distance',  # Bubble size represents distance
        title='Pace Trends Over Time',
        labels={'Date': 'Date', 'Pace': 'Pace (min/km)', 'Distance': 'Distance (km)'},
        trendline='lowess'  # Add a smoothed trendline
    )
    
    # Format y-axis labels to show minutes:seconds
    fig.update_yaxes(
        tickvals=[i for i in range(pace_min, pace_max)],
        ticktext=[f"{i}:00" for i in range(pace_min, pace_max)]
    )
    
    st.plotly_chart(fig, use_container_width=True)

def show_progress_analysis(df):
    """
    Display progress analysis over time
    """
    st.header("Progress Over Time")
    
    # Distance progress over time
    st.markdown("### Distance Trends")
    
    # Weekly distance
    df['Week'] = df['Date'].dt.to_period('W')
    weekly_distance = df.groupby('Week')['Distance'].sum().reset_index()
    weekly_distance['Week'] = weekly_distance['Week'].astype(str)
    
    fig = px.line(
        weekly_distance,
        x='Week',
        y='Distance',
        title='Weekly Running Distance',
        labels={'Week': 'Week', 'Distance': 'Distance (km)'},
        markers=True
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Running streak analysis
    st.markdown("### Running Streak Analysis")
    
    # Sort by date
    df_sorted = df.sort_values('Date')
    
    # Calculate days between consecutive runs
    df_sorted['NextDate'] = df_sorted['Date'].shift(-1)
    df_sorted['DaysBetween'] = (df_sorted['NextDate'] - df_sorted['Date']).dt.days
    
    # Identify streaks (consecutive days)
    df_sorted['NewStreak'] = df_sorted['DaysBetween'] > 1
    df_sorted['StreakId'] = df_sorted['NewStreak'].cumsum()
    
    # Calculate streak lengths
    streak_lengths = df_sorted.groupby('StreakId').size()
    max_streak = streak_lengths.max()
    current_streak = streak_lengths.iloc[-1] if df_sorted['DaysBetween'].iloc[-1] <= 1 else 0
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric("Longest Run Streak", f"{max_streak} days")
    
    with col2:
        st.metric("Current Run Streak", f"{current_streak} days")
    
    # Progress indicators
    st.markdown("### Progress Indicators")
    
    # Calculate 4-week moving averages for key metrics
    df['YearWeek'] = df['Date'].dt.to_period('W')
    weekly_metrics = df.groupby('YearWeek').agg({
        'Distance': 'sum',
        'Pace': 'mean'
    }).reset_index()
    
    weekly_metrics['YearWeek'] = weekly_metrics['YearWeek'].astype(str)
    weekly_metrics['Distance_MA'] = weekly_metrics['Distance'].rolling(window=4).mean()
    
    if 'Pace' in weekly_metrics.columns:
        weekly_metrics['Pace_MA'] = weekly_metrics['Pace'].rolling(window=4).mean()
    
    # Plot moving average of weekly distance
    fig = px.line(
        weekly_metrics,
        x='YearWeek',
        y=['Distance', 'Distance_MA'],
        title='Weekly Distance with 4-Week Moving Average',
        labels={'value': 'Distance (km)', 'YearWeek': 'Week', 'variable': 'Metric'},
        color_discrete_map={'Distance': 'lightblue', 'Distance_MA': 'darkblue'}
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Plot moving average of pace if available
    if 'Pace' in weekly_metrics.columns:
        fig = px.line(
            weekly_metrics,
            x='YearWeek',
            y=['Pace', 'Pace_MA'],
            title='Weekly Average Pace with 4-Week Moving Average',
            labels={'value': 'Pace (min/km)', 'YearWeek': 'Week', 'variable': 'Metric'},
            color_discrete_map={'Pace': 'lightgreen', 'Pace_MA': 'darkgreen'}
        )
        
        # Customize y-axis to show minutes:seconds format
        min_pace = weekly_metrics[['Pace', 'Pace_MA']].min().min()
        max_pace = weekly_metrics[['Pace', 'Pace_MA']].max().max()
        
        pace_min = int(min_pace)
        pace_max = int(max_pace) + 1
        
        fig.update_yaxes(
            tickvals=[i for i in range(pace_min, pace_max)],
            ticktext=[f"{i}:00" for i in range(pace_min, pace_max)]
        )
        
        st.plotly_chart(fig, use_container_width=True)