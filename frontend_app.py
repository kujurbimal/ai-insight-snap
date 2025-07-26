import streamlit as st
import requests
import pandas as pd

st.title("📸 AI Insight Snap")
st.write("Turn Any Data into Instant Insights – Just Snap & Analyze!")

uploaded = st.file_uploader("Upload spreadsheet image", type=["jpg", "jpeg", "png"])

if uploaded:
    with st.spinner("Analyzing..."):
        res = requests.post("http://localhost:8000/analyze", files={"file": uploaded})
        data = res.json()
        
        if "error" in data:
            st.error(data["error"])
        else:
            df = pd.DataFrame(data["dataframe"])
            st.subheader("Extracted Data")
            st.dataframe(df)

            st.subheader("Summary Statistics")
            st.json(data["summary"])
