from controladores.controlador import Controlador
from controladores.alumnado import ControladorAlumnado
from controladores.pruebas import ControladorPruebas

class ControladorPrincipal(Controlador):

    def getHTML(self):
        dom = self.cargarDOM("index.html")
        secciones = dom.getElementsByTagName("section")
        
        controlador= ControladorAlumnado()
        vista= controlador.getVista()
        self._cargarVistaEnSeccion(dom, vista, secciones[0])

        controlador= ControladorPruebas()
        vista= controlador.getVista()
        self._cargarVistaEnSeccion(dom, vista, secciones[3])

        return self.quitarCabeceraXML(dom)

    def _cargarVistaEnSeccion(self, dom, vista, seccion):
        vista_clon = dom.importNode(vista, deep=True)
        seccion.appendChild(vista_clon)
        
