from time import sleep
from machine import Pin
#from machine import I2C

"""
Declaracion de Pines
"""
HC_SR04_TRIG = 27
HC_SR04_ECHO = 26

class StateMachine(object):

    def Iniciar(self, event):
        """
        Inicializar todos los servicios.
        """
        if event == 'iniciar':

            # Iniciar I2C
            print("Iniciando I2C")
            
            # Iniciar dispositivos
            print("Iniciando RaspPi")
            print("iniciando RFID")
            print("Iniciando Display")
            
            return StateMachine.EsperandoPago(self, 'inicio_correcto')
        
        pass

    def EsperandoPago(self, event):
        """
        Esperar por un "pago" en el modulo RFID.
        """
        nfc = ''
        if event == 'inicio_correcto' or event == 'compra_exitosa':
            
            while nfc != '1':
                # Placeholder para la comunicacion con el RFID
                nfc = input("Lectura nfc:")
                sleep(2)

            return StateMachine.LecturaCamara(self, 'pago_recibido')
        
        pass

    def LecturaCamara(self, event):
        """
        Obtener el producto con la RPi/Camara.
        """
        if event == 'pago_recibido':
            # Placeholder para la comunicacion con la RPi/Camara
            producto = input("Lectura camara:") # p_[1,2,3,4]
            sleep(2)
            return StateMachine.ConfirmarCamara(self, producto)

        pass

    def ConfirmarCamara(self, event):
        pass

    def ActivarMotor(self, event):
        pass

    def LecturaSensor(self, event):
        """
        Comprobar que un producto haya caido usando el HC-SR04.
        """
        trig = Pin(HC_SR04_TRIG, Pin.OUT, value = 0)
        echo = Pin(HC_SR04_ECHO, Pin.IN)

        trig.value(1)
        sleep_us(10)
        trig.value(0)

        duracion = machine.time_pulse_us(echo, 1, timeout_us = 40000)
        
        distancia = duracion / 58
        
        if distancia < 30:
            return StateMachine.EsperandoPago(self, 'compra_exitosa')
        else:
            if event == 'p_1' or event == 'p_2' or event == 'p_3' or event == 'p_4':
                retry_product = {
                    'p_1': 'r_p_1',
                    'p_2': "r_p_2",
                    'p_3': 'r_p_3',
                    'p_4': "r_p_4",
                    }
                return StateMachine.ActivarMotor(self, retry_product[event])
            else:
                return StateMachine.FinalizarError(self, 'error')

    def FinalizarError(self, event):
        pass