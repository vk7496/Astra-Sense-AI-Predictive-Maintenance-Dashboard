import streamlit as st
import os
from openai import OpenAI
import numpy as np
import pandas as pd
import time
from datetime import datetime

# -------------------------------------------
#  🔧 Initialize OpenAI Client
# -------------------------------------------
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def generate_ai_insight(vibration, temperature):
    prompt = f"""
    You are an industrial predictive‑maintenance AI.
    Analyze the following industrial sensor readings and provide insights:
    - Condition summary
    - Likelihood of failure (0–100%)
    - Recommended action

    Sensor data:
    • Vibration: {vibration}
    • Temperature: {temperature} 
    provide anomaly detection and maintenance recommendations.
    """

    try:
        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"AI Insight unavailable. Error: {str(e)}"


# -------------------------------------------
#  🌡 Sensor Simulation
# -------------------------------------------

def generate_sensor_data():
    temperature = np.random.normal(52, 1.5)
    vibration = np.random.normal(0.4, 0.1)
    rpm = np.random.normal(1500, 8)

    # Random anomaly injection
    if np.random.rand() < 0.05:
        vibration += np.random.uniform(0.5, 1.0)
        temperature += np.random.uniform(6, 12)

    return temperature, vibration, rpm


# -------------------------------------------
#  🖥 Streamlit UI
# -------------------------------------------

st.set_page_config(page_title="AstraSense™ Predictive Dashboard", layout="wide")
st.title("AstraSense™ — AI‑Driven Predictive Maintenance Dashboard")

if "data" not in st.session_state:
    st.session_state.data = []

placeholder = st.empty()


# -------------------------------------------
#  🔄 Live Simulation Loop
# -------------------------------------------
for _ in range(120):
    temp, vib, rpm = generate_sensor_data()
    timestamp = datetime.now()

    st.session_state.data.append({
        "time": timestamp,
        "temperature": temp,
        "vibration": vib,
        "rpm": rpm,
    })

    df = pd.DataFrame(st.session_state.data)

    # Anomaly flag
    anomaly = (temp > 60) or (vib > 0.9)

    # Generate AI insight
    ai_result = generate_ai_insight(vibration=vib, temperature=temp)

    with placeholder.container():
        col1, col2 = st.columns([2, 1])

        with col1:
            st.subheader("📊 Live Sensor Feed")
            st.line_chart(df.set_index("time")[['temperature', 'vibration', 'rpm']])

        with col2:
            st.subheader("🤖 AI Diagnosis")
            if anomaly:
                st.error("⚠️ Potential Equipment Failure Detected!")
            else:
                st.success("✔ Normal Operation")

            st.metric("Temperature (°C)", f"{temp:.2f}")
            st.metric("Vibration (g)", f"{vib:.3f}")
            st.metric("RPM", f"{rpm:.0f}")

            st.write("---")
            st.write("### 🔎 AI Insight")
            st.write(ai_result)

    time.sleep(0.4)
