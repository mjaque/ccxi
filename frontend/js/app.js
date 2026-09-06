import { ControladorEstado } from './controladores/estado.js'
import { ControladorModulos } from './controladores/modulos.js'
import { ControladorEstudiantes } from './controladores/estudiantes.js'
import { ControladorResultados } from './controladores/resultados.js'
import { ControladorIndicadores } from './controladores/indicadores.js'
import { ControladorActividades } from './controladores/actividades.js'
import { ControladorCalificaciones } from './controladores/calificaciones.js'
import { ControladorInformes } from './controladores/informes.js'

class App {
	//Referencias del Intefaz de Usuario
	#divEstado
	#divModulos
	#divMenu
	#divEstudiantes
	#divActividades
	#divResultados
	#divIndicadores
	#divCalificaciones
	#divInformes

	//Controladores
	#controladorEstado
	#controladorModulo
	#controladorEstudiantes
	#controladorResultado
	#controladorIndicador
	#controladorPrueba
	#controladorCalificaciones
	#controladorInformes

	async iniciar() {
		this.#registrarReferenciasIU()

		this.#controladorEstado = new ControladorEstado(this.#divEstado)
		await this.#controladorEstado.comprobar()

		this.#controladorModulo = new ControladorModulos(this.#divModulos)
		await this.#controladorModulo.iniciar()

		this.#configurarMenu()

		this.#controladorEstudiantes = new ControladorEstudiantes(this.#divEstudiantes)
		await this.#controladorEstudiantes.iniciar()

		this.#controladorResultado = new ControladorResultados(this.#divResultados)
		await this.#controladorResultado.iniciar()

		this.#controladorIndicador = new ControladorIndicadores(this.#divIndicadores)
		await this.#controladorIndicador.iniciar()

		this.#controladorPrueba = new ControladorActividades(this.#divActividades)
		await this.#controladorPrueba.iniciar()

		this.#controladorCalificaciones = new ControladorCalificaciones(this.#divCalificaciones)
		await this.#controladorCalificaciones.iniciar()

		this.#controladorInformes = new ControladorInformes(this.#divInformes)
		await this.#controladorInformes.iniciar()

		/*
	registrarEventos();
	mostrarVista("estudiantes");

	await inicializarModulos();
	await cargarEstudiantes();
	await cargarActividades();
	await cargarResultados();
	await cargarIndicadores();
	*/
	}

	#configurarMenu(){
		for (const elemento of this.#divMenu.children)
			elemento.addEventListener('click', this.#cambiarVista.bind(this))
	}

	#cambiarVista(evento){
		evento.preventDefault()

		document.querySelector('div.vista.activa')?.classList.remove('activa')

		switch(event.currentTarget.dataset.vista){
		case 'estudiantes':
			this.#divEstudiantes.classList.add('activa')
			break
		case 'resultados':
			this.#divResultados.classList.add('activa')
			break
		case 'indicadores':
			this.#divIndicadores.classList.add('activa')
			break
		case 'actividades':
			this.#divActividades.classList.add('activa')
			break
		case 'calificaciones':
			this.#divCalificaciones.classList.add('activa')
			break
		case 'informes':
			this.#divInformes.classList.add('activa')
			break
	  }
	}

	#limpiarEstadoTrasCambioModulo() {
		/*
		if (typeof resetFormularioEstudiante === "function") resetFormularioEstudiante();
		if (typeof resetFormularioResultado === "function") resetFormularioResultado();
		if (typeof resetFormularioIndicador === "function") resetFormularioIndicador();
		if (typeof resetFormularioPrueba === "function") resetFormularioPrueba();

		mensajeEstudianteEl.textContent = "";
		mensajeResultadoEl.textContent = "";
		mensajeIndicadorEl.textContent = "";
		mensajePruebaEl.textContent = "";
		mensajeCalificacionEl.textContent = "";
		*/
	}

	#registrarReferenciasIU(){
		this.#divEstado = document.getElementById('divEstado')
		this.#divMenu = document.getElementById('divMenu')
		this.#divModulos = document.getElementById('divModulos')
		this.#divEstudiantes = document.getElementById('divEstudiantes')
		this.#divResultados = document.getElementById('divResultados')
		this.#divIndicadores = document.getElementById('divIndicadores')
		this.#divActividades = document.getElementById('divActividades')
		this.#divCalificaciones = document.getElementById('divCalificaciones')
		this.#divInformes = document.getElementById('divInformes')
	}

}

// LANZADOR
document.addEventListener('DOMContentLoaded', async () => {
	const app = new App()
	await app.iniciar()
})

window.addEventListener('error', (evento) => {
	console.log(evento.message)
	alert('Error inesperado. Consulta la consola.')
})
