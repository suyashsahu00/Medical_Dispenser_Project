import serial
import time

# Yahan COM port change karo apne hisaab se (COM3, COM4, etc.)
arduino = serial.Serial('COM4', 9600)
time.sleep(2)  # Arduino ko reset hone ka time

# Painkiller command
arduino.write(b"painkiller\n")
print("Painkiller command bhej diya")

time.sleep(5)

# Paracetamol command
arduino.write(b"paracetamol\n")
print("Paracetamol command bhej diya")

arduino.close()
