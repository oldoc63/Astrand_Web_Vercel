
import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

from vo2max_estimator import (
    estimate_vo2_max,
    get_age_correction,
    classify_fitness,
    AGE_CORRECTION,
    CLASSIFICATION_THRESHOLDS
)

# --- Streamlit Web Application ---

def main():
    st.set_page_config(page_title="VO2 Max Estimator", layout="wide")
    st.title("VO2 Max Estimator (Astrand-Rhyming Protocol)")

    # --- Input Section ---
    st.sidebar.header("Subject Data")
    name = st.sidebar.text_input("Name")
    age = st.sidebar.number_input("Age", min_value=15, max_value=100, value=25)
    sex = st.sidebar.selectbox("Sex", ("M", "F"))
    weight = st.sidebar.number_input("Body Weight (kg)", min_value=30.0, max_value=200.0, value=70.0)
    workload = st.sidebar.number_input("Workload (Watts)", min_value=150, max_value=600, value=300, step=50)
    avg_hr = st.sidebar.number_input("Average Heart Rate (bpm)", min_value=100, max_value=200, value=150)

    if st.sidebar.button("Calculate VO2 Max"):
        # --- Calculation ---
        vo2_abs = estimate_vo2_max(sex, avg_hr, workload)
        age_factor = get_age_correction(age)
        vo2_abs_corrected = vo2_abs * age_factor
        vo2_relative = (vo2_abs_corrected * 1000) / weight
        classification = classify_fitness(sex, age, vo2_relative)

        # --- Results Display ---
        st.header("Results")
        col1, col2 = st.columns(2)

        with col1:
            st.subheader("Calculations")
            st.metric(label="Estimated Absolute VO2 max (pre-correction)", value=f"{vo2_abs:.2f} L/min")
            st.metric(label="Age Correction Factor", value=f"{age_factor:.2f}")
            st.metric(label="Age-Corrected Absolute VO2 max", value=f"{vo2_abs_corrected:.2f} L/min")
            st.metric(label="Relative VO2 max", value=f"{vo2_relative:.1f} ml/kg/min")
            st.success(f"**Final Classification: {classification.upper()}**")

        with col2:
            st.subheader("Nomogram Visualization")
            fig, ax = plt.subplots(figsize=(8, 6))

            # Plotting the relationship
            hr_range = np.linspace(125, 170, 100)
            wl_range = np.linspace(150, 600, 100)
            
            # Create a grid to show the relationship
            X, Y = np.meshgrid(hr_range, wl_range)
            Z = np.zeros_like(X)
            for i in range(X.shape[0]):
                for j in range(X.shape[1]):
                    Z[i, j] = estimate_vo2_max(sex, X[i, j], Y[i, j])

            contour = ax.contourf(X, Y, Z, levels=15, cmap='viridis_r', alpha=0.7)
            fig.colorbar(contour, label='VO2 max (L/min)')

            ax.plot(avg_hr, workload, 'ro', markersize=10, label=f'Your Result ({avg_hr} bpm, {workload} W)')
            ax.set_xlabel("Heart Rate (bpm)")
            ax.set_ylabel("Workload (Watts)")
            ax.set_title("Heart Rate vs. Workload for VO2 Max Estimation")
            ax.legend()
            ax.grid(True)
            st.pyplot(fig)

    # --- Age Correction Table ---
    st.header("Age Correction Factors")
    age_data = {"Age Range": [f"{r[0]}-{r[1]}" for r in AGE_CORRECTION.keys()], "Factor": list(AGE_CORRECTION.values())}
    st.table(age_data)

if __name__ == "__main__":
    main()
