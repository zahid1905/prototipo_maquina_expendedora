from machine import Pin
from time import sleep

def activar_motor(motor):
    mot1_4 = Pin(2, Pin.OUT, value = 0)
    mot1 = Pin(12, Pin.OUT, value = 0)
    mot2 = Pin(13, Pin.OUT, value = 0)
    mot3 = Pin(14, Pin.OUT, value = 0)
    mot4 = Pin(15, Pin.OUT, value = 0)

    if  motor == 1:
        mot1.value(1)
        sleep(4)
        mot1.value(0)
    elif  motor == 2:
        mot2.value(1)
        sleep(4)
        mot2.value(0)
    elif  motor == 3:
        mot3.value(1)
        sleep(4)
        mot3.value(0)
    elif  motor == 4:
        mot4.value(1)
        sleep(4)
        mot4.value(0)
    else:
        print("No es un motor valido")