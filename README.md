# GPT-Lab Publication Year Wheel

This tool visualizes GPT-Lab AI research deadlines, demo days, and related milestones in a radial calendar. It's designed to eventually serve as an internal online dashboard showing when and where an AI agent updates project timelines.

![Sample Clock](docs/sample.png)

## Features

- Circular plot of key dates (conferences, journals, demo days)
- Auto-generated preparation periods and milestone markers
- Clear ring-based segmentation for event types

## Quick Start

```
git clone git@github.com:GPT-Laboratory/Publication-Year-Wheel.git
pip install matplotlib
python conference_clock.py
```

## TODO (Plz contribute)

- [ ] Modify the data, preprocessing, and plotting to include the preparation time into main data as a separate field
- [ ] If two events overlap, split the ring for those events and their preparation and milestones (others should not be impacted)
- [ ] Replace hardcoded data import with dynamic API or database queries  
- [ ] Implement an AI agent that scrapes up to date information from the internet
- [ ] Turn plotting into service endpoint 
- [ ] Add Flask/FastAPI backend to serve images and event updates  
- [ ] Implement some interactivity
- [ ] Implement authentication and update logging for AI agent actions  
- [ ] Export visualization as SVG for integration in web UIs  
