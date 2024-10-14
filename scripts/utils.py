import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from fpdf import FPDF

# Calculate the overall consent rate
def calculate_consent_rate(df):
    yes_consent_count = df['Consent Result'].value_counts().get('yes_consent', 0)
    total_calls = len(df)
    consent_rate = (yes_consent_count / total_calls) * 100
    return total_calls, consent_rate

# Group by time slot and calculate consent rates
def group_by_time_slot(df):
    def remove_timezone(time_str):
        if isinstance(time_str, str) and ('+' in time_str or '-' in time_str):
            return time_str.split('+')[0].split('-')[0].strip()
        return time_str

    df['IVR Time Attempted'] = df['IVR Time Attempted'].apply(remove_timezone)
    df['IVR Time Attempted'] = pd.to_datetime(df['IVR Time Attempted'], format='%H:%M:%S', errors='coerce').dt.time

    def categorize_time(time):
        if pd.isna(time):
            return np.nan
        hour = time.hour
        if hour < 12:
            return 'Morning'
        elif 12 <= hour < 17:
            return 'Afternoon'
        else:
            return 'Evening'
    
    df['Time Slot'] = df['IVR Time Attempted'].apply(categorize_time)
    consent_by_time = df.groupby('Time Slot')['Consent Result'].apply(lambda x: (x == 'yes_consent').mean() * 100)
    
    plt.figure(figsize=(10, 6))
    consent_by_time.plot(kind='bar', color=['#1f77b4', '#ff7f0e', '#2ca02c'], alpha=0.8)
    plt.title("Consent Rate by Time Slot", fontsize=16)
    plt.xlabel("Time Slot", fontsize=12)
    plt.ylabel("Consent Rate (%)", fontsize=12)
    plt.xticks(rotation=0)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.savefig('../output/consent_rate_by_time_slot.png')
    plt.show()

    return consent_by_time

# Analyze consent rates by day of the week in chronological order
def day_of_week_analysis(df):
    df['Day of Week'] = pd.to_datetime(df['IVR Date Attempted']).dt.day_name()
    days_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    consent_by_day = df.groupby('Day of Week')['Consent Result'].apply(lambda x: (x == 'yes_consent').mean() * 100)
    consent_by_day = consent_by_day.reindex(days_order)

    plt.figure(figsize=(10, 6))
    consent_by_day.plot(kind='bar', color='#17becf', alpha=0.8)
    plt.title("Consent Rate by Day of the Week", fontsize=16)
    plt.xlabel("Day of the Week", fontsize=12)
    plt.ylabel("Consent Rate (%)", fontsize=12)
    plt.xticks(rotation=45)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.savefig('../output/consent_rate_by_day.png')
    plt.show()

    return consent_by_day

# Perform cost analysis, considering reductions in call durations
def cost_analysis(df, reduction_percent=0):
    platform_fee = 10000
    airtime_cost_per_minute = 0.04
    admin_overhead = 0.12
    total_minutes = df['Call Duration [s]'].sum() / 60
    total_airtime_cost = total_minutes * airtime_cost_per_minute
    total_cost = (platform_fee + total_airtime_cost) * (1 + admin_overhead)
    yes_consent_count = df['Consent Result'].value_counts().get('yes_consent', 0)
    current_cost_per_mum = total_cost / yes_consent_count if yes_consent_count > 0 else 0

    reduced_minutes = total_minutes * (1 - reduction_percent / 100)
    reduced_airtime_cost = reduced_minutes * airtime_cost_per_minute
    reduced_total_cost = (platform_fee + reduced_airtime_cost) * (1 + admin_overhead)
    reduced_cost_per_mum = reduced_total_cost / yes_consent_count if yes_consent_count > 0 else 0

    return current_cost_per_mum, reduced_cost_per_mum, total_cost, reduced_total_cost

# Save results to Excel file
def export_to_excel(df, time_slot_consent, day_of_week_consent, cost_data):
    output_file = '../output/ivr_analysis_results.xlsx'
    
    with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
        time_slot_consent.to_excel(writer, sheet_name='Consent by Time Slot')
        day_of_week_consent.to_excel(writer, sheet_name='Consent by Day of Week')
        cost_data.to_excel(writer, sheet_name='Cost Analysis')

    print(f"Results successfully saved to {output_file}")

# Function to visualize cost comparison across different reduction strategies
def plot_cost_comparison(df):
    reductions = [0, 10, 20, 30]
    costs = []

    for reduction in reductions:
        _, reduced_cost_per_mum, _, _ = cost_analysis(df, reduction)
        costs.append(reduced_cost_per_mum)

    plt.figure(figsize=(10, 6))
    plt.bar([f'{r}% Reduction' for r in reductions], costs, color='#bcbd22', alpha=0.8)
    plt.title('Cost per Consented Mum Based on Call Duration Reductions', fontsize=16)
    plt.ylabel('Cost ($)', fontsize=12)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.savefig('../output/cost_comparison.png')
    plt.show()

# Generate a summary of key insights and recommendations
def generate_summary(df):
    total_calls, consent_rate = calculate_consent_rate(df)
    time_slot_consent = group_by_time_slot(df)
    day_of_week_consent = day_of_week_analysis(df)
    current_cost_per_mum, reduced_cost_per_mum_20, total_cost, reduced_total_cost_20 = cost_analysis(df, 20)

    cost_data = pd.DataFrame({
        'Reduction %': [0, 10, 20, 30],
        'Cost per Mum ($)': [current_cost_per_mum, reduced_cost_per_mum_20, reduced_cost_per_mum_20, reduced_cost_per_mum_20]
    })
    
    # Key insights
    print(f"\nTotal Calls: {total_calls}")
    print(f"Overall Consent Rate: {consent_rate:.2f}%\n")
    print(f"Consent Rates by Time Slot:\n{time_slot_consent}\n")
    print(f"Consent Rates by Day of Week:\n{day_of_week_consent}\n")
    print(f"Current Cost per Consented Mum: ${current_cost_per_mum:.2f}")
    print(f"Proposed Cost (20% Call Duration Reduction) per Consented Mum: ${reduced_cost_per_mum_20:.2f}")
    print(f"Total Cost (Current): ${total_cost:.2f}")
    print(f"Total Cost (20% Reduction): ${reduced_total_cost_20:.2f}")

    export_to_excel(df, time_slot_consent, day_of_week_consent, cost_data)

    # Recommendations based on analysis
    best_time_slot = time_slot_consent.idxmax()
    best_day = day_of_week_consent.idxmax()
    print("\nRecommendations:")
    print(f"1. Focus on calling during the '{best_time_slot}' time slot for higher consent rates.")
    print(f"2. Prioritize calling on '{best_day}', which shows the highest consent rate.")
    print("3. Consider reducing call durations by 20% to significantly lower costs while maintaining consent rates.")
    
    plot_cost_comparison(df)

# Main function to run the analysis
def run_analysis(df):
    print("Running IVR Data Analysis...")
    generate_summary(df)

# Example usage:
if __name__ == '__main__':
    data_path = '../data/ivr_data.xlsx'
    df = pd.read_excel(data_path, engine='openpyxl')
    run_analysis(df)
