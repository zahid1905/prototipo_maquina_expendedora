from state import State
from time import sleep
#from machine import I2C

class Iniciar(State):
    """
    Estado donde inicializamos todos los servicios.
    """
    def on_event(self, event):
        # Iniciar I2C
        print("Iniciando I2C")
        
        # Iniciar dispositivos
        print("Iniciando RaspPi")
        print("iniciando RFID")
        print("Iniciando Display")

        return EsperandoPago()

class EsperandoPago(State):
    """
    Estado donde inicializamos todos los servicios.
    """
    def on_event(self, event):
        if event == 'inicio_correcto' or event == 'compra_exitosa':
            while nfc != '1':
                # Placeholder para la comunicacion con el NFC
                nfc = input("Lectura nfc:")
                sleep(2)
            return LecturaCamara()
        return self

class LecturaCamara(State):
    def on_event(self, event):

        return self