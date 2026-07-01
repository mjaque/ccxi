import { Controlador } from './controlador.js'
import { Estudiante } from '../modelos/estudiante.js'

export class ControladorEstudiantes extends Controlador{
	URL_VISTA = './html/estudiantes.html'

	//Elementos del IU
	#inputId
	#inputNombre
	#botonGuardar
	#botonCancelar
	pMensaje
	#tbody

	//Registros
	#cache = []

	constructor(div){
		super(div)
		this.recibirMensaje('cambioModulo', function() {
			this.#cargar()
		}.bind(this))
	}

	async iniciar(){
		await this.cargarVista()
		this.#referenciarElementosIU()
		this.#registrarEventos()
		await this.#cargar()
	}

	/* MÉTODOS PRIVADOS */
	async #cargar(){
		const data = await this.api.getEstudiantes()
		this.#cache = data.items
		this.#cargarTabla()
	}

	#cargarTabla(){
		this.#tbody.innerHTML = ''

		if (this.#cache.length == 0){
    		const tr = document.createElement('tr')
			this.#tbody.appendChild(tr)
			const td = document.createElement('td')
			tr.appendChild(td)
			td.setAttribute('colspan', 2)
			td.textContent = 'No hay estudiantes registrados en este módulo.'
			return
		}
		//Cargamos la tabla con los estudiantes
		for (const estudiante of this.#cache) {
    		const tr = document.createElement('tr')
			this.#tbody.appendChild(tr)
			/* const tdId = document.createElement('td')
			tr.appendChild(tdId)
			tdId.textContent = estudiante.id */
			const tdNombre = document.createElement('td')
			tr.appendChild(tdNombre)
			tdNombre.textContent = estudiante.nombre
			const tdAcciones = document.createElement('td')
			tr.appendChild(tdAcciones)

			const botonEditar = this.crearBotonEditar()
			tdAcciones.appendChild(botonEditar)
			botonEditar.addEventListener('click', this.#editar.bind(this, estudiante))

			const botonEliminar = this.crearBotonEliminar()
			tdAcciones.appendChild(botonEliminar)
			botonEliminar.addEventListener('click', this.#eliminar.bind(this, estudiante))
		}
	}

	#editar(estudiante){
		this.#inputId.value = estudiante.id
		this.#inputNombre.value = estudiante.nombre
		this.#botonCancelar.hidden = false
		this.#inputNombre.focus()
	}

	async #eliminar(estudiante){
		const confirmado = window.confirm(`¿Quieres eliminar a "${estudiante.nombre}"?`)
		if (!confirmado)
			return

		try{
			await this.api.eliminarEstudiante(estudiante.id)
			this.mostrarInformacion('Estudiante eliminado/a correctamente.')
			this.emitirMensaje('cambioEstudiante')
			this.#cargar()
		} catch(error) {
			console.log(error)
			this.mostrarError('Error al eliminar la/el estudiante.')
		}
	}

	async #guardar(){
		const id = this.#inputId.value
		const nombre = this.#inputNombre.value.trim()
		if (!nombre){
			this.mostrarError('El nombre del estudiante es obligatorio.')
			return
		}

		try{
			const estudiante = new Estudiante(id, nombre)

			if (estudiante.id) {
				await this.api.actualizarEstudiante(estudiante)
				this.mostrarInformacion('Estudiante/a actualizado correctamente.')
			}
			else {
				await this.api.insertarEstudiante(estudiante)
				this.mostrarInformacion('Estudiante/a creado correctamente.')
			}
			this.emitirMensaje('cambioEstudiante')
			this.#limpiar()
			this.#cargar()
		} catch(error) {
			console.log(error)
			this.mostrarError('Error al guardar el/la estudiante')
		}
	}

	#limpiar(){
		this.#inputId.value = ''
		this.#inputNombre.value = ''
		this.#botonCancelar.hidden = true
	}

	#referenciarElementosIU(){
		this.#inputId = this.div.querySelector('input[type="hidden"]')
		this.#inputNombre = this.div.querySelectorAll('input')[1]
		this.#botonGuardar = this.div.querySelector('button')
		this.#botonCancelar = this.div.querySelectorAll('button')[1]
		this.pMensaje = this.div.querySelector('p.mensaje')
		this.#tbody = this.div.querySelector('tbody')
	}

	#registrarEventos(){
		this.#botonGuardar.addEventListener('click', this.#guardar.bind(this))
		this.#botonCancelar.addEventListener('click', this.#limpiar.bind(this))
	}

}

