import { MapContainer, TileLayer, CircleMarker, Popup } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';
import Nav from '../components/Nav';
import { useIndice } from '../data/useIndice';
import { DESTINOS, colorForIndice, formatMin, hayProvisional } from '../data/destinos';
import './Mapa.css';

export default function Mapa() {
  const { data, error } = useIndice();

  if (error) return <div className="mapa-page"><Nav /><p className="mapa-note">No se pudo cargar indice.json ({error})</p></div>;
  if (!data) return <div className="mapa-page"><Nav /><p className="mapa-note">Cargando…</p></div>;

  const provisional = hayProvisional(data);

  return (
    <div className="mapa-page">
      <Nav />

      <div className="mapa-header">
        <span className="mapa-tag">{provisional ? 'Datos provisionales' : 'Piloto v1'}</span>
        <h1>Índice de pobreza de tiempo</h1>
        <p>Municipios piloto del Estado de México, comparados contra tres destinos de empleo en la CDMX.</p>
      </div>

      <div className="mapa-layout">
        <div className="mapa-container">
          <MapContainer center={[19.5, -99.05]} zoom={10} style={{ height: '100%', width: '100%' }}>
            <TileLayer
              url={`https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png?key=${import.meta.env.VITE_CARTO_API_KEY}`}
              attribution='&copy; OpenStreetMap contributors &copy; CARTO'
            />

            {data.municipios.map((m) => (
              <CircleMarker
                key={m.id}
                center={[m.lat, m.lng]}
                radius={12}
                pathOptions={{ color: '#fff', weight: 1.5, fillColor: colorForIndice(m.ipt_100), fillOpacity: 0.9 }}
              >
                <Popup>
                  <div className="mapa-popup">
                    <div className="mapa-popup-title">{m.nombre}</div>
                    <div className="mapa-popup-row">
                      <span>Índice</span>
                      <span>{Math.round(m.ipt_100)}/100</span>
                    </div>
                    {m.destinos.map((d) => (
                      <div className="mapa-popup-row" key={d.nombre}>
                        <span>{d.nombre}</span>
                        <span>{formatMin(d.tp_min)}</span>
                      </div>
                    ))}
                    {m.tramo_mexibus_min && (
                      <div className="mapa-popup-flag">Incluye ~{Math.round(m.tramo_mexibus_min)} min de Mexibús (estimado)</div>
                    )}
                    {m.im_fuente === 'provisional' && (
                      <div className="mapa-popup-flag">Marginación provisional</div>
                    )}
                  </div>
                </Popup>
              </CircleMarker>
            ))}

            {DESTINOS.map((d) => (
              <CircleMarker
                key={d.nombre}
                center={[d.lat, d.lng]}
                radius={7}
                pathOptions={{ color: '#fff', weight: 1.5, fillColor: '#8A8A83', fillOpacity: 0.9 }}
              >
                <Popup>
                  <div className="mapa-popup">
                    <div className="mapa-popup-title">{d.nombre}</div>
                    <div className="mapa-popup-row"><span>Destino de empleo</span></div>
                  </div>
                </Popup>
              </CircleMarker>
            ))}
          </MapContainer>
        </div>

        <div className="mapa-legend">
          <h2>Índice de pobreza de tiempo</h2>
          <div className="mapa-scale">
            <div style={{ background: '#1D9E75' }}></div>
            <div style={{ background: '#7fae5a' }}></div>
            <div style={{ background: '#EF9F27' }}></div>
            <div style={{ background: '#D85A30' }}></div>
          </div>
          <div className="mapa-scale-labels"><span>Bajo</span><span>Alto</span></div>

          <div className="mapa-dot-key"><span className="mapa-dot" style={{ background: '#EF9F27' }}></span> Municipio de origen</div>
          <div className="mapa-dot-key"><span className="mapa-dot" style={{ background: '#8A8A83' }}></span> Destino de empleo</div>

          <p className="mapa-note">Haz clic en un punto para ver el tiempo estimado a cada destino.</p>
          {data.meta.advertencias.map((a) => (
            <p className="mapa-note" key={a}>{a}</p>
          ))}
        </div>
      </div>
    </div>
  );
}