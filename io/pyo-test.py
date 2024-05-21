import colorsys
import time

import serial
from pyo import *
from serial.tools import list_ports

BUFFER_SIZE = 10

rgb_buffer = [[0] * BUFFER_SIZE, [0] * BUFFER_SIZE, [0] * BUFFER_SIZE]

def send_integers_as_string(ser, int1, int2, int3):
    data = f"{int1},{int2},{int3}\n"
    ser.write(data.encode())

# List available usb ports
port = list(list_ports.comports())
for p in port:
    print(p.device)

port = serial.Serial('/dev/cu.usbmodem1301', 115200) # Replace with path to usb port

s = Server(nchnls=1).boot()

# White noise generator
# n = Noise(0.5)

# Read a file
# n = SfPlayer("/path/to/file.wav")

# Read default input (laptop mic)
n = Input()

# Common cutoff frequency control
freq = Sig(1000)
freq.ctrl([SLMap(50, 10000, "lin", "value", 1000)], title="Cutoff Frequency")

# Three different lowpass filters
tone = Tone(n, freq)
butlp = ButLP(n, freq)
mooglp = MoogLP(n, freq)

# Interpolates between input objects to produce a single output
sel = Selector([tone, butlp, mooglp])
sel.ctrl(title="Filter selector (0=Tone, 1=ButLP, 2=MoogLP)")

# Splits signal into frequency bands
mb = MultiBand(sel, num=3).out()
mb.setFrequencies([1500, 3000, 8000])

# Displays the spectrum contents of the chosen source
sp = Spectrum(mb)

# Colour selector. Audio selection is not actually used, but it gives us a UI input to read
cs = Selector([n, n])
cs.ctrl(title="Colour selector")


buffer_index = 0
def rms_to_rgb(*amplitudes):
    global buffer_index

    angle = cs.voice.get()
    r_in = amplitudes[0]
    g_in = amplitudes[1]
    b_in = amplitudes[2]

    h, s, v = colorsys.rgb_to_hsv(r_in, g_in, b_in)

    h += angle
    if h > 1.0:
        h -= 1.0

    r, g, b = colorsys.hsv_to_rgb(h, s, v)
    r, g, b = tuple(map(lambda x: int((x*255.0)//1), (r, g, b)))

    r = min(255, r * 2)
    g = min(255, g * 2)
    b = min(255, b * 2)

    r = min(255, r * 2)

    rgb_buffer[0][buffer_index] = r
    rgb_buffer[1][buffer_index] = g
    rgb_buffer[2][buffer_index] = b

    r_out = int(sum(rgb_buffer[0]) / BUFFER_SIZE)
    g_out = int(sum(rgb_buffer[1]) / BUFFER_SIZE)
    b_out = int(sum(rgb_buffer[2]) / BUFFER_SIZE)

    buffer_index += 1
    if buffer_index == BUFFER_SIZE:
        buffer_index = 0

    send_integers_as_string(port, r_out, g_out, b_out)
    # print(f"IN:  {r_in} {g_in} {b_in}")
    # print(f"OUT: {r_out} {g_out} {b_out}")

# Reports RMS of each band and passes them into callback function
rms = RMS(mb, function=rms_to_rgb)
rms.polltime(0.01)

s.gui(locals())


