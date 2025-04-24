import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import os
import subprocess
import platform
import time

file_listbox = None
all_files = []
last_opened_file = None
last_file_mtime = None

def get_modules():
    files = os.listdir("sources")
    return [f[:-5] for f in files if f.endswith(".vhdl")]

def run_simulation():
    module = selected_module.get()
    if not module:
        messagebox.showerror("Error", "Please select a module.")
        return

    try:
        subprocess.run(["python", "sim/simulate.py", "--file", f"sources/{module}.vhdl"], check=True)
        with open("reports/simulation_output.txt", "r") as f:
            output_text.delete("1.0", tk.END)
            output_text.insert(tk.END, f.read())
    except Exception as e:
        messagebox.showerror("Simulation Failed", str(e))

def simulate_all():
    try:
        subprocess.run(["tclsh", "build_project.tcl", "--simulate-all"], check=True)
        with open("reports/simulation_output.txt", "r") as f:
            output_text.delete("1.0", tk.END)
            output_text.insert(tk.END, f.read())
    except Exception as e:
        messagebox.showerror("Batch Simulation Failed", str(e))
        
def refresh_file_list():
    global all_files
    file_listbox.delete(0, tk.END)
    all_files = []

    for folder in ["sources", "tests", "logs", "reports"]:
        file_listbox.insert(tk.END, f"[{folder.upper()}]")
        all_files.append(None)

        folder_path = os.path.join(os.getcwd(), folder)
        if not os.path.isdir(folder_path):
            continue
        for fname in os.listdir(folder_path):
            full_path = os.path.join(folder, fname)
            file_listbox.insert(tk.END, f"  {fname}")
            all_files.append(full_path)

def open_selected_file(event):
    global last_opened_file
    index = file_listbox.curselection()
    if not index:
        return

    file_path = all_files[index[0]]
    if file_path is None:
        return

    last_opened_file = file_path  # <-- Track selected file

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            contents = f.read()
        output_text.delete("1.0", tk.END)
        output_text.insert(tk.END, f"===== {file_path} =====\n\n{contents}")
    except Exception as e:
        output_text.delete("1.0", tk.END)
        output_text.insert(tk.END, f"Could not open file: {file_path}\n\n{str(e)}")

def open_in_editor():
    if not last_opened_file:
        messagebox.showinfo("No file selected", "Please select a file from the left panel first.")
        return

    abs_path = os.path.abspath(last_opened_file)

    try:
        if platform.system() == "Windows":
            os.startfile(abs_path)
        elif platform.system() == "Darwin":  # macOS
            subprocess.run(["open", abs_path])
        else:  # Linux
            subprocess.run(["xdg-open", abs_path])
    except Exception as e:
        messagebox.showerror("Error", f"Could not open file:\n{abs_path}\n\n{str(e)}")

def save_file_contents():
    if not last_opened_file:
        messagebox.showinfo("No file selected", "Select a file from the left panel first.")
        return

    try:
        with open(last_opened_file, "w", encoding="utf-8") as f:
            content = output_text.get("1.0", tk.END)
            f.write(content)
        messagebox.showinfo("Saved", f"Changes saved to:\n{last_opened_file}")
    except Exception as e:
        messagebox.showerror("Save Failed", str(e))

def check_file_update():
    global last_file_mtime

    if last_opened_file and os.path.exists(last_opened_file):
        current_mtime = os.path.getmtime(last_opened_file)
        if last_file_mtime is None:
            last_file_mtime = current_mtime
        elif current_mtime != last_file_mtime:
            last_file_mtime = current_mtime
            try:
                with open(last_opened_file, "r", encoding="utf-8") as f:
                    contents = f.read()
                output_text.delete("1.0", tk.END)
                output_text.insert(tk.END, f"===== {last_opened_file} (auto-reloaded) =====\n\n{contents}")
            except:
                pass

    root.after(2000, check_file_update)  # Check every 2 seconds

def run_flow_command(command):
    try:
        subprocess.run(["tclsh", "build_project.tcl", command], check=True)
        with open("reports/simulation_output.txt", "r", encoding="utf-8") as f:
            output_text.delete("1.0", tk.END)
            output_text.insert(tk.END, f"===== Output from {command} =====\n\n")
            output_text.insert(tk.END, f.read())
    except Exception as e:
        output_text.delete("1.0", tk.END)
        output_text.insert(tk.END, f"Command '{command}' failed.\n\n{str(e)}")

# UI Setup
root = tk.Tk()
root.title("HDL Flow Studio")
root.geometry("900x550")

title = tk.Label(root, text="HDL Flow Studio GUI", font=("Arial", 16))
title.pack(pady=10)

# === MAIN LAYOUT FRAME ===
layout = tk.Frame(root)
layout.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

# === LEFT: FILE LIST PANEL ===
file_list_frame = tk.Frame(layout)
file_list_frame.pack(side=tk.LEFT, fill=tk.Y)

tk.Label(file_list_frame, text="Project Files").pack()
file_listbox = tk.Listbox(file_list_frame, width=30, height=25)
file_listbox.pack(side=tk.LEFT, fill=tk.Y)
file_listbox.bind("<<ListboxSelect>>", open_selected_file)
file_listbox.bind("<Double-Button-1>", lambda event: open_in_editor())


# === RIGHT: SIMULATION PANEL ===
right_frame = tk.Frame(layout)
right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

# Module dropdown + buttons
top_controls = tk.Frame(right_frame)
top_controls.pack(pady=5)

tk.Label(top_controls, text="Select module:").grid(row=0, column=0, padx=5)
selected_module = tk.StringVar()
dropdown = ttk.Combobox(top_controls, textvariable=selected_module, values=get_modules(), width=30)
dropdown.grid(row=0, column=1, padx=5)

run_button = tk.Button(top_controls, text="Run Simulation", command=run_simulation)
run_button.grid(row=0, column=2, padx=5)

batch_button = tk.Button(top_controls, text="Simulate All Modules", command=simulate_all)
batch_button.grid(row=0, column=3, padx=5)

open_button = tk.Button(top_controls, text="Open File", command=lambda: open_in_editor())
open_button.grid(row=0, column=4, padx=5)

full_button = tk.Button(top_controls, text="Run Full Flow", command=lambda: run_flow_command("--full"))
full_button.grid(row=1, column=0, padx=5, pady=5)

clean_button = tk.Button(top_controls, text="Clean Project", command=lambda: run_flow_command("--clean"))
clean_button.grid(row=1, column=1, padx=5, pady=5)

bit_button = tk.Button(top_controls, text="Bitstream Only", command=lambda: run_flow_command("--bitstream-only"))
bit_button.grid(row=1, column=2, padx=5, pady=5)

# Output + Save container
output_frame = tk.Frame(right_frame)
output_frame.pack(fill=tk.BOTH, expand=True)

output_text = tk.Text(output_frame, wrap=tk.NONE)
output_text.pack(fill=tk.BOTH, expand=True, pady=(0, 2))

save_button = tk.Button(output_frame, text="Save Changes", command=save_file_contents)
save_button.pack(pady=(0, 2))


# Populate left file panel
refresh_file_list()

# Start GUI
check_file_update()
root.mainloop()

