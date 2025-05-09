
import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import math

st.set_page_config(page_title="Container Yard Layout Generator", layout="wide")
st.title("📦 Container Yard Layout Generator")

# Dane wejściowe
plot_length = st.number_input("Plot Length (m)", min_value=10.0, value=80.0)
plot_width = st.number_input("Plot Width (m)", min_value=10.0, value=38.0)
num_containers = st.number_input("Number of Containers", min_value=1, value=50)
num_wash_stations = st.number_input("Number of Washing Stations", min_value=1, value=1)
entry_side = st.radio("Entry Side", options=["Short Side", "Long Side"])

# Parametry kontenera i layoutu
container_length = 6
container_width = 2.4
margin = 1
drive_gap = 4

# Obliczenia układu
containers_per_row = int((plot_length - 2 * margin) // container_length)
num_rows = math.ceil(num_containers / containers_per_row)
required_height = num_rows * container_width + (num_rows - 1) * drive_gap + 2 * margin

fig, ax = plt.subplots(figsize=(14, 8))
ax.set_xlim(0, plot_length)
ax.set_ylim(0, plot_width)
ax.set_title("Container Yard Layout")
ax.set_xlabel("Plot Length (m)")
ax.set_ylabel("Plot Width (m)")

# Granica działki
plot_border = patches.Rectangle((0, 0), plot_length, plot_width,
                                linewidth=2, edgecolor='black', facecolor='none')
ax.add_patch(plot_border)

# Etykieta wjazdu
if entry_side == "Short Side":
    ax.text(-5, plot_width - 1, "ENTRY FROM SHORT SIDE", fontsize=10, color='black', rotation=90)
else:
    ax.text(plot_length / 2 - 10, plot_width + 1, "ENTRY FROM LONG SIDE", fontsize=10, color='black')

# Rysowanie kontenerów
current_y = plot_width - margin - container_width
container_count = 0
for row in range(num_rows):
    current_x = margin
    for i in range(containers_per_row):
        if container_count >= num_containers:
            break
        if current_x + container_length <= plot_length - margin:
            container = patches.Rectangle((current_x, current_y), container_length, container_width,
                                          linewidth=1, edgecolor='blue', facecolor='lightblue')
            ax.add_patch(container)
            container_count += 1
            current_x += container_length
    current_y -= (container_width + drive_gap)

# Stacja myjąca
wash_width = 10
wash_height = 8 * num_wash_stations
wash_x = plot_length - wash_width - margin
wash_y = margin
wash_station = patches.Rectangle((wash_x, wash_y), wash_width, wash_height,
                                 linewidth=2, edgecolor='green', facecolor='lightgreen')
ax.add_patch(wash_station)
ax.text(wash_x + 0.5, wash_y + wash_height / 2 - 1, "WASHING\nSTATION", fontsize=9, color='darkgreen')

# Ciąg komunikacyjny
road_width = 4
road = patches.Rectangle((0, 0), road_width, plot_width,
                         linewidth=0, edgecolor='none', facecolor='lightgray', alpha=0.5)
ax.add_patch(road)
ax.text(road_width / 2 - 0.5, plot_width / 2, "DRIVEWAY", rotation=90, fontsize=8, color='black')

# Legenda
legend_elements = [
    patches.Patch(color='lightblue', label='Container'),
    patches.Patch(color='lightgreen', label='Washing Station'),
    patches.Patch(color='lightgray', label='Driveway')
]
ax.legend(handles=legend_elements, loc='lower right')

if required_height > plot_width:
    ax.text(plot_length / 2 - 10, plot_width - 1, "⚠️ Not enough vertical space for all rows!", color='red', fontsize=10)

ax.grid(True, linestyle=':', linewidth=0.5)
st.pyplot(fig)
