
import os
import pandas as pd
import numpy as np
import streamlit as st
import matplotlib.pyplot as plt

# Dropdown options
options = ["BCS", "MCS", "FCS", "Site"]

st.set_page_config(layout="wide")  # Full-width layout

st.markdown(
    "<h1 style='color: royalblue; font-size:36px'>POC: Web RPT<h1>",
    unsafe_allow_html=True
)

# Dropdown selection
selected_option = st.selectbox("Choose a VSL:", options)

#resource count

res_count = [12,11,10,33]
sel_idx = options.index(selected_option)

# Generate file name based on selection
if selected_option != "Site":
    csv_file = f"{selected_option}.csv"
    # Check if file exists
    if os.path.exists(csv_file):
        try:
            raw_data = pd.read_csv(csv_file)

        except Exception as e:
            st.error(f"Failed to load {csv_file}: {e}")
elif selected_option == "Site":
    df1 = pd.read_csv("BCS.csv")
    df2 = pd.read_csv("MCS.csv")
    df3 = pd.read_csv("FCS.csv")
    concat_data = pd.concat([df1, df2, df3])
    #st.warning(f"not found in the directory.")
    raw_data = concat_data.groupby(concat_data.columns[0]).sum(numeric_only=True)
    #st.write(raw_data)

st.markdown(
    "<h3 style='color: green; font-size:25px'>Edit the data as per need<h3>",
    unsafe_allow_html=True
)

edited_df = st.data_editor(
    raw_data, 
    num_rows="dynamic",
    use_container_width=True
    )

edited_df.rename(columns={edited_df.columns[0]: 'Weeks'}, inplace=True)
edited_df.set_index('Weeks',inplace=True)


df = edited_df.T


avail_resource = res_count[sel_idx]

st.subheader(f"Avaialble resource: {avail_resource} ")


#st.subheader("Timeseries plot")
st.markdown(
    "<h3 style='color: royalblue; font-size:25px'>Timeseries plot<h3>",
    unsafe_allow_html=True
)

fig,ax = plt.subplots(figsize=(15,6))
#df.plot(kind='area',ax=ax,stacked=True)
df.plot(kind='area',ax=ax, legend=True, alpha=0.5, linewidth=2)
plt.plot([0,25],[avail_resource ,avail_resource])
plt.title('Resource Chart')
plt.xlabel('Week')
plt.ylabel('Resource')
#plt.grid(True)
plt.tight_layout()
#plt.show()
st.pyplot(fig)