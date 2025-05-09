
import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import math

st.set_page_config(page_title="Container Yard Planner", page_icon="📐", layout="wide")
st.image("logo_tuiowdzie.png", width=200)  # lokalne logo w repozytorium

st.title("Container Yard Layout Generator")

# --- Formularz danych wejściowych ---
with st.sidebar:
    st.header("Configuration")

    plot_length = st.number_input("Plot Length (m)", min_value=10.0, value=80.0)
    plot_width = st.number_input("Plot Width (m)", min_value=10.0, value=38.0)
    num_containers = st.number_input("Number of Containers", min_value=1, value=50)
    num_wash_stations = st.number_input("Number of Washing Stations", min_value=1, value=2)
    wash_width = st.number_input("Washing Station Width (m)", min_value=1.0, value=2.44)
    wash_length = st.number_input("Washing Station Length (m)", min_value=1.0, value=4.88)
    wash_gap = 2  # odstęp między stacjami

    entry_side = st.radio("Entry from", options=["Short Side", "Long Side"])

# --- Parametry stałe ---
container_length = 6
container_width = 2.4
margin = 1
drive_gap = 4

# --- Oblicz układ zależny od wjazdu ---
if entry_side == "Short Side":
    rows_dir = "horizontal"
    containers_per_row = int((plot_length - 2 * margin) // container_length)
    num_rows = math.ceil(num_containers / containers_per_row)
else:
    rows_dir = "vertical"
    containers_per_row = int((plot_width - 2 * margin) // container_length)
    num_rows = math.ceil(num_containers / containers_per_row)

# --- Rysowanie ---
fig, ax = plt.subplots(figsize=(14, 8))
ax.set_xlim(0, plot_length)
ax.set_ylim(0, plot_width)
ax.set_title("Container Yard Layout")
ax.set_xlabel("Plot Length (m)")
ax.set_ylabel("Plot Width (m)")

plot_border = patches.Rectangle((0, 0), plot_length, plot_width,
                                linewidth=2, edgecolor='black', facecolor='none')
ax.add_patch(plot_border)

container_count = 0
if rows_dir == "horizontal":
    current_y = plot_width - margin - container_width
    for row in range(num_rows):
        current_x = margin
        for i in range(containers_per_row):
            if container_count >= num_containers:
                break
            container = patches.Rectangle((current_x, current_y), container_length, container_width,
                                          linewidth=1, edgecolor='blue', facecolor='lightblue')
            ax.add_patch(container)
            current_x += container_length
            container_count += 1
        current_y -= (container_width + drive_gap)
else:
    current_x = margin
    for row in range(num_rows):
        current_y = plot_width - margin - container_length
        for i in range(containers_per_row):
            if container_count >= num_containers:
                break
            container = patches.Rectangle((current_x, current_y), container_width, container_length,
                                          linewidth=1, edgecolor='blue', facecolor='lightblue')
            ax.add_patch(container)
            current_y -= container_length
            container_count += 1
        current_x += (container_width + drive_gap)

# Stacje myjące – na dole po prawej stronie
wash_x = plot_length - wash_length - margin
wash_start_y = margin
for i in range(num_wash_stations):
    wy = wash_start_y + i * (wash_width + wash_gap)
    if wy + wash_width + margin <= plot_width:
        wash_station = patches.Rectangle((wash_x, wy), wash_length, wash_width,
                                         linewidth=2, edgecolor='green', facecolor='lightgreen')
        ax.add_patch(wash_station)
        ax.text(wash_x + 0.2, wy + wash_width / 2 - 0.5, f"WASHING {i + 1}", fontsize=8, color='darkgreen')

road_width = 4
road = patches.Rectangle((0, 0), road_width, plot_width,
                         linewidth=0, edgecolor='none', facecolor='lightgray', alpha=0.5)
ax.add_patch(road)
ax.text(road_width / 2 - 0.5, plot_width / 2, "DRIVEWAY", rotation=90, fontsize=8, color='black')

legend_elements = [
    patches.Patch(color='lightblue', label='Container'),
    patches.Patch(color='lightgreen', label='Washing Station'),
    patches.Patch(color='lightgray', label='Driveway')
]
ax.legend(handles=legend_elements, loc='lower right')

ax.grid(True, linestyle=':', linewidth=0.5)
st.pyplot(fig)
