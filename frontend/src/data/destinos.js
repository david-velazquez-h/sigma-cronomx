// Coordenadas de los polos de empleo. Los nombres deben coincidir con indice.json
export const DESTINOS = [
  { nombre: 'Centro CDMX', lat: 19.4258, lng: -99.1334 },          // Pino Suárez
  { nombre: 'Reforma / Polanco', lat: 19.4333, lng: -99.1909 },    // Polanco
  { nombre: 'Santa Fe (Observatorio)', lat: 19.3985, lng: -99.2005 }, // Observatorio
];

// ipt_100: 0-100 (IPT_comp escalado sobre su máximo teórico de 2)
export function colorForIndice(v) {
  if (v < 30) return '#1D9E75';
  if (v < 55) return '#7fae5a';
  if (v < 75) return '#EF9F27';
  return '#D85A30';
}

export function formatMin(min) {
  if (min == null) return 'Sin ruta';
  const h = Math.floor(min / 60);
  const m = Math.round(min % 60);
  return h ? `${h}h ${String(m).padStart(2, '0')}min` : `${m}min`;
}

export const hayProvisional = (data) =>
  data.municipios.some((m) => m.im_fuente === 'provisional');