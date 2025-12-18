import pandas as pd
import matplotlib.pyplot as plt

def generate_dashboard():
    # Load data
    try:
        df = pd.read_csv('project_data.csv')
    except FileNotFoundError:
        print("Error: project_data.csv not found.")
        return

    # Calculate Metrics
    # Avoid division by zero by replacing 0 with 1 or handling it. 
    # For this sample, we assume non-zero values for active/completed tasks.
    df['CPI'] = df['Earned_Value'] / df['Actual_Cost']
    df['SPI'] = df['Earned_Value'] / df['Planned_Value']

    # Console Report
    print("="*60)
    print("PROJECT PERFORMANCE REPORT | LEAD: YOUNES BOUTELIDJANE")
    print("="*60)
    print(f"{'Task Name':<25} | {'CPI':<6} | {'SPI':<6} | {'Status':<12}")
    print("-" * 60)
    
    for index, row in df.iterrows():
        print(f"{row['Task_Name']:<25} | {row['CPI']:.2f}   | {row['SPI']:.2f}   | {row['Status']}")
    
    print("-" * 60)
    
    # Overall Metrics (Optional but good for summary)
    total_ev = df['Earned_Value'].sum()
    total_ac = df['Actual_Cost'].sum()
    total_pv = df['Planned_Value'].sum()
    
    overall_cpi = total_ev / total_ac if total_ac else 0
    overall_spi = total_ev / total_pv if total_pv else 0
    
    print(f"\nOVERALL PERFORMANCE:")
    print(f"Overall CPI: {overall_cpi:.2f} {'(Over Budget)' if overall_cpi < 1 else '(Under Budget)'}")
    print(f"Overall SPI: {overall_spi:.2f} {'(Behind Schedule)' if overall_spi < 1 else '(Ahead of Schedule)'}")
    print("="*60)

    # Visualization
    plot_budget_vs_actual(df)

def plot_budget_vs_actual(df):
    plt.figure(figsize=(10, 6))
    
    # Bar width
    bar_width = 0.35
    index = range(len(df))
    
    # Plotting
    p1 = plt.bar(index, df['Planned_Value'], bar_width, label='Planned Value (Budget)', color='#1f77b4')
    p2 = plt.bar([i + bar_width for i in index], df['Actual_Cost'], bar_width, label='Actual Cost', color='#d62728')
    
    plt.xlabel('Tasks', fontweight='bold')
    plt.ylabel('Currency ($)', fontweight='bold')
    plt.title('Budget (PV) vs Actual Cost (AC) per Task', fontweight='bold')
    plt.xticks([i + bar_width / 2 for i in index], df['Task_Name'], rotation=15, ha='right')
    plt.legend()
    
    plt.tight_layout()
    plt.savefig('budget_report.png')
    print("\n[INFO] Chart saved as 'budget_report.png'")

if __name__ == "__main__":
    generate_dashboard()
