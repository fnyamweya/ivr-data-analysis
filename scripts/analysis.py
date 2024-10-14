import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from utils import calculate_consent_rate, group_by_time_slot, day_of_week_analysis, cost_analysis

# Function to visualize cost comparison across different reduction strategies using a line graph
def plot_cost_comparison(df):
    """
    Plots the cost per consented mum for different call duration reduction strategies using a line graph.
    :param df: DataFrame containing IVR data
    """
    reductions = [0, 10, 20, 30]
    current_costs = []
    reduced_costs = []

    for reduction in reductions:
        current_cost_per_mum, reduced_cost_per_mum, _, _ = cost_analysis(df, reduction)
        current_costs.append(current_cost_per_mum)
        reduced_costs.append(reduced_cost_per_mum)

    # Line graph for cost comparison
    plt.figure(figsize=(10, 6))
    plt.plot(reductions, current_costs, marker='o', label='Current Cost per Mum', color='#1f77b4')
    plt.plot(reductions, reduced_costs, marker='o', label='Proposed Cost per Mum (Reduced Duration)', color='#ff7f0e')
    
    plt.title('Cost per Consented Mum with Call Duration Reductions', fontsize=16)
    plt.xlabel('Call Duration Reduction (%)', fontsize=12)
    plt.ylabel('Cost ($)', fontsize=12)
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.legend()
    plt.xticks(reductions)  # Ensure the x-axis has the correct percentage reduction values
    plt.show()

# Generate a summary of key insights and recommendations with improved visualizations
def generate_summary(df):
    """
    Generate a textual and visual summary of the analysis, including consent rates
    by time slot, day of the week, cost analysis, and recommendations.
    :param df: DataFrame containing IVR data
    """
    # Calculate overall consent rate
    total_calls, consent_rate = calculate_consent_rate(df)
    print(f"\nTotal Calls: {total_calls}, Consent Rate: {consent_rate:.2f}%")

    # Visualize consent rate by time slot using a line graph
    time_slot_consent = group_by_time_slot(df)
    plt.figure(figsize=(10, 6))
    time_slot_consent.plot(marker='o', linestyle='-', color='#2ca02c', alpha=0.8)
    plt.title('Consent Rate by Time Slot', fontsize=16)
    plt.xlabel('Time Slot', fontsize=12)
    plt.ylabel('Consent Rate (%)', fontsize=12)
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.xticks(rotation=0)
    plt.show()

    # Visualize consent rate by day of week using a line graph
    day_of_week_consent = day_of_week_analysis(df)
    plt.figure(figsize=(10, 6))
    day_of_week_consent.plot(marker='o', linestyle='-', color='#17becf', alpha=0.8)
    plt.title('Consent Rate by Day of the Week', fontsize=16)
    plt.xlabel('Day of the Week', fontsize=12)
    plt.ylabel('Consent Rate (%)', fontsize=12)
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.xticks(rotation=45)
    plt.show()

    # Perform cost analysis with 20% reduction
    current_cost_per_mum, reduced_cost_per_mum_20, total_cost, reduced_total_cost_20 = cost_analysis(df, 20)
    print(f"\nCurrent Cost per Consented Mum: ${current_cost_per_mum:.2f}")
    print(f"Proposed Cost (20% Call Duration Reduction) per Consented Mum: ${reduced_cost_per_mum_20:.2f}")
    print(f"Total Current Cost: ${total_cost:.2f}")
    print(f"Total Proposed Cost (20% Reduction): ${reduced_total_cost_20:.2f}")

    # Show cost comparison using a line graph
    plot_cost_comparison(df)

# Main function to run the analysis
def run_analysis(df):
    """
    Main entry point to run the full analysis pipeline.
    :param df: DataFrame containing IVR data
    """
    print("Running IVR Data Analysis...")
    generate_summary(df)

# Example usage
if __name__ == '__main__':
    data_path = '../data/ivr_data.xlsx'
    df = pd.read_excel(data_path, engine='openpyxl')
    run_analysis(df)
