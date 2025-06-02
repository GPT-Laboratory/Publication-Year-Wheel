import calendar
import numpy as np
import matplotlib.pyplot as plt
from datetime import date
from matplotlib.patches import Wedge, Circle

def date_to_degrees(the_date:date) -> float:
    """Convert year/month/day to degrees (June 2025 at top, clockwise)"""
    total_days = (the_date - date(2025, 6, 1)).days
    degrees = (total_days / 365.0) * 360.0
    return degrees % 360.0


def plot_calendar_rings(ax, rings, start_year_and_month, colors, num_months=12):
    
    start_year, start_month = start_year_and_month

    # Month ordering and positioning
    months = []
    prev_y = start_year
    change_year_idx = 0
    for i in range(num_months):
        y = start_year + (start_month - 1 + i) // 12
        m = (start_month - 1 + i) % 12 + 1
        months.append((y, calendar.month_abbr[m]))

        if y != prev_y:
            change_year_idx = i
        prev_y = y

    # Angles per month
    angle_per_month = 360 / num_months

    # Draw background wedges for each year
    
    spans = [(0, change_year_idx, colors['ring_bg_year_1']),
             (change_year_idx, num_months, colors['ring_bg_year_2'])]

    for _, ring_data in rings.items():
        for start_month_idx, end_month_idx, bg_color in spans:
            theta1 = 90 - start_month_idx * angle_per_month
            theta2 = 90 - end_month_idx * angle_per_month
            wedge = Wedge(
                (0, 0), ring_data['outer'],
                theta1, theta2,
                width=ring_data['outer'] - ring_data['inner'],
                facecolor=bg_color, alpha=0.3,
                edgecolor='gray' if y != start_year else 'none',
                linewidth=1 if y != start_year else 0
            )
            ax.add_patch(wedge)

    min_radius = min(
        min(r['inner'], r['outer']) for r in rings.values()
    )
    # Add month labels
    for i, (y, label) in enumerate(months):
        angle = np.radians(90 - i * angle_per_month)
        x = (min_radius-0.1) * np.cos(angle)
        y_label = (min_radius-0.1) * np.sin(angle)
        color = 'black' if i < change_year_idx else 'gray'
        ax.text(x, y_label, label, ha='center', va='center',
                fontsize=11, fontweight='bold', color=color)

    # Add ring boundaries
    for ring_data in rings.values():
        for radius in (ring_data['inner'], ring_data['outer']):
            ax.add_patch(Circle((0, 0), radius, fill=False, color='white', linewidth=2))

    # Add year labels
    ax.text(0, (min_radius-0.2), str(start_year), ha='center', va='center',
            fontsize=14, fontweight='bold', color='black')
    if change_year_idx > 0:
        # Calculate the angle for the second year label 
        second_year_angle = np.radians(90 - change_year_idx * angle_per_month)
        x = (min_radius-0.2) * np.cos(second_year_angle)
        y = (min_radius-0.2) * np.sin(second_year_angle)
        ax.text(x, y, str(start_year + 1), ha='center', va='center',
                fontsize=14, fontweight='bold', color='gray')
        
def plot_event_labels(event_labels, ax, rings, colors):
    # Add event labels
    for label_info in event_labels:
        label_radius = rings[label_info['ring']]['outer'] + 0.025 
        
        x = label_radius * np.cos(label_info['angle'])
        y = label_radius * np.sin(label_info['angle'])
        
        lt = label_info['type']
        label_color = colors[lt] if lt in colors else 'black'
        
        ax.text(x, y, label_info['abbrev'], ha='center', va='center',
                fontsize=7, fontweight='bold', color=label_color,
                bbox=dict(boxstyle='round,pad=0.1', facecolor='white', alpha=0.9, edgecolor=label_color))