## IVR Data Analysis

This repository contains the source code, data, and visualizations for the IVR data analysis project. The purpose of the analysis is to determine optimal time slots and days for calling participants, understand consent rates, and explore cost-saving strategies by reducing call durations.

## Project Overview

This project analyzes IVR (Interactive Voice Response) data to:

- Identify the best time slots and days to reach participants and obtain consent.
- Perform a cost analysis, exploring cost-saving strategies by reducing call durations.
- Generate visualizations to summarize findings and inform recommendations.

### Dataset

The dataset used in this project contains information about calls made to participants, including:

- Mum Unique ID: A unique identifier for each call participant.
- SMS Consent Sent: Date SMS consent was sent.
- IVR Date Attempted: Date when the IVR call was attempted.
- IVR Time Attempted: Time when the IVR call was attempted.
  -Consent Result: Whether the participant gave consent (yes_consent, no_consent).
  -Call Duration [s]: Duration of the call in seconds.
- Language: Language used during the call.
- Enrollment Method: Method of participant enrollment (e.g., "mystery").

### Analysis Breakdown

Consent Rate Analysis
The script calculates consent rates based on two factors:

- Time Slot Analysis: The day is divided into three slots: Morning, Afternoon, and Evening. The consent rates are calculated for each time slot to determine the most effective calling times.
- Day of the Week Analysis: Consent rates are calculated for each day of the week, showing the best days to reach participants.

### Cost Analysis

The cost per consented participant (mum) is calculated based on:

- Current Strategy: Based on current call durations and a fixed platform fee.
- Proposed Strategy: By reducing the call duration by 20%, the analysis explores how costs can be reduced while maintaining consent rates.

Dependencies
The following dependencies are required to run the analysis:

- pandas: For data manipulation and analysis.
- matplotlib: For creating visualizations.
- numpy: For numerical computations.
- openpyxl: For reading/writing Excel files.
- fpdf: For PDF generation (if necessary for reports).

## Results and Recommendations

The analysis produced several key insights:

- Best Time Slot for Calls: The Afternoon slot yielded the highest consent rate (36.66%).
- Best Days for Calls: Sunday and Friday showed the highest consent rates, with Sunday at 30.34% and Friday at 29.40%.
- Cost Optimization: Reducing call durations by 20% decreased the cost per consented mum from $1.85 to $1.84, saving approximately $27.73 for the entire campaign.
