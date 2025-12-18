# Technical PM Automation: EVM Dashboard

**Project Lead:** Younes Boutelidjane

## Description
An automated tool to calculate project health metrics using Python to ensure data-driven decision-making in the SDLC. This dashboard processes project task data to compute **Cost Performance Index (CPI)** and **Schedule Performance Index (SPI)**, providing instant visibility into budget and schedule adherence.

## Features
- **Data Ingestion**: Reads project status, values, and costs from CSV.
- **EVM Metrics**:
  - `CPI = Earned Value (EV) / Actual Cost (AC)`
  - `SPI = Earned Value (EV) / Planned Value (PV)`
- **Reporting**: Generates a console summary report and a "Budget vs. Actual" bar chart visualization.

## Instructions

### Prerequisites
- Python 3.x
- `pandas`
- `matplotlib`

Install dependencies:
```bash
pip install pandas matplotlib
```

### Running the Tool
1. Ensure `project_data.csv` is in the same directory.
2. Run the dashboard script:
   ```bash
   python3 pm_dashboard.py
   ```

### Interpreting Results
- **CPI (Cost Performance Index)**:
  - `> 1.0`: Under Budget (Good)
  - `< 1.0`: Over Budget (Bad)
- **SPI (Schedule Performance Index)**:
  - `> 1.0`: Ahead of Schedule (Good)
  - `< 1.0`: Behind Schedule (Bad)

The script generates a `budget_report.png` chart for visual analysis of Planned Value vs Actual Cost.
