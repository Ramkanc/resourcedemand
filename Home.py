import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import rd_data_ops


st.set_page_config(page_title="Inputs", layout="wide")
my_val_streams = rd_data_ops.val_streams


st.header("Resource Demand")


# Initialize session state variables

featched_df = None

form1_vals = {
    "name": "",
    "program": None,
    "stt_wk": None,
    "end_wk": None
}

st.subheader("Input resource projection")

def click_button(mgr):
    st.session_state['featched_df'] = rd_data_ops.get_mgr(mgr)



with st.container(border=True):
    selected_vsl = st.radio("Value stream: ", options=list(my_val_streams.keys()), horizontal=True,key="vsl_select")
    selected_mgr = st.selectbox("Select Manager: ", my_val_streams[selected_vsl], key="mgr_select")
    tbl_button = st.button("Get Table", key="get_table", on_click=click_button, args=(selected_mgr,))
    if tbl_button:
        st.info(f"Showing data for {selected_mgr} in {selected_vsl} value stream")
        st.session_state['featched_df'] = rd_data_ops.get_mgr(selected_mgr)
    
       

if 'featched_df' in st.session_state:
    featched_df = st.session_state['featched_df']
    if featched_df is not None:        
        eng_names = [""] + featched_df["EngNames"].to_list()
        prog_names = [""] + rd_data_ops.get_prog_of_vsl(selected_vsl)

        with st.form(key="rd_entry", clear_on_submit=True):
            st.subheader(f"Data for {selected_mgr} in {selected_vsl} value stream")
            st.dataframe(featched_df)
            st.subheader("Projection")
            form1_vals["name"] = st.selectbox("Engineer Name: ", eng_names)
            form1_vals["program"] = st.selectbox("Program Name: ", prog_names)
            form1_vals["stt_wk"] = st.number_input("Enter start week: ", min_value=2, max_value=56)
            form1_vals["end_wk"] = st.number_input("How many weeks projected: ", min_value=1, max_value=8)
            submit_button = st.form_submit_button(label="Submit")
            if submit_button:
                if not all(form1_vals.values()):
                    st.warning("Please fill all the fields")
                else:
                    st.info("Submitted")
                    for (k, v) in form1_vals.items():
                        st.write(f"{k}: {v}")
                    # Update the dataframe with the new projection
                    updated_df = rd_data_ops.set_mgr(selected_mgr, form1_vals)
                    st.session_state['featched_df'] = updated_df
                    st.dataframe(updated_df)