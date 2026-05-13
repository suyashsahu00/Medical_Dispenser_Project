import csv
import time
from datetime import datetime
import tkinter as tk
from tkinter import ttk, messagebox

import serial
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from pathlib import Path

# ---------------- CONFIG ---------------- #
ARDUINO_PORT = "COM4"      # Change this according to your Arduino port
BAUD_RATE = 115200

MEDICINE_FILE = Path(__file__).resolve().parent / "medicines.csv"
print(f"Looking for medicines.csv at: {MEDICINE_FILE}")

SHOP_NAME = "MediCare Pharmacy"
SHOP_ADDRESS_LINE1 = "13 Health Street"
SHOP_ADDRESS_LINE2 = "Mumbai, Maharashtra, India"
SHOP_PHONE = "+91-9345678991"
SHOP_GSTIN = "27AAAAA0000A1Z5"

# ---------------- ARDUINO ---------------- #
try:
    arduino = serial.Serial(ARDUINO_PORT, BAUD_RATE, timeout=1)
    time.sleep(2)
    print(f"✅ Arduino connected on {ARDUINO_PORT}")
except Exception as e:
    arduino = None
    print("⚠ Arduino not connected:", e)

# ---------------- DATA LOADING ---------------- #
def load_medicines():
    medicines = []
    try:
        with open(MEDICINE_FILE, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                clean_row = {k.strip(): (v.strip() if isinstance(v, str) else v) for k, v in row.items()}
                medicines.append(clean_row)
    except FileNotFoundError as e:
        print(f"⚠ medicines.csv not found: {e}")
    return medicines

all_medicines = load_medicines()

def to_float(val, default=0.0):
    try:
        return float(str(val).strip())
    except:
        return default

# ---------------- GLOBAL VARIABLES ---------------- #
cart_items = []
totals = {"mrp": 0.0, "discount": 0.0, "gst": 0.0, "grand": 0.0}
boxes_visible = False

# ---------------- BOX MAPPING ---------------- #
def get_box_number(med_type: str) -> int:
    mt = str(med_type).lower().strip()
    if mt in ("painkiller", "box1", "1"): return 1
    elif mt in ("paracetamol", "dolo", "box2", "2"): return 2
    elif mt in ("box3", "3"): return 3
    elif mt in ("box4", "4"): return 4
    return 1

# ---------------- UI SETUP ---------------- #
root = tk.Tk()
root.title("Medical Billing & Servo Dispenser")
root.geometry("1150x720")
root.configure(bg="#edf2ff")

style = ttk.Style()
style.theme_use("clam")

# Title
title_frame = tk.Frame(root, bg="#4c6fff")
title_frame.pack(fill="x")
tk.Label(title_frame, text="Medical Billing & Automatic Servo Dispenser", 
         bg="#4c6fff", fg="white", font=("Segoe UI", 14, "bold"), pady=8).pack()

# Search Frame
search_frame = tk.Frame(root, bg="#edf2ff")
search_frame.pack(fill="x", padx=10, pady=8)

tk.Label(search_frame, text="Search Medicine Name:", font=("Segoe UI", 11, "bold"), bg="#edf2ff").pack(side="left")
search_var = tk.StringVar()
search_entry = ttk.Entry(search_frame, textvariable=search_var, width=35)
search_entry.pack(side="left", padx=8)
search_entry.bind("<KeyRelease>", lambda e: update_table(search_var.get().strip()))

tk.Label(search_frame, text="Qty:", bg="#edf2ff").pack(side="left", padx=(15,5))
qty_var = tk.StringVar(value="1")
ttk.Entry(search_frame, textvariable=qty_var, width=8).pack(side="left")

ttk.Button(search_frame, text="Add to Cart", command=lambda: add_to_cart()).pack(side="left", padx=8)
ttk.Button(search_frame, text="Dispense Last Item", command=lambda: dispense_selected()).pack(side="left")

# Search Table
tree_search = ttk.Treeview(root, columns=("name","alt","strength","manu","type","sale","disc","tax"), 
                           show="headings", height=8)
cols = [("name","Medicine Name",230), ("alt","Alternate",200), ("strength","Strength",80),
        ("manu","Manufacturer",150), ("type","Type",90), ("sale","Rate",80),
        ("disc","Disc%",70), ("tax","GST%",70)]
for col, text, w in cols:
    tree_search.heading(col, text=text)
    tree_search.column(col, width=w)
tree_search.pack(fill="x", padx=10, pady=5)

# Cart
tk.Label(root, text="Cart", font=("Segoe UI", 12, "bold"), bg="#edf2ff").pack(anchor="w", padx=10, pady=(10,0))

tree_cart = ttk.Treeview(root, columns=("name","qty","mrp","gst","disc","total"), show="headings", height=7)
cart_cols = [("name","Medicine",300), ("qty","Qty",60), ("mrp","MRP",90), 
             ("gst","GST",90), ("disc","Discount",100), ("total","Total",100)]
for col, text, w in cart_cols:
    tree_cart.heading(col, text=text)
    tree_cart.column(col, width=w)
tree_cart.pack(fill="x", padx=10, pady=5)

# Cart Buttons
cart_btn_frame = tk.Frame(root, bg="#edf2ff")
cart_btn_frame.pack(fill="x", padx=10, pady=5)
ttk.Button(cart_btn_frame, text="↑ Increase", command=lambda: change_cart_qty(1)).pack(side="left", padx=5)
ttk.Button(cart_btn_frame, text="↓ Decrease", command=lambda: change_cart_qty(-1)).pack(side="left", padx=5)
ttk.Button(cart_btn_frame, text="Remove", command=lambda: remove_item()).pack(side="left", padx=5)

# Bottom Frame
bottom_frame = tk.Frame(root, bg="#edf2ff")
bottom_frame.pack(fill="both", expand=True, padx=10, pady=8)

boxes_frame = tk.Frame(bottom_frame, bg="#edf2ff")

# ================== BOXES ==================
box1 = tk.LabelFrame(boxes_frame, text="Box 1", bg="#35b52c", padx=8, pady=8, width=180, height=130, font=("Segoe UI", 10, "bold"))
box1.pack(side="left", padx=5, pady=5)
box1.pack_propagate(False)
box1_label = tk.Label(box1, text="", bg="#c8f7c5", font=("Segoe UI", 10))
box1_label.pack(expand=True)

box2 = tk.LabelFrame(boxes_frame, text="Box 2", bg="#dd3434", padx=8, pady=8, width=180, height=130, font=("Segoe UI", 10, "bold"))
box2.pack(side="left", padx=5, pady=5)
box2.pack_propagate(False)
box2_label = tk.Label(box2, text="", bg="#c7ddff", font=("Segoe UI", 10))
box2_label.pack(expand=True)

box3 = tk.LabelFrame(boxes_frame, text="Box 3", bg="#0051ca", padx=8, pady=8, width=180, height=130, font=("Segoe UI", 10, "bold"))
box3.pack(side="left", padx=5, pady=5)
box3.pack_propagate(False)
box3_label = tk.Label(box3, text="", bg="#ffb3b3", font=("Segoe UI", 10))
box3_label.pack(expand=True)

box4 = tk.LabelFrame(boxes_frame, text="Box 4", bg="#0EBDF0", padx=8, pady=8, width=180, height=130, font=("Segoe UI", 10, "bold"))
box4.pack(side="left", padx=5, pady=5)
box4.pack_propagate(False)
box4_label = tk.Label(box4, text="", bg="#0047ab", fg="white", font=("Segoe UI", 10, "bold"))
box4_label.pack(expand=True)

# Summary Frame
total_frame = tk.LabelFrame(bottom_frame, text="Bill Summary", padx=12, pady=10, font=("Segoe UI", 10, "bold"))
total_frame.pack(side="left", padx=10, fill="y")

tk.Label(total_frame, text="Total MRP:").grid(row=0, column=0, sticky="w")
label_total_mrp_val = tk.Label(total_frame, text="0.00", font=("Segoe UI", 10, "bold"))
label_total_mrp_val.grid(row=0, column=1, sticky="e")

tk.Label(total_frame, text="Total GST:").grid(row=1, column=0, sticky="w")
label_total_gst_val = tk.Label(total_frame, text="0.00", font=("Segoe UI", 10, "bold"))
label_total_gst_val.grid(row=1, column=1, sticky="e")

tk.Label(total_frame, text="Total Discount:").grid(row=2, column=0, sticky="w")
label_total_discount_val = tk.Label(total_frame, text="0.00", font=("Segoe UI", 10, "bold"))
label_total_discount_val.grid(row=2, column=1, sticky="e")

tk.Label(total_frame, text="Grand Total:", font=("Segoe UI", 11, "bold")).grid(row=3, column=0, sticky="w", pady=(8,0))
label_grand_total_val = tk.Label(total_frame, text="0.00", font=("Segoe UI", 11, "bold"))
label_grand_total_val.grid(row=3, column=1, sticky="e", pady=(8,0))

selected_box_label = tk.Label(total_frame, text="Selected Box: -", font=("Segoe UI", 9))
selected_box_label.grid(row=4, column=0, columnspan=2, pady=8)

ttk.Button(total_frame, text="Generate PDF Bill", command=lambda: generate_pdf()).grid(row=5, column=0, columnspan=2, pady=10)

# ---------------- FUNCTIONS ---------------- #
def show_boxes_if_needed():
    global boxes_visible
    if not boxes_visible:
        boxes_frame.pack(side="left", fill="both", expand=True, padx=5, pady=4)
        boxes_visible = True

def highlight_box(med_type: str, med_name: str):
    show_boxes_if_needed()
    box_num = get_box_number(med_type)

    for b, lbl in [(box1, box1_label), (box2, box2_label), (box3, box3_label), (box4, box4_label)]:
        b.config(bd=1, relief="ridge")
        lbl.config(text="")

    if box_num == 1:
        box1.config(bd=4, relief="solid"); box1_label.config(text=med_name)
    elif box_num == 2:
        box2.config(bd=4, relief="solid"); box2_label.config(text=med_name)
    elif box_num == 3:
        box3.config(bd=4, relief="solid"); box3_label.config(text=med_name)
    elif box_num == 4:
        box4.config(bd=4, relief="solid"); box4_label.config(text=med_name)

    selected_box_label.config(text=f"Selected Box: {box_num} – {med_name}")

def update_table(filter_text=""):
    for row in tree_search.get_children():
        tree_search.delete(row)
    if not filter_text.strip():
        return
    ft = filter_text.lower().strip()
    for med in all_medicines:
        if ft in med.get("medicine_name","").lower() or ft in med.get("type","").lower() or ft in med.get("alternate_medicine","").lower():
            tree_search.insert("", "end", values=(
                med.get("medicine_name",""), med.get("alternate_medicine",""), med.get("strength",""),
                med.get("manufacturer",""), med.get("type",""), med.get("sale_rate",""),
                med.get("discount",""), med.get("tax","")
            ))

def add_to_cart():
    # ... (same as before)
    selected = tree_search.focus()
    if not selected:
        messagebox.showwarning("No selection", "Please select a medicine first.")
        return
    values = tree_search.item(selected, "values")
    if not values:
        return

    try:
        qty = int(qty_var.get().strip() or 1)
        if qty <= 0: raise ValueError
    except:
        messagebox.showerror("Error", "Invalid Quantity")
        return

    cart_item = {
        "medicine_name": values[0],
        "type": values[4],
        "qty": qty,
        "unit_rate": to_float(values[5]),
        "discount_pct": to_float(values[6]),
        "tax_pct": to_float(values[7]),
    }
    recompute_cart_item(cart_item)
    cart_items.append(cart_item)
    refresh_cart_table()
    recalc_totals()

def recompute_cart_item(item):
    # same logic as before
    qty = item["qty"]
    unit_rate = item["unit_rate"]
    disc_pct = item["discount_pct"]
    tax_pct = item["tax_pct"]
    mrp_total = unit_rate * qty
    discount_amount = mrp_total * (disc_pct / 100)
    after_disc = mrp_total - discount_amount
    gst_amount = after_disc * (tax_pct / 100)
    final_total = after_disc + gst_amount

    item.update({"mrp_total": mrp_total, "discount_amount": discount_amount,
                 "gst_amount": gst_amount, "final_total": final_total})

def refresh_cart_table():
    for row in tree_cart.get_children():
        tree_cart.delete(row)
    for i, item in enumerate(cart_items):
        tree_cart.insert("", "end", iid=str(i), values=(
            item["medicine_name"], item["qty"], f"{item['mrp_total']:.2f}",
            f"{item['gst_amount']:.2f}", f"{item['discount_amount']:.2f}", f"{item['final_total']:.2f}"
        ))

def recalc_totals():
    totals["mrp"] = sum(i["mrp_total"] for i in cart_items)
    totals["discount"] = sum(i["discount_amount"] for i in cart_items)
    totals["gst"] = sum(i["gst_amount"] for i in cart_items)
    totals["grand"] = sum(i["final_total"] for i in cart_items)

    label_total_mrp_val.config(text=f"{totals['mrp']:.2f}")
    label_total_gst_val.config(text=f"{totals['gst']:.2f}")
    label_total_discount_val.config(text=f"{totals['discount']:.2f}")
    label_grand_total_val.config(text=f"{totals['grand']:.2f}")

def change_cart_qty(delta):
    sel = tree_cart.focus()
    if not sel: 
        messagebox.showwarning("No selection", "Select an item first")
        return
    idx = int(sel)
    if idx >= len(cart_items): return
    item = cart_items[idx]
    new_qty = item["qty"] + delta
    if new_qty <= 0:
        if messagebox.askyesno("Remove", "Remove item?"):
            del cart_items[idx]
    else:
        item["qty"] = new_qty
        recompute_cart_item(item)
    refresh_cart_table()
    recalc_totals()

def remove_item():
    sel = tree_cart.focus()
    if not sel: return
    if messagebox.askyesno("Remove", "Remove this item?"):
        del cart_items[int(sel)]
        refresh_cart_table()
        recalc_totals()

def dispense_selected():
    if not cart_items:
        messagebox.showwarning("Empty Cart", "Cart is empty")
        return
    med = cart_items[-1]
    cmd = str(get_box_number(med["type"]))

    if arduino:
        try:
            arduino.write((cmd + "\n").encode('utf-8'))
            arduino.flush()
            print(f"Sent: {cmd}")
        except Exception as e:
            messagebox.showerror("Serial Error", str(e))
    else:
        messagebox.showinfo("Demo Mode", "Arduino not connected (Demo)")

    highlight_box(med["type"], med["medicine_name"])
    messagebox.showinfo("Dispensed", f"Command '{cmd}' sent to Box {cmd}\n{med['medicine_name']}")

def generate_pdf():
    if not cart_items:
        messagebox.showwarning("Empty Cart", "Cart is empty. Cannot create bill.")
        return

    # Create Bills folder inside current directory
    bills_dir = Path(__file__).resolve().parent / "Bills"
    bills_dir.mkdir(exist_ok=True)   # Create folder if not exists

    now = datetime.now()
    filename = f"bill_{now.strftime('%Y%m%d_%H%M%S')}.pdf"
    filepath = bills_dir / filename

    try:
        c = canvas.Canvas(str(filepath), pagesize=A4)
        width, height = A4
        y = height - 40

        # Shop Header
        c.setFont("Helvetica-Bold", 18)
        c.drawString(40, y, SHOP_NAME)
        y -= 20

        c.setFont("Helvetica", 10)
        c.drawString(40, y, SHOP_ADDRESS_LINE1)
        y -= 12
        c.drawString(40, y, SHOP_ADDRESS_LINE2)
        y -= 12
        c.drawString(40, y, f"Phone: {SHOP_PHONE}")
        y -= 12
        c.drawString(40, y, f"GSTIN: {SHOP_GSTIN}")
        y -= 25

        # Invoice Info
        c.setFont("Helvetica-Bold", 12)
        c.drawString(40, y, "TAX INVOICE")
        c.setFont("Helvetica", 10)
        c.drawRightString(width - 40, y, f"Invoice No: {now.strftime('%Y%m%d%H%M')}")
        y -= 15
        c.drawRightString(width - 40, y, f"Date: {now.strftime('%d-%m-%Y %H:%M')}")
        y -= 25

        # Table Header
        c.setFont("Helvetica-Bold", 10)
        headers = ["Sr", "Medicine", "Qty", "MRP", "Disc%", "GST%", "Amount"]
        positions = [40, 80, 220, 280, 340, 390, 480]
        for i, text in enumerate(headers):
            c.drawString(positions[i], y, text)
        y -= 15

        # Items
        c.setFont("Helvetica", 9)
        sr = 1
        for item in cart_items:
            if y < 100:
                c.showPage()
                y = height - 60
            c.drawString(positions[0], y, str(sr))
            c.drawString(positions[1], y, item["medicine_name"][:28])
            c.drawRightString(positions[2]+20, y, str(item["qty"]))
            c.drawRightString(positions[3]+20, y, f"{item['unit_rate']:.2f}")
            c.drawRightString(positions[4]+20, y, f"{item['discount_pct']:.1f}")
            c.drawRightString(positions[5]+20, y, f"{item['tax_pct']:.1f}")
            c.drawRightString(positions[6]+20, y, f"{item['final_total']:.2f}")
            y -= 15
            sr += 1

        # Totals
        y -= 10
        c.setFont("Helvetica-Bold", 11)
        c.drawRightString(positions[6]+20, y, f"Grand Total: \u20b9{totals['grand']:.2f}")
        y -= 20
        c.setFont("Helvetica", 10)
        c.drawString(40, y, "Thank you for shopping with MediCare Pharmacy!")

        c.save()

        messagebox.showinfo(
            "PDF Saved",
            f"Bill successfully saved!\n\nLocation:\n{bills_dir}\n\nFile: {filename}"
        )

    except Exception as e:
        messagebox.showerror("PDF Error", f"Failed to generate PDF:\n{e}")

# Start the app
root.mainloop()