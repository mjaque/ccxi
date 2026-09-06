import { Controlador } from './controlador.js'

export class ControladorCalificaciones extends Controlador{
	URL_VISTA = './html/calificaciones.html'

	#selectActividad
	#selectEstudiante
	#tbodyCalificaciones
	#botonGuardar
	#campoEvaluacion
	#campoBuscarIndicador
	#campoNivelAdd
	#campoIncrementoAdd
	#botonAnadir
	#sugerenciasIndicador
	#indicadorSeleccionado
	pMensaje

	#cacheActividades = []
	#cacheEstudiantes = []

	constructor(div){
		super(div)
		this.recibirMensaje('cambioModulo', this.#cargar.bind(this))
		this.recibirMensaje('cambioActividad', this.#cargar.bind(this))
		this.recibirMensaje('cambioEstudiante', this.#cargar.bind(this))
	}

	async iniciar(){
		await this.cargarVista()
		this.#referenciarElementosIU()
		this.#registrarEventos()
		await this.#cargar()
	}

	async #cargar(){
		const [dataActividades, dataEstudiantes] = await Promise.all([
			this.api.getActividades(),
			this.api.getEstudiantes(),
		])
		this.#cacheActividades = dataActividades.items
		this.#cacheEstudiantes = dataEstudiantes.items
		this.#poblarSelectActividades()
		this.#poblarSelectEstudiantes()
		this.#cargarContexto()
	}

	#poblarSelectActividades(){
		this.#selectActividad.textContent = ''
		const opcionVacia = document.createElement('option')
		opcionVacia.value = ''
		opcionVacia.textContent = '-- Seleccionar actividad --'
		this.#selectActividad.appendChild(opcionVacia)

		for (const actividad of this.#cacheActividades) {
			const option = document.createElement('option')
			option.value = actividad.id
			option.textContent = `${actividad.codigo} - ${actividad.nombre}`
			this.#selectActividad.appendChild(option)
		}
	}

	#poblarSelectEstudiantes(){
		this.#selectEstudiante.textContent = ''
		const opcionVacia = document.createElement('option')
		opcionVacia.value = ''
		opcionVacia.textContent = '-- Seleccionar estudiante --'
		this.#selectEstudiante.appendChild(opcionVacia)

		for (const estudiante of this.#cacheEstudiantes) {
			const option = document.createElement('option')
			option.value = estudiante.id
			option.textContent = estudiante.nombre
			this.#selectEstudiante.appendChild(option)
		}
	}

	async #cargarContexto(){
		const actividadId = Number(this.#selectActividad.value)
		const estudianteId = Number(this.#selectEstudiante.value)

		this.#tbodyCalificaciones.innerHTML = ''
		this.#botonGuardar.hidden = true
		this.#campoEvaluacion.value = ''

		if (!actividadId || !estudianteId)
			return

		try{
			const data = await this.api.getContextoCalificacion(actividadId, estudianteId)
			this.#renderizarIndicadores(data.items)
			this.#campoEvaluacion.value = data.evaluacion || ''
			this.#botonGuardar.hidden = false
		} catch(error){
			console.error(error)
			this.mostrarError('Error al cargar el contexto de calificación.')
		}
	}

	#renderizarIndicadores(items){
		this.#tbodyCalificaciones.innerHTML = ''

		for (const item of items) {
			const tr = document.createElement('tr')

			const tdInfo = document.createElement('td')
			tdInfo.textContent = `${item.indicador_codigo} – ${item.indicador_nombre}`
			tr.appendChild(tdInfo)

			const tdActual = document.createElement('td')
			tdActual.textContent = item.calificacion_actual ?? '-'
			tr.appendChild(tdActual)

			const tdIncremento = document.createElement('td')
			const inputIncremento = document.createElement('input')
			inputIncremento.type = 'number'
			inputIncremento.className = 'calif-incremento'
			inputIncremento.dataset.id = item.id_indicador
			inputIncremento.placeholder = 'Incremento'
			inputIncremento.step = 'any'
			if (item.incremento !== null && item.incremento !== undefined)
				inputIncremento.value = item.incremento
			tdIncremento.appendChild(inputIncremento)
			if (!item.asociado){
				tdIncremento.colSpan = 2
				const botonEliminar = this.crearBotonEliminar()
				botonEliminar.addEventListener('click', () => tr.remove())
				tdIncremento.appendChild(botonEliminar)
			} else {const tdNivel = document.createElement('td')
				const inputNivel = document.createElement('input')
				inputNivel.type = 'number'
				inputNivel.className = 'calif-nivel'
				inputNivel.dataset.id = item.id_indicador
				inputNivel.placeholder = '0-10'
				inputNivel.min = 0
				inputNivel.max = 10
				inputNivel.step = 1
				if (item.nivel_logro !== null && item.nivel_logro !== undefined)
					inputNivel.value = item.nivel_logro
				tdNivel.appendChild(inputNivel)
				tr.appendChild(tdNivel)
			}
			tr.appendChild(tdIncremento)

			this.#tbodyCalificaciones.appendChild(tr)
		}
	}

