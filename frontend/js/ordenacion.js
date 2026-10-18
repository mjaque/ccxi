const comparadorNombres = new Intl.Collator('es', { sensitivity: 'accent' })

export function ordenarPorNombre(items) {
	return [...items].sort((a, b) => comparadorNombres.compare(a.nombre, b.nombre))
}
