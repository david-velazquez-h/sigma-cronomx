import { MapContainer, TileLayer, CircleMarker, Popup } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';
import Nav from '../components/Nav';
import { ORIGENES, DESTINOS, colorForIndice } from '../data/dummyData';
import './Mapa.css';

export default function Mapa() {
  return (
    <div className="mapa-page">
      <Nav />

      <div className="mapa-header">
        <span className="mapa-tag">Datos de ejemplo</span>
        <h1>Índice de pobreza de tiempo</h1>
        <p>Municipios piloto del Estado de México, comparados contra tres destinos de empleo en la CDMX.</p>
      </div>

      <div className="mapa-layout">
        <div className="mapa-container">
          <MapContainer
            center={[19.42, -99.05]}
            zoom={10}
            style={{ height: '100%', width: '100%' }}
          >
            <TileLayer
              url={`https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png?key=${import.meta.env.VITE_CARTO_API_KEY}`}
              attribution='&copy; OpenStreetMap contributors &copy; CARTO'
            />

            {ORIGENES.map((o) => (
              <CircleMarker
                key={o.nombre}
                center={[o.lat, o.lng]}
                radius={12}
                pathOptions={{ color: '#fff', weight: 1.5, fillColor: colorForIndice(o.indice), fillOpacity: 0.9 }}
              >
                <Popup>
                  <div className="mapa-popup">
                    <div className="mapa-popup-title">{o.nombre}</div>
                    <div className="mapa-popup-row">
                      <span>Índice (ejemplo)</span>
                      <span>{o.indice}/100</span>
                    </div>
                    {o.rutas.map((r) => (
                      <div className="mapa-popup-row" key={r.destino}>
                        <span>{r.destino}</span>
                        <span>{r.tp} vs {r.auto} (auto)</span>
                      </div>
                    ))}
                    <div className="mapa-popup-flag">Datos de ejemplo, no reales todavía</div>
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

          <p className="mapa-note">Haz clic en cualquier punto para ver la comparación de tiempo estimado.</p>
          <p className="mapa-note">Datos de ejemplo. Pendiente reemplazar con cálculos reales de Miguel (datos) y Max (fórmula del índice).</p>
        </div>
      </div>
    </div>
  );
}