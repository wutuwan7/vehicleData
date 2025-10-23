import streamlit as st
import pandas as pd

st.title("Vehicle Data Line Chart")

data_frame = st.file_uploader("Choose a CSV file", type=["csv"])

if data_frame is not None:
    st.write("Data Preview:")
    df = pd.read_csv(data_frame)
    df.columns = df.columns.str.strip()

    if 'StandardComsumptionKMPerLitre' in df.columns:
        df = df[df['StandardComsumptionKMPerLitre'] > 0].dropna(subset=['StandardComsumptionKMPerLitre'])
        st.dataframe(df)

    required_cols = ['VehicleTankCapacity', 'StandardComsumptionKMPerLitre']
    model_col = 'VehicleModelName'

    if model_col not in df.columns:
        df[model_col] = [f"Vehicle {i+1}" for i in range(len(df))]

    sort_option = st.selectbox(
        "Sort data by:",
        options=[
            "None",
            "Better Fuel Efficiency (Descending)",
            "Vehicle Model Name (A–Z)"
        ],
        index=0
    )

    if sort_option == "Better Fuel Efficiency (Descending)":
        df = df.sort_values(by='StandardComsumptionKMPerLitre', ascending=False)
    elif sort_option == "Vehicle Model Name (A–Z)":
        df = df.sort_values(by='VehicleModelName', ascending=True)

    column_display_map = {
        'Vehicle Model Name': 'VehicleModelName',
        'Vehicle Tank Capacity': 'VehicleTankCapacity',
    }

    x_axis_option = st.selectbox(
        "Select X-axis:",
        options=list(column_display_map.keys()),
        index=0
    )

    selected_column = column_display_map[x_axis_option]
    chart_data = df[[selected_column, 'StandardComsumptionKMPerLitre']]
    chart_data = chart_data.set_index(selected_column)

    st.write("Line Chart Based on Selected X-axis (Filtered out data with null standard comsumption):")
    st.line_chart(chart_data)

else:
    st.info("Please upload a file to begin.")
