"""
debug_one_servo_python.py
=========================
Minimal Python debug script — sends a single 'box1' command to Arduino
and prints every response line it receives back.

Prerequisites:
  pip install pyserial

Usage:
  python debug_one_servo_python.py

Adjust ARDUINO_PORT below to match your system (e.g. COM3, COM4, /dev/ttyUSB0).
"""

import serial
import time

# ── CONFIG ─────────────────────────────────────────────────────────────────
ARDUINO_PORT = "COM4"   # <-- Change this to your actual port
BAUD_RATE    = 9600
COMMAND      = "box1"   # Only Servo 1 will respond to 'box1' or 'painkiller'
# ───────────────────────────────────────────────────────────────────────────


def connect_arduino(port: str, baud: int) -> serial.Serial | None:
    """Open serial connection; return None on failure."""
    try:
        conn = serial.Serial(port, baud, timeout=5)
        time.sleep(2)  # Wait for Arduino bootloader to finish resetting
        print(f"✔  Connected to Arduino on {port} at {baud} baud")
        return conn
    except serial.SerialException as e:
        print(f"✘  Could not open {port}: {e}")
        return None


def read_all_available(conn: serial.Serial, wait_seconds: float = 4.5) -> None:
    """Read and print every line Arduino sends within the time window."""
    deadline = time.time() + wait_seconds
    print("─── Arduino responses ───")
    while time.time() < deadline:
        if conn.in_waiting:
            line = conn.readline().decode("utf-8", errors="replace").strip()
            if line:
                print(f"  Arduino: {line}")
        else:
            time.sleep(0.05)
    print("─── End of response window ───")


def main():
    print("=== Single-Servo Debug Script ===")
    print(f"Target port : {ARDUINO_PORT}")
    print(f"Command     : '{COMMAND}'")
    print()

    arduino = connect_arduino(ARDUINO_PORT, BAUD_RATE)
    if arduino is None:
        print("Aborting — Arduino not connected.")
        return

    # Drain any startup messages from the Arduino
    time.sleep(0.5)
    while arduino.in_waiting:
        startup_msg = arduino.readline().decode("utf-8", errors="replace").strip()
        if startup_msg:
            print(f"  [startup] Arduino: {startup_msg}")

    print(f"\nSending command: '{COMMAND}' ...")
    arduino.write((COMMAND + "\n").encode("utf-8"))

    # Listen for responses (open=3 s + close + some buffer)
    read_all_available(arduino, wait_seconds=5.0)

    arduino.close()
    print("\nDone. Serial port closed.")


if __name__ == "__main__":
    main()
