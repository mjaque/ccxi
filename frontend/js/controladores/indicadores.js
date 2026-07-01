import { Controlador } from './controlador.js'
import { Resultado } from '../modelos/resultado.js'
import { Indicador } from '../modelos/indicador.js'

export class ControladorIndicadores extends Controlador{
	URL_VISTA = './html/indicadores.html'

	//Elementos del IU
	#campoId
	#campoCodigo
	#campoNombre
	#selectResultado
	#campoPesoResultado
	#botonAnadirResultado
	#tbodyResultadosAsociados
	pMensaje
	#botonGuardar
	#botonCancelar
	#tbodyIndicadores
	#campoBuscador

	//Registros
	#cacheIndicadores = []
	#cacheResultados= new Map()
	#cacheResultadosAsociados = []

	constructor(div){
		super(div)
		this.recibirMensaje('cambioModulo', this.#cargar.bind(this))
		this.recibirMensaje('cambioResultado', this.#cargar.bind(this))
	}

	async iniciar(){
		await this.cargarVista()
		this.#referenciarElementosIU()
		this.#registrarEventos()
		await this.#cargar()
	}

	/* MÉTODOS PRIVADOS */
	async #cargar(){
		const dataIndicadores = await this.api.getIndicadores()
		this.#cacheIndicadores = dataIndicadores.items
		this.#cargarTablaIndicadores()
		this.#cargarSelectResultados()
	}

	async #cargarSelectResultados(){
		const resultados = await this.api.getResultados()
		this.#cacheResultados.clear()
		this.#selectResultado.textContent = ''
		for (const resultado of resultados.items) {
			const option = document.createElement('option')
			option.value = resultado.id
			option.textContent = resultado.codigo
			this.#selectResultado.appendChild(option)
			this.#cacheResultados.set(resultado.id, new Resultado(resultado.id, resultado.codigo, resultado.nombre, resultado.peso))
		}
	}

