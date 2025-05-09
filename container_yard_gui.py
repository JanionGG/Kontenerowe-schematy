
import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import math

def generate_layout():
    try:
        plot_length = float(entry_length.get())
        plot_width = float(entry_width.get())
        num_containers = int(entry_containers.get())
        num_wash_stations = int(entry_wash_stations.get())
        entry_side = entry_var.get()

        container_length = 6
        container_width = 2.4
        margin = 1
        drive_gap = 4

        containers_per_row = int((plot_length - 2 * margin) // container_length)
        num_rows = math.ceil(num_containers / containers_per_row)
        required_height = num_rows * container_width + (num_rows - 1) * drive_gap + 2 * margin

        fig, ax = plt.subplots(figsize=(14, 8))
        ax.set_xlim(0, plot_length)
        ax.set_ylim(0, plot_width)
        ax.set_title("Container Yard Layout")
        ax.set_xlabel("Plot Length (m)")
        ax.set_ylabel("Plot Width (m)")

        plot_border = patches.Rectangle((0, 0), plot_length, plot_width,
                                        linewidth=2, edgecolor='black', facecolor='none')
        ax.add_patch(plot_border)

        if entry_side == "short":
            ax.text(-5, plot_width - 1, "ENTRY FROM SHORT SIDE", fontsize=10, color='black', rotation=90)
        else:
            ax.text(plot_length / 2 - 10, plot_width + 1, "ENTRY FROM LONG SIDE", fontsize=10, color='black')

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

        wash_width = 10
        wash_height = 8 * num_wash_stations
        wash_x = plot_length - wash_width - margin
        wash_y = margin
        wash_station = patches.Rectangle((wash_x, wash_y), wash_width, wash_height,
                                         linewidth=2, edgecolor='green', facecolor='lightgreen')
        ax.add_patch(wash_station)
        ax.text(wash_x + 0.5, wash_y + wash_height / 2 - 1, "WASHING\nSTATION", fontsize=9, color='darkgreen')

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

        if required_height > plot_width:
            ax.text(plot_length / 2 - 10, plot_width - 1, "⚠️ Not enough vertical space for all rows!", color='red', fontsize=10)

        plt.grid(True, linestyle=':', linewidth=0.5)
        plt.tight_layout()
        plt.show()

    except ValueError:
        messagebox.showerror("Input Error", "Please enter valid numbers for all fields.")

root = tk.Tk()
root.title("Container Yard Layout Generator")

tk.Label(root, text="Plot Length (m):").grid(row=0, column=0, sticky='e')
entry_length = tk.Entry(root)
entry_length.grid(row=0, column=1)

tk.Label(root, text="Plot Width (m):").grid(row=1, column=0, sticky='e')
entry_width = tk.Entry(root)
entry_width.grid(row=1, column=1)

tk.Label(root, text="Number of Containers:").grid(row=2, column=0, sticky='e')
entry_containers = tk.Entry(root)
entry_containers.grid(row=2, column=1)

tk.Label(root, text="Number of Washing Stations:").grid(row=3, column=0, sticky='e')
entry_wash_stations = tk.Entry(root)
entry_wash_stations.grid(row=3, column=1)

tk.Label(root, text="Entry Side:").grid(row=4, column=0, sticky='e')
entry_var = tk.StringVar(value="short")
tk.Radiobutton(root, text="Short Side", variable=entry_var, value="short").grid(row=4, column=1, sticky='w')
tk.Radiobutton(root, text="Long Side", variable=entry_var, value="long").grid(row=4, column=2, sticky='w')

tk.Button(root, text="Generate Layout", command=generate_layout).grid(row=5, column=1, pady=10)

root.mainloop()
