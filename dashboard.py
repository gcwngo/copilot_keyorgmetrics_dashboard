import json
import pandas as pd
import os
import matplotlib.pyplot as plt
import streamlit as st

# Construct file paths
base_dir = os.path.dirname(__file__)
file_path_1 = os.path.join(base_dir, "data", "response-07-03-2024.json")
file_path_2 = os.path.join(base_dir, "data", "response-07-29-2024.json")

# Load JSON data
with open(file_path_1, "r") as f:
    data1 = json.load(f)

with open(file_path_2, "r") as f:
    data2 = json.load(f)

# Convert JSON data to DataFrame
df1 = pd.json_normalize(data1)
df2 = pd.json_normalize(data2)

# Combine data from both files
df = pd.concat([df1, df2])

# Convert the 'day' column to datetime
df['day'] = pd.to_datetime(df['day'])

# Define weekends and holidays
weekends = [
    "2024-06-08", "2024-06-09", "2024-06-15", "2024-06-16",
    "2024-06-22", "2024-06-23", "2024-06-29", "2024-06-30",
    "2024-07-06", "2024-07-07", "2024-07-13", "2024-07-14",
    "2024-07-20", "2024-07-21", "2024-07-27", "2024-07-28"
]
holidays = ["2024-06-19", "2024-07-04"]

# Combine weekends and holidays into a single list
excluded_dates = weekends + holidays

# Convert excluded dates to datetime
excluded_dates = pd.to_datetime(excluded_dates)

# Filter the data between June 6, 2024 and July 29, 2024, excluding weekends and holidays
start_date = "2024-06-06"
end_date = "2024-07-29"
mask = (df['day'] >= start_date) & (df['day'] <= end_date) & (~df['day'].isin(excluded_dates))
df_filtered = df[mask]

# Calculate the key metrics
total_suggestions = df_filtered['total_suggestions_count'].sum()
total_acceptances = df_filtered['total_acceptances_count'].sum()
total_lines_suggested = df_filtered['total_lines_suggested'].sum()
total_lines_accepted = df_filtered['total_lines_accepted'].sum()
total_active_users = df_filtered['total_active_users'].sum()

# Corrected Acceptance Rate calculation
acceptance_rate = (total_lines_accepted / total_lines_suggested) * 100 if total_lines_suggested > 0 else 0

# Copilot Chat Metrics
total_chat_acceptances = df_filtered['total_chat_acceptances'].sum()
total_chat_turns = df_filtered['total_chat_turns'].sum()
total_active_chat_users = df_filtered['total_active_chat_users'].sum()

# Display key metrics using Streamlit
st.title("GitHub Copilot Usage Metrics Dashboard")
st.write("Date Range: 2024-06-06 to 2024-07-29 (excluding weekends and holidays)")

key_metrics = {
    "Acceptance Rate (%)": round(acceptance_rate, 2),
    "Total Suggestions": int(total_suggestions),
    "Total Acceptances": int(total_acceptances),
    "Total Lines Suggested": int(total_lines_suggested),
    "Total Lines Accepted": int(total_lines_accepted),
    #"Total Active Users": int(total_active_users),
    "Total Chat Acceptances": int(total_chat_acceptances),
    "Total Chat Turns": int(total_chat_turns)
    #"Total Active Chat Users": int(total_active_chat_users)
}

# Display the key metrics as a table
st.table(pd.DataFrame([key_metrics]))

# Generate plots for visualization

# Combined plot for suggestions and acceptances over time
plt.figure(figsize=(10, 6))
plt.plot(df_filtered['day'], df_filtered['total_suggestions_count'], marker='o', label='Total Suggestions')
plt.plot(df_filtered['day'], df_filtered['total_acceptances_count'], marker='o', label='Total Acceptances')
plt.xlabel('Date')
plt.ylabel('Count')
plt.title('Total Suggestions and Acceptances Over Time')
plt.legend()
plt.grid(True)
st.pyplot(plt)

# Plot for lines suggested and accepted over time
plt.figure(figsize=(10, 6))
plt.plot(df_filtered['day'], df_filtered['total_lines_suggested'], marker='o', label='Total Lines Suggested')
plt.plot(df_filtered['day'], df_filtered['total_lines_accepted'], marker='o', label='Total Lines Accepted')
plt.xlabel('Date')
plt.ylabel('Lines of Code')
plt.title('Lines Suggested and Accepted Over Time')
plt.legend()
plt.grid(True)
st.pyplot(plt)

# Plot for total active users over time
plt.figure(figsize=(10, 6))
plt.plot(df_filtered['day'], df_filtered['total_active_users'], marker='o', label='Total Active Users')
plt.xlabel('Date')
plt.ylabel('Total Active Users')
plt.title('Total Active Users Over Time')
plt.legend()
plt.grid(True)
st.pyplot(plt)

# Plot for total active chat users over time
plt.figure(figsize=(10, 6))
plt.plot(df_filtered['day'], df_filtered['total_active_chat_users'], marker='o', label='Total Active Chat Users')
plt.xlabel('Date')
plt.ylabel('Total Active Chat Users')
plt.title('Total Active Chat Users Over Time')
plt.legend()
plt.grid(True)
st.pyplot(plt)

# Plot for acceptance rate over time
plt.figure(figsize=(10, 6))
plt.plot(df_filtered['day'], (df_filtered['total_lines_accepted'] / df_filtered['total_lines_suggested']) * 100, marker='o', label='Acceptance Rate')
plt.xlabel('Date')
plt.ylabel('Acceptance Rate (%)')
plt.title('Acceptance Rate Over Time')
plt.legend()
plt.grid(True)
st.pyplot(plt)

# Cumulative metrics plots
df_filtered['cumulative_suggestions'] = df_filtered['total_suggestions_count'].cumsum()
df_filtered['cumulative_acceptances'] = df_filtered['total_acceptances_count'].cumsum()
df_filtered['cumulative_lines_suggested'] = df_filtered['total_lines_suggested'].cumsum()
df_filtered['cumulative_lines_accepted'] = df_filtered['total_lines_accepted'].cumsum()

# Cumulative Suggestions and Acceptances
plt.figure(figsize=(10, 6))
plt.plot(df_filtered['day'], df_filtered['cumulative_suggestions'], marker='o', label='Cumulative Suggestions')
plt.plot(df_filtered['day'], df_filtered['cumulative_acceptances'], marker='o', label='Cumulative Acceptances')
plt.xlabel('Date')
plt.ylabel('Count')
plt.title('Cumulative Suggestions and Acceptances Over Time')
plt.legend()
plt.grid(True)
st.pyplot(plt)

# Cumulative Lines Suggested and Accepted
plt.figure(figsize=(10, 6))
plt.plot(df_filtered['day'], df_filtered['cumulative_lines_suggested'], marker='o', label='Cumulative Lines Suggested')
plt.plot(df_filtered['day'], df_filtered['cumulative_lines_accepted'], marker='o', label='Cumulative Lines Accepted')
plt.xlabel('Date')
plt.ylabel('Lines of Code')
plt.title('Cumulative Lines Suggested and Accepted Over Time')
plt.legend()
plt.grid(True)
st.pyplot(plt)
