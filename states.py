from state import State
from time import sleep
#from machine import I2C

class Iniciar(State):
    """
    Inicializar todos los servicios.
    """
    def on_event(self, event):
        # Iniciar I2C
        print("Iniciando I2C")
        
        # Iniciar dispositivos
        print("Iniciando RaspPi")
        print("iniciando RFID")
        print("Iniciando Display")

        return EsperandoPago.on_event(self, 'inicio_correcto')

class EsperandoPago(State):
    """
    Esperar por un "pago" en el modulo RFID.
    """
    def on_event(self, event):
        nfc = ''
        if event == 'inicio_correcto' or event == 'compra_exitosa':
            
            while nfc != '1':
                # Placeholder para la comunicacion con el RFID
                nfc = input("Lectura nfc:")
                sleep(2)

            return LecturaCamara().on_event(self, 'pago_recibido')
        
        return self

class LecturaCamara(State):
    """
    Obtener el producto con la RPi/Camara.
    """
    def on_event(self, event):
        if event == 'pago_recibido':
            # Placeholder para la comunicacion con la RPi/Camara
            producto = input("Lectura camara:") # p_[1,2,3,4]
            sleep(2)
            return

        return self

class ConfirmarCamara(State):
    def on_event(self, event):
        return self

class ActivarMotor(State):
    def on_event(self, event):
        return self

class LecturaSensor(State):
    def on_event(self, event):
        return self

class FinalizarError(State):
    def on_event(self, event):
        return self