import { Controlador } from './controlador.js'

export class ControladorModulos extends Controlador{
	URL_VISTA = './html/modulos.html'

	//Elementos del IU
	#moduloSelectEl
	#nuevoModuloNombreEl
	#crearModuloEl

	//Registros
	#moduloActual
	#cambioModuloBloqueado
	#cambioBaseBloqueado

	constructor(div){
		super(div)
	}

	bloquearCambioModulo() {
		this.#cambioBaseBloqueado = true
		this.#moduloSelectEl.disabled = true
		this.#nuevoModuloNombreEl.disabled = true
		this.#crearModuloEl.disabled = true
	}

	desbloquearCambioModulo() {
		this.#cambioBaseBloqueado = false

		this.#moduloSelectEl.disabled = !this.#moduloActual && this.#moduloSelectEl.options.length === 0
		this.#nuevoModuloNombreEl.disabled = false
		this.#crearModuloEl.disabled = false
	}

	async #inicializarModulos() {
		const data = await this.api.getModulos()
		const nombres = data.items.map((item) => item.name)

		this.#renderSelectorModulos(nombres)

		if (!nombres.length) {
			this.#moduloActual = ''
			this.#vaciarInterfazSinModulo()
			return
		}

		this.#moduloActual = nombres[0]
		this.api.setModulo(this.#moduloActual)
		this.#moduloSelectEl.value = this.#moduloActual
		this.desbloquearCambioModulo()
		await this.#recargarModuloActivo()
	}

	async iniciar(){
		await this.cargarVista()
		this.#referenciarElementosIU()
		this.#registrarEventos()
		await this.#inicializarModulos()
	}

	/* MÉTODOS PRIVADOS */
	async #cargarCalificacionesEnBlanco() {
		//TODO
		/*
		calificacionItemsCache = []
		renderSelectorCalificacionPruebas()
		renderSelectorCalificacionEstudiantes()
		renderTablaCalificaciones([])
		*/
	}

	async #onCambiarModulo(){
		if (this.#cambioModuloBloqueado) {
			return
		}

		const nueva = this.#moduloSelectEl.value
		if (!nueva || nueva === this.#moduloActual) {
			return
		}

		this.#moduloActual = nueva
		this.api.setModulo(this.#moduloActual)
		this.emitirMensaje('cambioModulo')
		this.desbloquearCambioModulo()
		await this.#recargarModuloActivo()
	}

	async #onCrearModulo(){
		const nombre = this.#nuevoModuloNombreEl.value.trim()

		if (!nombre) {
			return
		}

		try {
			const data = await this.api.crearModulo(nombre)
			const creada = data.item.name

			const listado = await this.api.getModulos()
			const nombresModulos = listado.items.map((item) => item.name)

			this.#renderSelectorModulos(nombresModulos)
			this.#moduloActual = creada
			this.#moduloSelectEl.value = creada
			this.api.setModulo(this.#moduloActual)
			this.#nuevoModuloNombreEl.value = ''

			this.emitirMensaje('cambioModulo')
			this.desbloquearCambioModulo()
			await this.#recargarModuloActivo()
		} catch (error) {
			console.error(error)
			this.mostrarError(error.message)
		}
	}

	#referenciarElementosIU(){
		this.#moduloSelectEl = this.div.querySelector('select')
		this.#nuevoModuloNombreEl = this.div.querySelector('input')
		this.#crearModuloEl = this.div.querySelector('button')
		this.#cambioModuloBloqueado = false
	}

	#registrarEventos(){
		this.#moduloSelectEl.addEventListener('change', this.#onCambiarModulo.bind(this))
		this.#crearModuloEl.addEventListener('click', this.#onCrearModulo.bind(this))
	}

	#renderSelectorModulos(names) {
		this.#moduloSelectEl.innerHTML = ''

		if (!names.length) {
			const option = document.createElement('option')
			option.value = ''
			option.textContent = 'No hay módulos'
			this.#moduloSelectEl.appendChild(option)
			this.#moduloSelectEl.disabled = true
			return
		}

		this.#moduloSelectEl.disabled = false

		for (const name of names) {
			const option = document.createElement('option')
			option.value = name
			option.textContent = name
			this.#moduloSelectEl.appendChild(option)
		}
	}

	async #recargarModuloActivo() {
		if (!this.#moduloActual) {
			this.#vaciarInterfazSinModulo()
			return
		}
	}

	#vaciarInterfazSinModulo() {
		//TODO
		/*
		renderTablaEstudiantes([])
		renderTablaResultados([])
		renderTablaIndicadores([])
		renderTablaPruebas([])
		renderTablaCalificaciones([])
		*/
	}

}
