# Runner Performance Metrics Calculator

A comprehensive web application providing scientifically validated metrics and calculations to help runners of all levels optimize their training and performance.

![Runner Performance Metrics Calculator](Logotype_Light@2x.png)

## Features

This application offers a suite of calculators and analysis tools for runners, including:

- **VO2 Max Calculator**: Estimate maximal oxygen uptake through multiple protocols
- **Training Zones**: Calculate personalized heart rate, pace, and power zones
- **Race Time Predictor**: Predict performance across race distances
- **Running Economy**: Assess efficiency metrics and identify improvements
- **VDOT Calculator**: Apply Jack Daniels' running formula for training
- **Running Power**: Estimate and analyze running power metrics
- **Heart Rate Reserve**: Calculate Karvonen formula zones
- **Training Load & Recovery**: Track training stress and optimize recovery
- **Running Form Analysis**: Identify form issues and receive targeted recommendations

## Scientific Basis

All metrics and recommendations in this application are based on validated scientific research in exercise physiology, biomechanics, and sports science. Each calculator includes references to relevant studies and explanations of the underlying concepts.

## Getting Started

### Prerequisites

- Python 3.7+
- Streamlit
- Pandas
- NumPy
- Matplotlib
- Plotly

### Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/runner-metrics-calculator.git
   cd runner-metrics-calculator
   ```

2. Install required packages:
   ```
   pip install -r requirements.txt
   ```

3. Run the Streamlit app:
   ```
   streamlit run app.py
   ```

4. Access the application in your web browser at `http://localhost:8501`

## Project Structure

The application is organized in a modular structure:

```
runner-metrics-calculator/
├── app.py                  # Main application file
├── requirements.txt        # Dependencies
├── README.md               # Project documentation
├── assets/
│   └── styles.css          # CSS styling
└── modules/
    ├── welcome.py          # Welcome page
    ├── vo2max_calculator.py # VO2 Max Calculator
    └── ...                 # Other calculator modules
```

## How to Contribute

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Exercise physiology research that makes these calculations possible
- The Streamlit team for their amazing framework
- The running community for feedback and suggestions