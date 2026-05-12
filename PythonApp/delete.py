import csv
import time
import tkinter as tk
from tkinter import ttk, messagebox

import serial  # pyserial

# ------------ ARDUINO CONNECTION ------------

try:
    # Yahan apna COM port daalo (Arduino IDE me jo dikh raha tha: COM4)
    arduino = serial.Serial("COM4", 9600)
    time.sleep(2)
    print("Arduino connected on COM4")
except Exception as e:
    arduino = None
    print("⚠ Arduino not connected:", e)


# ------------ LOAD MEDICINE DATA ------------

MEDICINE_FILE = "medicines.csv"

def load_medicines():
    medicines = []
    try:
        with open(MEDICINE_FILE, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                medicines.append(row)
    except FileNotFoundError:
        print("⚠ medicines.csv file nahi mila.")
    return medicines

all_medicines = load_medicines()


# ------------ GUI FUNCTIONS ------------

def update_table(filter_text: str = ""):
    """Search box ke hisaab se table filter karega."""
    # Purani rows clear karo
    for row in tree.get_children():
        tree.delete(row)

    ft = filter_text.lower().strip()

    for med in all_medicines:
        name = med["medicine_name"]
        if ft in name.lower():
            tree.insert(
                "",
                "end",
                values=(med["medicine_name"], med["strength"], med["manufacturer"], med["box"]),
            )


def on_search_key(event):
    text = search_var.get()
    update_table(text)


def get_selected_medicine():
    selected = tree.focus()
    if not selected:
        return None
    values = tree.item(selected, "values")
    if not values:
        return None

    # values = (medicine_name, strength, manufacturer, box)
    selected_med = {
        "medicine_name": values[0],
        "strength": values[1],
        "manufacturer": values[2],
        "box": values[3],
    }
    return selected_med


def highlight_box(box_type: str):
    """Kaunsa box active hai, uska border bold dikhao."""
    if box_type == "painkiller":
        box1.config(bd=4, relief="solid")
        box2.config(bd=1, relief="ridge")
        selected_box_label.config(text="Selected Box: 1 (Painkiller)")
    elif box_type == "dolo":
        box1.config(bd=1, relief="ridge")
        box2.config(bd=4, relief="solid")
        selected_box_label.config(text="Selected Box: 2 (Dolo)")
    else:
        box1.config(bd=1, relief="ridge")
        box2.config(bd=1, relief="ridge")
        selected_box_label.config(text="Selected Box: -")


def dispense_selected():
    med = get_selected_medicine()
    if not med:
        messagebox.showwarning("No selection", "Pehle koi medicine select karo.")
        return

    box_type = med["box"].lower()

    if not arduino:
        messagebox.showerror("Arduino Error", "Arduino connected nahi hai.")
        return

    # Arduino ko jo string chahiye:
    if box_type == "painkiller":
        cmd = "painkiller"
    elif box_type == "dolo":
        # Tumhare Arduino code me 'dolo' ke liye 'paracetamol' command jaayega
        cmd = "paracetamol"
    else:
        messagebox.showerror("Unknown Box", f"Box type '{box_type}' samajh nahi aaya.")
        return

    try:
        arduino.write((cmd + "\n").encode())
        highlight_box(box_type)
        messagebox.showinfo(
            "Dispensed",
            f"{med['medicine_name']} ({box_type}) command sent: {cmd}",
        )
    except Exception as e:
        messagebox.showerror("Serial Error", f"Command nahi bhej paaye:\n{e}")


# ------------ GUI LAYOUT ------------

root = tk.Tk()
root.title("Medical Shop Style Medicine Search + Dispenser")
root.geometry("800x500")

# Top: Search bar
search_frame = tk.Frame(root)
search_frame.pack(fill="x", padx=10, pady=10)

tk.Label(
    search_frame, text="Search Medicine Name:", font=("Arial", 12, "bold")
).pack(side="left")

search_var = tk.StringVar()
search_entry = tk.Entry(search_frame, textvariable=search_var, font=("Arial", 12), width=30)
search_entry.pack(side="left", padx=10)
search_entry.bind("<KeyRelease>", on_search_key)

# Center: Table (Treeview)
columns = ("name", "strength", "manufacturer", "box")
tree = ttk.Treeview(root, columns=columns, show="headings", height=12)

tree.heading("name", text="Medicine Name")
tree.heading("strength", text="Strength")
tree.heading("manufacturer", text="Manufacturer")
tree.heading("box", text="Box")

tree.column("name", width=320)
tree.column("strength", width=80, anchor="center")
tree.column("manufacturer", width=180)
tree.column("box", width=80, anchor="center")

tree.pack(fill="both", expand=True, padx=10)

# Initially show all medicines
update_table()

# Bottom: Box info + Dispense button
bottom_frame = tk.Frame(root)
bottom_frame.pack(fill="x", padx=10, pady=10)

# Box 1 – Painkiller (Green)
box1 = tk.LabelFrame(
    bottom_frame,
    text="Box 1 - Painkiller",
    bg="#b6f7b0",
    padx=10,
    pady=10,
)
box1.pack(side="left", fill="both", expand=True, padx=5)

tk.Label(box1, text="Servo for Painkiller", bg="#b6f7b0", font=("Arial", 11)).pack()

# Box 2 – Dolo (Blue)
box2 = tk.LabelFrame(
    bottom_frame,
    text="Box 2 - Dolo",
    bg="#b0d6ff",
    padx=10,
    pady=10,
)
box2.pack(side="left", fill="both", expand=True, padx=5)

tk.Label(box2, text="Servo for Dolo (Paracetamol)", bg="#b0d6ff", font=("Arial", 11)).pack()

# Right side: controls
control_frame = tk.Frame(bottom_frame)
control_frame.pack(side="left", padx=5)

dispense_btn = tk.Button(
    control_frame,
    text="Dispense Selected",
    font=("Arial", 12, "bold"),
    command=dispense_selected,
    width=18,
)
dispense_btn.pack(pady=5)

selected_box_label = tk.Label(control_frame, text="Selected Box: -", font=("Arial", 11))
selected_box_label.pack(pady=5)

root.mainloop()
