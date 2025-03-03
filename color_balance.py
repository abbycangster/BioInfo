#!/usr/bin/env python
# coding: utf-8

# In[4]:


import numpy as np 
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
from io import BytesIO

st.title("Index Color Balance")

st.write("Download the template and upload the indexes to check the color balance")

def generate_template(): 
    template_df = pd.DataFrame ({"Sample Name": [], "I7 ID": [],"I7 Sequence": [],"I5 ID": [],"I5 Sequence": []})
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        template_df.to_excel(writer, index=False, sheet_name="Index Template")
    output.seek(0)
    return output

st.download_button(
    label="Download Excel Template",
    data=generate_template(),
    file_name="Index_Template.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

uploaded_file = st.file_uploader("Upload your filled-in template (Excel file)", type=["xlsx"])

def check_color_balance(indexes):
    index_length = len(indexes[0])
    
    if any(len(idx) != index_length for idx in indexes):
        st.error("All index sequences must be the same length.")
        return None

    index_matrix = np.array([list(idx.upper()) for idx in indexes])
    nucleotide_counts = {nuc: np.count_nonzero(index_matrix == nuc, axis=0) for nuc in "ATCG"}
    df = pd.DataFrame(nucleotide_counts)
    df = df.div(df.sum(axis=1), axis=0) * 100  

    df.index = df.index+1
    return df

if uploaded_file:
    try:
        df = pd.read_excel(uploaded_file, sheet_name="Index Template")
        
        if "I7 Sequence" in df.columns and "I5 Sequence" in df.columns:
            i7_indexes = df["I7 Sequence"].dropna().astype(str).tolist()
            i5_indexes = df["I5 Sequence"].dropna().astype(str).tolist()
            
            st.subheader("I7 Index")
            color_balance_df_i7 = check_color_balance(i7_indexes)
            if color_balance_df_i7 is not None:
                st.dataframe(color_balance_df_i7)
                
                fig, ax = plt.subplots()
                color_balance_df_i7.plot(kind="bar", stacked=True, ax=ax, colormap="viridis")
                ax.set_xlabel("Cycle Position")
                ax.set_ylabel("Nucleotide %")
                ax.set_title("I7 Nucleotide % Per Cycle")
                st.pyplot(fig)
            
            st.subheader("I5 Index")
            color_balance_df_i5 = check_color_balance(i5_indexes)
            if color_balance_df_i5 is not None:
                st.dataframe(color_balance_df_i5)
                
                fig, ax = plt.subplots()
                color_balance_df_i5.plot(kind="bar", stacked=True, ax=ax, colormap="viridis")
                ax.set_xlabel("Cycle Position")
                ax.set_ylabel("Nucleotide %")
                ax.set_title("I5 Nucleotide % Per Cycle")
                st.pyplot(fig)
            
    except Exception as e:
        st.error(f"Error processing file: {e}")

st.write("Checking to ensure A, T, C, G are well-distributed across cycles.")
    

    
    


# In[ ]:




