// Coordenadas de los polos de empleo. Los nombres deben coincidir con indice.json
export const DESTINOS = [
  { nombre: 'Centro CDMX', lat: 19.4258, lng: -99.1334 },          // Pino Suárez
  { nombre: 'Reforma / Polanco', lat: 19.4333, lng: -99.1909 },    // Polanco
  { nombre: 'Santa Fe (Observatorio)', lat: 19.3985, lng: -99.2005 }, // Observatorio
];

// Umbrales sobre IPT_comp (escala natural 0-2). 0.8 = "exclusión severa" (criterio de Max)
export const NIVELES = [
  { max: 0.3, color: '#1D9E75', etiqueta: 'Bajo' },
  { max: 0.5, color: '#7fae5a', etiqueta: 'Moderado' },
  { max: 0.8, color: '#EF9F27', etiqueta: 'Alto' },
  { max: Infinity, color: '#D85A30', etiqueta: 'Exclusión severa' },
];

export const nivelIpt = (ipt) => NIVELES.find((n) => ipt < n.max);
export const colorForIpt = (ipt) => nivelIpt(ipt).color;

export function formatMin(min) {
  if (min == null) return 'Sin ruta';
  const h = Math.floor(min / 60);
  const m = Math.round(min % 60);
  return h ? `${h}h ${String(m).padStart(2, '0')}min` : `${m}min`;
}

export const hayProvisional = (data) =>
  data.municipios.some((m) => m.im_fuente === 'provisional');