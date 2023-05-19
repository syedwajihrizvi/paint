import RPi.GPIO as GPIO
from time import sleep


class Motor:
    def __init__(self, en, in1, in2, freq, dutyCycle):
        self.en = en
        self.in1 = in1
        self.in2 = in2
        self.dc = dutyCycle
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(in1, GPIO.OUT)
        GPIO.setup(in2, GPIO.OUT)
        GPIO.setup(en, GPIO.OUT)
        GPIO.output(in1, GPIO.LOW)
        GPIO.output(in2, GPIO.LOW)
        self.p = GPIO.PWM(en, freq)
        self.p.start(dutyCycle)

    def start(self):
        self.p.start(self.dc)

    def rotate_forward(self):
        GPIO.output(self.in1, GPIO.HIGH)
        GPIO.output(self.in2, GPIO.LOW)

    def rotate_backward(self):
        GPIO.output(self.in1, GPIO.LOW)
        GPIO.output(self.in2, GPIO.HIGH)

    def stop(self):
        GPIO.output(self.in1, GPIO.LOW)
        GPIO.output(self.in2, GPIO.LOW)

    def change_speed(self, new_dc):
        # print(f"CHANGING DUTY CYCLE to {new_dc}")
        self.p.ChangeDutyCycle(new_dc)

    def change_frequency(self, new_fr):
        # print(f"CHANGING Frequency to {new_fr}")
        self.p.ChangeFrequency(new_fr)
