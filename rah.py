import time
import serial
import numpy as np

port = serial.Serial('/dev/cu.usbserial-0001', 9600)

send_text = "wassup"

while (True):
  port.write(send_text.encode())
