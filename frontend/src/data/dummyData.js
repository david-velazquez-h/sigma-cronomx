// Datos de ejemplo (dummy) reemplazar cuando Max entregue el cálculo real del índice
// Municipios piloto finales: Ecatepec, Nezahualcóyotl, Chimalhuacán, Tecámac
// (Chalco quedó fuera, sin fuente pública de datos de transporte disponible, ver docs/notas.md)
export const ORIGENES = [
  {
    nombre: 'Ecatepec de Morelos',
    lat: 19.6015, lng: -99.0503,
    indice: 82,
    rutas: [
      { destino: 'Centro CDMX', tp: '2h 40min', auto: '1h 10min' },
      { destino: 'Reforma / Polanco', tp: '3h 05min', auto: '1h 25min' },
      { destino: 'Santa Fe', tp: '3h 40min', auto: '1h 50min' },
    ],
  },
  {
    nombre: 'Nezahualcóyotl',
    lat: 19.4003, lng: -99.0148,
    indice: 68,
    rutas: [
      { destino: 'Centro CDMX', tp: '1h 20min', auto: '0h 45min' },
      { destino: 'Reforma / Polanco', tp: '1h 50min', auto: '1h 00min' },
      { destino: 'Santa Fe', tp: '2h 30min', auto: '1h 20min' },
    ],
  },
  {
    nombre: 'Chimalhuacán',
    lat: 19.4200, lng: -98.9575,
    indice: 87,
    rutas: [
      { destino: 'Centro CDMX', tp: '2h 15min', auto: '1h 05min' },
      { destino: 'Reforma / Polanco', tp: '2h 45min', auto: '1h 20min' },
      { destino: 'Santa Fe', tp: '3h 25min', auto: '1h 45min' },
    ],
  },
  {
    nombre: 'Tecámac',
    lat: 19.7128, lng: -98.9767,
    indice: 90,
    rutas: [
      { destino: 'Centro CDMX', tp: '3h 10min', auto: '1h 20min' },
      { destino: 'Reforma / Polanco', tp: '3h 35min', auto: '1h 35min' },
      { destino: 'Santa Fe', tp: '4h 05min', auto: '2h 00min' },
    ],
  },
];

export const DESTINOS = [
  { nombre: 'Centro CDMX', lat: 19.4326, lng: -99.1332 },
  { nombre: 'Reforma / Polanco', lat: 19.4326, lng: -99.1908 },
  { nombre: 'Santa Fe', lat: 19.3592, lng: -99.2596 },
];

export function colorForIndice(v) {
  if (v < 30) return '#1D9E75';
  if (v < 55) return '#7fae5a';
  if (v < 75) return '#EF9F27';
  return '#D85A30';
}

// Convierte "2h 40min" a minutos totales, para calcular el ancho de las barras
export function parseTiempo(str) {
  const h = /(\d+)h/.exec(str);
  const m = /(\d+)min/.exec(str);
  return (h ? parseInt(h[1]) * 60 : 0) + (m ? parseInt(m[1]) : 0);
}