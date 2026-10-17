import { useEffect, useState } from 'react';

// Carga public/data/indice.json (generado por backend/sigma_indice.py)
export function useIndice() {
  const [data, setData] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetch('/data/indice.json')
      .then((r) => {
        if (!r.ok) throw new Error(`HTTP ${r.status}`);
        return r.json();
      })
      .then(setData)
      .catch((e) => setError(e.message));
  }, []);

  return { data, error };
}