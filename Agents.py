import os
import json
import tkinter as tk
from tkinter import messagebox, Listbox, Scrollbar, OptionMenu, StringVar

# Constants for file paths
ACCOUNT_DATA_FOLDER = 'account_data'
AGENTS_FILE = os.path.join(ACCOUNT_DATA_FOLDER, 'agents.json')
ZZZ_AGENTS_FILE = 'zenless_zone_zero_agents.json'

# Dictionary to hold promotion costs based on promotion level transitions and styles
promotion_costs = {
    (0, 1): ['Green', 4],
    (1, 2): ['Blue', 12],
    (2, 3): ['Blue', 20],
    (3, 4): ['Purple', 10],
    (4, 5): ['Purple', 20]
}

# Mapping from style to certification seal names based on seal colour.
style_certification_seal_map = {
    'Stun': {
        'Green': 'Basic Stun Certification Seal',
        'Blue': 'Advanced Stun Certification Seal',
        'Purple': 'Buster Certification Seal'
    },
    'Attack': {
        'Green': 'Basic Attack Certification Seal',
        'Blue': 'Advanced Attack Certification Seal',
        'Purple': "Pioneer's Certification Seal"
    },
    'Support': {
        'Green': 'Basic Support Certification Seal',
        'Blue': 'Advanced Support Certification Seal',
        'Purple': 'Ruler Certification Seal'
    },
    'Anomaly': {
        'Green': 'Basic Anomaly Certification Seal',
        'Blue': 'Advanced Anomaly Certification Seal',
        'Purple': 'Controller Certification Seal'
    },
        'Defense': {
        'Green': 'Basic Defense Certification Seal',
        'Blue': 'Advanced Defense Certification Seal',
        'Purple': 'Defender Certification Seal'
    }
}

# Function to load JSON data from a file
def load_json(filepath):
    """Load JSON data from a specified file."""
    with open(filepath, 'r') as file:
        return json.load(file)

# Function to save JSON data to a file
def save_json(filepath, data):
    """Save JSON data to a specified file."""
    with open(filepath, 'w') as file:
        json.dump(data, file, indent=4)

# Function to calculate promotion costs based on agent's current and target promotion levels
def calculate_promotion_cost(agent, current_level, target_level):
    """Calculate promotion costs based on promotion level transitions and agent style."""
    if current_level >= target_level:
        return "No promotion needed."
    
    total_cost = {}
    for level in range(current_level, target_level):
        style = agent['style']
        if (level, level + 1) in promotion_costs:
            colour = promotion_costs[(level, level + 1)][0]
            if style in style_certification_seal_map:
                seal_type = style_certification_seal_map[style][colour]
                if seal_type in total_cost:
                    total_cost[seal_type] += promotion_costs[(level, level + 1)][1]
                else:
                    total_cost[seal_type] = promotion_costs[(level, level + 1)][1]
    
    # Format output as requested
    output = []
    for seal, count in total_cost.items():
        output.append(f"{count}x {seal}")
    
    return ", ".join(output)

# Function to calculate total promotion costs for all owned agents
def sum_promotion_costs(agents):
    """Calculate and sum promotion costs for all owned agents."""
    total_cost = {}
    for agent in agents:
        current_level = int(agent['promotion_level'])
        target_level = int(agent['target_promotion_level'])
        cost_details = calculate_promotion_cost(agent, current_level, target_level)
        
        # Check if there's no promotion needed
        if cost_details == "No promotion needed.":
            continue
        
        # Accumulate costs
        for seal_cost in cost_details.split(', '):
            parts = seal_cost.split('x ')
            if len(parts) == 2:
                count, seal = parts
                count = int(count)
                if seal in total_cost:
                    total_cost[seal] += count
                else:
                    total_cost[seal] = count
    
    # Format output as requested
    output = []
    for seal, count in total_cost.items():
        output.append(f"{count}x {seal}")
    
    return ", ".join(output)

