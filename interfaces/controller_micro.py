from machine import Pin, PWM
import sys
from time import sleep

DUTY_MAX = 65025
pwm_g = PWM(Pin(13))
pwm_b = PWM(Pin(15))
pwm_r = PWM(Pin(11))

pwm_b.freq(50)
pwm_g.freq(50)
pwm_r.freq(50)

while True:
    # read a command from the host
    v = sys.stdin.readline().strip()

    # perform the requested action


    r_value, g_value, b_value = [i for i in v.split(',')]
    pwm_b.duty_u16(b_value * 255)
    pwm_g.duty_u16(g_value * 255)
    pwm_r.duty_u16(r_value * 255)


print('do the thing')
while True:
    pwm_b.duty_u16(DUTY_MAX)
    pwm_g.duty_u16(DUTY_MAX)
    pwm_r.duty_u16(0)

    for i in range(3):
        sleep(0.1)
        pwm_b.duty_u16(DUTY_MAX // 2)

        sleep(0.4)
        pwm_b.duty_u16(0)

    pwm_b.duty_u16(0)
    pwm_g.duty_u16(0)
    pwm_r.duty_u16(DUTY_MAX)

    for i in range(2):
        pwm_b.duty_u16(DUTY_MAX)
        sleep(0.1)
        pwm_b.duty_u16(0)
        sleep(0.2)

