from xml.dom import minidom

class Controlador():

    def cargarDOM(self, nombre):
        return minidom.parse("backend/vistas/" + nombre)

    def getVista(self, nombre):
        dom = self.cargarDOM(nombre)
        vista = dom.documentElement
        return vista
        
        
    def quitarCabeceraXML(self, dom):
        cabecera = "<?xml version=\"1.0\" encoding=\"utf-8\"?>"
        codificacion = "utf-8"
        html_str = dom.toxml(encoding = codificacion).decode(codificacion)
        return html_str.replace(cabecera, "").encode(codificacion)


