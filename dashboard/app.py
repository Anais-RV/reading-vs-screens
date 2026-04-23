"""
app.py — Punto de entrada del dashboard "Tu cerebro cuando lees"
"""
import sys
from pathlib import Path

import streamlit as st

# Permite ejecutar la app desde raiz del repo o desde el directorio dashboard.
sys.path.insert(0, str(Path(__file__).parent))

from data_loader import load_dataset_lazy
from components.utils import load_css

# ── Configuración global ─────────────────────────────────────────────────────
st.set_page_config(
    page_title="Tu cerebro cuando lees",
    page_icon="R",
    layout="wide",
    initial_sidebar_state="expanded",
)

load_css(str(Path(__file__).parent / "assets" / "custom.css"))

instagram_handle = "@anaisentrelineas"
github_repo_url = "https://github.com/anaisentrelineas/reading-vs-screens"
try:
    instagram_handle = st.secrets.get("instagram_handle", instagram_handle)
    github_repo_url = st.secrets.get("github_repo_url", github_repo_url)
except Exception:
    pass

screen_df = load_dataset_lazy("screen_time")
reading_df = load_dataset_lazy("reading_habits")

headline_screen = 420
headline_reading = 18
if screen_df is not None and reading_df is not None:
    try:
        s = screen_df[(screen_df["country"] == "España") & (screen_df["year"] == 2024)].iloc[0]
        r = reading_df[(reading_df["country"] == "España") & (reading_df["year"] == 2024)].iloc[0]
        headline_screen = int(s["avg_daily_total_screen_min"])
        headline_reading = int(r["avg_daily_reading_min"])
    except Exception:
        pass

# ── Sidebar ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.title("Tu cerebro cuando lees")
    st.markdown(
        """
        Exploramos el impacto cognitivo real de la lectura frente al consumo
        de pantallas, con datos de estudios internacionales y encuestas de
        hábitos culturales en 10 países.
        """
    )
    st.divider()

    st.subheader("Navega por el análisis")
    st.page_link("app.py", label="Inicio")
    st.page_link("pages/01_cognitivo.py", label="Impacto cognitivo")
    st.page_link("pages/02_tiempo.py", label="Tiempo y hábitos")
    st.page_link("pages/03_cerebro.py", label="El cerebro")

    st.divider()

    st.subheader("Fuentes de datos")
    st.markdown(
        """
        - [Reuters Institute Digital Report 2024](https://reutersinstitute.politics.ox.ac.uk)
        - [FGEE Hábitos de Lectura 2024](https://www.federacioneditores.org)
        - [CERLALC Indicadores 2024](https://cerlalc.org)
        - [Pew Research / Books & Reading](https://www.pewresearch.org)
        - [PubMed / DOI](https://pubmed.ncbi.nlm.nih.gov)
        """
    )
    st.divider()
    st.markdown(
        """
        <div class="trust-note compact">
            <strong>Datos reales, no frases vacias.</strong><br>
            Cada pagina parte de estudios y fuentes citadas en el propio dashboard.
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.divider()
    st.markdown(
        "[![GitHub](https://img.shields.io/badge/GitHub-repo-black?logo=github)]"
        f"({github_repo_url})"
    )

# ── Página de inicio ─────────────────────────────────────────────────────────
st.markdown(
    """
    <section class="brain-hero home-hero">
        <div class="brain-hero-copy">
            <span class="brain-kicker">Si llegaste desde el post del 23, empieza aqui</span>
            <h1>Recupera minutos de lectura, gana criterio</h1>
            <p>
                No es solo productividad ni nostalgia: es autonomia mental.
                Este dashboard muestra con datos reales por que parar, leer y elegir con calma
                es una forma concreta de recuperar atencion, criterio y libertad personal.
            </p>
        </div>
        <div class="brain-hero-panel">
            <div class="brain-panel-label">Foto rapida de Espana (2024)</div>
            <div class="brain-panel-value">{headline_screen} min pantalla vs {headline_reading} min lectura</div>
            <div class="brain-panel-copy">
                El contraste es fuerte: cuanto mas decide el algoritmo por ti, menos tiempo queda
                para decidir tu que quieres pensar, leer y recordar.
            </div>
        </div>
    </section>
    """.format(headline_screen=headline_screen, headline_reading=headline_reading),
    unsafe_allow_html=True,
)

st.markdown(
    """
    <section class="manifesto-card">
        <h3>Manifiesto lector</h3>
        <p>
            Leer hoy tambien es un acto reivindicativo: elegir profundidad frente a interrupcion,
            contexto frente a titular, y criterio propio frente a recomendacion automatica.
        </p>
        <p>
            No venimos a demonizar pantallas. Venimos a recordar que puedes parar,
            volver a elegir y usar tu atencion para lo que de verdad te importa.
        </p>
    </section>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="trust-strip">
        <div class="trust-pill">10 paises analizados</div>
        <div class="trust-pill">2019-2024</div>
        <div class="trust-pill">Estudios con DOI y encuestas citadas</div>
        <div class="trust-pill">Datos observados + estimaciones marcadas</div>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    f"""
    <div class="ig-cta">
        <strong>Te ha explotado la cabeza con algun dato?</strong>
        Comparte una captura en stories, menciona <strong>{instagram_handle}</strong>
        y suma una idea: <em>"Recupera minutos de lectura, gana criterio"</em>.
    </div>
    """,
    unsafe_allow_html=True,
)