	async #guardar(){
		const actividadId = Number(this.#selectActividad.value)
		const estudianteId = Number(this.#selectEstudiante.value)

		if (!actividadId || !estudianteId)
			return

		const inputs = this.#tbodyCalificaciones.querySelectorAll('tr')
		const items = []

		for (const fila of inputs) {
			const inputNivel = fila.querySelector('.calif-nivel')
			const inputIncremento = fila.querySelector('.calif-incremento')
			if (!inputIncremento) continue
			const id = Number(inputIncremento.dataset.id)
			const nivelVal = inputNivel ? inputNivel.value.trim() : ''
			const incVal = inputIncremento.value.trim()

			const nivel = nivelVal !== '' ? Number(nivelVal) : null
			const incremento = incVal !== '' ? Number(incVal) : null

			if (nivel !== null && (nivel < 0 || nivel > 10)){
				this.mostrarError('El nivel de logro debe estar entre 0 y 10.')
				return
			}

			if (nivel === null && incremento === null)
				continue

			items.push({
				id_indicador: id,
				nivel_logro: nivel,
				incremento: incremento,
			})
		}

		try{
			await this.api.guardarCalificacion(
				actividadId,
				estudianteId,
				items,
				this.#campoEvaluacion.value.trim() || null,
			)
			this.mostrarInformacion('Calificaciones guardadas correctamente.')
			await this.#cargarContexto()
		} catch(error){
			console.error(error)
			this.mostrarError(error.message || 'Error al guardar las calificaciones.')
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

			const idsEnTabla = new Set()
			for (const tr of this.#tbodyCalificaciones.querySelectorAll('tr')) {
				const input = tr.querySelector('.calif-nivel, .calif-incremento')
				if (input) idsEnTabla.add(Number(input.dataset.id))
			}

			const disponibles = data.items.filter(i => !idsEnTabla.has(i.id))

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
		this.#campoBuscarIndicador.value = `${indicador.codigo} - ${indicador.nombre}`
		this.#sugerenciasIndicador.innerHTML = ''
		this.#sugerenciasIndicador.style.display = 'none'
	}

	#anadirIndicadorACalificacion(){
		if (!this.#indicadorSeleccionado){
			this.mostrarError('Selecciona un indicador de la lista de sugerencias.')
			return
		}

		const idsEnTabla = new Set()
		for (const tr of this.#tbodyCalificaciones.querySelectorAll('tr')) {
			const input = tr.querySelector('.calif-nivel, .calif-incremento')
			if (input) idsEnTabla.add(Number(input.dataset.id))
		}
		if (idsEnTabla.has(this.#indicadorSeleccionado.id)){
			this.mostrarError('Este indicador ya está en la tabla.')
			return
		}

		const incVal = this.#campoIncrementoAdd.value.trim()
		const incremento = incVal !== '' ? Number(incVal) : null

		const tr = document.createElement('tr')

		const tdInfo = document.createElement('td')
		tdInfo.textContent = `${this.#indicadorSeleccionado.codigo} – ${this.#indicadorSeleccionado.nombre}`
		tr.appendChild(tdInfo)

		const tdActual = document.createElement('td')
		tdActual.textContent = '-'
		tr.appendChild(tdActual)

		const tdIncremento = document.createElement('td')
		tdIncremento.colSpan = 2
		const inputIncremento = document.createElement('input')
		inputIncremento.type = 'number'
		inputIncremento.className = 'calif-incremento'
		inputIncremento.dataset.id = this.#indicadorSeleccionado.id
		inputIncremento.placeholder = 'Incremento'
		inputIncremento.step = 'any'
		if (incremento !== null) inputIncremento.value = incremento
		tdIncremento.appendChild(inputIncremento)
		const botonEliminar = this.crearBotonEliminar()
		botonEliminar.addEventListener('click', () => tr.remove())
		tdIncremento.appendChild(botonEliminar)
		tr.appendChild(tdIncremento)

		this.#tbodyCalificaciones.appendChild(tr)

		this.#indicadorSeleccionado = null
		this.#campoBuscarIndicador.value = ''
		this.#campoIncrementoAdd.value = ''
		this.mostrarInformacion('')
	}

	#referenciarElementosIU(){
		this.#selectActividad = this.div.querySelector('#calificaciones-actividad')
		this.#selectEstudiante = this.div.querySelector('#calificaciones-estudiante')
		this.#tbodyCalificaciones = this.div.querySelector('#calificaciones-tbody')
		this.#botonGuardar = this.div.querySelector('#calificaciones-guardar')
		this.#campoEvaluacion = this.div.querySelector('#calificaciones-evaluacion')
		this.#campoBuscarIndicador = this.div.querySelector('#calif-buscar')
		this.#campoNivelAdd = this.div.querySelector('#calif-nivel-add')
		this.#campoIncrementoAdd = this.div.querySelector('#calif-incremento-add')
		this.#botonAnadir = this.div.querySelector('#calif-anadir')
		this.#sugerenciasIndicador = this.div.querySelector('#calif-sugerencias')
		this.pMensaje = this.div.querySelector('#calificaciones-mensaje')
	}

	#registrarEventos(){
		this.#selectActividad.addEventListener('change', this.#cargarContexto.bind(this))
		this.#selectEstudiante.addEventListener('change', this.#cargarContexto.bind(this))
		this.#botonGuardar.addEventListener('click', this.#guardar.bind(this))
		this.#campoBuscarIndicador.addEventListener('input', this.#buscarIndicadores.bind(this))
		this.#botonAnadir.addEventListener('click', this.#anadirIndicadorACalificacion.bind(this))
	}
}
