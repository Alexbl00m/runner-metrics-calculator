"""
Calculation utilities for the Runner Performance Metrics Calculator.
"""
import numpy as np
from math import exp, log


def calculate_vo2max_cooper(distance_m, age, gender="Male"):
    """
    Calculate VO2 Max using Cooper test formula.

    Args:
        distance_m (float): Distance covered in meters during 12-minute test
        age (int): Age in years
        gender (str, optional): "Male" or "Female". Defaults to "Male".

    Returns:
        float: Estimated VO2 Max in ml/kg/min
    """
    # Cooper formula (ml/kg/min)
    vo2max = (distance_m - 504.9) / 44.73

    # Age/sex adjusted
    if gender == "Female":
        vo2max = vo2max * 0.85  # Women typically 15% lower than men

    return vo2max


def calculate_vo2max_bruce(time_min, gender="Male"):
    """
    Calculate VO2 Max using Bruce protocol formula.

    Args:
        time_min (float): Time completed on test in minutes
        gender (str, optional): "Male" or "Female". Defaults to "Male".

    Returns:
        float: Estimated VO2 Max in ml/kg/min
    """
    if gender == "Male":
        vo2max = 14.8 - (1.379 * time_min) + (0.451 * time_min ** 2) - (0.012 * time_min ** 3)
    else:  # Female
        vo2max = 4.38 * time_min - 3.9

    return vo2max


def calculate_vdot_from_performance(distance_km, time_seconds):
    """
    Calculate VDOT value from race performance using Daniels' formula.

    Args:
        distance_km (float): Race distance in kilometers
        time_seconds (float): Race time in seconds

    Returns:
        float: VDOT value
    """
    # Calculate velocity in meters per minute
    velocity = (distance_km * 1000) / (time_seconds / 60)

    # Calculate percent VO2 max for given race distance
    percent_vo2 = 0.8 + 0.1894393 * exp(-0.012778 * (time_seconds / 60)) + 0.2989558 * exp(
        -0.1932605 * (time_seconds / 60))

    # Calculate VO2 max
    vo2 = -4.60 + 0.182258 * velocity + 0.000104 * velocity * velocity

    # Calculate VDOT
    vdot = vo2 / percent_vo2

    return vdot


def calculate_training_paces_from_vdot(vdot):
    """
    Calculate training paces based on VDOT value.

    Args:
        vdot (float): VDOT value

    Returns:
        dict: Dictionary of training paces in seconds per kilometer
    """
    # Calculate training paces (seconds per km) based on VDOT value
    # These formulas are derived from Daniels' Running Formula
    paces = {
        "easy_min": (180 * (vdot ** -0.79)) * (60 / 1000),
        "easy_max": (150 * (vdot ** -0.75)) * (60 / 1000),
        "marathon": (120 * (vdot ** -0.73)) * (60 / 1000),
        "threshold": (100 * (vdot ** -0.71)) * (60 / 1000),
        "interval": (77 * (vdot ** -0.67)) * (60 / 1000),
        "repetition": (64 * (vdot ** -0.65)) * (60 / 1000)
    }

    return paces


def calculate_max_hr(age, formula="Fox"):
    """
    Calculate maximum heart rate based on age.

    Args:
        age (int): Age in years
        formula (str, optional): Formula to use, options are:
            - "Fox": 220 - age
            - "Tanaka": 208 - 0.7 * age
            - "Gellish": 207 - 0.7 * age

    Returns:
        float: Estimated maximum heart rate
    """
    if formula == "Tanaka":
        return 208 - (0.7 * age)
    elif formula == "Gellish":
        return 207 - (0.7 * age)
    else:  # Default to Fox
        return 220 - age


def calculate_hr_zones_karvonen(max_hr, resting_hr, zone_model="5-Zone"):
    """
    Calculate heart rate zones using Karvonen formula (Heart Rate Reserve method).

    Args:
        max_hr (int): Maximum heart rate in beats per minute
        resting_hr (int): Resting heart rate in beats per minute
        zone_model (str, optional): Zone model to use, options are:
            - "5-Zone": Standard 5-zone model
            - "7-Zone": Detailed 7-zone model
            - "3-Zone": Polarized training model

    Returns:
        dict: Dictionary of zone names and heart rate ranges
    """
    hrr = max_hr - resting_hr

    if zone_model == "5-Zone":
        zones = {
            "Zone 1 (Recovery)": (int(resting_hr + (hrr * 0.5)), int(resting_hr + (hrr * 0.6))),
            "Zone 2 (Aerobic)": (int(resting_hr + (hrr * 0.6) + 1), int(resting_hr + (hrr * 0.7))),
            "Zone 3 (Tempo)": (int(resting_hr + (hrr * 0.7) + 1), int(resting_hr + (hrr * 0.8))),
            "Zone 4 (Threshold)": (int(resting_hr + (hrr * 0.8) + 1), int(resting_hr + (hrr * 0.9))),
            "Zone 5 (Anaerobic)": (int(resting_hr + (hrr * 0.9) + 1), int(max_hr))
        }
    elif zone_model == "7-Zone":
        zones = {
            "Zone 1 (Recovery)": (int(resting_hr + (hrr * 0.5)), int(resting_hr + (hrr * 0.55))),
            "Zone 2 (Easy)": (int(resting_hr + (hrr * 0.55) + 1), int(resting_hr + (hrr * 0.65))),
            "Zone 3 (Aerobic)": (int(resting_hr + (hrr * 0.65) + 1), int(resting_hr + (hrr * 0.75))),
            "Zone 4 (Tempo)": (int(resting_hr + (hrr * 0.75) + 1), int(resting_hr + (hrr * 0.82))),
            "Zone 5 (Threshold)": (int(resting_hr + (hrr * 0.82) + 1), int(resting_hr + (hrr * 0.89))),
            "Zone 6 (VO2 Max)": (int(resting_hr + (hrr * 0.89) + 1), int(resting_hr + (hrr * 0.94))),
            "Zone 7 (Anaerobic)": (int(resting_hr + (hrr * 0.94) + 1), int(max_hr))
        }
    else:  # 3-Zone Polarized
        zones = {
            "Zone 1 (Easy)": (int(resting_hr + (hrr * 0.5)), int(resting_hr + (hrr * 0.77))),
            "Zone 2 (Moderate)": (int(resting_hr + (hrr * 0.77) + 1), int(resting_hr + (hrr * 0.87))),
            "Zone 3 (Hard)": (int(resting_hr + (hrr * 0.87) + 1), int(max_hr))
        }

    return zones


