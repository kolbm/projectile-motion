import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Constants
g = 10  # Gravity in m/s^2

# Function to calculate projectile motion
def calculate_motion(v0, angle, h0=0):
    angle_rad = np.radians(angle)
    v0x = v0 * np.cos(angle_rad)
    v0y = v0 * np.sin(angle_rad)
    
    # Time of flight calculation, considering initial height h0
    discriminant = v0y**2 + 2 * g * h0
    if discriminant < 0:
        t_flight = 0  # No flight possible if starting conditions are impossible
    else:
        t_flight = (v0y + np.sqrt(discriminant)) / g

    # Time intervals
    t = np.linspace(0, t_flight, num=500)

    # Position calculations
    x = v0x * t
    y = h0 + v0y * t - 0.5 * g * t**2

    # Velocity components
    vx = np.full_like(t, v0x)
    vy = v0y - g * t

    # Acceleration components
    ax = np.zeros_like(t)
    ay = np.full_like(t, -g)

    # Create a DataFrame with results
    data = {
        "Time (s)": t,
        "Position X (m)": x,
        "Position Y (m)": y,
        "Velocity X (m/s)": vx,
        "Velocity Y (m/s)": vy,
        "Acceleration X (m/s²)": ax,
        "Acceleration Y (m/s²)": ay
    }
    df = pd.DataFrame(data)
    
    return df

# Streamlit app interface
st.title("Mr. Kolb's Projectile Motion Simulator")
st.image("https://github.com/kolbm/projectile-motion/blob/main/logo-projectile.jpg?raw=true")

# Inputs
v0 = st.number_input("Enter initial velocity (m/s)", min_value=0.0, value=50.0)
angle = st.number_input("Enter angle of projection (degrees)", min_value=0.0, max_value=90.0, value=45.0)
elevated_start = st.checkbox("Start from an elevated position?")
if elevated_start:
    h0 = st.number_input("Enter initial height (m)", min_value=0.0, value=10.0)
else:
    h0 = 0

# Calculate and display results
if st.button("Simulate"):
    df = calculate_motion(v0, angle, h0)

    # Plotting the trajectory
    fig, ax = plt.subplots()
    ax.plot(df["Position X (m)"], df["Position Y (m)"])
    ax.set_xlabel("Position X (m)")
    ax.set_ylabel("Position Y (m)")
    ax.set_title("Projectile Trajectory")
    st.pyplot(fig)

    # Display data
    st.write("Projectile Data")
    st.dataframe(df)

    # Export data
    csv = df.to_csv(index=False)
    st.download_button(label="Download CSV", data=csv, file_name="projectile_data.csv", mime="text/csv")
