export class API{
	//Actúa como Singleton
	static #instancia = null

	#modulo
	#URL_ESTADO = '/api/health'
	#URL_MODULOS = '/api/modulos'
	#URL_ESTUDIANTES = '/api/estudiantes'
	#URL_RESULTADOS = '/api/resultados'
	#URL_INDICADORES = '/api/indicadores'
	#URL_ACTIVIDADES = '/api/actividades'

	constructor(){
		if (API.#instancia == null)
			API.#instancia = this
		return API.#instancia
	}

	getInstancia(){
		if (API.#instancia == null)
			new API()
		return API.#instancia()
	}

	async #pedir(url, options = {}) {
		const headers = {
			'Content-Type': 'application/json',
			...(options.headers || {})
		}

		if (!url.startsWith('/api/health') && this.#modulo) {
			headers['X-CCXI-Modulo'] = this.#modulo
		}

		const response = await fetch(url, {
			...options,
			headers
		})

		const data = await response.json()

		if (!response.ok) {
			throw new Error(data.error || 'Error en la petición')
		}

		return data
	}

	/* MÉTODOS PÚBLICOS */

	// Estado
	async comprobarServidor(){
		return this.#pedir(this.#URL_ESTADO)
	}

	// Módulos
	async crearModulo(nombre) {
		return this.#pedir(this.#URL_MODULOS, {
			method: 'POST',
			body: JSON.stringify({ nombre })
		})
	}

	async getModulos() {
		return this.#pedir(this.#URL_MODULOS)
	}

	setModulo(modulo){
		this.#modulo = modulo
	}

	// Estudiantes
	async actualizarEstudiante(estudiante) {
		return this.#pedir(`${this.#URL_ESTUDIANTES}/${estudiante.id}`, {
			method: 'PUT',
			body: JSON.stringify({ estudiante })
		})
	}

	async eliminarEstudiante(id) {
		return this.#pedir(`${this.#URL_ESTUDIANTES}/${id}`, {
			method: 'DELETE'
		})
	}

	async insertarEstudiante(estudiante) {
		return this.#pedir(this.#URL_ESTUDIANTES, {
			method: 'POST',
			body: JSON.stringify({ estudiante })
		})
	}

	async getEstudiantes() {
		return this.#pedir(this.#URL_ESTUDIANTES)
	}

	// Resultados
	async getResultados() {
		return this.#pedir(this.#URL_RESULTADOS)
	}

	async crearResultado(resultado) {
		return this.#pedir(this.#URL_RESULTADOS, {
			method: 'POST',
			body: JSON.stringify(resultado)
		})
	}

	async actualizarResultado(resultado) {
		return this.#pedir(`${this.#URL_RESULTADOS}/${resultado.id}`, {
			method: 'PUT',
			body: JSON.stringify({ resultado })
		})
	}

	async eliminarResultado(id) {
		return this.#pedir(`${this.#URL_RESULTADOS}/${id}`, {
			method: 'DELETE'
		})
	}

	// Actividades
	async getActividades() {
	  return this.#pedir(this.#URL_ACTIVIDADES)
	}

	async insertarActividad(data) {
		return this.#pedir(this.#URL_ACTIVIDADES, {
			method: 'POST',
			body: JSON.stringify(data)
		})
	}

	async actualizarActividad(id, data) {
		return this.#pedir(`${this.#URL_ACTIVIDADES}/${id}`, {
			method: 'PUT',
			body: JSON.stringify(data)
		})
	}

	async eliminarActividad(id) {
		return this.#pedir(`${this.#URL_ACTIVIDADES}/${id}`, {
			method: 'DELETE'
		})
	}

	// Calificaciones
	async getContextoCalificacion(actividadId, estudianteId) {
		let url = `/api/calificaciones/contexto?actividad_id=${actividadId}`
		if (estudianteId) url += `&estudiante_id=${estudianteId}`
		return this.#pedir(url)
	}

	async guardarCalificacion(actividadId, estudianteId, items) {
		return this.#pedir('/api/calificaciones', {
			method: 'PUT',
			body: JSON.stringify({ actividad_id: actividadId, estudiante_id: estudianteId, items })
		})
	}

	async borrarCalificacion(actividadId, estudianteId) {
		return this.#pedir(`/api/calificaciones?actividad_id=${actividadId}&estudiante_id=${estudianteId}`, {
			method: 'DELETE'
		})
	}

	// Indicadores
	async getIndicadores() {
		return this.#pedir(this.#URL_INDICADORES)
	}

	async crearIndicador(indicador) {
		return this.#pedir(this.#URL_INDICADORES, {
			method: 'POST',
			body: JSON.stringify(indicador.aJSON())
		})
	}

	async actualizarIndicador(indicador) {
		return this.#pedir(`${this.#URL_INDICADORES}/${indicador.id}`, {
			method: 'PUT',
			body: JSON.stringify(indicador.aJSON())
		})
	}

	async eliminarIndicador(id) {
		return this.#pedir(`${this.#URL_INDICADORES}/${id}`, {
			method: 'DELETE'
		})
	}

	async buscarIndicadores(query) {
		return this.#pedir(`${this.#URL_INDICADORES}/buscar?q=${encodeURIComponent(query)}`)
	}

	// Informes
	async getInformeEstudiante(estudianteId, fechaInforme) {
		let url = `/api/informes/estudiantes?estudiante_id=${estudianteId}`
		if (fechaInforme) url += `&fecha_informe=${fechaInforme}`
		return this.#pedir(url)
	}

	async getInformeActividadesPorResultados(estudianteId, fechaInforme) {
		let url = `/api/informes/actividades-por-resultados?estudiante_id=${estudianteId}`
		if (fechaInforme) url += `&fecha_informe=${fechaInforme}`
		return this.#pedir(url)
	}

}
