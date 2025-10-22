import streamlit as st
import pandas as pd

st.title("Vehicle Data Line Chart")

data_frame = st.file_uploader("Chooose a CSV file", type=["csv"])

if data_frame is not None:
    st.write("Data Preview:")
    df = pd.read_csv(data_frame)
    st.dataframe(df)

    st.write("Line Chart of Tank Capacity and Standard Comsumption (km/litre):")

    required_cols = ['VehicleTankCapacity', 'StandardComsumptionKMPerLitre']
    if all(col in df.columns for col in required_cols):
        data = df[required_cols]

        st.subheader("Line Chart: Tank Capacity & Standard Consumption")
        st.line_chart(data)
    else:
        st.error("The file must contain 'VehicleTankCapacity' and 'StandardComsumptionKMPerLitre' columns.")


else:
    st.info("Please upload a file to begin.")       

