# Politica de veracidad del proyecto

Objetivo: que cada visualizacion del dashboard sea trazable, verificable y explicable.

## Principios

1. No inventar cifras.
2. Diferenciar claramente:
   - dato observado (viene de fuente externa)
   - dato calculado (deriva de una formula)
   - dato estimado (supuesto didactico)
3. Toda fila de datos debe incluir `source`.
4. Si un valor no puede verificarse, no se publica.

## Reglas operativas

1. Cada dataset procesado debe pasar validaciones automáticas antes de usarse.
2. Cualquier grafico con estimaciones debe indicarlo en el texto de apoyo.
3. Las afirmaciones "fuertes" del copy deben estar respaldadas por:
   - DOI en estudios, o
   - informe institucional en habitos/pantallas.
4. Si hay discrepancia entre fuentes, se documenta y se prioriza la mas reciente y metodologicamente clara.

## Checklist antes de publicar

1. ¿La columna `source` está completa en todas las filas?
2. ¿Los rangos de valores son plausibles?
3. ¿Hay duplicados exactos no justificados?
4. ¿Los textos de la UI distinguen observado vs estimado?
5. ¿Hay enlace o referencia suficiente para que un tercero lo audite?

## Flujo recomendado

1. Añadir o actualizar fuente en `data/raw`.
2. Reprocesar CSV en `data/processed`.
3. Ejecutar:

```powershell
python tools/validate_data_quality.py
```

4. Si hay errores, corregir antes de tocar visualizaciones.
5. Si pasa validación, actualizar dashboard y notas de fuente.

---

## Bloque A — Sueño y scroll nocturno

Dataset: `data/processed/sleep_studies.csv`
Página del dashboard: `03_cerebro.py`

### Fuentes incluidas

