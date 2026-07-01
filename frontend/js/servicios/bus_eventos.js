export class BusEventos extends EventTarget {

	on(nombreEvento, callback) {
		const handler = (evento) => callback(evento.detail)
		this.addEventListener(nombreEvento, handler)

		//return () => this.removeEventListener(nombreEvento, handler);
	}

	emitir(nombreEvento, detalles = {}) {
		this.dispatchEvent(new CustomEvent(nombreEvento, { detail: detalles }))
	}
}
