import { Link } from 'react-router-dom';
import cronoLogo from '../assets/logo-crono-sin-f.png';
import './Nav.css';

export default function Nav() {
  return (
    <nav className="site-nav">
      <Link to="/">
        <img src={cronoLogo} alt="CronoMX" className="site-nav-logo" />
      </Link>
      <div className="site-nav-links">
        <Link to="/mapa">Mapa</Link>
        <Link to="/comparador">Comparador</Link>
        <Link to="/metodologia">Metodología</Link>
      </div>
      <Link to="/mapa" className="site-nav-cta">Explorar</Link>
    </nav>
  );
}