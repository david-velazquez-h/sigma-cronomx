import { Link } from 'react-router-dom';
import sigmaLogo from '../assets/logo-sigma-sin-f.png';

export default function SigmaExplainer() {
  return (
    <section className="sigma-explainer">
      <img src={sigmaLogo} alt="SIGMA" className="sigma-explainer-logo" />
      <div className="sigma-explainer-body">
        <h2>¿Qué es SIGMA?</h2>
        <p>
          Sistema de índices georreferenciados de movilidad y accesibilidad (SIGMA).
          Es el motor detrás de CronoMX: la fórmula que convierte datos abiertos
          de transporte (GTFS, afluencia) en un índice de pobreza de tiempo por
          municipio. CronoMX lo muestra. SIGMA lo calcula.
        </p>
        <Link to="/metodologia" className="sigma-explainer-link">
          Ver la metodología completa →
        </Link>
      </div> 
    </section>
  );
}