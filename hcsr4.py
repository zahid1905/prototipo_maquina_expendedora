from time import sleep_us
from machine import Pin
from machine import time_pulse_us

HC_SR04_TRIG = 27
HC_SR04_ECHO = 26

def hcsr4():
    print("Iniciando Sensor") #Debug
    trig = Pin(HC_SR04_TRIG, Pin.OUT, value = 0)
    echo = Pin(HC_SR04_ECHO, Pin.IN)
    
    trig.value(1)
    sleep_us(10)
    trig.value(0)

    duracion = time_pulse_us(echo, 1, 30000)
    
    distancia = (duracion / 2) / 29.1
    
    print('Distancia: {0}'.format(distancia)) #Debug