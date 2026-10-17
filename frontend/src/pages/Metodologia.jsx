import Nav from '../components/Nav';
import { useIndice } from '../data/useIndice';
import './Metodologia.css';

export default function Metodologia() {
  const { data } = useIndice();
  const p = data?.meta.parametros;

  return (
    <div className="metodo-page">
      <Nav />

      <article className="metodo-body">
        <span className="metodo-tag">Piloto v1</span>
        <h1>Metodología</h1>
        <p className="metodo-lead">
          Cómo calculamos el índice de pobreza de tiempo, de dónde salen los datos y qué no
          sabemos todavía. Todo el código es abierto para que pueda auditarse.
        </p>

        <section>
          <h2>1. La fórmula</h2>
          <pre className="metodo-formula">IPT = (1 − Acc_Relativa) × (1 + IM)
Acc_Relativa = máx(0, 1 − t / {p?.decaimiento_min ?? 120})</pre>
          <p>
            <strong>t</strong> es el tiempo mínimo en transporte público, en minutos, desde la
            estación de origen del municipio hasta el polo de empleo más cercano.
            <strong> Acc_Relativa</strong> vale 1 si t = 0 y 0 si t llega a {p?.decaimiento_min ?? 120} minutos.
            <strong> IM</strong> es la marginación del municipio, normalizada de 0 a 1.
          </p>
          <p>
            Para dibujar el mapa, el IPT se escala sobre su máximo teórico (2) y se muestra de 0 a 100.
          </p>
        </section>

        <section>
          <h2>2. Cómo calculamos el tiempo</h2>
          <p>
            Construimos un grafo dirigido con las paradas del GTFS de Metro y Metrobús de la CDMX.
            Cada tramo pesa lo que tarda el viaje programado entre dos paradas. Los transbordos
            entre andenes de una misma estación suman {p?.transbordo_min ?? 5} minutos. Con el algoritmo de
            Dijkstra obtenemos el camino más corto desde la estación de origen de cada municipio
            hasta tres polos de empleo: Pino Suárez (Centro), Polanco (Reforma/Polanco) y
            Observatorio (Santa Fe).
          </p>
        </section>

        <section>
          <h2>3. Mexibús: un tramo estimado</h2>
          <p>
            No existe un GTFS público de Mexibús. Para Chimalhuacán y Tecámac sumamos el tramo
            en Mexibús como distancia ÷ velocidad ({p?.velocidad_mexibus_kmh ?? 20} km/h), más un transbordo.
            Esa velocidad es un supuesto nuestro y no una medición; estos dos municipios son los más
            sensibles a ella.
          </p>
        </section>

        <section>
          <h2>4. Marginación (IM)</h2>
          <p>
            Usamos el índice de marginación municipal 2020 de CONAPO. En esa escala, un valor alto
            significa <em>menos</em> marginación, así que lo invertimos y lo normalizamos de 0 a 1
            sobre los 125 municipios del Estado de México (1 = el más marginado).
          </p>
          <p>
            Los cuatro municipios piloto tienen grado "Muy bajo" en CONAPO, con valores muy cercanos,
            por lo que en esta versión el IM modifica poco el resultado: el índice depende sobre todo
            del tiempo de viaje.
          </p>
        </section>

        <section>
          <h2>5. Limitaciones conocidas</h2>
          <ul>
            <li>Los datos de Metro y Metrobús vienen del GTFS de SEMOVI, versión del 31 de octubre de 2022.</li>
            <li>Son tiempos programados: no incluyen esperas, caminata a la estación, congestión ni saturación.</li>
            <li>Cada municipio se representa con una sola estación de origen, no con toda su población.</li>
            <li>El IM es un promedio municipal y oculta diferencias internas. Una versión futura debería usar AGEB o localidad.</li>
            <li>No comparamos contra auto particular: aún no tenemos una fuente de tiempos.</li>
            <li>Piloto de 4 municipios y 3 destinos: no representa a toda la ZMVM.</li>
          </ul>
        </section>

        <section>
          <h2>6. Datos y código</h2>
          <ul>
            <li>GTFS de la CDMX: portal de datos abiertos de la CDMX / SEMOVI.</li>
            <li>Estaciones de Mexibús: OpenStreetMap, vía Overpass API.</li>
            <li>Índice de marginación 2020: CONAPO, con datos del Censo de Población y Vivienda 2020 (INEGI).</li>
            <li>Código y documentación: repositorio de GitHub del proyecto, licencia MIT.</li>
          </ul>
        </section>
      </article>
    </div>
  );
}