# Function to refresh the list of agents displayed in the GUI
def refresh_agent_list(agents, listbox_agents):
    """Refresh the list of agents displayed in the GUI."""
    listbox_agents.delete(0, tk.END)
    for agent in agents:
        listbox_agents.insert(tk.END, f"{agent['name']} (Promotion Level: {agent['promotion_level']}, Target Level: {agent['target_promotion_level']}, Style: {agent['style']})")

# Function to add a selected agent to the owned agents list
def add_agent(agents, listbox_zzz_agents, zzz_agents):
    """Add a selected agent from the available agents list to the owned agents list."""
    selected_index = listbox_zzz_agents.curselection()
    if selected_index:
        selected_agent_data = zzz_agents[selected_index[0]]
        selected_agent_name = selected_agent_data[0]
        selected_agent_style = selected_agent_data[1]
        
        # Check if agent is already owned
        if not any(agent['name'] == selected_agent_name for agent in agents):
            agents.append({'name': selected_agent_name, 'promotion_level': 0, 'target_promotion_level': 0, 'style': selected_agent_style})
            save_json(AGENTS_FILE, agents)
            refresh_agent_list(agents, listbox_agents)
        else:
            messagebox.showinfo("Info", "Agent already owned.")
    else:
        messagebox.showinfo("Info", "No agent selected.")

# Function to delete a selected agent from the owned agents list
def delete_agent(agents, listbox_agents):
    """Delete the selected agent from the owned agents list."""
    selected_index = listbox_agents.curselection()
    if selected_index:
        selected_agent = agents[selected_index[0]]
        agents.remove(selected_agent)
        save_json(AGENTS_FILE, agents)
        refresh_agent_list(agents, listbox_agents)
    else:
        messagebox.showinfo("Info", "No agent selected to delete.")

# Function to edit the promotion levels of a selected agent
def edit_promotion_levels(agents, listbox_agents, current_promotion_var, target_promotion_var):
    """Edit the promotion levels of the selected agent."""
    selected_index = listbox_agents.curselection()
    if selected_index:
        agent = agents[selected_index[0]]
        new_promotion_level = current_promotion_var.get()
        new_target_level = target_promotion_var.get()
        
        # Update agent's promotion levels
        agent['promotion_level'] = new_promotion_level
        agent['target_promotion_level'] = new_target_level
        save_json(AGENTS_FILE, agents)
        refresh_agent_list(agents, listbox_agents)

# Function to calculate and display promotion costs for the selected agent
def show_promotion_cost(agents, listbox_agents):
    """Calculate and display promotion costs for the selected agent."""
    selected_index = listbox_agents.curselection()
    if selected_index:
        agent = agents[selected_index[0]]
        current_level = int(agent['promotion_level'])
        target_level = int(agent['target_promotion_level'])
        
        # Calculate promotion cost
        promotion_cost = calculate_promotion_cost(agent, current_level, target_level)
        if promotion_cost is not None:
            messagebox.showinfo("Promotion Cost", f"Promotion cost: {promotion_cost} seals.")
    else:
        messagebox.showinfo("Info", "No agent selected.")

# Function to handle the sum promotion costs for all owned agents
def sum_promotion_costs_action(agents):
    """Display the total promotion costs for all owned agents."""
    total_cost = sum_promotion_costs(agents)
    messagebox.showinfo("Total Promotion Costs", f"Total Promotion Costs:\n{total_cost}")

# Check if agents.json exists, load it if it does, otherwise initialize an empty list
if os.path.isfile(AGENTS_FILE):
    agents = load_json(AGENTS_FILE)
else:
    agents = []
    save_json(AGENTS_FILE, agents)

# Check if zenless_zone_zero_agents.json exists, load and extract agent data if it does
if os.path.isfile(ZZZ_AGENTS_FILE):
    zzz_agents_data = load_json(ZZZ_AGENTS_FILE)
    zzz_agents = [(agent[0], agent[2]) for agent in zzz_agents_data]  # Extract name and style
