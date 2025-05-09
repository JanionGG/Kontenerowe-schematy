
import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import math

st.set_page_config(page_title="Container Yard Planner", page_icon="📐", layout="wide")
st.image("logo_tuiowdzie.png", width=200)

st.title("Container Yard Layout Generator")

# --- Sidebar: Input ---
with st.sidebar:
    st.header("Configuration")

    plot_length = st.number_input("Plot Length (m)", min_value=10.0, value=80.0)
    plot_width = st.number_input("Plot Width (m)", min_value=10.0, value=38.0)
    num_containers = st.number_input("Number of Containers", min_value=1, value=50)
    num_wash_stations = st.number_input("Number of Washing Stations", min_value=1, value=2)
    wash_width = st.number_input("Washing Station Width (m)", min_value=1.0, value=2.44)
    wash_length = st.number_input("Washing Station Length (m)", min_value=1.0, value=4.88)
    entry_side = st.radio("Entry from", options=["Short Side", "Long Side"])

# --- Constants ---
container_length = 6
container_width = 2.4
margin = 1
access_road_width = 4
wash_gap = 2
entry_width = 6

# --- Layout Direction ---
if entry_side == "Short Side":
    rows_dir = "horizontal"
    containers_per_row = int((plot_length - 2 * margin) // container_length)
    num_rows = math.ceil(num_containers / containers_per_row)
else:
    rows_dir = "vertical"
    containers_per_row = int((plot_width - 2 * margin) // container_length)
    num_rows = math.ceil(num_containers / containers_per_row)

# --- Drawing ---
fig, ax = plt.subplots(figsize=(14, 8))
ax.set_xlim(0, plot_length)
ax.set_ylim(0, plot_width)
ax.set_title("Container Yard Layout")
ax.set_xlabel("Plot Length (m)")
ax.set_ylabel("Plot Width (m)")

# Yard Border
ax.add_patch(patches.Rectangle((0, 0), plot_length, plot_width,
                               linewidth=2, edgecolor='black', facecolor='none'))

# Entry Placement
if entry_side == "Short Side":
    ex = (plot_length - entry_width) / 2
    ax.add_patch(patches.Rectangle((ex, plot_width), entry_width, 1,
                                   linewidth=0, edgecolor='none', facecolor='orange'))
    ax.text(ex + 0.5, plot_width + 0.5, "ENTRY", color='orange')
else:
    ey = (plot_width - entry_width) / 2
    ax.add_patch(patches.Rectangle((-1, ey), 1, entry_width,
                                   linewidth=0, edgecolor='none', facecolor='orange'))
    ax.text(-5, ey + entry_width / 2, "ENTRY", color='orange', rotation=90)

# Containers & Access Roads
container_count = 0
if rows_dir == "horizontal":
    current_y = plot_width - margin - container_width
    for row in range(num_rows):
        current_x = margin
        for i in range(containers_per_row):
            if container_count >= num_containers:
                break
            if current_x >= access_road_width:
                ax.add_patch(patches.Rectangle((current_x, current_y), container_length, container_width,
                                               linewidth=1, edgecolor='blue', facecolor='lightblue'))
                container_count += 1
            current_x += container_length
        current_y -= (container_width + access_road_width)
else:
    current_x = margin
    for row in range(num_rows):
        current_y = plot_width - margin - container_length
        for i in range(containers_per_row):
            if container_count >= num_containers:
                break
            if current_x >= access_road_width:
                ax.add_patch(patches.Rectangle((current_x, current_y), container_width, container_length,
                                               linewidth=1, edgecolor='blue', facecolor='lightblue'))
                container_count += 1
            current_y -= container_length
        current_x += (container_width + access_road_width)

# Wash Stations (non-overlapping and off driveway)
wash_x = plot_length - wash_length - margin
wash_y_start = margin
for i in range(num_wash_stations):
    wy = wash_y_start + i * (wash_width + wash_gap)
    if wy + wash_width <= plot_width - margin and wash_x >= access_road_width:
        ax.add_patch(patches.Rectangle((wash_x, wy), wash_length, wash_width,
                                       linewidth=2, edgecolor='green', facecolor='lightgreen'))
        ax.text(wash_x + 0.2, wy + wash_width / 2 - 0.5,
                f"WASH {i + 1}", fontsize=8, color='darkgreen')
    else:
        st.warning("⚠️ Not enough vertical space or wash station conflicts with driveway.")

# Main Driveway
road = patches.Rectangle((0, 0), access_road_width, plot_width,
                         linewidth=0, edgecolor='none', facecolor='lightgray', alpha=0.5)
ax.add_patch(road)
ax.text(access_road_width / 2 - 0.5, plot_width / 2, "DRIVEWAY", rotation=90, fontsize=8, color='black')

# Legend
legend_elements = [
    patches.Patch(color='lightblue', label='Container'),
    patches.Patch(color='lightgreen', label='Washing Station'),
    patches.Patch(color='lightgray', label='Driveway'),
    patches.Patch(color='orange', label='Entry')
]
ax.legend(handles=legend_elements, loc='lower right')

ax.grid(True, linestyle=':', linewidth=0.5)
st.pyplot(fig)
