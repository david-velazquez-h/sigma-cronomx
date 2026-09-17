import { Routes, Route } from 'react-router-dom';
import Hero from './components/Hero';
import Mapa from './pages/Mapa';
import Comparador from './pages/Comparador';
import Metodologia from './pages/Metodologia.jsx';
import './App.css';

function App() {
  return (
    <Routes>
      <Route path="/" element={<Hero />} />
      <Route path="/mapa" element={<Mapa />} />
      <Route path="/comparador" element={<Comparador />} />
      <Route path="/metodologia" element={<Metodologia />} />
    </Routes>
  );
}

export default App