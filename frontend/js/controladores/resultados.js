import { Controlador } from './controlador.js'
import { Resultado } from '../modelos/resultado.js'

export class ControladorResultados extends Controlador{
	URL_VISTA = './html/resultados.html'

	//Elementos del IU
	#campoId
	#campoCodigo
	#campoNombre
	#campoPeso
	pMensaje
	#botonGuardar
	#botonCancelar
	#tbodyResultados

	//Registros
	#cacheResultados = []

	constructor(div){
		super(div)
		this.recibirMensaje('cambioModulo', this.#cargar.bind(this))
	}

	async iniciar(){
		await this.cargarVista()
		this.#referenciarElementosIU()
		this.#registrarEventos()
		await this.#cargar()
	}

	/* MÉTODOS PRIVADOS */
	async #cargar(){
		const dataResultados = await this.api.getResultados()
		this.#cacheResultados = dataResultados.items
		this.#cargarTablaResultados()
	}

	#cargarTablaResultados(){
		this.#tbodyResultados.innerHTML = ''

		if (this.#cacheResultados.length == 0){
    		const tr = document.createElement('tr')
			this.#tbodyResultados.appendChild(tr)
			const td = document.createElement('td')
			tr.appendChild(td)
			td.setAttribute('colspan', 4)
			td.textContent = 'No hay resultados de aprendizaje registrados en este módulo.'
			return
		}
		const campos = [ 'codigo', 'nombre', 'peso' ]
		for (const resultado of this.#cacheResultados) {
    		const tr = document.createElement('tr')
			this.#tbodyResultados.appendChild(tr)
			campos.forEach( campo => {
				const td = document.createElement('td')
				tr.appendChild(td)
				td.textContent = resultado[campo]
			})
			const tdAcciones = document.createElement('td')
			tr.appendChild(tdAcciones)

			const botonEditar = this.crearBotonEditar()
			tdAcciones.appendChild(botonEditar)
			botonEditar.addEventListener('click', this.#editarResultado.bind(this, resultado))

			const botonEliminar = this.crearBotonEliminar()
			tdAcciones.appendChild(botonEliminar)
			botonEliminar.addEventListener('click', this.#eliminarResultado.bind(this, resultado))
		}
	}

	#editarResultado(resultado){
		this.#campoId.value = resultado.id
		this.#campoCodigo.value = resultado.codigo
		this.#campoNombre.value = resultado.nombre
		this.#campoPeso.value = resultado.peso
		this.#botonCancelar.hidden = false
		this.#campoCodigo.focus()
	}

	async #eliminarResultado(resultado){
		if (!confirm(`¿Quiere ELIMINAR el resultado ${resultado.codigo}?`))
			return
		try{
			await this.api.eliminarResultado(resultado.id)
			this.emitirMensaje('cambioResultado')
			this.mostrarInformacion('El Resultado se ha eliminado correctamente.')
			this.#cargarTablaResultados()
			this.#limpiar()
			this.#campoCodigo.focus()
		}
		catch (error) {
			console.error(error)
			this.mostrarError(error.message)
		}
	}

	async #guardar(){
		const id = this.#campoId.value ? Number(this.#campoId.value.trim()) : null
		const codigo = this.#campoCodigo.value.trim()
		const nombre = this.#campoNombre.value.trim()
		const peso = Number(this.#campoPeso.value.trim())

		const error = []
		if (codigo.length < 3){
			error.push('El código debe tener una longitud mínima de 3 caracteres.')
		}
		if (nombre.length < 3){
			error.push('El nombre debe tener una longitud mínima de 3 caracteres.')
		}
		if (peso < 0){
			error.push('El peso debe ser positivo.')
		}
		if (error.length > 0){
			this.mostrarError(error.join(' '))
			return
		}

		try{
			if (id){
				await this.api.actualizarResultado(new Resultado(id, codigo, nombre, peso))
				this.mostrarInformacion('El Resultado se ha actualizado correctamente.')
			}
			else{
				await this.api.crearResultado(new Resultado(id, codigo, nombre, peso))
				this.mostrarInformacion('El Resultado se ha creado correctamente.')
			}
			this.emitirMensaje('cambioResultado')
			this.#limpiar()
			this.#campoCodigo.focus()
		}
		catch (error) {
			console.error(error)
			this.mostrarError(error.message)
		}
	}

	#limpiar(){
		this.#campoId.value = ''
		this.#campoCodigo.value = ''
		this.#campoNombre.value = ''
		this.#campoPeso.value = ''
		this.#botonCancelar.hidden = true
		this.#cargar()
	}

	#referenciarElementosIU(){
		this.#campoId = this.div.querySelector('#resultado-id')
		this.#campoCodigo = this.div.querySelector('#resultado-codigo')
		this.#campoNombre = this.div.querySelector('#resultado-nombre')
		this.#campoPeso = this.div.querySelector('#resultado-peso')
		this.pMensaje = this.div.querySelector('#resultado-mensaje')
		this.#botonGuardar = this.div.querySelector('#resultado-guardar')
		this.#botonCancelar = this.div.querySelector('#resultado-cancelar')
		this.#tbodyResultados = this.div.querySelector('#resultado-tabla')
	}

	#registrarEventos(){
		this.#botonGuardar.addEventListener('click', this.#guardar.bind(this))
		this.#botonCancelar.addEventListener('click', this.#limpiar.bind(this))
	}

}
