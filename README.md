# LED Zeppelin

LED Zeppelin is our DO.IT Hackathon 2024 submission. We created an RGB LED light strip that reacts to the frequency response of input audio.

This repository contains the control software that runs on a personal computer and the onboard software for the Raspberry Pi Pico that controls the LEDs.

# Installation

I recommend setting up a virtual environment to keep a separate python instance and any libraries local to this project:

```bash
# Install and run virtualenv
pip install virtualenv
virtualenv do-it-2024

# Activate virtualenv
source do-it-2024/bin/activate

# To deactivate
deactivate
```
_I realize now that giving the venv the same name as the project was a bad idea_

Install [pyo](https://github.com/belangeo/pyo)

```bash
pip install pyo
```
I had to install [portmidi](https://github.com/PortMidi/portmidi). Clone the repo and follow the installation steps.

Pyo also requires [portaudio](https://github.com/GoogleCloudPlatform/python-docs-samples/blob/main/scripts/readme-gen/templates/install_portaudio.tmpl.rst).

# Running

The source file for running the Audio to LED system is `io/pyo-test.py`.

`interfaces/communicate.py` is a useful script for testing communication between the main computer, Pi Pico, and the LEDs.

Both scripts require a Pic Pico connected via usb and the file system path to the usb port connected to the Pi Pico. Update this path in the source files before running them.

Using a program that can push python code to a Pi Pico like [Thonny](https://thonny.org/), deploy the script `interfaces/controller_micro.py`.
