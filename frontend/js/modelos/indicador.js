export class Indicador {
	id = null
	codigo = null
	nombre = null
	resultados = null

	constructor(id, codigo, nombre, resultados = []) {
		this.id = id
		this.codigo = codigo
		this.nombre = nombre
		this.resultados = resultados
	}

	aJSON() {
		return {
			codigo: this.codigo,
			nombre: this.nombre,
			resultados: this.resultados.map(r => ({
				id_resultado: r.id,
				peso: r.peso
			}))
		}
	}
}
