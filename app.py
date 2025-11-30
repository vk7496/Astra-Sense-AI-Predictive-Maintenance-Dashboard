# AstraSense™ - Industrial AI Predictive Maintenance Dashboard

## 📘 Introduction
Welcome to **AstraSense™ Predictive Intelligence** — a lightweight, real-time AI system for industrial equipment monitoring and predictive failure detection.

This demo includes:
- Real-time vibration & temperature simulation
- AI-based anomaly detection
- Early warning insights (bearing failure scenario)
- Professional industrial UI

---

import streamlit as st
import os
from openai import OpenAI

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_ai_insight(vibration, temperature):
    prompt = f"""
    Analyze the following industrial sensor readings and provide insights:
    - Vibration data: {vibration}
    - Temperature data: {temperature}
    Provide anomaly detection and maintenance recommendations.
    """
    try:
        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message["content"]
    except Exception:
        return "AI Insight unavailable (fallback mode)."
import numpy as np
import pandas as pd
import time
from datetime import datetime

st.set_page_config(page_title="AI Predictive Maintenance Demo", layout="wide")
st.title("AstraSense™ Predictive Intelligence Dashboard")

# --- Simulated Data Function ---
def generate_sensor_data():
    temperature = np.random.normal(52, 1.5)
    vibration = np.random.normal(0.4, 0.1)
    rpm = np.random.normal(1500, 10)

    # Inject anomaly occasionally
    if np.random.rand() < 0.05:
        vibration += np.random.uniform(0.5, 1.0)
        temperature += np.random.uniform(5, 10)

    return temperature, vibration, rpm

# --- Storage ---
if "data" not in st.session_state:
    st.session_state.data = []

placeholder = st.empty()

# --- Live Simulation ---
for _ in range(150): # Simulate 150 cycles
    temp, vib, rpm = generate_sensor_data()
    timestamp = datetime.now()

    st.session_state.data.append({
        "time": timestamp,
        "temperature": temp,
        "vibration": vib,
        "rpm": rpm,
    })

    df = pd.DataFrame(st.session_state.data)

    # --- Simple anomaly rule ---
    anomaly = (temp > 60) or (vib > 0.9)

    with placeholder.container():
        col1, col2 = st.columns(2)

        with col1:
            st.subheader("📊 Live Sensor Data")
            st.line_chart(df.set_index("time")[["temperature", "vibration", "rpm"]])

        with col2:
            st.subheader("🔍 AI Diagnosis")
            if anomaly:
                st.error("⚠️ Potential Failure Detected! High vibration/temperature levels.")
            else:
                st.success("✔ Equipment Operating Normally")

            st.metric("Temperature (°C)", f"{temp:.2f}")
            st.metric("Vibration (g)", f"{vib:.2f}")
            st.metric("RPM", f"{rpm:.0f}")

    time.sleep(0.5) # simulate real-time stream
