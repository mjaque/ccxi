import { Controlador } from './controlador.js'

export class ControladorInformes extends Controlador{
	URL_VISTA = './html/informes.html'

	#selectEstudiante
	#inputFecha
	#botonGenerar
	pMensaje

	#cacheEstudiantes = []

	constructor(div) {
		super(div)
		this.recibirMensaje('cambioModulo', this.#cargar.bind(this))
		this.recibirMensaje('cambioEstudiante', this.#cargar.bind(this))
	}

	async iniciar() {
		await this.cargarVista()
		this.#referenciarElementosIU()
		this.#registrarEventos()
		await this.#cargar()
	}

	async #cargar() {
		await this.#cargarEstudiantes()
	}

	async #cargarEstudiantes() {
		try {
			const data = await this.api.getEstudiantes()
			this.#cacheEstudiantes = data.items || []
		} catch {
			this.#cacheEstudiantes = []
		}
		this.#rellenarSelectEstudiantes()
	}

	#rellenarSelectEstudiantes() {
		this.#selectEstudiante.innerHTML = '<option value="">— Seleccionar estudiante —</option>'
		for (const est of this.#cacheEstudiantes) {
			const opt = document.createElement('option')
			opt.value = est.id
			opt.textContent = est.nombre
			this.#selectEstudiante.appendChild(opt)
		}
	}

	async #generarInforme() {
		const estudianteId = this.#selectEstudiante.value
		if (!estudianteId) {
			this.mostrarError('Debes seleccionar un estudiante.')
			return
		}

		const fecha = this.#inputFecha.value || null

		try {
			const data = await this.api.getInformeEstudiante(estudianteId, fecha)
			const informe = data.item
			this.#abrirInforme(informe)
		} catch (error) {
			this.mostrarError(error.message)
		}
	}

	#abrirInforme(informe) {
		const ventana = window.open('', '_blank')
		if (!ventana) {
			this.mostrarError('No se pudo abrir la nueva pestaña. Permite ventanas emergentes.')
			return
		}

		const titulo = `Informe - ${informe.estudiante.nombre}`
		const fechaMostrar = informe.fecha_informe
			? new Date(informe.fecha_informe + 'T00:00:00').toLocaleDateString('es-ES')
			: '—'

		const notaFinal = informe.nota_final != null ? informe.nota_final.toFixed(2) : 'Sin calificar'

		const resultadosHtml = informe.resultados.map(r => {
			const notaR = r.nota != null ? r.nota.toFixed(2) : 'Sin calificar'

			const indicadoresHtml = (r.indicadores || []).map(i => {
				const notaI = i.nota != null ? i.nota.toFixed(2) : '—'
				return `<tr>
					<td>${this.#escaparHtml(i.codigo)}</td>
					<td>${this.#escaparHtml(i.nombre)}</td>
					<td class=centro>${i.peso}</td>
					<td class=centro><span ${this.#colorNota(i.nota)}>${notaI}</span></td>
				</tr>`
			}).join('')

			return `<section class=resultado>
				<h3>${this.#escaparHtml(r.codigo)}: ${this.#escaparHtml(r.nombre)} <span class=peso>(peso: ${r.peso})</span></h3>
				<p class=nota-resultado>Calificación: <span ${this.#colorNota(r.nota)}>${notaR}</span></p>
				<table>
					<thead><tr>
						<th>Código</th>
						<th>Nombre</th>
						<th>Peso</th>
						<th>Calificación</th>
					</tr></thead>
					<tbody>${indicadoresHtml || '<tr><td colspan=4 class=vacio>No hay indicadores asociados</td></tr>'}</tbody>
				</table>
			</section>`
		}).join('')

		const resultadoVacio = informe.resultados.length === 0
			? '<p class=vacio>No hay resultados de aprendizaje en este módulo.</p>'
			: ''

		ventana.document.open()
		ventana.document.write(`<!DOCTYPE html>
<html lang=es>
<head>
<meta charset=UTF-8>
<meta name=viewport content="width=device-width, initial-scale=1.0">
<title>${this.#escaparHtml(titulo)}</title>
<style>
	*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
	body {
		font-family: 'Segoe UI', system-ui, -apple-system, sans-serif;
		font-size: 14px;
		line-height: 1.6;
		color: #1a1a1a;
		background: #f5f5f5;
		padding: 20px;
	}
	.report {
		max-width: 900px;
		margin: 0 auto;
		background: #fff;
		border-radius: 8px;
		box-shadow: 0 2px 8px rgba(0,0,0,0.1);
		padding: 40px;
	}
	h1 { font-size: 22px; color: #1a3a5c; margin-bottom: 24px; padding-bottom: 12px; border-bottom: 3px solid #1a3a5c; }
	h2 { font-size: 16px; color: #333; margin-top: 28px; margin-bottom: 8px; }
	h3 { font-size: 15px; color: #1a3a5c; margin-bottom: 4px; }
	.header-info { display: grid; grid-template-columns: 1fr 1fr; gap: 8px 24px; margin-bottom: 28px; }
	.header-info p { font-size: 14px; }
	.header-info .label { color: #666; }
	.header-info .value { font-weight: 600; color: #1a1a1a; }
	.nota-modulo { font-size: 18px; font-weight: 700; color: #1a3a5c; text-align: center; padding: 16px; background: #eef4fa; border-radius: 6px; margin-bottom: 28px; }
	.resultado { margin-bottom: 24px; padding: 16px; background: #fafbfc; border: 1px solid #e0e4e8; border-radius: 6px; }
	.peso { font-weight: 400; color: #666; font-size: 13px; }
	.nota-resultado { font-size: 14px; font-weight: 600; color: #2a5a2a; margin-bottom: 12px; }
	table { width: 100%; border-collapse: collapse; font-size: 13px; }
	thead th { background: #1a3a5c; color: #fff; padding: 8px 12px; text-align: left; font-weight: 500; }
	thead th:first-child { border-radius: 4px 0 0 0; }
	thead th:last-child { border-radius: 0 4px 0 0; }
	tbody td { padding: 8px 12px; border-bottom: 1px solid #e0e4e8; }
	tbody tr:nth-child(even) { background: #f5f7f9; }
	tbody tr:hover { background: #eef4fa; }
	.centro { text-align: center; }
	.vacio { color: #888; font-style: italic; padding: 20px; text-align: center; }
	.footer { margin-top: 32px; padding-top: 12px; border-top: 1px solid #e0e4e8; font-size: 12px; color: #888; text-align: center; }
	@media print {
		body { background: #fff; padding: 0; }
		.report { box-shadow: none; padding: 20px; }
		.resultado { break-inside: avoid; }
	}
</style>
</head>
<body>
<div class=report>
	<h1>CCxI — Informe de Estudiante</h1>
	<div class=header-info>
		<p><span class=label>Módulo:</span> <span class=value>${this.#escaparHtml(informe.modulo)}</span></p>
		<p><span class=label>Fecha del informe:</span> <span class=value>${this.#escaparHtml(fechaMostrar)}</span></p>
		<p><span class=label>Estudiante:</span> <span class=value>${this.#escaparHtml(informe.estudiante.nombre)}</span></p>
		<p></p>
	</div>
	<div class=nota-modulo>Calificación del módulo: <span ${this.#colorNota(informe.nota_final)}>${this.#escaparHtml(notaFinal)}</span></div>
	<h2>Resultados de Aprendizaje</h2>
	${resultadoVacio || resultadosHtml}
	<div class=footer>Generado por CCxI — Calificador de Competencias por Indicadores</div>
</div>
</body>
</html>`)
		ventana.document.close()
	}

	#colorNota(nota) {
		if (nota == null) return 'style="background:#e0e0e0;color:#333;padding:2px 6px;border-radius:3px;font-weight:700"'
		if (nota < 4) return 'style="background:#d32f2f;color:#fff;padding:2px 6px;border-radius:3px;font-weight:700"'
		if (nota < 5) return 'style="background:#fbc02d;color:#1a1a1a;padding:2px 6px;border-radius:3px;font-weight:700"'
		if (nota < 8) return 'style="background:#388e3c;color:#fff;padding:2px 6px;border-radius:3px;font-weight:700"'
		return 'style="background:#1976d2;color:#fff;padding:2px 6px;border-radius:3px;font-weight:700"'
	}

	#escaparHtml(texto) {
		if (texto == null) return ''
		const div = document.createElement('div')
		div.textContent = String(texto)
		return div.innerHTML
	}

	#referenciarElementosIU() {
		this.#selectEstudiante = this.div.querySelector('#informe-estudiante-select')
		this.#inputFecha = this.div.querySelector('#informe-fecha')
		this.#botonGenerar = this.div.querySelector('#informe-generar')
		this.pMensaje = this.div.querySelector('#informe-mensaje')
	}

	#registrarEventos() {
		this.#botonGenerar.addEventListener('click', this.#generarInforme.bind(this))
	}
}
