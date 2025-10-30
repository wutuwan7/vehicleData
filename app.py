import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

st.title("Vehicle Data Line Chart")

data_frame = st.file_uploader("Choose a CSV file", type=["csv"])

if data_frame is not None:
    try:
        df = pd.read_csv(data_frame, sep=",")
    except Exception:
        df = pd.read_csv(data_frame)
    df.columns = df.columns.str.strip()
    
    if 'StandardComsumptionKMPerLitre' in df.columns:
        df = df[df['StandardComsumptionKMPerLitre'] > 0].dropna(subset=['StandardComsumptionKMPerLitre'])

    if 'VehicleModelName' not in df.columns:
        df['VehicleModelName'] = [f"Vehicle {i+1}" for i in range(len(df))]

    sort_option = st.radio(
        "Sort data by:",
        ("None", "Fuel Efficiency", "Tank Capacity", "Model Name")
    )

    if sort_option == "Fuel Efficiency":
        df = df.sort_values(by='StandardComsumptionKMPerLitre', ascending=False)
    elif sort_option == "Tank Capacity":
        df = df.sort_values(by='VehicleTankCapacity', ascending=False)
    elif sort_option == "Model Name":
        df = df.sort_values(by='VehicleModelName')
    
    st.subheader("Data Preview")
    st.dataframe(df, use_container_width=True, height=(len(df) * 35 if len(df) < 20 else 700))

    # Create figure with twin y-axes
    fig, ax1 = plt.subplots(figsize=(max(12, len(df)*0.6), 10))

    x = np.arange(len(df))
    ax1.plot(x, df['VehicleTankCapacity'], color='red', marker='s', linewidth=2, label='Tank Capacity (L)')
    ax1.set_ylabel('Tank Capacity (L)', color='red')
    ax1.tick_params(axis='y', labelcolor='red')

    ax2 = ax1.twinx()
    ax2.plot(x, df['StandardComsumptionKMPerLitre'], color='blue', marker='o', linewidth=2, label='Fuel Efficiency (KM/L)')
    ax2.set_ylabel('Fuel Efficiency (KM/L)', color='blue')
    ax2.tick_params(axis='y', labelcolor='blue')
    
    plt.xticks(x, df['VehicleModelName'])
    ax1.set_xticklabels(df['VehicleModelName'], rotation=90, ha='center', va='top')

    plt.title("Vehicle Tank Capacity and Fuel Efficiency (Two Line Chart)")
    ax1.legend(loc='upper left')
    ax2.legend(loc='upper right')

    plt.subplots_adjust(bottom=0.1)  

    st.pyplot(fig)