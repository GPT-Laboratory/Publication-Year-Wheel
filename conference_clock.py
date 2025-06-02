import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Wedge
from datetime import date, timedelta
from math import copysign

from preprocessing import generate_demo_day_events, generate_preparation_and_milestones
from plot_helpers import plot_calendar_rings, plot_event_labels, date_to_degrees

# === Import Event data === 
from data import events, start_from_month, demo_months

# === Some Output definitions ===

# Colors
colors = {
    'se_conf': '#7BA5CC',
    'ai_conf': '#95BC95',
    'journal': '#C795C7',

    'demo': '#F4D03F',
    'summer': "#1ABE11",
    'events': '#F4D03F',

    'demo_prep': '#F9E79F',
    'se_conf_prep': '#D6E9F7',
    'ai_conf_prep': "#DAF7D6",
    'jour_prep': "#FFD0FF",

    'submission': '#FF6B6B',
    'milestone': "#FF8F44",

    'ring_bg_year_1': '#E8E8E8', #1st_year
    'ring_bg_year_2': "#C5C5C5"  #2nd_year (if needed)
}

draw_order_and_legend = [
    ('demo_prep', False, None),
    ('ai_conf_prep', False, None),
    ('se_conf_prep', False, 'Preparation'),
    ('jour_prep', False, None),
    
    ('se_conf', False, 'SE Conferences'),
    ('ai_conf', False, 'AI/ML Conferences'),
    ('journal', False, 'Journal Special Issues'),

    ('demo', False, 'Demo Days'),
    ('summer', False, None),
    ('events', False, None),
    
    ('milestone', True, 'Final comments from co-writers'),
    ('submission', True, 'Submission Deadline')
]

# Ring configuration
rings = {
    'events': {'inner': 0.55, 'outer': 0.70}, 
    'conferences': {'inner': 0.95, 'outer': 1.10},
    'journals': {'inner': 0.75, 'outer': 0.90},
}

# === Do Event preprocessing ===

events+=generate_demo_day_events(demo_months)
events+=generate_preparation_and_milestones(
    [e for e in events if e['type'] in ['se_conf', 'ai_conf', 'journal']]
)

# === Proceed to Plot ===

# Create figure
fig, ax = plt.subplots(figsize=(12, 12))
ax.set_xlim(-1.3, 1.3)
ax.set_ylim(-1.3, 1.3)
ax.set_aspect('equal')
ax.axis('off')
ax.set_facecolor('white')


plot_calendar_rings(ax, rings, start_from_month, colors)

# Process events
event_labels = []

for now_drawing, _, _ in draw_order_and_legend:
    for event in (e for e in events if e['type'] == now_drawing):
        event_abbrev = event.get('abbrev', '')

        # Use the submission date
        if event['type'] == 'se_conf' or event['type'] == 'ai_conf' or 'event_date' not in event:
            event_start_date = date.fromisoformat(event['submission_date'])
            event_abbrev+="\n(Sub)"
        else:
            event_start_date = date.fromisoformat(event['event_date'])    
        

        # Make sure the start date is within 1 year from start_from_month
        year_from_start = event_start_date + timedelta(days=364)
        year, month, day = event_start_date.year, event_start_date.month, event_start_date.day
        if (year, month) < start_from_month or (year, month) > (year_from_start.year, year_from_start.month):
            continue
     
        start_degrees = date_to_degrees(event_start_date)

        # Handle milestones as diamond markers
        if event['type'] == 'milestone' or event['type'] == 'submission':
            angle_rad = np.radians(90 - start_degrees)
            radius = (rings[event['ring']]['inner'] + rings[event['ring']]['outer']) / 2
            x = radius * np.cos(angle_rad)
            y = radius * np.sin(angle_rad)
            ax.scatter(x, y, marker='D', s=50, color=colors[event['type']], 
                    edgecolor='white', linewidth=1, zorder=10)
            continue
        
        # Create wedge for other events
        duration_degrees = event['duration'] / 365.0 * 360.0
        end_degrees = start_degrees + duration_degrees

        if duration_degrees >= 0:
            theta1 = 90 - end_degrees
            theta2 = 90 - start_degrees
        else:
            theta1 = 90 - start_degrees
            theta2 = 90 - end_degrees

        wedge = Wedge(
            (0, 0), rings[event['ring']]['outer'],
            theta1, theta2,
            width=rings[event['ring']]['outer'] - rings[event['ring']]['inner'],
            facecolor=colors[event['type']], alpha=0.5,
            edgecolor='white', linewidth=1
        )
        ax.add_patch(wedge)
        
        # Store labels (exclude preparation events)
        if 'prep' not in event['type'] and event['abbrev']:
            mid_angle = (start_degrees + end_degrees) / 2
            mid_angle_rad = np.radians(90 - mid_angle)
            event_labels.append({
                'abbrev': event_abbrev,
                'angle': mid_angle_rad,
                'ring': event['ring'],
                'type': event['type']
            })

        """
        # Draw an arrow from submission date to event date
        if 'submission_date' in event and event['submission_date'] != event['event_date']:

            submission_date = date.fromisoformat(event['submission_date'])
            submission_degrees = date_to_degrees(submission_date)
            submission_angle_rad = np.radians(90 - submission_degrees)

            print (f"Drawing submission arrow for {event['name']} from {event['submission_date']} to {event['event_date']}")
            
            
            # Calculate the position for the arrow
            event_ring = rings[event['ring']]
            arrow_radius = (event_ring['inner']+event_ring['outer'])/2
            x_start = arrow_radius * np.cos(submission_angle_rad)
            y_start = arrow_radius * np.sin(submission_angle_rad)
            start_event_angle_rad = np.radians(90 - start_degrees)
            x_end = arrow_radius * np.cos(start_event_angle_rad)
            y_end = arrow_radius * np.sin(start_event_angle_rad)

            ax.annotate('', xy=(x_end, y_end), xytext=(x_start, y_start),
                        arrowprops=dict(arrowstyle='->', color=colors['submission'], lw=1.5),
                        fontsize=8, color=colors['submission'])
        """

plot_event_labels(event_labels, ax, rings, colors)

# Legend
legend_elements = []
for type, is_marker, legend_text in draw_order_and_legend:
    if legend_text is None:
        continue
    legend_elements.append(
            plt.Line2D([0], [0], marker='D', color='w', markerfacecolor=colors[type], markersize=8, label=legend_text)
        if is_marker else 
            plt.Rectangle((0, 0), 1, 1, facecolor=colors[type], alpha=0.8, label=legend_text)
    )


ax.legend(handles=legend_elements, loc='center', bbox_to_anchor=(0.5, -0.1),
          ncol=4, frameon=False, fontsize=9)

plt.title('GPT-Lab Research Year Clock', fontsize=16, fontweight='bold', pad=30)
plt.tight_layout()
plt.show()