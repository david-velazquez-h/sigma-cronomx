import { Link } from 'react-router-dom';
import Nav from './Nav';
import './Hero.css';

export default function Hero() {
  return (
    <section className="hero">
      <div className="hero-glow" aria-hidden="true" />

      <Nav />

      <div className="hero-body">
        <span className="hero-badge">Estado de México → Ciudad de México</span>

        <h1 className="hero-stat">5h 49min</h1>

        <p className="hero-copy">
          Es lo que le puede tomar a una persona cruzar la Zona Metropolitana
          del Valle de México en transporte público. En auto particular,
          poco más de la mitad.
        </p>

        <div className="hero-actions">
          <Link to="/mapa" className="hero-cta">Ver el mapa</Link>
          <Link to="/metodologia" className="hero-cta-ghost">Ver metodología</Link>
        </div>
      </div>

      <div className="hero-stats">
        <div className="hero-stat-item">
          <span className="hero-stat-number">3</span>
          <span className="hero-stat-label">Municipios piloto</span>
        </div>
        <div className="hero-stat-item">
          <span className="hero-stat-number">GTFS</span>
          <span className="hero-stat-label">Datos abiertos de transporte</span>
        </div>
        <div className="hero-stat-item">
          <span className="hero-stat-number">MIT</span>
          <span className="hero-stat-label">Código abierto</span>
        </div>
      </div>
    </section>
  );
}