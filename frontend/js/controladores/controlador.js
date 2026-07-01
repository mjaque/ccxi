import { API } from '../servicios/api.js'
import { BusEventos } from '../servicios/bus_eventos.js'

export class Controlador{
	static busEventos = new BusEventos()

	api		//Servicio de API REST. Público.
	div		//HTMLDivElement que alberga la vista.


	constructor(div){
		this.div = div
		this.observadores = new Set()
		this.api = new API()
	}

	async cargarVista() {
		// Realizar la petición fetch al servidor
		const respuesta = await fetch(this.URL_VISTA, {
			method: 'GET',
			headers: {
				'Content-Type': 'text/html',
			},
		})

		// Verificar si la respuesta es exitosa
		if (!respuesta.ok) {
			throw new Error(`Error al obtener el HTML de la vista: ${respuesta.statusText}`)
		}

		const fragmentoHTML = await respuesta.text()
		this.div.insertAdjacentHTML('beforeend', fragmentoHTML)
	}

	mostrarError(texto){
		this.pMensaje.textContent = texto
		this.pMensaje.setAttribute('class', 'error')
	}

	mostrarInformacion(texto){
		this.pMensaje.textContent = texto
		this.pMensaje.setAttribute('class', 'informacion')
	}

	emitirMensaje(mensaje, opciones = {}) {
		return Controlador.busEventos.emitir(mensaje, opciones)
	}

	recibirMensaje(mensaje, callback) {
		return Controlador.busEventos.on(mensaje, callback)
	}

	referenciarElementosIU(){}

	registrarEventos(){}

	crearBotonEditar() {
		const boton = document.createElement('button')
		boton.type = 'button'
		boton.innerHTML = '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"/><path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"/></svg>'
		boton.title = 'Editar'
		return boton
	}

	crearBotonEliminar() {
		const boton = document.createElement('button')
		boton.type = 'button'
		boton.innerHTML = '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="3 6 5 6 21 6"/><path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"/></svg>'
		boton.title = 'Eliminar'
		return boton
	}

}