st.divider()

col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Países analizados", "10", delta=None)
with col2:
    st.metric("Estudios científicos", "10", delta=None)
with col3:
    st.metric("Años de datos", "2019–2024", delta=None)

st.divider()

st.markdown('<div class="brain-section-eyebrow">Empieza aqui</div>', unsafe_allow_html=True)
st.subheader("Elige una ruta en 20 segundos")
st.caption("Si vienes del post del 23, entra por la pregunta que mas te interese y tendras una respuesta clara con datos.")
c1, c2, c3 = st.columns(3)
with c1:
    st.markdown(
        """
        <div class="brain-gallery-card">
            <span class="brain-gallery-tag">Impacto cognitivo</span>
            <h4>Que mejora en tu cerebro cuando lees de forma habitual</h4>
            <p><strong>Veras:</strong> memoria, empatia, vocabulario y concentracion.</p>
            <p><strong>Te llevas:</strong> evidencia cientifica lista para explicar y compartir.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
with c2:
    st.markdown(
        """
        <div class="brain-gallery-card">
            <span class="brain-gallery-tag">Tiempo y habitos</span>
            <h4>Cuantos minutos pierdes en pantalla y cuantos puedes recuperar leyendo</h4>
            <p><strong>Veras:</strong> comparativas por pais y evolucion anual.</p>
            <p><strong>Te llevas:</strong> una calculadora y tarjetas para stories/feed.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
with c3:
    st.markdown(
        """
        <div class="brain-gallery-card dark">
            <span class="brain-gallery-tag">El cerebro</span>
            <h4>Que pasa dentro de tu cabeza: lectura profunda vs scroll infinito</h4>
            <p><strong>Veras:</strong> diferencias de atencion, estres y procesamiento mental.</p>
            <p><strong>Te llevas:</strong> una explicacion visual que engancha al primer vistazo.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown(
    """
    <div class="trust-note">
        <strong>Importante:</strong> las cifras del dashboard proceden de los CSV procesados del proyecto.
        Cuando una visualizacion es una sintesis o una estimacion, se indica de forma explicita para no mezclar datos observados con recursos narrativos.
    </div>
    """,
    unsafe_allow_html=True,
)

# ── Footer ───────────────────────────────────────────────────────────────────
st.divider()
st.markdown(
    "<p style='text-align:center; color:gray; font-size:0.85rem;'>"
    "Proyecto de divulgacion con datos trazables · Datos actualizados: abril 2026 · "
    f"<a href='{github_repo_url}' style='color:#1D9E75;'>reading-vs-screens</a>"
    "</p>",
    unsafe_allow_html=True,
)
