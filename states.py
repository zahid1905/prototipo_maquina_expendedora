from states_declaration import States
from time import sleep
#from machine import I2C

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
        pass

    def FinalizarError(self, event):
        pass