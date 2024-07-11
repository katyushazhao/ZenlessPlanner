import tkinter as tk
import subprocess
import os
import json

def ensure_json_file_exists(filepath, default_content=[]):
    if not os.path.isfile(filepath):
        with open(filepath, 'w') as file:
            json.dump(default_content, file, indent=4)

def main():
    folder_path = 'account_data'
    os.makedirs(folder_path, exist_ok=True)

    json_files = ['agents.json', 'w-engines.json', 'inventory.json']

    for json_file in json_files:
        filepath = os.path.join(folder_path, json_file)
        ensure_json_file_exists(filepath)

if __name__ == "__main__":
    main()

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