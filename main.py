import tkinter as tk
import subprocess

def run_agents():
    subprocess.run(["python", "Agents.py"])

def run_w_engines():
    subprocess.run(["python", "W-Engines.py"])

def run_planner():
    subprocess.run(["python", "Planner.py"])

def run_inventory():
    subprocess.run(["python", "Inventory.py"])

# Create the main window
root = tk.Tk()
root.title("Main GUI")

# Create buttons
agents_button = tk.Button(root, text="Agents", command=run_agents)
w_engines_button = tk.Button(root, text="W-Engines", command=run_w_engines)
planner_button = tk.Button(root, text="Planner", command=run_planner)
inventory_button = tk.Button(root, text="Inventory", command=run_inventory)

# Place buttons in the window
agents_button.pack(pady=10)
w_engines_button.pack(pady=10)
planner_button.pack(pady=10)
inventory_button.pack(pady=10)

# Run the main event loop
root.mainloop()