import { Controlador } from './controlador.js'

export class ControladorActividades extends Controlador{
	URL_VISTA = './html/actividades.html'

	//Elementos del IU
	#tbodyActividades
	#tbodyIndicadores
	#campoBuscarIndicador
	#sugerenciasIndicador
	#campoIdIndicadorSeleccionado
	#campoIndicadorSeleccionado
	#selectTipoCalificacion
	#inputPeso
	#botonAnadirIndicador
	#botonGuardar
	#botonCancelar
	#campoBuscador
	#indicadorSeleccionado
	#inputId
	#inputCodigo
	#inputNombre
	#inputFecha
	pMensaje

	//Registros
	#cache = []
	#cacheIndicadoresAsociados = []

	constructor(div){
		super(div)
		this.recibirMensaje('cambioModulo', this.#cargar.bind(this))
		this.recibirMensaje('cambioIndicador', this.#cargar.bind(this))
	}

	async iniciar(){
		await this.cargarVista()
		this.#referenciarElementosIU()
		this.#registrarEventos()
		await this.#cargar()
	}

	/* MÉTODOS PRIVADOS */
	async #cargar(){
		const data = await this.api.getActividades()
		this.#cache = data.items
		this.#cargarTabla()
	}

	#cargarTabla(){
		this.#tbodyActividades.innerHTML = ''

		const texto = (this.#campoBuscador?.value || '').toLowerCase().trim()
		const datos = texto
			? this.#cache.filter(a => {
				const enCodigo = a.codigo.toLowerCase().includes(texto)
				const enNombre = a.nombre.toLowerCase().includes(texto)
				const enFecha = (a.fecha || '').toLowerCase().includes(texto)
				const enIndicadores = (a.indicadores || []).some(i =>
					i.codigo.toLowerCase().includes(texto) ||
					i.nombre.toLowerCase().includes(texto)
				)
				return enCodigo || enNombre || enFecha || enIndicadores
			})
			: this.#cache