def predict_race_time(base_distance, base_time, target_distance, method="Riegel"):
    """
    Predict race time for a target distance based on a recent performance.

    Args:
        base_distance (float): Recent race distance in kilometers
        base_time (float): Recent race time in seconds
        target_distance (float): Target race distance in kilometers
        method (str, optional): Prediction method to use, options are:
            - "Riegel": Riegel formula (standard power law)
            - "Cameron": Cameron formula (adjusted fatigue factor)
            - "Daniels": Daniels VDOT method

    Returns:
        float: Predicted race time in seconds
    """
    if method == "Cameron":
        # Cameron's formula adjusts the fatigue factor based on distance
        fatigue = 1.07 if base_distance <= 10 else 1.05
        return base_time * (target_distance / base_distance) ** fatigue

    elif method == "Daniels":
        # Calculate VDOT from base performance
        vdot = calculate_vdot_from_performance(base_distance, base_time)

        # Target distance in meters
        target_distance_m = target_distance * 1000

        # Calculate percent VO2 max for target distance (estimated)
        # Start with Riegel estimate for initial approximation
        estimated_time = base_time * (target_distance / base_distance) ** 1.06

        # Iterate to refine the estimate (3 iterations is usually sufficient)
        for _ in range(3):
            percent_vo2_target = 0.8 + 0.1894393 * exp(-0.012778 * (estimated_time / 60)) + 0.2989558 * exp(
                -0.1932605 * (estimated_time / 60))

            # Calculate required velocity
            vo2_target = vdot * percent_vo2_target

            # Convert VO2 to velocity using quadratic formula
            # vo2 = -4.60 + 0.182258 * velocity + 0.000104 * velocity * velocity
            a = 0.000104
            b = 0.182258
            c = -4.60 - vo2_target

            # Velocity = (-b ± sqrt(b² - 4ac)) / 2a (we want the positive solution)
            velocity_target = (-b + (b ** 2 - 4 * a * c) ** 0.5) / (2 * a)

            # Calculate new estimated time
            estimated_time = (target_distance_m / velocity_target) * 60

        return estimated_time

    else:  # Default to Riegel
        # Standard Riegel formula with fatigue factor of 1.06
        return base_time * (target_distance / base_distance) ** 1.06


def calculate_running_power(
        weight, height, speed_kph, incline_pct=0, wind_speed_kph=0,
        terrain_coef=1.0, altitude_m=0, temperature_c=20
):
    """
    Calculate running power based on runner parameters and environmental conditions.

    Args:
        weight (float): Runner's weight in kilograms
        height (float): Runner's height in centimeters
        speed_kph (float): Running speed in kilometers per hour
        incline_pct (float, optional): Incline/grade in percent. Defaults to 0.
        wind_speed_kph (float, optional): Wind speed in km/h (positive=headwind, negative=tailwind). Defaults to 0.
        terrain_coef (float, optional): Terrain coefficient (1.0=track/road). Defaults to 1.0.
        altitude_m (int, optional): Altitude in meters. Defaults to 0.
        temperature_c (float, optional): Temperature in Celsius. Defaults to 20.

    Returns:
        float: Estimated running power in watts
    """
    # Convert speed to m/s
    speed_ms = speed_kph / 3.6

    # Convert wind speed to m/s
    wind_ms = wind_speed_kph / 3.6

    # Gravitational acceleration (m/s²)
    g = 9.81

    # Calculate incline angle in radians
    incline_rad = np.arctan(incline_pct / 100)

    # Calculate gravitational force component
    grav_force = weight * g * np.sin(incline_rad)

    # Calculate air resistance
    # Adjust air density for altitude and temperature
    air_density_sl = 1.225  # kg/m³ at sea level, 15°C
    air_density = air_density_sl * np.exp(-altitude_m / 7000) * (273 / (273 + temperature_c))

    # Calculate frontal area
    frontal_area = 0.266 * ((weight) ** 0.425) * ((height / 100) ** 0.725) / 10000  # m²

    # Drag coefficient
    cd = 0.9  # typical value for runner

    # Calculate air resistance force
    rel_velocity = speed_ms + wind_ms  # Positive = headwind, Negative = tailwind
    air_resist = 0.5 * air_density * cd * frontal_area * rel_velocity ** 2

    # Calculate rolling resistance
    rolling_coef = 0.01 * terrain_coef
    rolling_resist = rolling_coef * weight * g * np.cos(incline_rad)

    # Calculate total resistance force
    total_force = grav_force + air_resist + rolling_resist

    # Calculate power
    power = total_force * speed_ms

    # Apply efficiency factor
    efficiency = 0.25  # Typical running efficiency
    power_output = power / efficiency

    return power_output