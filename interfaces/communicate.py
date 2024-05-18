import serial
import time
import random
COMMA = ','
# open a serial connection
s = serial.Serial("/dev/ttyACM0", 115200)

def rand_8bit():
    return random.randint(0, 255)

def rand_blue():
    return random.randint(0, 128)

def send_integers_as_string(ser, int1, int2, int3):
    data = f"{int1},{int2},{int3}\n"
    ser.write(data.encode())

# blink the led
while True:

    send_integers_as_string(s, rand_8bit(), rand_blue(), rand_blue())
    time.sleep(0.5)
    s.write(b"255,5,4\n")
    time.sleep(0.5)
    # time.sleep(1)
    # s.write(b"0,0,254\n")
    # time.sleep(1)
    # s.write(b"254,0,0\n")
    # time.sleep(1)

