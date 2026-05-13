<div align="center">

# 💊 Medical Billing & Automatic Servo Dispenser

### A Python + Arduino integrated system for smart pharmacy billing and automated medicine dispensing

[![Python](https://img.shields.io/badge/Python-3.8%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Arduino](https://img.shields.io/badge/Arduino-UNO-00979D?style=for-the-badge&logo=arduino&logoColor=white)](https://www.arduino.cc/)
[![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Active-brightgreen?style=for-the-badge)]()
[![Platform](https://img.shields.io/badge/Platform-Windows-0078D6?style=for-the-badge&logo=windows&logoColor=white)](https://www.microsoft.com/windows)
[![Hardware](https://img.shields.io/badge/Hardware-Servo%20Motors-orange?style=for-the-badge)]()

<br/>

> 🏥 **An intelligent pharmacy management system** that seamlessly combines a Python desktop billing application with an Arduino-controlled servo mechanism to automatically dispense medicines from the correct storage box — all while generating a professional PDF invoice.

<br/>

[🚀 Get Started](#-installation--setup) · [📖 Documentation](#-how-it-works) · [🐛 Report Bug](https://github.com/suyashsahu00/Medical_Dispenser_Project/issues) · [✨ Request Feature](https://github.com/suyashsahu00/Medical_Dispenser_Project/issues)

</div>

---

## 📚 Table of Contents

- [✨ Features](#-features)
- [🏗️ System Architecture](#️-system-architecture)
- [📁 Project Structure](#-project-structure)
- [⚙️ Hardware Requirements](#️-hardware-requirements)
- [🛠️ Installation &amp; Setup](#️-installation--setup)
  - [1. Clone the Repository](#1-clone-the-repository)
  - [2. Set Up Python Environment](#2-set-up-python-environment)
  - [3. Upload Arduino Firmware](#3-upload-arduino-firmware)
  - [4. Wiring the Hardware](#4-wiring-the-hardware)
- [▶️ Running the Project](#️-running-the-project)
- [📖 How It Works](#-how-it-works)
- [🧪 Usage Examples](#-usage-examples)
- [🗂️ Medicine Database](#️-medicine-database)
- [🤝 Contributing](#-contributing)
- [📄 License](#-license)
- [🙏 Credits &amp; Acknowledgments](#-credits--acknowledgments)

---

## ✨ Features

| Feature                            | Description                                                               |
| ---------------------------------- | ------------------------------------------------------------------------- |
| 🔍**Live Medicine Search**   | Real-time search through the medicine database as you type                |
| 🛒**Shopping Cart System**   | Add, remove, increase/decrease quantities before billing                  |
| 🤖**Automatic Dispensing**   | Arduino-controlled servo motors dispense from the right box automatically |
| 💡**LED Indicators**         | Visual LED feedback for each activated dispenser box                      |
| 📦**4-Box Management**       | Manages 4 independent medicine storage boxes with dedicated servos        |
| 🧾**PDF Invoice Generation** | Auto-generates professional tax invoices with GST breakdown               |
| 💰**Billing Calculations**   | Automatic computation of MRP, GST, discounts, and grand total             |
| 🔌**Demo Mode**              | Works without Arduino connected — useful for testing/offline use         |
| 📊**CSV-Based Database**     | Easy-to-edit medicine inventory using a standard `.csv` file            |
| 🖥️**Desktop GUI**          | Clean, user-friendly Tkinter-based interface                              |

---

## 🏗️ System Architecture

```
┌──────────────────────────────────────────────────────────────────────┐
│                        USER INTERFACE (Python / Tkinter)             │
│                                                                      │
│   Search Box ──► Medicine Table ──► Cart ──► Bill Summary           │
│                                                │                     │
│                                       [ Generate PDF Bill ]         │
│                                       [ Dispense Last Item ]        │
└─────────────────────────────┬────────────────────────────────────────┘
                              │
                   Serial Port (COM4) @ 115200 baud
                              │
                              ▼
┌──────────────────────────────────────────────────────────────────────┐
│                        ARDUINO UNO                                   │
│                                                                      │
│   Receives: '1' / '2' / '3' / '4'                                   │
│                                                                      │
│   ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐              │
│   │ SERVO 1 │  │ SERVO 2 │  │ SERVO 3 │  │ SERVO 4 │              │
│   │  Pin 5  │  │  Pin 6  │  │  Pin 9  │  │  Pin 10 │              │
│   │ + LED 4 │  │ + LED 7 │  │ + LED 8 │  │ + LED11 │              │
│   └─────────┘  └─────────┘  └─────────┘  └─────────┘              │
│      Box 1        Box 2        Box 3        Box 4                   │
└──────────────────────────────────────────────────────────────────────┘
```

**The flow is simple:**

1. Pharmacist searches for a medicine in the Python app
2. Selects it, sets quantity, and adds to cart
3. Clicks **"Dispense Last Item"** — the app sends a command (`1`–`4`) over serial
4. The Arduino receives the command and activates the matching servo + LED
5. The servo sweeps 0° → 180° → 0° to release the medicine from the box
6. Pharmacist clicks **"Generate PDF Bill"** to create the invoice

---

## 📁 Project Structure

```
Medical_Dispenser_Project/
│
├── 📄 README.md                        ← You are here!
│
└── 📂 PythonApp/
    │
    ├── 🐍 app_billing_two_boxes.py     ← Main application (run this!)
    │                                     Full billing GUI + Arduino serial
    │
    ├── 🐍 delete.py                    ← Older prototype (2-box version)
    │                                     Kept for reference
    │
    ├── ⚡ four_servos_medical.ino      ← Arduino firmware
    │                                     Controls 4 servos + 4 LEDs
    │
    ├── 📊 medicines.csv                ← Medicine database (edit freely!)
    │                                     24 medicines across 4 box types
    │
    ├── 📋 requirements.txt             ← Python dependencies
    │
    └── 📂 Bills/                       ← Auto-created folder for PDF invoices
            bill_YYYYMMDD_HHMMSS.pdf
```

### Key Files Explained

| File                         | Purpose                                                                                             |
| ---------------------------- | --------------------------------------------------------------------------------------------------- |
| `app_billing_two_boxes.py` | **Main entry point.** Full-featured GUI with 4-box support, cart, billing, and PDF generation |
| `four_servos_medical.ino`  | **Arduino firmware.** Listens for `'1'`–`'4'` over serial and drives corresponding servo |
| `medicines.csv`            | **Medicine inventory.** Add/edit medicines here — no code changes needed                     |
| `delete.py`                | Older 2-box prototype (legacy reference, not used in production)                                    |
| `requirements.txt`         | Contains `pyserial` and `reportlab`                                                             |

---

## ⚙️ Hardware Requirements

| Component                                         | Quantity | Notes                              |
| ------------------------------------------------- | -------- | ---------------------------------- |
| **Arduino UNO**                             | 1        | Any compatible board works         |
| **Servo Motor (SG90 or MG996R)**            | 4        | One per dispenser box              |
| **LED (any color)**                         | 4        | One per box as indicator           |
| **Resistors (220Ω)**                       | 4        | For current limiting on LEDs       |
| **Jumper Wires**                            | Several  | Male-to-male & male-to-female      |
| **Breadboard**                              | 1        | For prototyping connections        |
| **USB Type-B Cable**                        | 1        | Arduino ↔ PC connection           |
| **External 5V Power Supply** *(optional)* | 1        | Recommended if servos are sluggish |

---

## 🛠️ Installation & Setup

### Prerequisites

Make sure you have the following installed before starting:

- ✅ [Python 3.8+](https://www.python.org/downloads/)
- ✅ [Arduino IDE](https://www.arduino.cc/en/software)
- ✅ [Git](https://git-scm.com/downloads)

---

### 1. Clone the Repository

```bash
git clone https://github.com/suyashsahu00/Medical_Dispenser_Project.git
cd Medical_Dispenser_Project
```

---

### 2. Set Up Python Environment

It is **strongly recommended** to use a virtual environment to keep your dependencies isolated.

```bash
# Navigate to the Python app directory
cd PythonApp

# Create a virtual environment
python -m venv venv

# Activate it (Windows)
venv\Scripts\activate

# Activate it (macOS/Linux)
source venv/bin/activate

# Install all required packages
pip install -r requirements.txt
```

**What gets installed:**

| Package       | Version | Purpose                           |
| ------------- | ------- | --------------------------------- |
| `pyserial`  | Latest  | Serial communication with Arduino |
| `reportlab` | Latest  | Generating PDF invoices           |

> 💡 `tkinter` is included with Python by default — no extra installation needed!

---

### 3. Upload Arduino Firmware

1. Open **Arduino IDE**
2. Go to `File` → `Open` and select `PythonApp/four_servos_medical.ino`
3. Connect your Arduino UNO via USB
4. Select the correct **Board**: `Tools` → `Board` → `Arduino UNO`
5. Select the correct **Port**: `Tools` → `Port` → `COM4` *(or whatever your port is)*
6. Click **Upload** (→ button)
7. Open **Serial Monitor** (set to `115200 baud`) — you should see:
   ```
   Servo & LED Control Ready! Send 1,2,3 or 4
   ```

---

### 4. Wiring the Hardware

Wire your components as follows:

```
Arduino Pin  │  Component
─────────────┼───────────────────────────────
    5         │  Servo 1 (Signal) — Box 1
    6         │  Servo 2 (Signal) — Box 2
    9         │  Servo 3 (Signal) — Box 3
   10         │  Servo 4 (Signal) — Box 4
    4         │  LED 1 (via 220Ω resistor) — Box 1
    7         │  LED 2 (via 220Ω resistor) — Box 2
    8         │  LED 3 (via 220Ω resistor) — Box 3
   11         │  LED 4 (via 220Ω resistor) — Box 4
   5V         │  All servo VCC lines
  GND         │  All servo GND + LED GND
```

> ⚠️ **Important:** If your servos are twitching or weak, power them from an **external 5V supply** instead of the Arduino's 5V pin to avoid overloading the board.

---

### 5. Configure the COM Port

Open `PythonApp/app_billing_two_boxes.py` and find line 13:

```python
# Line 13 – Change "COM4" to your actual Arduino port
ARDUINO_PORT = "COM4"      # ← Update this!
BAUD_RATE = 115200
```

**How to find your COM port:**

- **Windows:** Open Device Manager → `Ports (COM & LPT)` → Look for `Arduino UNO (COMx)`
- **macOS:** Run `ls /dev/tty.*` in terminal, look for `/dev/tty.usbmodem...`
- **Linux:** Run `ls /dev/ttyUSB*` or `ls /dev/ttyACM*`

---

## ▶️ Running the Project

Once your hardware is wired and your COM port is configured:

```bash
# Make sure you're in the PythonApp directory with venv active
cd PythonApp
python app_billing_two_boxes.py
```

**Expected console output on successful start:**

```
Looking for medicines.csv at: C:\...\Medical_Dispenser_Project\PythonApp\medicines.csv
✅ Arduino connected on COM4
```

> 💡 **No Arduino?** No problem! The app launches in **Demo Mode** — you can still use all billing and PDF features. A message will appear instead of dispensing.

---

## 📖 How It Works

### Billing Workflow

```
① Search Medicine        Type in the search bar — results filter live
         ↓
② Select & Set Quantity  Click a result row, enter quantity (default: 1)
         ↓
③ Add to Cart            Click "Add to Cart" — bill totals update instantly
         ↓
④ Dispense               Click "Dispense Last Item" — servo activates!
         ↓
⑤ Generate PDF           Click "Generate PDF Bill" — saved to Bills/
```

### Arduino Command Protocol

The Python app sends a **single character** over the serial port:

| Command Sent | Box Activated                         | Servo Pin | LED Pin |
| :----------: | ------------------------------------- | :-------: | :-----: |
|   `'1'`   | Box 1 (Painkillers/Anti-inflammatory) |     5     |    4    |
|   `'2'`   | Box 2 (Antibiotics/Antihistamines)    |     6     |    7    |
|   `'3'`   | Box 3 (Digestive/Supplements)         |     9     |    8    |
|   `'4'`   | Box 4 (Vitamins/Misc)                 |    10    |   11   |

### Servo Motion

Each servo follows this motion sequence when triggered:

```
0°  ──────────────────►  180°   (dispensing sweep)
      ~90ms @ 2°/step
         ↓ 5ms hold
180° ◄──────────────────  0°    (return sweep)
      ~90ms @ 2°/step
```

### Box Type → Box Number Mapping

```python
# From app_billing_two_boxes.py
"box1" or "painkiller"  →  Box 1
"box2" or "paracetamol" →  Box 2
"box3"                  →  Box 3
"box4"                  →  Box 4
```

---

## 🧪 Usage Examples

### Example 1: Searching and Adding a Medicine

```python
# What happens internally when you type "Dolo" in the search bar:
filter_text = "dolo"
matching = [med for med in all_medicines
            if filter_text in med["medicine_name"].lower()]
# → Returns: "Dolo 650 Tablet", "Dolo 500 Tablet"
```

### Example 2: Billing Calculation

```python
# For: Dolo 650, Qty=2, Rate=₹35, Discount=5%, GST=12%
unit_rate  = 35.00
qty        = 2
mrp_total  = 35.00 × 2  = ₹70.00
discount   = 70.00 × 5% = ₹3.50
after_disc = 70.00 - 3.50 = ₹66.50
gst        = 66.50 × 12% = ₹7.98
final      = 66.50 + 7.98 = ₹74.48  ✅
```

### Example 3: Sending a Serial Command to Arduino

```python
import serial

arduino = serial.Serial("COM4", 115200, timeout=1)

# Send command to dispense from Box 3
box_number = 3
arduino.write((str(box_number) + "\n").encode('utf-8'))
arduino.flush()
# Arduino receives '3' → Activates Servo 3 + LED 8
```

### Example 4: PDF Bill Location

```
Bills/
└── bill_20261115_143022.pdf   ← Format: bill_YYYYMMDD_HHMMSS.pdf
```

---

## 🗂️ Medicine Database

The `medicines.csv` file contains the pharmacy's inventory. Here's the structure:

| Column                 | Description              | Example                                |
| ---------------------- | ------------------------ | -------------------------------------- |
| `medicine_name`      | Primary drug name        | `Dolo 650 Tablet`                    |
| `alternate_medicine` | Substitute drug          | `Calpol 650 Tablet`                  |
| `strength`           | Dosage strength          | `650mg`                              |
| `manufacturer`       | Pharma company           | `Micro Labs Ltd`                     |
| `type`               | Dispenser box assignment | `box1`, `box2`, `box3`, `box4` |
| `color`              | Tablet color             | `Blue`                               |
| `batch_no`           | Batch identifier         | `BAT001`                             |
| `expiry_date`        | Expiry (MM/YYYY)         | `12/2026`                            |
| `quantity`           | Stock quantity           | `40`                                 |
| `purchase_rate`      | Buying price (₹)        | `28`                                 |
| `sale_rate`          | Selling price (₹)       | `35`                                 |
| `discount`           | Discount percentage      | `5`                                  |
| `tax`                | GST percentage           | `12`                                 |

### Current Medicine Distribution

| Box                | Type                            | Sample Medicines                              |
| ------------------ | ------------------------------- | --------------------------------------------- |
| **Box 1** 🟢 | Painkillers & Anti-inflammatory | Dolo 650, Calpol 500, Zerodol P, Combiflam    |
| **Box 2** 🔴 | Antibiotics & Antihistamines    | Augmentin 625, Azithral 500, Allegra 120      |
| **Box 3** 🔵 | Digestive & Supplements         | Pantocid D, Digene, ORS Powder, Becosules     |
| **Box 4** 🩵 | Vitamins & Misc                 | Evion 400, Shelcal 500, Meftal Spas, Sinarest |

### Adding a New Medicine

Simply open `medicines.csv` and add a new row:

```csv
Paracetamol IP,Calpol 500 Tablet,500mg,Generic,box1,White,BAT025,06/2027,100,10,18,5,12,Generic Pharma,INV025,2026-05-13
```

> ✅ The app reads this file dynamically — **no code changes needed**!

---

## 🤝 Contributing

Contributions are what make the open-source community such an amazing place! Any contributions you make are **greatly appreciated**.

### How to Contribute

1. **Fork** the repository

   ```bash
   # Click "Fork" on GitHub, then:
   git clone https://github.com/YOUR_USERNAME/Medical_Dispenser_Project.git
   ```
2. **Create a Feature Branch**

   ```bash
   git checkout -b feature/your-amazing-feature
   ```
3. **Make Your Changes** and commit them

   ```bash
   git add .
   git commit -m "✨ Add: your amazing feature description"
   ```
4. **Push** to your fork

   ```bash
   git push origin feature/your-amazing-feature
   ```
5. **Open a Pull Request** on GitHub

### Commit Message Convention

Use emoji prefixes for clarity:

| Prefix             | When to Use              |
| ------------------ | ------------------------ |
| `✨ Add:`        | New feature              |
| `🐛 Fix:`        | Bug fix                  |
| `♻️ Refactor:` | Code refactoring         |
| `📝 Docs:`       | Documentation changes    |
| `⚡ Perf:`       | Performance improvements |
| `🎨 Style:`      | UI/formatting changes    |

### Ideas for Contribution

- [ ] 🏥 Add patient name and prescription tracking
- [ ] 📱 Build a web-based version of the billing interface
- [ ] 🔔 Add low-stock alerts when medicine quantity is running low
- [ ] 📈 Add daily/monthly sales reports
- [ ] 🗄️ Migrate from CSV to SQLite for better data management
- [ ] 🖨️ Add thermal printer support for physical receipts
- [ ] 🔐 Add pharmacist login/authentication

---

## 📄 License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for full details.

```
MIT License

Copyright (c) 2026 Suyash Sahu

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software...
```

---

## 🙏 Credits & Acknowledgments

| Resource                                                        | Contribution                                     |
| --------------------------------------------------------------- | ------------------------------------------------ |
| 🐍[Python Tkinter](https://docs.python.org/3/library/tkinter.html) | Desktop GUI framework                            |
| ⚡[Arduino](https://www.arduino.cc/)                               | Microcontroller platform and `Servo.h` library |
| 📄[ReportLab](https://www.reportlab.com/)                          | PDF generation engine                            |
| 🔌[PySerial](https://pyserial.readthedocs.io/)                     | Python ↔ Arduino serial communication           |
| 💊[Open Medicine Data](https://open.fda.gov/)                      | Inspiration for medicine database structure      |

### Built With 💙 By

**Suyash Sahu** — [@suyashsahu00](https://github.com/suyashsahu00)

---

<div align="center">

**If this project helped you, please consider giving it a ⭐ on GitHub!**

[![GitHub Stars](https://img.shields.io/github/stars/suyashsahu00/Medical_Dispenser_Project?style=social)](https://github.com/suyashsahu00/Medical_Dispenser_Project/stargazers)

<br/>

*Made with 💊 + ☕ + 🤖*

</div>