else:
    zzz_agents = []
    messagebox.showerror("Error", "zenless_zone_zero_agents.json not found.")
    exit()

# Create GUI window
root = tk.Tk()
root.title("Agents")

# Configure resizing behavior
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)

# Frame and widgets for owned agents list
frame_owned = tk.Frame(root)
frame_owned.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

label_owned = tk.Label(frame_owned, text="Owned Agents")
label_owned.pack()

listbox_agents = Listbox(frame_owned, selectmode=tk.SINGLE)
listbox_agents.pack(fill=tk.BOTH, expand=True)

scrollbar_owned = Scrollbar(frame_owned, orient=tk.VERTICAL, command=listbox_agents.yview)
scrollbar_owned.pack(side=tk.RIGHT, fill=tk.Y)
listbox_agents.config(yscrollcommand=scrollbar_owned.set)

refresh_agent_list(agents, listbox_agents)

# Frame and widgets for available agents list
frame_zzz = tk.Frame(root)
frame_zzz.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

label_zzz = tk.Label(frame_zzz, text="Zenless Zone Zero Agents")
label_zzz.pack()

listbox_zzz_agents = Listbox(frame_zzz, selectmode=tk.SINGLE)
listbox_zzz_agents.pack(fill=tk.BOTH, expand=True)

scrollbar_zzz = Scrollbar(frame_zzz, orient=tk.VERTICAL, command=listbox_zzz_agents.yview)
scrollbar_zzz.pack(side=tk.RIGHT, fill=tk.Y)
listbox_zzz_agents.config(yscrollcommand=scrollbar_zzz.set)

for agent_name, style in zzz_agents:
    listbox_zzz_agents.insert(tk.END, f"{agent_name} (Style: {style})")

# Buttons and widgets for adding, deleting, and editing agent information
button_add_agent = tk.Button(root, text="Add Agent", command=lambda: add_agent(agents, listbox_zzz_agents, zzz_agents))
button_add_agent.grid(row=1, column=0, pady=10)

button_delete_agent = tk.Button(root, text="Delete Agent", command=lambda: delete_agent(agents, listbox_agents))
button_delete_agent.grid(row=1, column=1, pady=10)

label_current_promotion = tk.Label(root, text="Current Promotion Level:")
label_current_promotion.grid(row=2, column=0, pady=5)

current_promotion_var = tk.StringVar(root)
current_promotion_var.set('0')
optionmenu_current_promotion = OptionMenu(root, current_promotion_var, *range(6))
optionmenu_current_promotion.grid(row=2, column=1, pady=5)

label_target_promotion = tk.Label(root, text="Target Promotion Level:")
label_target_promotion.grid(row=3, column=0, pady=5)

target_promotion_var = tk.StringVar(root)
target_promotion_var.set('0')
optionmenu_target_promotion = OptionMenu(root, target_promotion_var, *range(6))
optionmenu_target_promotion.grid(row=3, column=1, pady=5)

button_edit_promotion_levels = tk.Button(root, text="Edit Promotion Levels", command=lambda: edit_promotion_levels(agents, listbox_agents, current_promotion_var, target_promotion_var))
button_edit_promotion_levels.grid(row=3, column=2, pady=5)

button_calculate_cost = tk.Button(root, text="Calculate Promotion Cost", command=lambda: show_promotion_cost(agents, listbox_agents))
button_calculate_cost.grid(row=4, column=1, pady=10)

# Button to sum promotion costs for all agents
button_sum_promotion_costs = tk.Button(root, text="Sum Promotion Costs", command=lambda: sum_promotion_costs_action(agents))
button_sum_promotion_costs.grid(row=4, column=0, pady=10)

# Configure resizing behavior for the main window
root.grid_rowconfigure(1, weight=1)
root.grid_columnconfigure(1, weight=1)

# Start the GUI event loop
root.mainloop()
