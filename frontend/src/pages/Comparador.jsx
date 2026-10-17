import { useState } from 'react';
import Nav from '../components/Nav';
import { useIndice } from '../data/useIndice';
import { formatMin, hayProvisional, nivelIpt } from '../data/destinos';
import './Comparador.css';

// Quita acentos y mayúsculas para comparar nombres
const norm = (s) =>
  s.normalize('NFD').replace(/[̀-ͯ]/g, '').toLowerCase().trim();

export default function Comparador() {
  const { data, error } = useIndice();
  const [q, setQ] = useState('');

  if (error) return <div className="comparador-page"><Nav /><p>No se pudo cargar indice.json ({error})</p></div>;
  if (!data) return <div className="comparador-page"><Nav /><p>Cargando…</p></div>;

  const umbral = data.meta.parametros.decaimiento_min;
  const catalogo = data.catalogo ?? [];
  const nq = norm(q);

  const piloto = nq
    ? data.municipios.find((m) => norm(m.nombre) === nq || norm(m.nombre_conapo) === nq)
    : null;
  const enCatalogo = nq ? catalogo.find((c) => norm(c.nombre) === nq) : null;

  return (
    <div className="comparador-page">
      <Nav />

      <div className="comparador-header">
        <span className="comparador-tag">{hayProvisional(data) ? 'Datos provisionales' : 'Piloto v1'}</span>
        <h1>Comparador de destinos</h1>
        <p>Busca tu municipio del Estado de México y mira el tiempo <strong>mínimo estimado</strong> en transporte público a cada polo de empleo.</p>
      </div>

      <div className="comparador-card">
        <div className="comparador-selects">
          <label className="comparador-field">
            <span>Tu municipio</span>
            <input
              type="text"
              list="municipios-edomex"
              value={q}
              placeholder="Escribe: Ecatepec, Tecámac…"
              onChange={(e) => setQ(e.target.value)}
            />
            <datalist id="municipios-edomex">
              {catalogo.map((c) => <option key={c.nombre} value={c.nombre} />)}
            </datalist>
          </label>
        </div>

        <div className="comparador-chips">
          {data.municipios.map((m) => (
            <button key={m.id} className="comparador-chip" onClick={() => setQ(m.nombre)}>
              {m.nombre}
            </button>
          ))}
        </div>

        {!nq && (
          <p className="comparador-msg">
            SIGMA cubre por ahora {data.municipios.length} municipios piloto. Elige uno o busca el tuyo.
          </p>
        )}

        {piloto && (
          <>
            <div className="comparador-result">
              {piloto.destinos.map((d) => (
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
              Índice de {piloto.nombre}: {piloto.ipt_comp.toFixed(2)} ({nivelIpt(piloto.ipt_comp).etiqueta})
              {piloto.acceso_min ? ` · ~${Math.round(piloto.acceso_min)} min de acceso a la estación (estimado)` : ''}
              {piloto.tramo_mexibus_min ? ` · ~${Math.round(piloto.tramo_mexibus_min)} min de Mexibús (estimado)` : ''}
              {` · ${piloto.espera_min} min de espera inicial`}
            </p>
            <p className="comparador-legend-note">
              Es un piso, no un techo: no incluye tráfico, obras, manifestaciones, saturación ni esperas en transbordos. El tiempo real suele ser mayor.
            </p>
          </>
        )}

        {!piloto && enCatalogo && (
          <p className="comparador-msg">
            <strong>{enCatalogo.nombre}</strong> todavía no está calculado en SIGMA. Nuestros datos cubren Metro y Metrobús de la CDMX
            y el Mexibús de los municipios piloto. Si tu municipio no tiene una estación cercana de esos sistemas, es probable que dependa
            de transporte concesionado (combis, colectivos), que SIGMA aún no incluye. Eso no significa que no haya transporte: significa que
            todavía no lo medimos.
          </p>
        )}

        {nq && !piloto && !enCatalogo && (
          <p className="comparador-msg">
            No encontramos ese municipio. Por ahora el buscador solo incluye el Estado de México.
          </p>
        )}
      </div>
    </div>
  );
}