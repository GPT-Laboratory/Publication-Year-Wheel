from datetime import datetime, timedelta, date

def _get_first_wednesday(year, month):
    """Get the day of the first Wednesday in a given month"""
    first_day = datetime(year, month, 1)
    days_until_wednesday = (2 - first_day.weekday()) % 7
    first_wednesday = first_day + timedelta(days=days_until_wednesday)
    return first_wednesday.day

def generate_demo_day_events(demo_months):
    """ Generate demo day events based on the provided months.
    
    Args:   
        demo_months (list of tuples): List of (year, month) tuples for demo days.

    Returns:
        list: A list of dictionaries representing demo day events.
    """
    

    # Add demo days and their preparation
    demo_day_events = []
    for year, month in demo_months:
        demo_day = _get_first_wednesday(year, month)
        demo_date = datetime(year, month, demo_day)
        
        # 1-week preparation ending at demo day
        prep_start = demo_date - timedelta(days=7)
        demo_day_events.append({
            'name': 'Demo Prep',
            'event_date': f'{prep_start.year}-{prep_start.month:02d}-{prep_start.day:02d}',
            'duration': 7,
            'type': 'demo_prep',
            'ring': 'events',
            'abbrev': ''
        })
        
        # Demo day
        demo_day_events.append({
            'name': 'Demo Day',
            'event_date': f'{year}-{month:02d}-{demo_day:02d}',
            'duration': 1,
            'type': 'demo',
            'ring': 'events',
            'abbrev': 'Demo'
        })
    return demo_day_events

def generate_preparation_and_milestones(events):
    # Add conference and journal preparation and milestones
    new_events = []
    for event in events:
        
        # If the event has a submission date, use that for the deadline
        if 'submission_date' in event:
            deadline_date = date.fromisoformat(event['submission_date'])
        else:
            deadline_date = date.fromisoformat(event['event_date'])
        
        ring_for_event = 'conferences' if event['type'] != 'journal' else 'journals'
        
        # 2-week preparation
        prep_start = deadline_date - timedelta(
            28 if event['type'] == 'journal' else 14
        )
        new_events.append({
            'name': event['name']+' Conference Prep',
            'event_date': f'{prep_start.year}-{prep_start.month:02d}-{prep_start.day:02d}',
            'duration': 28 if event['type'] == 'journal' else 14,
            'type': event['type']+'_prep' if event['type'] != 'journal' else 'jour_prep',
            'ring': ring_for_event,
            'abbrev': ''
        })
        
        # Milestone: Last comments (1 week before deadline)
        milestone_date = deadline_date - timedelta(
            days=7 if event['type'] != 'journal' else 14
        )
        new_events.append({
            'name': event['name']+' Last Comments',
            'event_date': f'{milestone_date.year}-{milestone_date.month:02d}-{milestone_date.day:02d}',
            'duration': 1,
            'type': 'milestone',
            'ring': ring_for_event,
            'abbrev': '◊'
        })

        if 'submission_date' in event:
            # Add submission date as a milestone
            submission_date = date.fromisoformat(event['submission_date'])
            new_events.append({
                'name': event['name']+' Submission Deadline',
                'event_date': f'{submission_date.year}-{submission_date.month:02d}-{submission_date.day:02d}',
                'duration': 1,
                'type': 'submission',
                'ring': ring_for_event,
                'abbrev': '◊'
            })

    return new_events
        
