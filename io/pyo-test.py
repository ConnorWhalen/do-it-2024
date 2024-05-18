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
mb = MultiBand(sel).out()

# Displays the spectrum contents of the chosen source
sp = Spectrum(mb)


def print_rms(*amplitudes):
    print(amplitudes)

# Reports RMS of each band and passes them into callback function
rms = RMS(mb, function=print_rms)
rms.polltime(1)

s.gui(locals())