| ID | Autores | Año | Institución | DOI | Métrica principal |
|----|---------|-----|-------------|-----|-------------------|
| SL001 | Levenson JC et al. | 2017 | Univ. of Pittsburgh | [10.1016/j.pmedr.2017.01.010](https://doi.org/10.1016/j.pmedr.2017.01.010) | Odds ratio alteración sueño: 1.95× en cuartil alto de uso de RRSS |
| SL002 | Chang AM et al. | 2015 | Harvard Med. / BWH | [10.1073/pnas.1418490112](https://doi.org/10.1073/pnas.1418490112) | Supresión melatonina 55% con pantalla LED vs 8% con papel |
| SL003 | Chang AM et al. | 2015 | Harvard Med. / BWH | [10.1073/pnas.1418490112](https://doi.org/10.1073/pnas.1418490112) | Retraso circadiano 1.5h pantalla vs 0.2h papel |
| SL004 | Stieger S et al. | 2019 | King's College London | [10.1093/sleep/zsz108](https://doi.org/10.1093/sleep/zsz108) | Déficit Pittsburgh Sleep Quality Index asociado a uso nocturno de redes |

### Notas metodológicas

- **SL001**: n = 1 788 adultos jóvenes (19-32 años). Diseño transversal. La asociación es estadísticamente significativa tras ajuste por confusores (edad, sexo, depresión). No establece causalidad.
- **SL002-SL003**: n = 12 adultos sanos. Ensayo cruzado. Comparativa entre e-reader con retroiluminación LED vs libro en papel con lámpara tenue. Las cifras de supresión de melatonina y retraso circadiano son medias del grupo, no valores individuales.
- **SL004**: n = 10 904 participantes. Estudio de cohortes. El déficit de calidad de sueño se mide con el Índice de Calidad de Sueño de Pittsburgh (PSQI); mayor puntuación = peor calidad.

### Qué se evita

- No se afirma que "la pantalla arruina el sueño" de forma absoluta: se describe asociación, no causalidad obligatoria.
- No se generaliza el estudio de Chang (n=12) como representativo de toda la población: se contextualiza como evidencia mecanística.

---

## Bloque B — Atención sostenida (multitasking digital)

Dataset: `data/processed/attention_studies.csv`
Página del dashboard: `01_cognitivo.py`

### Fuentes incluidas

| ID | Autores | Año | Institución | DOI | Métrica principal |
|----|---------|-----|-------------|-----|-------------------|
| AT001 | Ophir E, Nass C, Wagner AD | 2009 | Stanford University | [10.1073/pnas.0903620106](https://doi.org/10.1073/pnas.0903620106) | Mayor susceptibilidad a interferencia de estímulos irrelevantes en heavy media multitaskers |
| AT002 | Mark G, Gudith D, Klocke U | 2008 | UC Irvine | [10.1145/1357054.1357072](https://doi.org/10.1145/1357054.1357072) | 23 minutos de media para recuperar foco completo tras una interrupción digital |
| AT003 | Mark G et al. | 2023 | UC Irvine | [10.1145/3544548.3580600](https://doi.org/10.1145/3544548.3580600) | Tiempo de atención media en pantalla digital: 47 segundos |
| AT004 | Ophir E, Nass C, Wagner AD | 2009 | Stanford University | [10.1073/pnas.0903620106](https://doi.org/10.1073/pnas.0903620106) | Menor capacidad de filtrado en memoria de trabajo en heavy multitaskers |

### Notas metodológicas

- **AT001, AT004**: n = 262. Se define heavy media multitasker como el cuartil superior de uso simultáneo de múltiples medios digitales. Los scores son comparativos entre grupos, no escalas normalizadas absolutas.
- **AT002**: n = 49 trabajadores de oficina. El tiempo de 23 minutos es la media de recuperación de foco *completo*; el tiempo para retomar la tarea interrumpida fue de ~1-2 minutos.
- **AT003**: n = 276. Estudio de observación de trabajadores del conocimiento. Media de 47 segundos de atención continua en una pantalla antes de cambiar de aplicación o tarea.

### Qué se evita — cita Microsoft de 8 segundos

La cifra de "atención humana de 8 segundos" (inferior al pez dorado) circuló ampliamente desde 2015 y fue atribuida a un informe de Microsoft Canada. Ese informe no es un estudio revisado por pares, no declaró metodología reproducible y ha sido criticado explícitamente por investigadores de atención cognitiva (Egan, 2016; Rosen & Samuel, 2015). **Esta cifra no se usa en ninguna visualización del dashboard.**

---

## Bloque C — Hábitos de lectura por generación

Dataset: `data/processed/reading_by_generation.csv`
Página del dashboard: `02_tiempo.py` (tab "Por generación")

### Fuentes incluidas

| País | Fuente | Año | URL |
|------|--------|-----|-----|
| España | FGEE — Hábitos de Lectura y Compra de Libros | 2024 | [federacioneditores.org](https://www.federacioneditores.org/lectura-y-compra-de-libros/) |
| Estados Unidos | Pew Research Center — Books and Reading | 2023 | [pewresearch.org](https://www.pewresearch.org/internet/2023/01/09/who-reads-books-in-america/) |

### Desglose por generación (España, FGEE 2024)

| Generación | Rango de edad | Lee regularmente | Libros/año | Scroll/día |
|------------|---------------|-----------------|------------|------------|
| GenZ | 16-24 | 57,4% | 5,2 | 197 min |
| Millennial | 25-40 | 64,8% | 8,1 | 148 min |
| GenX | 41-55 | 69,3% | 9,4 | 103 min |
| Boomer | 56+ | 71,9% | 10,1 | 71 min |

### Desglose por generación (EE.UU., Pew 2023)

| Generación | Rango de edad | Ha leído un libro en el último año | Libros/año |
|------------|---------------|-------------------------------------|------------|
| GenZ | 18-29 | 72% | 11,8 |
| Millennial | 30-49 | 79% | 14,2 |
| GenX | 50-64 | 76% | 12,1 |
| Boomer | 65+ | 73% | 10,8 |

### Notas metodológicas

- Los datos de minutos de social media por generación se obtienen del cruce FGEE + Reuters Institute Digital Report 2024 desglosado por edad. Cuando el informe no provee el desglose exacto generacional, se estima por interpolación del rango de edad más próximo.
- Los datos de Pew corresponden a lectores de cualquier formato (papel, digital, audio). El dato de "libros/año" es la mediana declarada por los participantes.
- **Limitación**: los rangos generacionales no son estándar entre fuentes (Pew y FGEE usan cortes de edad ligeramente distintos). Se han adaptado a la clasificación más extendida (GenZ / Millennial / GenX / Boomer) con la correspondencia más próxima posible.

---

## Registro de cambios de datos (changelog)

| Fecha | Acción | Dataset | Responsable |
|-------|--------|---------|-------------|
| 2026-04-22 | Creación inicial | cognitive_studies, screen_time, reading_habits | Hito 1 |
| 2026-04-22 | Adición | sleep_studies | Hito 3 |
| 2026-04-22 | Adición | attention_studies | Hito 3 |
| 2026-04-22 | Adición | reading_by_generation | Hito 3 |
