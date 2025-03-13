"""
Visualization utilities for the Runner Performance Metrics Calculator.
"""
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd


def create_zone_bar_chart(zones, values, labels=None, title="Training Zones"):
    """
    Create a horizontal bar chart for training zones.

    Args:
        zones (list): List of zone names
        values (list): List of values (can be single values or ranges)
        labels (list, optional): Labels for the chart. Defaults to zones.
        title (str, optional): Chart title. Defaults to "Training Zones".

    Returns:
        plotly.graph_objects.Figure: A plotly figure object
    """
    fig = go.Figure()

    if labels is None:
        labels = zones

    for i, (zone, value) in enumerate(zip(zones, values)):
        if isinstance(value, tuple):  # Range values
            lower, upper = value
            width = upper - lower
            fig.add_trace(go.Bar(
                name=labels[i],
                y=[zone],
                x=[width],
                base=lower,
                orientation='h',
                marker=dict(color=f'rgba(230, 117, 78, {1 - i * 0.1})')
            ))
        else:  # Single values
            fig.add_trace(go.Bar(
                name=labels[i],
                y=[zone],
                x=[value],
                orientation='h',
                marker=dict(color=f'rgba(230, 117, 78, {1 - i * 0.1})')
            ))

    fig.update_layout(
        title=title,
        barmode='stack',
        height=300,
        margin=dict(l=0, r=0, t=50, b=0)
    )

    return fig


def create_pie_chart(labels, values, title="Distribution", hole=0.3, colors=None):
    """
    Create a pie chart for data distribution.

    Args:
        labels (list): List of slice labels
        values (list): List of values for each slice
        title (str, optional): Chart title. Defaults to "Distribution".
        hole (float, optional): Size of center hole (0-1). Defaults to 0.3.
        colors (list, optional): Custom colors for slices. Defaults to None.

    Returns:
        plotly.graph_objects.Figure: A plotly figure object
    """
    if colors is None:
        colors = px.colors.sequential.Oranges_r[:len(labels)]

    fig = go.Figure(data=[go.Pie(
        labels=labels,
        values=values,
        hole=hole,
        marker=dict(colors=colors)
    )])

    fig.update_layout(
        title=title,
        margin=dict(t=50, b=0, l=0, r=0)
    )

    return fig


def create_comparison_bar_chart(
        categories, values, color='#E6754E',
        title="Comparison", x_label="", y_label=""
):
    """
    Create a bar chart for comparing values across categories.

    Args:
        categories (list): List of category names
        values (list): List of values for each category
        color (str, optional): Bar color. Defaults to '#E6754E'.
        title (str, optional): Chart title. Defaults to "Comparison".
        x_label (str, optional): X-axis label. Defaults to "".
        y_label (str, optional): Y-axis label. Defaults to "".

    Returns:
        plotly.graph_objects.Figure: A plotly figure object
    """
    fig = go.Figure(data=[
        go.Bar(x=categories, y=values, marker_color=color)
    ])

    fig.update_layout(
        title=title,
        xaxis_title=x_label,
        yaxis_title=y_label
    )

    return fig


def create_gauge_chart(value, min_val=0, max_val=100, title="Gauge", threshold_ranges=None):
    """
    Create a gauge chart for displaying a value within a range.

    Args:
        value (float): The value to display
        min_val (int, optional): Minimum gauge value. Defaults to 0.
        max_val (int, optional): Maximum gauge value. Defaults to 100.
        title (str, optional): Chart title. Defaults to "Gauge".
        threshold_ranges (list, optional): List of tuples defining ranges and colors.
            Example: [(0, 40, "red"), (40, 70, "yellow"), (70, 100, "green")]

    Returns:
        plotly.graph_objects.Figure: A plotly figure object
    """
    if threshold_ranges is None:
        threshold_ranges = [
            (min_val, max_val * 0.4, "rgba(255, 0, 0, 0.3)"),
            (max_val * 0.4, max_val * 0.7, "rgba(255, 165, 0, 0.3)"),
            (max_val * 0.7, max_val, "rgba(0, 255, 0, 0.3)")
        ]

    steps = []
    for start, end, color in threshold_ranges:
        steps.append({
            'range': [start, end],
            'color': color
        })

    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=value,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': title},
        gauge={
            'axis': {'range': [min_val, max_val]},
            'bar': {'color': "#E6754E"},
            'steps': steps,
            'threshold': {
                'line': {'color': "black", 'width': 4},
                'thickness': 0.75,
                'value': value
            }
        }
    ))

    fig.update_layout(
        height=300,
        margin=dict(l=10, r=10, t=50, b=10),
    )

    return fig