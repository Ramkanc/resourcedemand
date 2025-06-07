import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import rd_data_ops

st.set_page_config(page_title="Charts", layout="wide")
st.title("Charts")

st.subheader("Resource Demand Charts")

featched_df = None

with st.container(border=True):
    selected_vsl = st.radio("Value stream: ", options=["All"]+list(rd_data_ops.val_streams.keys()), horizontal=True, key="vsl_select")
    get_tbl = st.button("Get Table", key="get_table")
    if get_tbl:
        if selected_vsl == "All":
            st.info("Showing data for all value streams")
            featched_df = rd_data_ops.get_whole_vls()
        else:
            st.info(f"Showing data for {selected_vsl} value stream")
            featched_df = rd_data_ops.get_single_vls(selected_vsl)

        st.session_state['featched_df'] = featched_df
        plot_df = rd_data_ops.get_plot_df(featched_df)
        # Plotting the data
        if not plot_df.empty:
            fig, ax = plt.subplots(figsize=(10, 6))            
            plot_df.plot(kind='area', ax=ax)
            ax.legend(loc='upper left', bbox_to_anchor=(1, 1))
            plt.title('Resource Chart')
            plt.xlabel('Weeks')
            plt.ylabel('Resource')
            #plt.grid(True)
            plt.tight_layout()
            #plt.show()
            st.pyplot(fig)
        
        else:
            st.warning("No data available for the selected value stream.")

        st.dataframe(featched_df)

   
    







    
    # if tbl_button:
    #     st.info(f"Showing data for {selected_mgr} in {selected_vsl} value stream")
    #     df = rd_data_ops.get_vls(selected_mgr)
    #     st.dataframe(df)
        
    #     # Plotting the data
    #     fig, ax = plt.subplots(figsize=(10, 6))
    #     df.plot(x='EngNames', kind='bar', ax=ax)
    #     ax.set_title(f"Resource Demand for {selected_mgr} in {selected_vsl}")
    #     ax.set_ylabel("Demand")
    #     ax.set_xlabel("Engineers")
    #     plt.xticks(rotation=45)
        
    #     st.pyplot(fig)