export class Resultado {
	id = null
	codigo = null
	nombre = null
	peso = null

	constructor(id, codigo, nombre, peso = 0){
		this.id = id
		this.codigo = codigo
		this.nombre = nombre
		this.peso = peso
	}
}
