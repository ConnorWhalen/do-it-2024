import colorsys
from pyo import *

s = Server(nchnls=1).boot()

# White noise generator
n = Noise(0.5)

# Common cutoff frequency control
freq = Sig(1000)
freq.ctrl([SLMap(50, 5000, "lin", "value", 1000)], title="Cutoff Frequency")

# Three different lowpass filters
tone = Tone(n, freq)
butlp = ButLP(n, freq)
mooglp = MoogLP(n, freq)

# Interpolates between input objects to produce a single output
sel = Selector([tone, butlp, mooglp])
sel.ctrl(title="Filter selector (0=Tone, 1=ButLP, 2=MoogLP)")

# Splits signal into frequency bands
mb = MultiBand(sel, num=3).out()

# Displays the spectrum contents of the chosen source
sp = Spectrum(mb)

cs = Selector([Noise(0.5), Noise(0.5)])
cs.ctrl(title="Colour selector")


def rms_to_rgb(*amplitudes):
    angle = cs.voice.get() * 2.0 * math.pi

    r_in = amplitudes[0]
    g_in = amplitudes[1]
    b_in = amplitudes[2]

    h, s, v = colorsys.rgb_to_hsv(r_in, g_in, b_in)

    h += angle
    if h > 2.0 * math.pi:
        h -= 2.0 * math.pi

    r, g, b = colorsys.hsv_to_rgb(h, s, v)

    print(f"IN:  {r_in} {g_in} {b_in}")
    print(f"OUT: {r} {g} {b}")

# Reports RMS of each band and passes them into callback function
rms = RMS(mb, function=print_rms)
rms.polltime(1)

s.gui(locals())


