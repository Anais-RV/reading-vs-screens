# Tu cerebro cuando lees 📖 vs. cuando scrolleas 📱

[![Python](https://img.shields.io/badge/Python-3.11%2B-blue?logo=python)](https://www.python.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

---

## Por qué este proyecto

El español medio pasa **más de 7 horas al día frente a pantallas** y solo **18 minutos leyendo**.
No es un dato de opinión: es la media que reportan el Reuters Institute Digital Report 2024 y la
Federación de Gremios de Editores de España.

¿Qué consecuencias tiene eso en nuestro cerebro? ¿Qué gana —o pierde— quien lee habitualmente
frente a quien no lo hace? Eso es exactamente lo que analiza este proyecto, combinando datos de
hábitos culturales internacionales con hallazgos de neurociencia revisados por pares.

---

## Hallazgos principales

- 📌 **[STAT] 6 minutos de lectura reducen el estrés un 68 %** — más que escuchar música (61 %)
  o salir a caminar (42 %). *(University of Sussex, 2009)*
- 📌 **[STAT] Los lectores habituales tienen un 32 % menos de riesgo de deterioro cognitivo**
  en la vejez. *(Rush University Medical Center, 2013)*
- 📌 **[STAT] En España el ratio pantallas/lectura es de 23:1** — 420 min de pantallas frente a 18 min de lectura al día.
  *(Reuters Institute 2024 / FGEE 2024)*
- 📌 **[STAT] México lidera el tiempo en pantallas en habla hispana: 7 h 25 min/día** frente a
  solo 14 minutos de lectura en promedio. *(Reuters Institute 2024 / CANIEM 2024)*
- 📌 **[STAT] Desde 2019 el tiempo en redes sociales en España ha crecido un +63 %**, mientras
  que la lectura diaria ha quedado prácticamente plana. *(Reuters Institute 2019–2024 / FGEE 2019–2024)*
- 📌 **[STAT] Leer ficción mejora la empatía cognitiva un 29 %** en grupos experimentales
  frente a controles. *(University of Toronto, 2013)*
- 📌 **[STAT] En Japón la media de lectura diaria es de 26 min** — 1,4× la de España (18 min) y 2× la de Colombia (13 min).
  *(JPIC Reading Survey 2024)*

---

## Metodología

### Datos

Los datos provienen de cuatro fuentes principales:

| Dataset | Fuente | Cobertura |
|---|---|---|
| `screen_time.csv` | Reuters Institute Digital Report | 10 países, 2019–2024 |
| `reading_habits.csv` | FGEE / CERLALC / Stiftung Lesen / Pew | 10 países, 2019–2024 |
| `cognitive_studies.csv` | PubMed (curación manual) | 10 estudios, 2008–2019 |

Todos los archivos incluyen una columna `source` con la referencia completa de la fuente original.
Los datos de pantallas y lectura son medias nacionales autorreportadas; los estudios cognitivos
son grupos experimentales de laboratorio. **No se deben comparar directamente las magnitudes**
de ambos tipos de datos.

### Veracidad y trazabilidad

- Política de veracidad: `docs/veracidad_metodologia.md`
- Backlog de nuevas fuentes: `docs/fuentes_backlog.md`
- Validación automática de calidad de datos:

```bash
python tools/validate_data_quality.py
```

Si esta validación falla, no se debe publicar ni actualizar visualizaciones.

### Análisis

El notebook `notebooks/01_analysis.ipynb` realiza:
1. Validación de esquemas de columnas
2. EDA con distribuciones y detección de outliers
3. Análisis comparativo por país (ratio pantallas/lectura)
4. Evolución temporal 2019–2024 en países hispanohablantes
5. Scatter plots de beneficios cognitivos por estudio

---

## Arquitectura actual

El proyecto se centra en una capa pública:

- `frontend-prototype/`: landing React/Vite orientada a captación, simulación y descarga de cards compartibles.

Los datos analizados y la metodología permanecen en el repositorio para trazabilidad y evolución del contenido.

---

## Cómo ejecutar la landing pública localmente

```bash
cd frontend-prototype
npm install
npm run dev
```

La landing quedará disponible en `http://localhost:4173` o en el siguiente puerto libre.

## Cómo ejecutar análisis y utilidades de datos

### 1. Clonar el repositorio

```bash
git clone https://github.com/anaisentrelineas/reading-vs-screens.git
cd reading-vs-screens
```

### 2. Crear entorno virtual e instalar dependencias

```bash
python -m venv .venv
# En macOS / Linux:
source .venv/bin/activate
# En Windows:
.venv\Scripts\activate

pip install -r requirements.txt
```

### 3. (Opcional) Ejecutar el notebook de análisis

```bash
jupyter notebook notebooks/01_analysis.ipynb
```

---

## Estructura del repositorio

```
reading-vs-screens/
├── data/
│   ├── raw/                  # CSVs originales con fuente en el nombre
│   └── processed/            # Datos limpios listos para el dashboard
├── notebooks/
│   └── 01_analysis.ipynb
├── frontend-prototype/
│   ├── src/                  # Landing React/Vite para cards y captación
│   ├── package.json
│   └── README.md
├── requirements.txt
└── SPEC.md
```

---

## Contenido para el Día del Libro

En la carpeta `contenido-dia-del-libro/` están los materiales de divulgación listos para publicar:

- `carrusel_instagram.md` — guión de 10 slides para maquetar en Canva/Figma, con paleta, tipografías y todas las cifras ya verificadas contra los CSV.
- `caption_post.md` — tres versiones de caption (larga, corta, reflexiva) + estrategia de publicación.
- `hashtags.md` — tres sets rotables de hashtags + lista de editoriales a las que etiquetar con criterio.

Estos materiales se generan a partir del análisis del notebook (`notebooks/01_analysis.ipynb`, sección 7). Si los datos cambian, regenerar los mensajes clave antes de publicar.

---

## Cómo contribuir

1. Abre un _issue_ describiendo el cambio o corrección propuesta
2. Haz un _fork_ del repo y crea una rama: `git checkout -b mejora/mi-aportacion`
3. Haz commit con mensajes descriptivos en español o inglés
4. Abre un _pull request_ hacia `main`

Las contribuciones más bienvenidas son: **nuevas fuentes de datos**, **correcciones de cifras**
con enlace a la fuente original, y **mejoras de visualización**.

---

## Licencia

MIT © 2026 — Publicado el Día del Libro, 23 de abril de 2026
