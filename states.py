from time import sleep
from time import sleep_us
from machine import Pin
from machine import time_pulse_us
from machine import UART
import moda

"""
Declaracion de Pines
"""
HC_SR04_TRIG = 27
HC_SR04_ECHO = 26
RFID_TRIG = 25
RASP_TX = 0 # No se utiliza
RASP_RX = 4
MOTOR_1_IN1 = 12
MOTOR_2_IN4 = 13
MOTOR_3_IN1 = 14
MOTOR_4_IN4 = 15
MOTOR_1_4_IN2_IN3 = 2
LED_ESTADO = 32

DIC_PRODUCTO = {
                    b'0': 'cancelar',
                    b'1': 'p_1',
                    b'2': 'p_2',
                    b'3': 'p_3',
                    b'4': 'p_4',
                    b'5': 'confirmar'
                }

RETRY_PRODUCT = {
                    'p_1': 'r_p_1',
                    'p_2': "r_p_2",
                    'p_3': 'r_p_3',
                    'p_4': "r_p_4",
                } 


class StateMachine(object):

    def Iniciar(self, event):
        """
        Inicializar todos los servicios.
        """
        if event == 'iniciar' or 'test':

            # Iniciar dispositivos
            print("Iniciando Sensor") #Debug
            self.trig = Pin(HC_SR04_TRIG, Pin.OUT, value = 0)
            self.echo = Pin(HC_SR04_ECHO, Pin.IN)

            print("Iniciando RFID") #Debug
            self.rfid = Pin(RFID_TRIG, Pin.IN)

            print("Iniciando Motores") #Debug
            self.mot1_4 = Pin(MOTOR_1_4_IN2_IN3, Pin.OUT, value = 0)
            self.mot1 = Pin(MOTOR_1_IN1, Pin.OUT, value = 0)
            self.mot2 = Pin(MOTOR_2_IN4, Pin.OUT, value = 0)
            self.mot3 = Pin(MOTOR_3_IN1, Pin.OUT, value = 0)
            self.mot4 = Pin(MOTOR_4_IN4, Pin.OUT, value = 0)

            print("Iniciando RaspPi") #Debug
            self.uart2 = UART(2, baudrate=9600, tx=RASP_TX, rx=RASP_RX)
            self.uart2.init(bits=8, parity=None, stop=1)
            self.led = Pin(LED_ESTADO, Pin.OUT, value = 0)
            
            print("llamando EsperandoPago") #Debug
            if event == 'test':
                return self.ActivarMotor('p_1')
            return self.EsperandoPago('inicio_correcto')

    def EsperandoPago(self, event):
        """
        Esperar por un "pago" en el modulo RFID.
        """
        print("EsperandoPago") #Debug
        if event == 'inicio_correcto' or event == 'compra_exitosa':
                        
            while self.rfid.value() != 1:
                sleep_us(1)

            print("llamando LecturaCamara")
            return self.LecturaCamara('pago_recibido')

    def LecturaCamara(self, event):
        """
        Obtener el producto con la RPi/Camara.
        """

        print("LecturaCamara") #Debug
        if event == 'pago_recibido' or event == 'reintentar_lectura':
            self.led.value(1)
            sleep(4)
            self.uart2.read()
            sleep(3)

            lectura = []

            for x in range(10):
                lectura.append(self.uart2.read(1))
                
            print(lectura) #Debug

            lista = [i for i in lectura if i is not None]

            print(lista) #Debug

            if not lista:
                print("llamando LecturaCamara again") #Debug
                return self.LecturaCamara('reintentar_lectura')
            
            producto = DIC_PRODUCTO[moda.Moda(lista)]

            print(producto) #Debug

            self.led.value(0)

            if producto == 'confirmar' or producto == 'cancelar':
                print("llamando LecturaCamara again") #Debug
                return self.LecturaCamara('reintentar_lectura')

            print("llamando ConfirmarCamara") #Debug
            return self.ConfirmarCamara(producto)

    def ConfirmarCamara(self, event):
        """
        Confirmar la seleccion con la RPi/Camara.
        """
        print("ConfirmarCamara") #Debug
        if event == 'p_1' or event == 'p_2' or event == 'p_3' or event == 'p_4':
            self.led.value(1)
            sleep(4)
            self.uart2.read()
            sleep(3)

            lectura = []

            for x in range(10):
                lectura.append(self.uart2.read(1))

            print(lectura) #Debug

            lista = [i for i in lectura if i is not None]

            print(lista) #Debug

            if not lista:
                print("llamando LecturaCamara again") #Debug
                return self.LecturaCamara('reintentar_lectura')
            
            producto = DIC_PRODUCTO[moda.Moda(lista)]

            self.led.value(0)

            if producto == 'cancelar':
                print("llamando LecturaCamara again") #Debug
                return self.LecturaCamara('reintentar_lectura')
            elif producto == 'confirmar':
                print("llamando ActivarMotor") #Debug
                return self.ActivarMotor(event)
            else:
                print("llamando ConfirmarCamara again") #Debug
                return self.ConfirmarCamara(event)  

    def ActivarMotor(self, event):
        """
        Activar el motor correspondiente al producto.
        """

        print("ActivarMotor") #Debug
        print(event) #Debug
        if event == 'p_1' or event == 'r_p_1':
            self.mot1.value(1)
            sleep(3)
            self.mot1.value(0)

        elif event == 'p_2' or event == 'r_p_2':
            self.mot2.value(1)
            sleep(3)
            self.mot2.value(0)

        elif event == 'p_3' or event == 'r_p_3':
            self.mot3.value(1)
            sleep(3)
            self.mot3.value(0)

        elif event == 'p_4' or event == 'r_p_4':
            self.mot4.value(1)
            sleep(3)
            self.mot4.value(0)

        print("llamando LecturaSensor")
        return self.LecturaSensor(event)

    def LecturaSensor(self, event):
        """
        Comprobar que un producto haya caido usando el HC-SR04.
        """

        self.trig.value(1)
        sleep_us(10)
        self.trig.value(0)

        duracion = time_pulse_us(self.echo, 1, 30000)
        
        distancia = (duracion / 2) / 29.1
        
        print('Distancia: {0}'.format(distancia)) #Debug
        
        if distancia < 20:
            return self.EsperandoPago('compra_exitosa')
        else:
            if event == 'p_1' or event == 'p_2' or event == 'p_3' or event == 'p_4':
                
                print('Retry motor: ' + RETRY_PRODUCT[event]) #Debug

                return self.ActivarMotor(RETRY_PRODUCT[event])
            else:

                print('error') #Debug

                return self.FinalizarError('error')

    def FinalizarError(self, event):
        print("Algo salio mal xddd")