import { useEffect, useState } from 'react'
import './App.css'

const VACIO = { nombre: '', descripcion: '', precio: '', cantidad: 0 }

function App() {
  const [productos, setProductos] = useState([])
  const [form, setForm] = useState(VACIO)
  const [editandoId, setEditandoId] = useState(null)
  const [error, setError] = useState('')

  async function cargar() {
    try {
      const res = await fetch('/productos')
      if (!res.ok) throw new Error()
      setProductos(await res.json())
    } catch {
      setError('No se pudo conectar con el servidor.')
    }
  }

  useEffect(() => {
    cargar()
  }, [])

  function cambiar(e) {
    setForm({ ...form, [e.target.name]: e.target.value })
  }

  async function guardar(e) {
    e.preventDefault()
    setError('')
    const datos = {
      nombre: form.nombre.trim(),
      descripcion: form.descripcion.trim() || null,
      precio: Number(form.precio),
      cantidad: Number(form.cantidad),
    }
    const url = editandoId ? `/productos/${editandoId}` : '/productos'
    try {
      const res = await fetch(url, {
        method: editandoId ? 'PUT' : 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(datos),
      })
      if (!res.ok) {
        setError('Revisa los datos: el nombre no puede estar vacío y el precio y la cantidad no pueden ser negativos.')
        return
      }
      cancelar()
      cargar()
    } catch {
      setError('No se pudo conectar con el servidor.')
    }
  }

  function editar(p) {
    setError('')
    setEditandoId(p.id)
    setForm({
      nombre: p.nombre,
      descripcion: p.descripcion ?? '',
      precio: p.precio,
      cantidad: p.cantidad,
    })
    window.scrollTo({ top: 0, behavior: 'smooth' })
  }

  async function eliminar(id) {
    if (!window.confirm('¿Eliminar este producto?')) return
    await fetch(`/productos/${id}`, { method: 'DELETE' })
    cargar()
  }

  function cancelar() {
    setEditandoId(null)
    setForm(VACIO)
  }

  const totalUnidades = productos.reduce((s, p) => s + p.cantidad, 0)
  const valorInventario = productos.reduce((s, p) => s + Number(p.precio) * p.cantidad, 0)

  return (
    <>
      <header className="banda">
        <div className="banda-interior">
          <h1>Inventario de productos</h1>
        </div>
      </header>

      <main className="pagina">
        <div className="indicadores">
          <div className="indicador">
            <span>Productos</span>
            <strong>{productos.length}</strong>
          </div>
          <div className="indicador">
            <span>Unidades en stock</span>
            <strong>{totalUnidades}</strong>
          </div>
          <div className="indicador">
            <span>Valor del inventario</span>
            <strong>{valorInventario.toLocaleString('es-DO', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}</strong>
          </div>
        </div>

        {error && <div className="error">{error}</div>}

        <section className="tarjeta">
          <h2>{editandoId ? 'Editar producto' : 'Nuevo producto'}</h2>
          <form className="formulario" onSubmit={guardar}>
            <div className="campo">
              <label htmlFor="nombre">Nombre</label>
              <input id="nombre" name="nombre" value={form.nombre} onChange={cambiar} required maxLength={100} />
            </div>
            <div className="campo">
              <label htmlFor="descripcion">Descripción</label>
              <input id="descripcion" name="descripcion" value={form.descripcion} onChange={cambiar} maxLength={500} />
            </div>
            <div className="campo">
              <label htmlFor="precio">Precio</label>
              <input id="precio" name="precio" type="number" step="0.01" min="0" value={form.precio} onChange={cambiar} required />
            </div>
            <div className="campo">
              <label htmlFor="cantidad">Cantidad</label>
              <input id="cantidad" name="cantidad" type="number" min="0" value={form.cantidad} onChange={cambiar} required />
            </div>
            <div className="acciones-form">
              <button type="submit" className="principal">
                {editandoId ? 'Guardar cambios' : 'Agregar producto'}
              </button>
              {editandoId && (
                <button type="button" onClick={cancelar}>Cancelar</button>
              )}
            </div>
          </form>
        </section>

        <section className="tarjeta">
          <table>
            <thead>
              <tr>
                <th>Nombre</th>
                <th>Descripción</th>
                <th className="num">Precio</th>
                <th className="num">Cantidad</th>
                <th></th>
              </tr>
            </thead>
            <tbody>
              {productos.map((p) => (
                <tr key={p.id}>
                  <td className="nombre">{p.nombre}</td>
                  <td>{p.descripcion}</td>
                  <td className="num">{Number(p.precio).toFixed(2)}</td>
                  <td className="num">
                    <span className={p.cantidad <= 5 ? 'etiqueta bajo' : 'etiqueta'}>{p.cantidad}</span>
                  </td>
                  <td className="acciones">
                    <button onClick={() => editar(p)}>Editar</button>
                    <button className="peligro" onClick={() => eliminar(p.id)}>Eliminar</button>
                  </td>
                </tr>
              ))}
              {productos.length === 0 && (
                <tr><td colSpan="5" className="vacio">Aún no hay productos.</td></tr>
              )}
            </tbody>
          </table>
        </section>
      </main>
    </>
  )
}

export default App