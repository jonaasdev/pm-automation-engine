"""
Technical PM Command Center Dashboard
Project Manager: Younes Boutelidjane

A tool I developed to automate my project management workflows, providing:
- Earned Value Management (EVM) metrics calculation
- Predictive analytics with Estimate at Completion (EAC)
- Resource allocation analysis
- Risk visualization and heatmaps
- Professional stakeholder reporting

Author: Younes Boutelidjane
Version: 2.0
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import json
from datetime import datetime
from tabulate import tabulate


def load_project_data():
    """
    Load project data from CSV file.
    
    Returns:
        pd.DataFrame: Project data with all task information
    """
    try:
        df = pd.read_csv('project_data.csv')
        return df
    except FileNotFoundError:
        print("Error: project_data.csv not found.")
        return None


def load_milestones():
    """
    Load milestone data from JSON file.
    
    Returns:
        dict: Milestone tracking information
    """
    try:
        with open('milestones.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print("Warning: milestones.json not found.")
        return None


def calculate_evm_metrics(df):
    """
    Calculate Earned Value Management metrics.
    
    Args:
        df (pd.DataFrame): Project data
        
    Returns:
        pd.DataFrame: Data with CPI and SPI columns added
    """
    # Avoid division by zero
    df['CPI'] = df['Earned_Value'] / df['Actual_Cost'].replace(0, 1)
    df['SPI'] = df['Earned_Value'] / df['Planned_Value'].replace(0, 1)
    return df


def calculate_eac(df):
    """
    Calculate Estimate at Completion (EAC) for predictive analysis.
    
    EAC = BAC / CPI
    where BAC (Budget at Completion) = Planned_Value
    
    Args:
        df (pd.DataFrame): Project data with CPI calculated
        
    Returns:
        pd.DataFrame: Data with EAC column added
    """
    df['EAC'] = df['Planned_Value'] / df['CPI'].replace(0, 1)
    df['Variance_at_Completion'] = df['Planned_Value'] - df['EAC']
    return df


def identify_overallocated_resources(df):
    """
    Identify resources assigned to more than 3 active tasks.
    
    Args:
        df (pd.DataFrame): Project data
        
    Returns:
        pd.DataFrame: Resources with their active task counts
    """
    # Filter for active tasks (In Progress)
    active_tasks = df[df['Status'] == 'In Progress']
    
    # Count tasks per resource
    resource_counts = active_tasks['Resource_Name'].value_counts().reset_index()
    resource_counts.columns = ['Resource_Name', 'Active_Tasks']
    
    # Identify overallocated (>3 tasks)
    overallocated = resource_counts[resource_counts['Active_Tasks'] > 3]
    
    return resource_counts, overallocated


def generate_project_health_scorecard(df):
    """
    Generate a comprehensive project health scorecard.
    
    Args:
        df (pd.DataFrame): Project data with all metrics
    """
    print("\n" + "="*80)
    print("MY PERFORMANCE REPORT | LEAD: YOUNES BOUTELIDJANE")
    print("="*80)
    
    # Overall metrics
    total_ev = df['Earned_Value'].sum()
    total_ac = df['Actual_Cost'].sum()
    total_pv = df['Planned_Value'].sum()
    
    overall_cpi = total_ev / total_ac if total_ac else 0
    overall_spi = total_ev / total_pv if total_pv else 0
    
    # Calculate overall EAC
    overall_eac = total_pv / overall_cpi if overall_cpi else 0
    variance_at_completion = total_pv - overall_eac
    
    # Summary metrics table
    summary_data = [
        ["Total Budget (PV)", f"${total_pv:,.2f}"],
        ["Total Actual Cost (AC)", f"${total_ac:,.2f}"],
        ["Total Earned Value (EV)", f"${total_ev:,.2f}"],
        ["Cost Performance Index (CPI)", f"{overall_cpi:.2f}"],
        ["Schedule Performance Index (SPI)", f"{overall_spi:.2f}"],
        ["Estimate at Completion (EAC)", f"${overall_eac:,.2f}"],
        ["Variance at Completion (VAC)", f"${variance_at_completion:,.2f}"]
    ]
    
    print("\n📊 EXECUTIVE SUMMARY")
    print(tabulate(summary_data, headers=["Metric", "Value"], tablefmt="grid"))
    
    # Status interpretation
    print("\n🎯 PERFORMANCE INDICATORS")
    status_data = [
        ["Cost Performance", 
         "✅ Under Budget" if overall_cpi > 1 else "⚠️ Over Budget",
         f"{abs(1-overall_cpi)*100:.1f}%"],
        ["Schedule Performance", 
         "✅ Ahead of Schedule" if overall_spi > 1 else "⚠️ Behind Schedule",
         f"{abs(1-overall_spi)*100:.1f}%"]
    ]
    print(tabulate(status_data, headers=["Category", "Status", "Variance"], tablefmt="grid"))
    
    # Task-level details
    print("\n📋 TASK-LEVEL PERFORMANCE")
    task_data = []
    for _, row in df.iterrows():
        task_data.append([
            row['Task_Name'][:30],
            row['Department'],
            row['Resource_Name'],
            f"{row['CPI']:.2f}",
            f"{row['SPI']:.2f}",
            row['Risk_Level'],
            row['Status']
        ])
    
    print(tabulate(task_data, 
                   headers=["Task", "Dept", "Resource", "CPI", "SPI", "Risk", "Status"],
                   tablefmt="grid"))
    
    print("="*80 + "\n")


def analyze_resource_allocation(df):
    """
    Analyze and report on resource allocation.
    
    Args:
        df (pd.DataFrame): Project data
    """
    resource_counts, overallocated = identify_overallocated_resources(df)
    
    print("\n" + "="*80)
    print("🔍 RESOURCE ALLOCATION ANALYSIS")
    print("="*80)
    
    # All resources with active tasks
    print("\n📊 Active Task Distribution")
    resource_data = []
    for _, row in resource_counts.iterrows():
        status = "⚠️ OVERALLOCATED" if row['Active_Tasks'] > 3 else "✅ Normal"
        resource_data.append([row['Resource_Name'], row['Active_Tasks'], status])
    
    print(tabulate(resource_data, 
                   headers=["Resource", "Active Tasks", "Status"],
                   tablefmt="grid"))
    
    # Overallocated resources warning
    if not overallocated.empty:
        print("\n⚠️ CRITICAL: The following resources are overallocated (>3 active tasks):")
        for _, row in overallocated.iterrows():
            print(f"   • {row['Resource_Name']}: {row['Active_Tasks']} active tasks")
    else:
        print("\n✅ All resources are within normal allocation limits.")
    
    print("="*80 + "\n")


def generate_budget_chart(df):
    """
    Generate Budget vs Actual Cost bar chart.
    
    Args:
        df (pd.DataFrame): Project data
    """
    plt.figure(figsize=(14, 7))
    
    bar_width = 0.25
    index = range(len(df))
    
    # Plotting
    p1 = plt.bar(index, df['Planned_Value'], bar_width, 
                 label='Planned Value (Budget)', color='#2E86AB', alpha=0.8)
    p2 = plt.bar([i + bar_width for i in index], df['Actual_Cost'], bar_width, 
                 label='Actual Cost', color='#A23B72', alpha=0.8)
    p3 = plt.bar([i + 2*bar_width for i in index], df['Earned_Value'], bar_width, 
                 label='Earned Value', color='#F18F01', alpha=0.8)
    
    plt.xlabel('Tasks', fontweight='bold', fontsize=12)
    plt.ylabel('Currency ($)', fontweight='bold', fontsize=12)
    plt.title('Budget (PV) vs Actual Cost (AC) vs Earned Value (EV) per Task', 
              fontweight='bold', fontsize=14)
    plt.xticks([i + bar_width for i in index], df['Task_Name'], 
               rotation=45, ha='right', fontsize=9)
    plt.legend(fontsize=10)
    plt.grid(axis='y', alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('budget_report.png', dpi=300)
    print("[INFO] Chart saved as 'budget_report.png'")


def generate_risk_heatmap(df):
    """
    Generate risk heatmap visualization.
    
    Args:
        df (pd.DataFrame): Project data with risk levels
    """
    # Create risk matrix by department
    risk_by_dept = df.groupby(['Department', 'Risk_Level']).size().unstack(fill_value=0)
    
    plt.figure(figsize=(10, 6))
    sns.heatmap(risk_by_dept, annot=True, fmt='d', cmap='YlOrRd', 
                cbar_kws={'label': 'Number of Tasks'}, linewidths=0.5)
    
    plt.title('Risk Distribution Heatmap by Department', fontweight='bold', fontsize=14)
    plt.xlabel('Risk Level (1=Low, 5=Critical)', fontweight='bold', fontsize=12)
    plt.ylabel('Department', fontweight='bold', fontsize=12)
    
    plt.tight_layout()
    plt.savefig('risk_heatmap.png', dpi=300)
    print("[INFO] Risk heatmap saved as 'risk_heatmap.png'")


def display_milestone_status():
    """
    Display milestone tracking status.
    """
    milestones_data = load_milestones()
    
    if not milestones_data:
        return
    
    print("\n" + "="*80)
    print("🎯 MILESTONE TRACKING")
    print("="*80)
    
    milestone_table = []
    for milestone in milestones_data['milestones']:
        status_icon = {
            'Completed': '✅',
            'In Progress': '🔄',
            'Not Started': '⏳'
        }.get(milestone['status'], '❓')
        
        milestone_table.append([
            milestone['name'],
            milestone['owner'],
            milestone['target_date'],
            milestone['completion_date'] or 'N/A',
            f"{status_icon} {milestone['status']}"
        ])
    
    print(tabulate(milestone_table,
                   headers=["Milestone", "Owner", "Target Date", "Completed", "Status"],
                   tablefmt="grid"))
    print("="*80 + "\n")


def main():
    """
    Main execution function for the PM Command Center Dashboard.
    """
    print("\n" + "🚀 " * 20)
    print("MY TECHNICAL PM COMMAND CENTER")
    print("Project Manager: Younes Boutelidjane")
    print("🚀 " * 20 + "\n")
    
    # Load data
    df = load_project_data()
    if df is None:
        return
    
    # Calculate metrics
    df = calculate_evm_metrics(df)
    df = calculate_eac(df)
    
    # Generate reports
    generate_project_health_scorecard(df)
    analyze_resource_allocation(df)
    display_milestone_status()
    
    # Generate visualizations
    print("\n📈 Generating visualizations...")
    generate_budget_chart(df)
    generate_risk_heatmap(df)
    
    print("\n✅ Dashboard generation complete!")
    print("📊 Review 'budget_report.png' and 'risk_heatmap.png' for visual insights.\n")


if __name__ == "__main__":
    main()
