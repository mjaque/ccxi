import { Controlador } from './controlador.js'

export class ControladorEstado extends Controlador{
	constructor(div){
		super(div)
 	}

	/**
		Comprueba el estado del servidor y lo muestra en la vista.
	**/
 	async comprobar() {
 		try {
			const data = await this.api.comprobarServidor()
			this.div.textContent = data.message
			this.div.style.display = 'none'
		} catch (error) {
			this.div.textContent = `Error: ${error.message}`
		}
	}

}