	#leerResultados(indicador){
		if (!indicador.resultados || indicador.resultados.length == 0)
			return '-'
		return indicador.resultados.map((r) => `${r.codigo}`).join(', ')
	}

	#cargarTablaIndicadores(){
		this.#tbodyIndicadores.innerHTML = ''

		const texto = (this.#campoBuscador?.value || '').toLowerCase().trim()
		const datos = texto
			? this.#cacheIndicadores.filter(i => {
				const enCodigo = i.codigo.toLowerCase().includes(texto)
				const enNombre = i.nombre.toLowerCase().includes(texto)
				const enResultados = (i.resultados || []).some(r =>
					r.codigo.toLowerCase().includes(texto) ||
					r.nombre.toLowerCase().includes(texto)
				)
				return enCodigo || enNombre || enResultados
			})
			: this.#cacheIndicadores

		if (datos.length == 0){
    		const tr = document.createElement('tr')
			this.#tbodyIndicadores.appendChild(tr)
			const td = document.createElement('td')
			tr.appendChild(td)
			td.setAttribute('colspan', 5)
			td.textContent = texto
				? 'No hay indicadores que coincidan con la búsqueda.'
				: 'No hay indicadores de logro registrados en este módulo.'
			return
		}
		const campos = [ 'codigo', 'nombre' ]
		for (const indicador of datos) {
    		const tr = document.createElement('tr')
			this.#tbodyIndicadores.appendChild(tr)
			campos.forEach( campo => {
				const td = document.createElement('td')
				tr.appendChild(td)
				td.textContent = indicador[campo]
			})
			const tdResultados = document.createElement('td')
			tr.appendChild(tdResultados)
			tdResultados.textContent = this.#leerResultados(indicador)
			const tdAcciones = document.createElement('td')
			tr.appendChild(tdAcciones)

			const botonEditar = this.crearBotonEditar()
			tdAcciones.appendChild(botonEditar)
			botonEditar.addEventListener('click', this.#editarIndicador.bind(this, indicador))

			const botonEliminar = this.crearBotonEliminar()
			tdAcciones.appendChild(botonEliminar)
			botonEliminar.addEventListener('click', this.#eliminarIndicador.bind(this, indicador))
		}
	}

	#anadirResultado(){
		const option = this.#selectResultado.selectedOptions[0]
		if (!option) return

		const resultadoId = Number(option.value)
		const peso = Number(this.#campoPesoResultado.value)

		if (!peso || peso < 0){
			this.mostrarError('El peso debe ser un número positivo.')
			return
		}

		if (this.#cacheResultadosAsociados.some(r => r.id === resultadoId)){
			this.mostrarError('Este resultado ya está asociado.')
			return
		}

		this.#cacheResultadosAsociados.push({
			'id': resultadoId,
			'peso': peso})

		this.#campoPesoResultado.value = ''
		this.#cargarTablaResultadosAsociados()
		this.mostrarInformacion('')
	}

	#cargarTablaResultadosAsociados(){
		this.#tbodyResultadosAsociados.textContent = ''

		for (const resultadoAsociado of this.#cacheResultadosAsociados) {
			const tr = document.createElement('tr')
			this.#tbodyResultadosAsociados.appendChild(tr)

			const resultado = this.#cacheResultados.get(resultadoAsociado.id)

			const tdCodigo = document.createElement('td')
			tr.appendChild(tdCodigo)
			tdCodigo.textContent = `${resultado.codigo}: ${resultado.nombre}`

			const tdPeso = document.createElement('td')
			tr.appendChild(tdPeso)
			tdPeso.textContent = resultadoAsociado.peso

			const tdAccion = document.createElement('td')
			tr.appendChild(tdAccion)

			const botonEliminar = this.crearBotonEliminar()
			tdAccion.appendChild(botonEliminar)
			botonEliminar.title = 'Desasociar resultado'
			botonEliminar.addEventListener('click', this.#eliminarResultadoAsociado.bind(this, resultadoAsociado))
		}
	}

	#eliminarResultadoAsociado(resultado){
		this.#cacheResultadosAsociados = this.#cacheResultadosAsociados.filter(r => r.id !== resultado.id)
		this.#cargarTablaResultadosAsociados()
	}

	#editarIndicador(indicador){
		this.#campoId.value = indicador.id
		this.#campoCodigo.value = indicador.codigo
		this.#campoNombre.value = indicador.nombre
		this.#cacheResultadosAsociados = (indicador.resultados || []).map(r => ({ id: r.id, peso: r.peso }))
		this.#cargarTablaResultadosAsociados()
		this.#botonCancelar.hidden = false
		this.#campoCodigo.focus()
	}

	async #eliminarIndicador(indicador){
		if (!confirm(`¿Quiere ELIMINAR el indicador ${indicador.codigo}?`))
			return
		try{
			await this.api.eliminarIndicador(indicador.id)
			this.emitirMensaje('cambioIndicador')
			this.mostrarInformacion('Indicador eliminado correctamente.')
			this.#cargar()
			this.#limpiar()
		}
		catch (error) {
			console.error(error)
			this.mostrarError(error.message)
		}
	}

	async #guardarIndicador(){
		const id = this.#campoId.value ? Number(this.#campoId.value.trim()) : null
		const codigo = this.#campoCodigo.value.trim()
		const nombre = this.#campoNombre.value.trim()

		if (codigo.length < 3){
			this.mostrarError('El código debe tener al menos 3 caracteres.')
			return
		}
		if (nombre.length < 3){
			this.mostrarError('El nombre debe tener al menos 3 caracteres.')
			return
		}

		const indicador = new Indicador(id, codigo, nombre, this.#cacheResultadosAsociados)

		try{
			if (id){
				await this.api.actualizarIndicador(indicador)
				this.mostrarInformacion('Indicador actualizado correctamente.')
			} else {
				await this.api.crearIndicador(indicador)
				this.mostrarInformacion('Indicador creado correctamente.')
			}
			this.emitirMensaje('cambioIndicador')
			this.#limpiar()
			this.#cargar()
		} catch(error){
			this.mostrarError(error.message)
		}
	}

	#limpiar(){
		this.#campoId.value = ''
		this.#campoCodigo.value = ''
		this.#campoNombre.value = ''
		this.#cacheResultadosAsociados = []
		this.#cargarTablaResultadosAsociados()
		this.#botonCancelar.hidden = true
	}

	#referenciarElementosIU(){
		this.#campoId = this.div.querySelector('#indicador-id')
		this.#campoCodigo = this.div.querySelector('#indicador-codigo')
		this.#campoNombre = this.div.querySelector('#indicador-nombre')
		this.#selectResultado = this.div.querySelector('#indicador-resultado-select')
		this.#campoPesoResultado = this.div.querySelector('#indicador-resultado-peso')
		this.#botonAnadirResultado = this.div.querySelector('#indicador-anadir-resultado')
		this.#tbodyResultadosAsociados = this.div.querySelector('#indicador-resultados-tabla')
		this.pMensaje = this.div.querySelector('#indicador-mensaje')
		this.#botonGuardar = this.div.querySelector('#indicador-guardar')
		this.#botonCancelar = this.div.querySelector('#cancelar-edicion-indicador')
		this.#tbodyIndicadores = this.div.querySelector('#indicador-tabla')
		this.#campoBuscador = this.div.querySelector('#indicador-buscador')
	}

	#registrarEventos(){
		this.#botonAnadirResultado.addEventListener('click', this.#anadirResultado.bind(this))
		this.#botonGuardar.addEventListener('click', this.#guardarIndicador.bind(this))
		this.#botonCancelar.addEventListener('click', this.#limpiar.bind(this))
		this.#campoBuscador.addEventListener('input', this.#cargarTablaIndicadores.bind(this))
	}

}
