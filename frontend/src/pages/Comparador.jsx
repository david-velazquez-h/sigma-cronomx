import { useState } from 'react';
import Nav from '../components/Nav';
import { useIndice } from '../data/useIndice';
import { formatMin, hayProvisional } from '../data/destinos';
import './Comparador.css';

export default function Comparador() {
  const { data, error } = useIndice();
  const [origenId, setOrigenId] = useState(null);

  if (error) return <div className="comparador-page"><Nav /><p>No se pudo cargar indice.json ({error})</p></div>;
  if (!data) return <div className="comparador-page"><Nav /><p>Cargando…</p></div>;

  const umbral = data.meta.parametros.decaimiento_min; // 120
  const origen = data.municipios.find((m) => m.id === origenId) ?? data.municipios[0];

  return (
    <div className="comparador-page">
      <Nav />

      <div className="comparador-header">
        <span className="comparador-tag">{hayProvisional(data) ? 'Datos provisionales' : 'Piloto v1'}</span>
        <h1>Comparador de destinos</h1>
        <p>Tiempo estimado en transporte público desde tu municipio a cada polo de empleo. La barra completa equivale a {umbral} min, el punto donde la accesibilidad llega a cero.</p>
      </div>

      <div className="comparador-card">
        <div className="comparador-selects">
          <label className="comparador-field">
            <span>Origen</span>
            <select value={origen.id} onChange={(e) => setOrigenId(e.target.value)}>
              {data.municipios.map((m) => (
                <option key={m.id} value={m.id}>{m.nombre}</option>
              ))}
            </select>
          </label>
        </div>

        <div className="comparador-result">
          {origen.destinos.map((d) => (
            <div className="comparador-bar-row" key={d.nombre}>
              <div className="comparador-bar-label">
                <span>{d.nombre}</span>
                <span className="comparador-bar-value">{formatMin(d.tp_min)}</span>
              </div>
              <div className="comparador-bar-track">
                <div
                  className="comparador-bar-fill comparador-bar-fill--tp"
                  style={{ width: `${Math.min(100, ((d.tp_min ?? umbral) / umbral) * 100)}%` }}
                />
              </div>
            </div>
          ))}
        </div>

        <p className="comparador-legend-note">
          Índice de {origen.nombre}: {Math.round(origen.ipt_100)}/100
          {origen.tramo_mexibus_min ? ` · incluye ~${Math.round(origen.tramo_mexibus_min)} min de Mexibús estimados` : ''}
        </p>
      </div>
    </div>
  );
}