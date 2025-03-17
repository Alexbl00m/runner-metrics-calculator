# Runner Metrics Calculator

A comprehensive Streamlit web application for runners to calculate, analyze, and visualize their running metrics.

## Features

- **Pace Calculator**: Convert between different pace metrics (min/km, min/mile, km/h, mph)
- **Race Time Predictor**: Predict finish times for various race distances based on previous performances
- **Split Calculator**: Generate even or negative splits for race planning
- **Metrics Analyzer**: Upload and analyze your running data with interactive visualizations

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/runner-metrics-calculator.git
   cd runner-metrics-calculator
   ```

2. Create a virtual environment and activate it:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Run the application:
   ```
   streamlit run app.py
   ```

## Project Structure

```
runner-metrics-calculator/
├── app.py                  # Main Streamlit application
├── modules/                # Application modules
│   ├── __init__.py
│   ├── welcome.py          # Welcome page and about sections
│   ├── pace_calculator.py  # Pace calculation utilities
│   └── metrics_analyzer.py # Data analysis functionality
├── requirements.txt        # Python dependencies
└── README.md               # This file
```

## Usage

1. Launch the application by running `streamlit run app.py`
2. Navigate between different sections using the sidebar
3. For metrics analysis, upload a CSV or Excel file containing your running data
4. The application supports multiple data formats, including Strava and Garmin exports

## Data Format

For the metrics analyzer, the application supports the following data formats:

- Standard format: columns for date, distance, time
- Strava exports: Activity Date, Distance, Moving Time
- Garmin exports: start_time, distance, duration
- Simple format: date, km, pace

If your data doesn't match any of these formats, you can manually map the columns in the interface.

## Dependencies

- streamlit
- pandas
- numpy
- plotly

## License

This project is open source and available under the [MIT License](LICENSE).

## Contributing

Contributions, issues, and feature requests are welcome! Feel free to check the [issues page](https://github.com/yourusername/runner-metrics-calculator/issues).