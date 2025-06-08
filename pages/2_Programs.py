import streamlit as st
import pandas as pd
import rd_data_ops
import matplotlib.pyplot as plt
from io import StringIO

st.set_page_config(page_title="Programs", layout="wide")
st.subheader("Programs and Milestones")

df = pd.read_csv(rd_data_ops.df_prgms)
milestones = df.columns[2:].tolist()

# Data for plotting : draw bars for each program
plot_data = []
for _, row in df.iterrows():
    for i in range(len(milestones) - 1):
        plot_data.append({
            'Program': row['Program name'],
            'Start': row[milestones[i]],
            'End': row[milestones[i + 1]],
            'Milestone': f"{milestones[i]} → {milestones[i + 1]}"
        })
#st.write("plot_data:", plot_data)
plot_df = pd.DataFrame(plot_data)

plot_df['Start'] = pd.to_datetime(plot_df['Start'])
plot_df['End'] = pd.to_datetime(plot_df['End'])
plot_df['Duration'] = (plot_df['End'] - plot_df['Start']).dt.days

#st.dataframe(plot_df)


# Plot
fig, ax = plt.subplots(figsize=(16, 10))
y_labels = plot_df['Program'].unique()[::-1]
y_mapping = {name: idx for idx, name in enumerate(y_labels)}

for _, row in plot_df.iterrows():
    y = y_mapping[row['Program']]
    ax.barh(y=y, left=row['Start'], width=row['Duration'], height=0.4, label=row['Milestone'], alpha=0.8)

ax.set_yticks(list(y_mapping.values()))
ax.set_yticklabels(list(y_mapping.keys()))
ax.set_xlabel("Date")
ax.set_title("Program vs Milestone Dates")
#ax.legend(title="Milestones", bbox_to_anchor=(1.05, 1), loc='upper left')
ax.grid(True, axis='x', linestyle='--', alpha=0.7)

plt.tight_layout()
#plt.show()
st.pyplot(fig, use_container_width=True)

st.dataframe(df)