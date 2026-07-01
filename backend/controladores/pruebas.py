from controladores.controlador import Controlador

class ControladorPruebas(Controlador):

    def getVista(self):
        return super().getVista("pruebas.xml")
