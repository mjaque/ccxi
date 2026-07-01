from controladores.controlador import Controlador

class ControladorAlumnado(Controlador):

    def getVista(self):
        return super().getVista("alumnado.xml")
