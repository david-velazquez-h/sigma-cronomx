import { useState } from 'react';
import Nav from '../components/Nav';
import { ORIGENES, DESTINOS, parseTiempo } from '../data/dummyData';
import './Comparador.css';

export default function Comparador() {
  const [origenNombre, setOrigenNombre] = useState(ORIGENES[0].nombre);
  const [destinoNombre, setDestinoNombre] = useState(DESTINOS[0].nombre);

  const origen = ORIGENES.find((o) => o.nombre === origenNombre);
  const ruta = origen.rutas.find((r) => r.destino === destinoNombre);

  const minTp = parseTiempo(ruta.tp);
  const minAuto = parseTiempo(ruta.auto);
  const maxMin = Math.max(minTp, minAuto);

  return (
    <div className="comparador-page">
      <Nav />

      <div className="comparador-header">
        <span className="comparador-tag">Datos de ejemplo</span>
        <h1>Comparador de rutas</h1>
        <p>Tiempo estimado en transporte público frente a auto particular.</p>
      </div>

      <div className="comparador-card">
        <div className="comparador-selects">
          <label className="comparador-field">
            <span>Origen</span>
            <select value={origenNombre} onChange={(e) => setOrigenNombre(e.target.value)}>
              {ORIGENES.map((o) => (
                <option key={o.nombre} value={o.nombre}>{o.nombre}</option>
              ))}
            </select>
          </label>

          <label className="comparador-field">
            <span>Destino</span>
            <select value={destinoNombre} onChange={(e) => setDestinoNombre(e.target.value)}>
              {DESTINOS.map((d) => (
                <option key={d.nombre} value={d.nombre}>{d.nombre}</option>
              ))}
            </select>
          </label>
        </div>

        <div className="comparador-result">
          <div className="comparador-bar-row">
            <div className="comparador-bar-label">
              <span>Transporte público</span>
              <span className="comparador-bar-value">{ruta.tp}</span>
            </div>
            <div className="comparador-bar-track">
              <div
                className="comparador-bar-fill comparador-bar-fill--tp"
                style={{ width: `${(minTp / maxMin) * 100}%` }}
              />
            </div>
          </div>

          <div className="comparador-bar-row">
            <div className="comparador-bar-label">
              <span>Auto particular</span>
              <span className="comparador-bar-value">{ruta.auto}</span>
            </div>
            <div className="comparador-bar-track">
              <div
                className="comparador-bar-fill comparador-bar-fill--auto"
                style={{ width: `${(minAuto / maxMin) * 100}%` }}
              />
            </div>
          </div>
        </div>

        <p className="comparador-legend-note">Coral = mayor costo de tiempo · Verde = menor costo de tiempo</p>
      </div>
    </div>
  );
}