		if (datos.length == 0){
    		const tr = document.createElement('tr')
			this.#tbodyActividades.appendChild(tr)
			const td = document.createElement('td')
			tr.appendChild(td)
			td.setAttribute('colspan', 5)
			td.textContent = texto
				? 'No hay actividades que coincidan con la búsqueda.'
				: 'No hay ninguna actividad registrada en este módulo.'
			return
		}
		//Cargamos la tabla con las actividades
		const campos = [ 'codigo', 'nombre', 'fecha' ]
		for (const actividad of datos) {
    		const tr = document.createElement('tr')
			this.#tbodyActividades.appendChild(tr)
			campos.forEach( campo => {
				const td = document.createElement('td')
				tr.appendChild(td)
				td.textContent = actividad[campo]
			})
			const tdIndicadores = document.createElement('td')
			tr.appendChild(tdIndicadores)
			tdIndicadores.textContent = this.#leerIndicadores(actividad)
			const tdAcciones = document.createElement('td')
			tr.appendChild(tdAcciones)

			const botonEditar = this.crearBotonEditar()
			tdAcciones.appendChild(botonEditar)
			botonEditar.addEventListener('click', this.#editar.bind(this, actividad))

			const botonEliminar = this.crearBotonEliminar()
			tdAcciones.appendChild(botonEliminar)
			botonEliminar.addEventListener('click', this.#eliminar.bind(this, actividad))
		}
	}

	#editar(actividad){
		this.#inputId.value = actividad.id
		this.#inputCodigo.value = actividad.codigo
		this.#inputNombre.value = actividad.nombre
		this.#inputFecha.value = actividad.fecha || ''
		this.#cacheIndicadoresAsociados = (actividad.indicadores || []).map(i => ({
			id: i.id,
			codigo: i.codigo,
			nombre: i.nombre,
			tipoCalificacion: i.tipo_calificacion || 'ponderada',
			peso: i.peso,
		}))
		this.#cargarTablaIndicadoresAsociados()
		this.#botonCancelar.hidden = false
		this.#inputCodigo.focus()
	}

	async #eliminar(actividad){
		const confirmado = window.confirm(`¿Quieres eliminar la actividad "${actividad.nombre}"?`)
		if (!confirmado)
			return

		try{
			await this.api.eliminarActividad(actividad.id)
			this.mostrarInformacion('Actividad eliminada correctamente.')
			this.emitirMensaje('cambioActividad')
			this.#cargar()
		} catch(error) {
			console.error(error)
			this.mostrarError('Error al eliminar la actividad.')
		}
	}

	async #guardar(){
		const id = this.#inputId.value
		const codigo = this.#inputCodigo.value.trim()
		const nombre = this.#inputNombre.value.trim()
		const fecha = this.#inputFecha.value.trim() || null

		if (!codigo){
			this.mostrarError('El código de actividad es obligatorio.')
			return
		}
		if (!nombre){
			this.mostrarError('El nombre de actividad es obligatorio.')
			return
		}

		const indicadores = this.#cacheIndicadoresAsociados.map(i => ({
			id_indicador: i.id,
			tipo_calificacion: i.tipoCalificacion,
			peso: i.peso,
		}))

		const data = { codigo, nombre, fecha, indicadores }

		try{
			if (id) {
				await this.api.actualizarActividad(id, data)
				this.mostrarInformacion('Actividad actualizada correctamente.')
			}
			else {
				await this.api.insertarActividad(data)
				this.mostrarInformacion('Actividad creada correctamente.')
			}
			this.emitirMensaje('cambioActividad')
			this.#limpiar()
			this.#cargar()
		} catch(error) {
			console.error(error)
			this.mostrarError('Error al guardar la actividad.')
		}
	}

	async #buscarIndicadores(){
		const texto = this.#campoBuscarIndicador.value.trim()

		if (texto.length < 3){
			this.#sugerenciasIndicador.innerHTML = ''
			this.#sugerenciasIndicador.style.display = 'none'
			return
		}

		try{
			const data = await this.api.buscarIndicadores(texto)
			this.#sugerenciasIndicador.innerHTML = ''

			const idsAsociados = new Set(this.#cacheIndicadoresAsociados.map(i => i.id))
			const disponibles = data.items.filter(i => !idsAsociados.has(i.id))

			for (const indicador of disponibles) {
				const div = document.createElement('div')
				div.className = 'item-sugerencia'
				div.textContent = `${indicador.codigo} - ${indicador.nombre}`
				div.addEventListener('click', () => this.#seleccionarIndicador(indicador))
				this.#sugerenciasIndicador.appendChild(div)
			}

			this.#sugerenciasIndicador.style.display = disponibles.length > 0 ? 'block' : 'none'
		} catch(error){
			console.error(error)
		}
	}

	#seleccionarIndicador(indicador){
		this.#indicadorSeleccionado = indicador
		this.#campoIdIndicadorSeleccionado.value = indicador.id
		this.#campoIndicadorSeleccionado.value = `${indicador.codigo} - ${indicador.nombre}`
		this.#campoBuscarIndicador.value = ''
		this.#sugerenciasIndicador.innerHTML = ''
		this.#sugerenciasIndicador.style.display = 'none'
	}

	#anadirIndicador(){
		if (!this.#indicadorSeleccionado){
			this.mostrarError('Debes seleccionar un indicador.')
			return
		}

		if (this.#cacheIndicadoresAsociados.some(i => i.id === this.#indicadorSeleccionado.id)){
			this.mostrarError('Este indicador ya está asociado.')
			return
		}

		const esPonderada = this.#selectTipoCalificacion.value === 'ponderada'
		this.#cacheIndicadoresAsociados.push({
			id: this.#indicadorSeleccionado.id,
			codigo: this.#indicadorSeleccionado.codigo,
			nombre: this.#indicadorSeleccionado.nombre,
			tipoCalificacion: this.#selectTipoCalificacion.value,
			peso: esPonderada && this.#inputPeso.value !== '' ? Number(this.#inputPeso.value) : null,
		})

		this.#indicadorSeleccionado = null
		this.#campoIdIndicadorSeleccionado.value = ''
		this.#campoIndicadorSeleccionado.value = ''
		this.#cargarTablaIndicadoresAsociados()
		this.mostrarInformacion('')
	}

	#cargarTablaIndicadoresAsociados(){
		this.#tbodyIndicadores.textContent = ''

		for (const item of this.#cacheIndicadoresAsociados) {
			const tr = document.createElement('tr')
			this.#tbodyIndicadores.appendChild(tr)

			const tdIndicador = document.createElement('td')
			tr.appendChild(tdIndicador)
			tdIndicador.textContent = `${item.codigo}: ${item.nombre}`

			const tdTipo = document.createElement('td')
			tr.appendChild(tdTipo)
			tdTipo.textContent = item.tipoCalificacion

			const tdPeso = document.createElement('td')
			tr.appendChild(tdPeso)
			tdPeso.textContent = item.peso ?? '—'

			const tdAccion = document.createElement('td')
			tr.appendChild(tdAccion)

			const botonEliminar = this.crearBotonEliminar()
			tdAccion.appendChild(botonEliminar)
			botonEliminar.title = 'Desasociar indicador'
			botonEliminar.addEventListener('click', () => this.#eliminarIndicadorAsociado(item))
		}
	}

	#eliminarIndicadorAsociado(item){
		this.#cacheIndicadoresAsociados = this.#cacheIndicadoresAsociados.filter(i => i.id !== item.id)
		this.#cargarTablaIndicadoresAsociados()
	}

	#leerIndicadores(actividad){
		if (!actividad.indicadores || actividad.indicadores.length == 0)
			return '-'
		return actividad.indicadores.map((indicador) => `${indicador.codigo}`).join(', ')
	}

	#limpiar(){
		this.#inputId.value = ''
		this.#inputCodigo.value = ''
		this.#inputNombre.value = ''
		this.#inputFecha.value = ''
		this.#botonCancelar.hidden = true
		this.#cacheIndicadoresAsociados = []
		this.#selectTipoCalificacion.value = 'ponderada'
		this.#inputPeso.value = ''
		this.#inputPeso.disabled = false
		this.#cargarTablaIndicadoresAsociados()
		this.mostrarInformacion('')
	}

	#togglePeso(){
		const esPonderada = this.#selectTipoCalificacion.value === 'ponderada'
		this.#inputPeso.disabled = !esPonderada
		if (!esPonderada) this.#inputPeso.value = ''
	}

	#referenciarElementosIU(){
		this.#tbodyActividades = this.div.querySelector('#tabla-actividades')
		this.#tbodyIndicadores = this.div.querySelector('#actividad-tabla-indicadores')
		this.#campoBuscarIndicador = this.div.querySelector('#actividad-buscar-indicador')
		this.#sugerenciasIndicador = this.div.querySelector('#actividad-sugerencias-indicador')
		this.#campoIdIndicadorSeleccionado = this.div.querySelector('#actividad-id-indicador-seleccionado')
		this.#campoIndicadorSeleccionado = this.div.querySelector('#actividad-indicador-seleccionado')
		this.#selectTipoCalificacion = this.div.querySelector('#actividad-tipo-calificacion')
		this.#inputPeso = this.div.querySelector('#actividad-peso')
		this.#botonAnadirIndicador = this.div.querySelector('#actividad-anadir-indicador')
		this.#botonGuardar = this.div.querySelector('#actividad-guardar')
		this.#botonCancelar = this.div.querySelector('#actividad-cancelar-edicion')
		this.#inputId = this.div.querySelector('#actividad-id')
		this.#inputCodigo = this.div.querySelector('#actividad-codigo')
		this.#inputNombre = this.div.querySelector('#actividad-nombre')
		this.#inputFecha = this.div.querySelector('#actividad-fecha')
		this.#campoBuscador = this.div.querySelector('#actividad-buscador')
		this.pMensaje= this.div.querySelector('#actividad-mensaje')
	}

	#registrarEventos(){
		this.#campoBuscarIndicador.addEventListener('input', this.#buscarIndicadores.bind(this))
		this.#selectTipoCalificacion.addEventListener('change', this.#togglePeso.bind(this))
		this.#botonAnadirIndicador.addEventListener('click', this.#anadirIndicador.bind(this))
		this.#botonGuardar.addEventListener('click', this.#guardar.bind(this))
		this.#botonCancelar.addEventListener('click', this.#limpiar.bind(this))
		this.#campoBuscador.addEventListener('input', this.#cargarTabla.bind(this))
	}

}
