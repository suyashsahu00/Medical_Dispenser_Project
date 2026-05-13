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

ARDUINO_PORT = "COM4"     # change if your Arduino uses another port COM3 example
BAUD_RATE = 9600
# Use script-relative path for medicines.csv so the file is found
# even when the script is launched from a different CWD.
MEDICINE_FILE = Path(__file__).resolve().parent / "medicines.csv"
print(f"Looking for medicines.csv at: {MEDICINE_FILE}")

SHOP_NAME = "MediCare Pharmacy"
SHOP_ADDRESS_LINE1 = "13 Health Street"
SHOP_ADDRESS_LINE2 = "Mumbai, Maharashtra, India"
SHOP_PHONE = "+91-9345678991"
SHOP_GSTIN = "27AAAAA0000A1Z5"   # Placeholder GSTIN for project demo


# ---------------- ARDUINO ---------------- #

try:
    arduino = serial.Serial(ARDUINO_PORT, BAUD_RATE)
    time.sleep(2)
    print(f"Arduino connected on {ARDUINO_PORT}")
except Exception as e:
    arduino = None
    print("⚠ Arduino not connected:", e)


# ---------------- DATA LOADING ---------------- #

def load_medicines():
    medicines = []
    try:
        with open(MEDICINE_FILE, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            # Guard against missing/None fieldnames
            fieldnames = reader.fieldnames or []
            reader.fieldnames = [h.strip() for h in fieldnames]

            for row in reader:
                clean_row = {
                    k.strip(): (v.strip() if isinstance(v, str) else v)
                    for k, v in row.items()
                }
                medicines.append(clean_row)
    except FileNotFoundError as e:
        print(f"⚠ medicines.csv not found at {MEDICINE_FILE}: {e}")
    return medicines


all_medicines = load_medicines()


def to_float(val: str, default: float = 0.0) -> float:
    try:
        val = val.strip()
        if not val:
            return default
        return float(val)
    except Exception:
        return default


# ---------------- CART STATE ---------------- #

cart_items = []
totals = {"mrp": 0.0, "discount": 0.0, "gst": 0.0, "grand": 0.0}


# ---------------- SEARCH TABLE ---------------- #

def update_table(filter_text: str = ""):
    """Fill search table based on search text (name, type, alternate)."""
    for row in tree_search.get_children():
        tree_search.delete(row)

    ft = filter_text.lower().strip()
    if ft == "":
        return

    for med in all_medicines:
        name = med.get("medicine_name", "").lower()
        mtype = med.get("type", "").lower()
        alt = med.get("alternate_medicine", "").lower()

        if ft in name or ft in mtype or ft in alt:
            tree_search.insert(
                "",
                "end",
                values=(
                    med.get("medicine_name", ""),
                    med.get("alternate_medicine", ""),
                    med.get("strength", ""),
                    med.get("manufacturer", ""),
                    med.get("type", ""),
                    med.get("sale_rate", ""),
                    med.get("discount", ""),
                    med.get("tax", ""),
                ),
            )


def on_search_key(event):
    text = search_var.get().strip()
    if text == "":
        for row in tree_search.get_children():
            tree_search.delete(row)
    else:
        update_table(text)


def get_selected_medicine():
    selected = tree_search.focus()
    if not selected:
        return None
    values = tree_search.item(selected, "values")
    if not values:
        return None

    med = {
        "medicine_name": values[0],
        "alternate_medicine": values[1],
        "strength": values[2],
        "manufacturer": values[3],
        "type": values[4],
        "sale_rate": values[5],
        "discount": values[6],
        "tax": values[7],
    }
    return med


# ---------------- BOX HIGHLIGHT (4 servos) ---------------- #

boxes_visible = False  # control initial visibility


def show_boxes_if_needed():
    """Show all four boxes only after first dispense."""
    global boxes_visible
    if not boxes_visible:
        boxes_frame.pack(side="left", fill="both", expand=True, padx=5, pady=4)
        boxes_visible = True


def highlight_box(med_type: str, med_name: str):
    """Highlight the correct box and show medicine name."""
    show_boxes_if_needed()

    # reset borders and text
    for box, label in (
        (box1, box1_label),
        (box2, box2_label),
        (box3, box3_label),
        (box4, box4_label),
    ):
        box.config(bd=1, relief="ridge")
        label.config(text="")

    mt = med_type.lower()

    if mt in ("painkiller", "box1"):
        box1.config(bd=4, relief="solid")
        box1_label.config(text=med_name)
        selected_box_label.config(text=f"Selected Box: 1 – {med_name}")
    elif mt in ("paracetamol", "box2", "dolo"):
        box2.config(bd=4, relief="solid")
        box2_label.config(text=med_name)
        selected_box_label.config(text=f"Selected Box: 2 – {med_name}")
    elif mt == "box3":
        box3.config(bd=4, relief="solid")
        box3_label.config(text=med_name)
        selected_box_label.config(text=f"Selected Box: 3 – {med_name}")
    elif mt == "box4":
        box4.config(bd=4, relief="solid")
        box4_label.config(text=med_name)
        selected_box_label.config(text=f"Selected Box: 4 – {med_name}")
    else:
        selected_box_label.config(text="Selected Box: -")


# ---------------- CART CALCULATIONS ---------------- #

def recompute_cart_item(item):
    qty = item["qty"]
    unit_rate = item["unit_rate"]
    disc_pct = item["discount_pct"]
    tax_pct = item["tax_pct"]

    mrp_total = unit_rate * qty
    discount_amount = mrp_total * (disc_pct / 100.0)
    after_discount = mrp_total - discount_amount
    gst_amount = after_discount * (tax_pct / 100.0)
    final_total = after_discount + gst_amount

    item["mrp_total"] = mrp_total
    item["discount_amount"] = discount_amount
    item["gst_amount"] = gst_amount
    item["final_total"] = final_total


def recalc_totals():
    totals["mrp"] = sum(item["mrp_total"] for item in cart_items)
    totals["discount"] = sum(item["discount_amount"] for item in cart_items)
    totals["gst"] = sum(item["gst_amount"] for item in cart_items)
    totals["grand"] = sum(item["final_total"] for item in cart_items)

    label_total_mrp_val.config(text=f"{totals['mrp']:.2f}")
    label_total_gst_val.config(text=f"{totals['gst']:.2f}")
    label_total_discount_val.config(text=f"{totals['discount']:.2f}")
    label_grand_total_val.config(text=f"{totals['grand']:.2f}")


def refresh_cart_table():
    for row in tree_cart.get_children():
        tree_cart.delete(row)

    for idx, item in enumerate(cart_items):
        tree_cart.insert(
            "",
            "end",
            iid=str(idx),
            values=(
                item["medicine_name"],
                item["qty"],
                f"{item['mrp_total']:.2f}",
                f"{item['gst_amount']:.2f}",
                f"{item['discount_amount']:.2f}",
                f"{item['final_total']:.2f}",
            ),
        )


def add_to_cart():
    med = get_selected_medicine()
    if not med:
        messagebox.showwarning("No selection", "Please select a medicine first.")
        return

    qty_str = qty_var.get().strip()
    if not qty_str:
        qty = 1
    else:
        try:
            qty = int(qty_str)
            if qty <= 0:
                raise ValueError()
        except ValueError:
            messagebox.showerror("Quantity Error", "Quantity must be a positive number.")
            return

    med_type = med["type"].lower()
    allowed_types = ("painkiller", "paracetamol", "box1", "box2", "box3", "box4")
    if med_type not in allowed_types:
        med_type = "box1"  # default servo group

    sale_rate = to_float(med["sale_rate"], 0.0)
    discount_pct = to_float(med["discount"], 0.0)
    tax_pct = to_float(med["tax"], 0.0)

    cart_item = {
        "medicine_name": med["medicine_name"],
        "type": med_type,
        "qty": qty,
        "unit_rate": sale_rate,
        "discount_pct": discount_pct,
        "tax_pct": tax_pct,
    }
    recompute_cart_item(cart_item)
    cart_items.append(cart_item)

    refresh_cart_table()
    recalc_totals()


def get_selected_cart_index():
    sel = tree_cart.focus()
    if not sel:
        return None
    try:
        return int(sel)
    except ValueError:
        return None


def change_cart_qty(delta: int):
    idx = get_selected_cart_index()
    if idx is None or idx >= len(cart_items):
        messagebox.showwarning("No selection", "Please select an item in the cart.")
        return

    item = cart_items[idx]
    new_qty = item["qty"] + delta

    if new_qty <= 0:
        if messagebox.askyesno(
            "Remove Item", "Quantity will become zero. Remove this item from cart?"
        ):
            del cart_items[idx]
        else:
            return
    else:
        item["qty"] = new_qty
        recompute_cart_item(item)

    refresh_cart_table()
    recalc_totals()


def increase_qty():
    change_cart_qty(+1)


def decrease_qty():
    change_cart_qty(-1)


def remove_item():
    idx = get_selected_cart_index()
    if idx is None or idx >= len(cart_items):
        messagebox.showwarning("No selection", "Please select an item in the cart.")
        return

    if messagebox.askyesno("Remove Item", "Remove this item from the cart?"):
        del cart_items[idx]
        refresh_cart_table()
        recalc_totals()


# ---------------- DISPENSE (ARDUINO) ---------------- #

def dispense_selected():
    if not cart_items:
        messagebox.showwarning("Empty Cart", "Cart is empty. Add some items first.")
        return

    med = cart_items[-1]  # last added
    med_type = med["type"]

    if not arduino:
        messagebox.showerror("Arduino Error", "Arduino is not connected.")
        return

    cmd = med_type  # "painkiller"/"paracetamol"/"box1".."box4"

    try:
        arduino.write((cmd + "\n").encode())
        highlight_box(med_type, med["medicine_name"])
        messagebox.showinfo(
            "Dispensed",
            f"{med['medicine_name']} (qty {med['qty']}) command '{cmd}' sent to Arduino.",
        )
    except Exception as e:
        messagebox.showerror("Serial Error", f"Failed to send command:\n{e}")


# ---------------- PDF INVOICE ---------------- #

def generate_pdf():
    if not cart_items:
        messagebox.showwarning("Empty Cart", "Cart is empty. Cannot create bill.")
        return

    now = datetime.now()
    filename = f"bill_{now.strftime('%Y%m%d_%H%M%S')}.pdf"

    c = canvas.Canvas(filename, pagesize=A4)
    width, height = A4
    y = height - 40

    # Shop header
    c.setFont("Helvetica-Bold", 18)
    c.drawString(40, y, SHOP_NAME)
    y -= 18

    c.setFont("Helvetica", 10)
    c.drawString(40, y, SHOP_ADDRESS_LINE1)
    y -= 12
    c.drawString(40, y, SHOP_ADDRESS_LINE2)
    y -= 12
    c.drawString(40, y, f"Phone: {SHOP_PHONE}")
    y -= 12
    c.drawString(40, y, f"GSTIN: {SHOP_GSTIN}")
    y -= 20

    # Invoice meta
    invoice_no = now.strftime("%Y%m%d%H%M")
    c.setFont("Helvetica-Bold", 11)
    c.drawString(40, y, "TAX INVOICE")
    c.setFont("Helvetica", 9)
    c.drawRightString(width - 40, y, f"Invoice No: {invoice_no}")
    y -= 14
    c.drawRightString(width - 40, y, f"Invoice Date: {now.strftime('%d-%m-%Y')}")
    y -= 18

    # Table header
    c.setFont("Helvetica-Bold", 9)
    c.drawString(30, y, "Sr")
    c.drawString(55, y, "Medicine")
    c.drawString(220, y, "Qty")
    c.drawString(255, y, "MRP")
    c.drawString(305, y, "Disc%")
    c.drawString(350, y, "GST%")
    c.drawString(400, y, "GST Amt")
    c.drawString(460, y, "Disc Amt")
    c.drawString(520, y, "Amount")
    y -= 12

    c.setFont("Helvetica", 9)
    sr_no = 1
    for item in cart_items:
        if y < 90:
            c.showPage()
            y = height - 60
            c.setFont("Helvetica-Bold", 9)
            c.drawString(30, y, "Sr")
            c.drawString(55, y, "Medicine")
            c.drawString(220, y, "Qty")
            c.drawString(255, y, "MRP")
            c.drawString(305, y, "Disc%")
            c.drawString(350, y, "GST%")
            c.drawString(400, y, "GST Amt")
            c.drawString(460, y, "Disc Amt")
            c.drawString(520, y, "Amount")
            y -= 12
            c.setFont("Helvetica", 9)

        c.drawString(30, y, str(sr_no))
        c.drawString(55, y, item["medicine_name"][:25])
        c.drawRightString(245, y, str(item["qty"]))
        c.drawRightString(295, y, f"{item['unit_rate']:.2f}")
        c.drawRightString(340, y, f"{item['discount_pct']:.1f}")
        c.drawRightString(385, y, f"{item['tax_pct']:.1f}")
        c.drawRightString(445, y, f"{item['gst_amount']:.2f}")
        c.drawRightString(505, y, f"{item['discount_amount']:.2f}")
        c.drawRightString(570, y, f"{item['final_total']:.2f}")
        y -= 12
        sr_no += 1

    # Totals
    y -= 10
    c.setFont("Helvetica-Bold", 10)
    c.drawRightString(445, y, f"{totals['gst']:.2f}")
    c.drawRightString(505, y, f"{totals['discount']:.2f}")
    c.drawRightString(570, y, f"{totals['grand']:.2f}")
    y -= 18

    c.drawRightString(570, y, f"Total MRP: {totals['mrp']:.2f}")
    y -= 14
    c.drawRightString(570, y, f"Total GST: {totals['gst']:.2f}")
    y -= 14
    c.drawRightString(570, y, f"Total Discount: {totals['discount']:.2f}")
    y -= 14
    c.drawRightString(570, y, f"Grand Total: {totals['grand']:.2f}")
    y -= 25

    c.setFont("Helvetica", 9)
    c.drawString(40, y, "Thank you for your purchase.")
    c.drawRightString(width - 40, y, "Authorised Signatory")
    c.save()

    messagebox.showinfo(
        "PDF Created",
        f"Bill saved as {filename} in the current folder.",
    )


# ---------------- UI SETUP ---------------- #

root = tk.Tk()
root.title("Medical Billing & Servo Dispenser")
root.geometry("1150x720")
root.configure(bg="#edf2ff")

# ttk styling
style = ttk.Style()
style.theme_use("clam")
style.configure("TButton", font=("Segoe UI", 10), padding=6)
style.configure("TLabel", font=("Segoe UI", 10))
style.configure("Treeview.Heading", font=("Segoe UI", 10, "bold"))
style.configure("Treeview", rowheight=22)

# Top title bar
title_frame = tk.Frame(root, bg="#4c6fff")
title_frame.pack(fill="x")
tk.Label(
    title_frame,
    text="Medical Billing & Automatic Servo Dispenser",
    bg="#4c6fff",
    fg="white",
    font=("Segoe UI", 14, "bold"),
    pady=6,
).pack()

# Search row
search_frame = tk.Frame(root, bg="#edf2ff")
search_frame.pack(fill="x", padx=10, pady=8)

tk.Label(
    search_frame, text="Search Medicine Name:", font=("Segoe UI", 11, "bold"), bg="#edf2ff"
).pack(side="left")

search_var = tk.StringVar()
search_entry = ttk.Entry(
    search_frame, textvariable=search_var, font=("Segoe UI", 11), width=32
)
search_entry.pack(side="left", padx=10)
search_entry.bind("<KeyRelease>", on_search_key)

tk.Label(search_frame, text="Qty:", font=("Segoe UI", 11), bg="#edf2ff").pack(
    side="left", padx=(20, 5)
)
qty_var = tk.StringVar(value="1")
qty_entry = ttk.Entry(
    search_frame, textvariable=qty_var, font=("Segoe UI", 11), width=6
)
qty_entry.pack(side="left")

ttk.Button(search_frame, text="Add to Cart", command=add_to_cart).pack(
    side="left", padx=10
)
ttk.Button(
    search_frame, text="Dispense (Last Cart Item)", command=dispense_selected
).pack(side="left", padx=6)

# Search results table
columns_search = (
    "name",
    "alt",
    "strength",
    "manufacturer",
    "type",
    "sale",
    "disc",
    "tax",
)
tree_search = ttk.Treeview(root, columns=columns_search, show="headings", height=8)

search_cols = [
    ("name", "Medicine Name", 230, "w"),
    ("alt", "Alternate", 220, "w"),
    ("strength", "Strength", 80, "center"),
    ("manufacturer", "Manufacturer", 150, "w"),
    ("type", "Type", 90, "center"),
    ("sale", "Sale Rate", 80, "center"),
    ("disc", "Disc %", 70, "center"),
    ("tax", "GST %", 70, "center"),
]

for col, text, width, anchor in search_cols:
    tree_search.heading(col, text=text)
    tree_search.column(col, width=width, anchor=anchor)

tree_search.pack(fill="x", padx=10, pady=5)

# Cart table
cart_label = tk.Label(
    root, text="Cart", font=("Segoe UI", 12, "bold"), bg="#edf2ff"
)
cart_label.pack(anchor="w", padx=10, pady=(8, 0))

columns_cart = ("c_name", "c_qty", "c_mrp", "c_gst", "c_disc", "c_total")
tree_cart = ttk.Treeview(root, columns=columns_cart, show="headings", height=7)

cart_cols = [
    ("c_name", "Medicine", 280),
    ("c_qty", "Qty", 60),
    ("c_mrp", "MRP Total", 90),
    ("c_gst", "GST Amt", 90),
    ("c_disc", "Discount Amt", 100),
    ("c_total", "Final Total", 100),
]

for col, text, width in cart_cols:
    tree_cart.heading(col, text=text)
    tree_cart.column(col, width=width, anchor="center" if col != "c_name" else "w")

tree_cart.pack(fill="x", padx=10, pady=5)

cart_btn_frame = tk.Frame(root, bg="#edf2ff")
cart_btn_frame.pack(fill="x", padx=10, pady=(0, 6))

ttk.Button(cart_btn_frame, text="Increase Qty", command=increase_qty).pack(
    side="left"
)
ttk.Button(cart_btn_frame, text="Decrease Qty", command=decrease_qty).pack(
    side="left", padx=5
)
ttk.Button(cart_btn_frame, text="Remove Item", command=remove_item).pack(
    side="left", padx=5
)

# Bottom section: boxes + summary
bottom_frame = tk.Frame(root, bg="#edf2ff")
bottom_frame.pack(fill="both", expand=True, padx=10, pady=8)

# frame that will hold 4 boxes (hidden initially)
boxes_frame = tk.Frame(bottom_frame, bg="#edf2ff")

box1 = tk.LabelFrame(
    boxes_frame,
    text="Box 1",
    bg="#35b52c",
    padx=8,
    pady=8,
    font=("Segoe UI", 10, "bold"),
    width=180,
    height=120,
)
box1.pack(side="left", padx=4, pady=4)
box1.pack_propagate(False)
box1_label = tk.Label(box1, text="", bg="#c8f7c5", font=("Segoe UI", 10))
box1_label.pack(expand=True)

box2 = tk.LabelFrame(
    boxes_frame,
    text="Box 2",
    # bg="#c7ddff",
    bg="#dd3434",
    padx=8,
    pady=8,
    font=("Segoe UI", 10, "bold"),
    width=180,
    height=120,
)
box2.pack(side="left", padx=4, pady=4)
box2.pack_propagate(False)
box2_label = tk.Label(box2, text="", bg="#c7ddff", font=("Segoe UI", 10))
box2_label.pack(expand=True)

box3 = tk.LabelFrame(
    boxes_frame,
    text="Box 3",
    bg="#0051ca",  # Light Red background
    padx=8,
    pady=8,
    font=("Segoe UI", 10, "bold"),
    width=180,
    height=120,
)
box3.pack(side="left", padx=4, pady=4)
box3.pack_propagate(False)
box3_label = tk.Label(box3, text="", bg="#ffb3b3", font=("Segoe UI", 10))
box3_label.pack(expand=True)


box4 = tk.LabelFrame(
    boxes_frame,
    text="Box 4",
    bg="#0EBDF0",  # Dark Blue background
    padx=8,
    pady=8,
    font=("Segoe UI", 10, "bold"),
    width=180,
    height=120,
)
box4.pack(side="left", padx=4, pady=4)
box4.pack_propagate(False)
box4_label = tk.Label(box4, text="", bg="#0047ab", font=("Segoe UI", 10, "bold"), fg="white")
box4_label.pack(expand=True)


# Summary frame (always visible)
total_frame = tk.LabelFrame(
    bottom_frame, text="Bill Summary", padx=12, pady=10, font=("Segoe UI", 10, "bold")
)
total_frame.pack(side="left", padx=5, fill="y")

tk.Label(total_frame, text="Total MRP:", font=("Segoe UI", 10)).grid(
    row=0, column=0, sticky="w"
)
label_total_mrp_val = tk.Label(
    total_frame, text="0.00", font=("Segoe UI", 10, "bold")
)
label_total_mrp_val.grid(row=0, column=1, sticky="e")

tk.Label(total_frame, text="Total GST:", font=("Segoe UI", 10)).grid(
    row=1, column=0, sticky="w"
)
label_total_gst_val = tk.Label(
    total_frame, text="0.00", font=("Segoe UI", 10, "bold")
)
label_total_gst_val.grid(row=1, column=1, sticky="e")

tk.Label(total_frame, text="Total Discount:", font=("Segoe UI", 10)).grid(
    row=2, column=0, sticky="w"
)
label_total_discount_val = tk.Label(
    total_frame, text="0.00", font=("Segoe UI", 10, "bold")
)
label_total_discount_val.grid(row=2, column=1, sticky="e")

tk.Label(total_frame, text="Grand Total:", font=("Segoe UI", 11, "bold")).grid(
    row=3, column=0, sticky="w", pady=(5, 0)
)
label_grand_total_val = tk.Label(
    total_frame, text="0.00", font=("Segoe UI", 11, "bold")
)
label_grand_total_val.grid(row=3, column=1, sticky="e", pady=(5, 0))

selected_box_label = tk.Label(
    total_frame, text="Selected Box: -", font=("Segoe UI", 9)
)
selected_box_label.grid(row=4, column=0, columnspan=2, pady=(6, 0))

ttk.Button(
    total_frame,
    text="Generate PDF Bill",
    command=generate_pdf,
).grid(row=5, column=0, columnspan=2, pady=(10, 0))

root.mainloop()
