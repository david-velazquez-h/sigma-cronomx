const PERFILES = [
  {
    titulo: 'Si vives la ruta',
    copy: 'Compara tu municipio contra distintos destinos y decide con datos reales, no con intuición.',
  },
  {
    titulo: 'Si investigas movilidad',
    copy: 'Metodología abierta, datos descargables, y un índice pensado para ser auditado o extendido.',
  },
  {
    titulo: 'Si tomas decisiones de ciudad',
    copy: 'Evidencia cuantificada de dónde el transporte le cuesta más tiempo a la gente, no solo dinero.',
  },
];

export default function Audiencias() {
  return (
    <section className="audiencias">
      <h2 className="audiencias-title">¿Para quién es CronoMX?</h2>
      <div className="audiencias-grid">
        {PERFILES.map((p) => (
          <div className="audiencias-card" key={p.titulo}>
            <h3>{p.titulo}</h3>
            <p>{p.copy}</p>
          </div>
        ))}
      </div>
    </section>
  );
}