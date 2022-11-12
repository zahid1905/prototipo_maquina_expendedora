# state.py

class State(object):
    """
    Objeto estado; proporciona funciones de utilidad para los
    estados individuales dentro de la maquina de estados.
    """

    def __init__(self):
        print('Procesando estado actual:', str(self))

    def on_event(self, event):
        """
        Manejar eventos delegados a este estado.
        """
        pass

    def __repr__(self):
        """
        Aprovecha el método __str__ para describir el estado.
        """
        return self.__str__()

    def __str__(self):
        """
        Devuelve el nombre del estado.
        """
        return self.__class__.__name__