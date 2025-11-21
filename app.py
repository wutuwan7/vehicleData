import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(layout="wide")
st.title("Vehicle Data Line Chart")

data_file = st.file_uploader("Choose a CSV file", type=["csv"])

if data_file is not None:
    df = pd.read_csv(data_file)
    df.columns = df.columns.str.strip()

    st.write("Data Preview:")
    st.dataframe(df)

    if "VehicleModelName" not in df.columns:
        df["VehicleModelName"] = [f"Vehicle {i+1}" for i in range(len(df))]

    df = df[df["StandardComsumptionKMPerLitre"] > 0].dropna(subset=["StandardComsumptionKMPerLitre"])

    sort_option = st.radio(
        "Sort data by:",
        ["None", "Fuel Efficiency", "Tank Capacity", "Model Name"]
    )

    if sort_option == "Fuel Efficiency":
        df = df.sort_values(by="StandardComsumptionKMPerLitre", ascending=False)
    elif sort_option == "Tank Capacity":
        df = df.sort_values(by="VehicleTankCapacity", ascending=False)
    elif sort_option == "Model Name":
        df = df.sort_values(by="VehicleModelName", ascending=True)

    x = range(len(df))
    y_left = df["VehicleTankCapacity"]
    y_right = df["StandardComsumptionKMPerLitre"]
    x_labels = df["VehicleModelName"]

    fig, ax1 = plt.subplots(figsize=(14, 6), dpi=150)

    line1 = ax1.plot(x, y_left, color="tab:blue", marker="o", label="Tank Capacity (L)")
    ax1.set_ylabel("Tank Capacity (Litres)", color="tab:blue")
    ax1.tick_params(axis="y", labelcolor="tab:blue")

    ax2 = ax1.twinx()
    line2 = ax2.plot(x, y_right, color="tab:red", marker="o", label="Fuel Efficiency (KM/L)")
    ax2.set_ylabel("Fuel Efficiency (KM/L)", color="tab:red")
    ax2.tick_params(axis="y", labelcolor="tab:red")

    ax1.set_xticks(x)
    ax1.set_xticklabels(x_labels, rotation=60, ha="right")

    lines = line1 + line2
    labels = [l.get_label() for l in lines]
    ax1.legend(lines, labels, loc='upper left', bbox_to_anchor=(1.02, 1), fontsize=10)

    plt.title("Tank Capacity vs Fuel Efficiency by Vehicle Model")

    plt.subplots_adjust(bottom=0.25, right=0.75)

    plt.grid(True, linestyle="--", alpha=0.4)

    fig.tight_layout()

    st.pyplot(fig, clear_figure=True)

else:
    st.info("Please upload a file to begin.")

