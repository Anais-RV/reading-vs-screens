"""
02_tiempo.py — Comparativa de tiempo y hábitos: lectura vs. pantallas
"""
import sys
import time
from datetime import datetime
from pathlib import Path

import plotly.graph_objects as go
import streamlit as st

sys.path.insert(0, str(Path(__file__).parent.parent))
from data_loader import load_dataset_lazy
from components.image_exporter import export_figure_with_branding
from components.share_card import (
    export_profile_share_card,
    export_share_card,
    render_profile_share_card,
    render_share_card,
)
from components.utils import load_css

DASHBOARD_URL = "https://reading-vs-screens.streamlit.app"
try:
    DASHBOARD_URL = st.secrets.get("dashboard_url", DASHBOARD_URL)
except Exception:
    pass

st.set_page_config(page_title="Tiempo y hábitos", page_icon="R", layout="wide")

load_css(str(Path(__file__).parent.parent / "assets" / "custom.css"))

st.markdown(
    """
    <section class="brain-hero inner-page-hero">
        <div class="brain-hero-copy">
            <span class="brain-kicker">Tiempo y habitos</span>
            <h1>Los minutos que te quitan criterio y los que te devuelve la lectura</h1>
            <p>
                Esta es la parte mas clara del dashboard: comparas paises, ves tendencias y calculas en segundos
                cuanto cambia tu ano lector si reduces tiempo de pantallas.
            </p>
        </div>
        <div class="brain-hero-panel">
            <div class="brain-panel-label">Promesa de la pagina</div>
            <div class="brain-panel-value">Datos comparables y accionables</div>
            <div class="brain-panel-copy">
                Mostramos minutos observados por pais y ano. Cuando algo es estimado, queda marcado como estimado.
            </div>
        </div>
    </section>
    """,
    unsafe_allow_html=True,
)

# ── Datos ────────────────────────────────────────────────────────────────────
screen_df = load_dataset_lazy("screen_time")
reading_df = load_dataset_lazy("reading_habits")

if screen_df is None or reading_df is None:
    st.error("No se pudieron cargar los datos. Vuelve a la página de inicio.")
    st.stop()

# ── Selector de país ──────────────────────────────────────────────────────────
paises_disponibles = sorted(screen_df["country"].unique().tolist())
pais = st.selectbox("Selecciona un país", paises_disponibles, index=0)

screen_pais = screen_df[screen_df["country"] == pais]
reading_pais = reading_df[reading_df["country"] == pais]

if screen_pais.empty or reading_pais.empty:
    st.warning(f"No hay datos disponibles para {pais}.")
    st.stop()


# ── Helpers ───────────────────────────────────────────────────────────────────

def _books_from_minutes(minutes_per_day: int) -> float:
    """Convierte minutos diarios en libros al año (estimación de orden de magnitud)."""
    paginas_libro = 300
    minutos_pagina = 2
    return (minutes_per_day * 365) / (paginas_libro * minutos_pagina)


def _next_book_day(now: datetime) -> datetime:
    """Devuelve el próximo 23 de abril 23:59:59."""
    target = datetime(now.year, 4, 23, 23, 59, 59)
    if now > target:
        target = datetime(now.year + 1, 4, 23, 23, 59, 59)
    return target


def _reader_profile(books_last_year: int, social_minutes: int, reading_place: str, goal: str) -> tuple[str, str]:
    """Clasifica un perfil lector con una narrativa compartible."""
    score = 0
    if books_last_year >= 12:
        score += 2
    elif books_last_year >= 5:
        score += 1

    if social_minutes <= 90:
        score += 2
    elif social_minutes <= 180:
        score += 1

    if reading_place != "No suelo leer":
        score += 1

    if goal in {"Recuperar foco", "Profundizar ideas"}:
        score += 1

    if score <= 2:
        return (
            "Lector en transicion",
            "Estas en fase de despegue: tienes curiosidad, pero las pantallas aun compiten por tu atencion.",
        )
    if score <= 4:
        return (
            "Lector en reconstruccion",
            "Ya proteges bloques de lectura. Tu siguiente salto es volverlo rutina semanal no negociable.",
        )
    if score <= 5:
        return (
            "Lector estrategico",
            "Lees con intencion y criterio. Tu reto ahora es blindar tiempo para lectura larga.",
        )
    return (
        "Lector voraz con tiempo robado",
        "Tu habito es fuerte, pero aun hay minutos capturados por scroll que podrian ser lectura profunda.",
    )


@st.cache_data
def _book_pile_svg(n_books: int) -> str:
    """Genera un SVG de lomos de libros apilados como una estantería que crece."""
    if n_books == 0:
        return (
            '<div style="padding:12px 0; color:#999; font-style:italic; font-size:0.9rem;">'
            "Sin libros aún — mueve el slider de lectura"
            "</div>"
        )

    SPINE_COLORS = ["#1D9E75", "#D85A30", "#8B6E4E", "#2D5E8E", "#A85C8E", "#5E8E2D", "#C4A832"]
    cap = min(n_books, 14)
    book_w = 16
    book_h = 72
    gap = 3
    base_y = 8
    svg_w = gap + cap * (book_w + gap)
    svg_h = book_h + base_y + 20

    spines = ""
    for i in range(cap):
        x = gap + i * (book_w + gap)
        col = SPINE_COLORS[i % len(SPINE_COLORS)]
        # Lomo con ligera variación de altura para naturalidad
        h_var = book_h - (i % 3) * 4
        y = base_y + (book_h - h_var)
        spines += (
            f'<rect x="{x}" y="{y}" width="{book_w}" height="{h_var}" '
            f'rx="2" ry="2" fill="{col}" opacity="0.92"/>\n'
            f'<line x1="{x + 2}" y1="{y + 4}" x2="{x + 2}" y2="{y + h_var - 4}" '
            f'stroke="rgba(255,255,255,0.25)" stroke-width="1"/>\n'
        )

    extra_label = ""
    if n_books > 14:
        extra_label = (
            f'<text x="{svg_w // 2}" y="{svg_h - 2}" text-anchor="middle" '
            f'font-size="9" fill="#888" font-family="sans-serif">+{n_books - 14} más</text>'
        )

    return (
        f'<svg width="{svg_w}" height="{svg_h}" xmlns="http://www.w3.org/2000/svg">'
        f"{spines}{extra_label}</svg>"
    )


# Datos del año más reciente
latest_year = int(screen_pais["year"].max())
row_screen = screen_pais[screen_pais["year"] == latest_year].iloc[0]
row_reading = reading_pais[reading_pais["year"] == latest_year].iloc[0]

st.markdown(
    f"""
    <div class="trust-strip">
        <div class="trust-pill">Pantallas: {row_screen['source']}</div>
        <div class="trust-pill">Lectura: {row_reading['source']}</div>
        <div class="trust-pill">Pais activo: {pais}</div>
    </div>
    """,
    unsafe_allow_html=True,
)

st.divider()

# ── Simulador dual ────────────────────────────────────────────────────────────
st.subheader("Simulador: redistribuye tu tiempo")
st.markdown(
    "Mueve cualquiera de los dos sliders — están enlazados. "
    "Cada minuto que recuperas del scroll pasa automáticamente a lectura posible."
)

TOTAL_MIN = 120  # ventana de tiempo a redistribuir

# Inicializar estado — el slider de scroll lidera por defecto
if "scroll_sim_min" not in st.session_state:
    st.session_state.scroll_sim_min = 90
if "lectura_sim_min" not in st.session_state:
    st.session_state.lectura_sim_min = TOTAL_MIN - 90


def _on_scroll_sim() -> None:
    st.session_state.lectura_sim_min = TOTAL_MIN - st.session_state.scroll_sim_min


def _on_lectura_sim() -> None:
    st.session_state.scroll_sim_min = TOTAL_MIN - st.session_state.lectura_sim_min


sim_c1, sim_c2 = st.columns(2)
with sim_c1:
    st.slider(
        "Scroll al día (min)",
        min_value=0,
        max_value=TOTAL_MIN,
        step=5,
        key="scroll_sim_min",
        on_change=_on_scroll_sim,
        help=f"Minutos diarios de redes sociales / scroll dentro de una ventana de {TOTAL_MIN} min",
    )
with sim_c2:
    st.slider(
        "Lectura al día (min)",
        min_value=0,
        max_value=TOTAL_MIN,
        step=5,
        key="lectura_sim_min",
        on_change=_on_lectura_sim,
        help="Minutos de lectura — se ajusta automáticamente al mover el slider de scroll",
    )

scroll_val: int = st.session_state.scroll_sim_min
lectura_val: int = st.session_state.lectura_sim_min

PAGINAS_LIBRO = 300
MINUTOS_PAGINA = 2
libros: float = (lectura_val * 365) / (PAGINAS_LIBRO * MINUTOS_PAGINA)

# Alias de compatibilidad para la share card
minutos = lectura_val

# Barra dual de distribución
pct_scroll = (scroll_val / TOTAL_MIN * 100) if TOTAL_MIN > 0 else 0
pct_lectura = (lectura_val / TOTAL_MIN * 100) if TOTAL_MIN > 0 else 0

st.markdown(
    f"""
    <div style="margin: 1.2rem 0 0.4rem; font-size: 0.82rem; color: #888; letter-spacing: 0.03em;">
        Distribución de los {TOTAL_MIN} minutos simulados
    </div>
    <div style="display:flex; height:22px; border-radius:8px; overflow:hidden; background:#EDE8DF;">
        <div style="width:{pct_scroll:.1f}%; background:#D85A30; transition:width 0.3s ease;"></div>
        <div style="width:{pct_lectura:.1f}%; background:#1D9E75; transition:width 0.3s ease;"></div>
    </div>
    <div style="display:flex; justify-content:space-between; font-size:0.8rem; margin-top:5px; font-weight:600;">
        <span style="color:#D85A30;">Scroll · {scroll_val} min</span>
        <span style="color:#1D9E75;">Lectura · {lectura_val} min</span>
    </div>
    """,
    unsafe_allow_html=True,
)

# Pila de libros creciente
st.markdown("<div style='margin-top:1.2rem;'></div>", unsafe_allow_html=True)
pile_col, result_col = st.columns([1, 2])
n_libros_display = max(0, round(libros))

with pile_col:
    st.markdown(_book_pile_svg(n_libros_display), unsafe_allow_html=True)

with result_col:
    st.markdown(f"### {int(libros)} libros al año")
    if lectura_val == 0:
        st.info("Sube el slider de lectura para ver cuántos libros ganarías.")
    else:
        st.success(
            f"Con **{lectura_val} min/día** de lectura leerías **{int(libros)} libros** este año."
        )

st.caption(
    f"Estimación basada en un libro de {PAGINAS_LIBRO} páginas a {MINUTOS_PAGINA} min/página. "
    f"Sirve para visualizar escala, no como dato observado del dataset."
)

# Share card — misma lógica que antes, ahora alimentada por lectura_val
fig_card = render_share_card(minutos, libros, DASHBOARD_URL)
st.image(fig_card, use_container_width=True)

st.markdown(
    """
    <div class="trust-note compact">
        <strong>Tip:</strong> comparte esta tarjeta y usa la comparativa por pais para abrir conversacion
        sobre como recuperar tiempo de lectura en el dia a dia.
    </div>
    """,
    unsafe_allow_html=True,
)

col1, col2 = st.columns(2)
with col1:
    try:
        img_square = export_share_card(minutos, libros, DASHBOARD_URL, format="square")
        st.download_button(
            label="Descargar (Instagram feed)",
            data=img_square,
            file_name="mi_resultado_feed.png",
            mime="image/png",
        )
    except Exception as exc:
        st.error(f"No se pudo generar la imagen para feed: {exc}")
with col2:
    try:
        img_story = export_share_card(minutos, libros, DASHBOARD_URL, format="story")
        st.download_button(
            label="Descargar (Story)",
            data=img_story,
            file_name="mi_resultado_story.png",
            mime="image/png",
        )
    except Exception as exc:
        st.error(f"No se pudo generar la imagen para story: {exc}")

st.divider()

# ── Timer 6 minutos ───────────────────────────────────────────────────────────
TIMER_DURATION_S = 360  # 6 minutos en segundos

# Citas de dominio público o con licencia libre
CITAS_LITERARIAS = [
    {
        "texto": (
            "No hay amigo tan leal como un libro."
        ),
        "autor": "Ernest Hemingway",
        "contexto": "Cita atribuida",
    },
    {
        "texto": (
            "Leer es beber y comer. El que no lee se seca."
        ),
        "autor": "Victor Hugo",
        "contexto": "El hombre que ríe, 1869",
    },
    {
        "texto": (
            "Un lector vive mil vidas antes de morir. "
            "El hombre que no lee vive solo una."
        ),
        "autor": "George R.R. Martin",
        "contexto": "Danza de Dragones, 2011",
    },
    {
        "texto": (
            "La lectura es para el alma lo que el ejercicio para el cuerpo."
        ),
        "autor": "Joseph Addison",
        "contexto": "The Spectator, 1711 — dominio público",
    },
    {
        "texto": (
            "Podeis encadenar mi cuerpo, atar mis manos, gobernar mis acciones: "
            "sois los mas fuertes y el mundo esta con vosotros. "
            "Pero con mi voluntad, señores, no podeis nada."
        ),
        "autor": "Charlotte Brontë",
        "contexto": "Jane Eyre, 1847 — dominio público",
    },
    {
        "texto": (
            "Era el mejor de los tiempos, era el peor de los tiempos; "
            "era la edad de la sabiduría, era la edad de la insensatez."
        ),
        "autor": "Charles Dickens",
        "contexto": "Historia de dos ciudades, 1859 — dominio público",
    },
]

# Estado del timer
if "timer_start" not in st.session_state:
    st.session_state.timer_start = None
if "timer_done" not in st.session_state:
    st.session_state.timer_done = False

st.subheader("Prueba 6 minutos de lectura real")
st.markdown(
    "La Universidad de Sussex (2009) demostró que **6 minutos de lectura** reducen "
    "los marcadores de estrés un **68 %** — más que escuchar música o dar un paseo. "
    "Pon el móvil boca abajo y empieza."
)

# Botón de arranque — solo visible cuando el timer no está corriendo
timer_running = st.session_state.timer_start is not None

if not timer_running and not st.session_state.timer_done:
    if st.button("Pruébalo ahora", type="primary"):
        st.session_state.timer_start = time.time()
        st.session_state.timer_done = False
        st.rerun()

# Display del timer en curso
if st.session_state.timer_start is not None:
    elapsed = time.time() - st.session_state.timer_start
    remaining = TIMER_DURATION_S - elapsed

    if remaining > 0:
        mins_left = int(remaining // 60)
        secs_left = int(remaining % 60)

        # Layout: contador + cita
        t_col, q_col = st.columns([1, 2])

        with t_col:
            st.metric(
                label="Tiempo restante",
                value=f"{mins_left}:{secs_left:02d}",
                help="Quedan estos minutos de lectura activa",
            )
            # Barra de progreso
            progress_pct = elapsed / TIMER_DURATION_S
            st.progress(min(progress_pct, 1.0))

        with q_col:
            # Rotar cita cada minuto
            cita_idx = int(elapsed // 60) % len(CITAS_LITERARIAS)
            cita = CITAS_LITERARIAS[cita_idx]
            st.markdown(
                f"""
                <div style="
                    background:#F7F3EC;
                    border-left: 4px solid #1D9E75;
                    padding: 1.1rem 1.4rem;
                    border-radius: 6px;
                    margin-top: 0.2rem;
                ">
                    <p style="
                        font-style:italic;
                        font-size:1.05rem;
                        color:#2C2C2C;
                        margin:0 0 0.6rem;
                        line-height:1.55;
                    ">«{cita['texto']}»</p>
                    <span style="font-size:0.8rem; color:#888; font-weight:600;">
                        — {cita['autor']}
                    </span>
                    <span style="font-size:0.75rem; color:#aaa; margin-left:0.4rem;">
                        {cita['contexto']}
                    </span>
                </div>
                """,
                unsafe_allow_html=True,
            )

        if st.button("Cancelar", key="cancel_timer"):
            st.session_state.timer_start = None
            st.session_state.timer_done = False
            st.rerun()

        # Recargar cada segundo sin bloquear el servidor
        time.sleep(1)
        st.rerun()

    else:
        # Timer completado
        st.session_state.timer_start = None
        st.session_state.timer_done = True
        st.rerun()

# Mensaje de cierre al terminar
if st.session_state.timer_done:
    st.success(
        "Acabas de recortar el 68 % de tus marcadores de estrés, según Sussex. "
        "Seis minutos. Sin apps, sin algoritmos, sin coste."
    )
    st.markdown(
        """
        <div style="
            background:#F7F3EC;
            border: 1.5px solid #1D9E75;
            border-radius:8px;
            padding:1rem 1.4rem;
            margin-top:0.8rem;
            font-size:0.88rem;
            color:#444;
        ">
            <strong>Fuente:</strong> Lewis, D. (2009). <em>Galaxy Stress Research</em>.
            University of Sussex / Mindlab International.
            La lectura superó a la música (61 %), el té (54 %) y el paseo (42 %) en reducción
            de frecuencia cardíaca y tensión muscular.
        </div>
        """,
        unsafe_allow_html=True,
    )
    if st.button("Repetir", key="restart_timer"):
        st.session_state.timer_done = False
        st.rerun()

st.divider()

# ── Accionables ───────────────────────────────────────────────────────────────
st.subheader("Accionables para mover conversion y engagement")
tabs = st.tabs([
    "Quiz de perfil lector",
    "Comparador de tiempo",
    "Por generacion",
    "Contador Dia del Libro",
])

with tabs[0]:
    st.markdown(
        "Responde 4 preguntas rapidas y genera una tarjeta con tu perfil para compartir. "
        "Este bloque esta pensado para viralidad personal: habla de ti, no solo de estadistica."
    )

    q1_books = st.slider("1) Cuantos libros leiste el ano pasado", 0, 40, 6)
    q2_place = st.selectbox(
        "2) Donde lees normalmente",
        ["Casa", "Transporte", "Trabajo/estudio", "Antes de dormir", "No suelo leer"],
    )
    q3_social = st.slider(
        "3) Cuanto tiempo pasas en redes al dia",
        0, 360, int(row_screen["avg_daily_social_media_min"]), step=5,
    )
    q4_goal = st.radio(
        "4) Que te gustaria ganar leyendo mas",
        ["Recuperar foco", "Profundizar ideas", "Leer por placer", "Simplemente empezar"],
        horizontal=True,
    )

    profile_name, profile_message = _reader_profile(q1_books, q3_social, q2_place, q4_goal)

    st.success(f"Tu perfil: **{profile_name}**")
    st.write(profile_message)

    profile_fig = render_profile_share_card(profile_name, profile_message, q3_social, DASHBOARD_URL)
    st.image(profile_fig, use_container_width=True)

    pc1, pc2 = st.columns(2)
    with pc1:
        try:
            profile_square = export_profile_share_card(
                profile_name, profile_message, q3_social, DASHBOARD_URL, format="square",
            )
            st.download_button(
                label="Descargar perfil (feed)",
                data=profile_square,
                file_name="perfil_lector_feed.png",
                mime="image/png",
            )
        except Exception as exc:
            st.error(f"No se pudo exportar el perfil para feed: {exc}")
    with pc2:
        try:
            profile_story = export_profile_share_card(
                profile_name, profile_message, q3_social, DASHBOARD_URL, format="story",
            )
            st.download_button(
                label="Descargar perfil (story)",
                data=profile_story,
                file_name="perfil_lector_story.png",
                mime="image/png",
            )
        except Exception as exc:
            st.error(f"No se pudo exportar el perfil para story: {exc}")

    st.caption("Perfil orientativo y narrativo. No es diagnostico clinico ni psicometrico.")

with tabs[1]:
    st.markdown(
        "Cuantifica horas al ano y traducelas a obras concretas para que el coste de oportunidad sea visible."
    )

    insta_minutes = st.slider(
        "Minutos diarios en Instagram/Reels/TikTok",
        min_value=0,
        max_value=360,
        value=int(row_screen["avg_daily_social_media_min"]),
        step=5,
    )

    insta_hours_year = (insta_minutes * 365) / 60
    books_equivalent = _books_from_minutes(insta_minutes)

    st.metric("Horas al ano en scroll", f"{insta_hours_year:,.0f} h")
    st.metric("Libros equivalentes (estimado)", f"{books_equivalent:,.1f}")

    st.markdown(
        f"Con **{insta_hours_year:,.0f} horas al ano** podrias cubrir una ruta de lectura extensa. "
        "Ejemplo editorial de referencia: Kafka (obra seleccionada), Ursula K. Le Guin "
        "(ciclo de Terramar) y aun quedaria margen para ensayo contemporaneo."
    )
    st.caption(
        "Equivalencias estimadas con 300 paginas/libro y 2 min/pagina. "
        "Sirven para visualizar escala, no para afirmar consumo real."
    )

    if insta_minutes >= 180:
        st.warning(
            "Zona de riesgo de atencion: estas cediendo mas de 3 horas diarias "
            "a plataformas de captura de tiempo."
        )
    elif insta_minutes >= 90:
        st.info(
            "Zona intermedia: hay margen claro para recuperar foco "
            "si blindas un bloque diario de lectura."
        )
    else:
        st.success(
            "Zona de control: ya estas protegiendo parte de tu tiempo frente al scroll continuo."
        )

with tabs[2]:
    st.markdown(
        "Cuanto lees depende de cuándo naciste — pero también de cuánto scroll consumes. "
        "Esta comparativa cruza hábitos lectores y tiempo en redes por generación."
    )

    gen_df = load_dataset_lazy("reading_by_generation")

    if gen_df is None or gen_df.empty:
        st.info("Dataset por generación en construcción — volverá pronto.")
    else:
        # Selector de país
        gen_paises = sorted(gen_df["country"].unique().tolist())
        gen_pais = st.selectbox("País", gen_paises, key="gen_country_sel")
        gen_pais_df = gen_df[gen_df["country"] == gen_pais].copy()

        # Orden generacional coherente
        GEN_ORDER = ["GenZ", "Millennial", "GenX", "Boomer"]
        gen_pais_df["_order"] = gen_pais_df["generation_label"].map(
            {g: i for i, g in enumerate(GEN_ORDER)}
        )
        gen_pais_df = gen_pais_df.sort_values("_order")

        # Métricas rápidas: generación que más lee y la que más hace scroll
        top_reader = gen_pais_df.loc[gen_pais_df["avg_books_per_year"].idxmax()]
        top_scroller = gen_pais_df.loc[gen_pais_df["avg_daily_social_media_min"].idxmax()]

        gk1, gk2, gk3 = st.columns(3)
        gk1.metric(
            "Generación que más lee",
            top_reader["generation_label"],
            f"{top_reader['avg_books_per_year']:.1f} libros/año",
        )
        gk2.metric(
            "Generación que más hace scroll",
            top_scroller["generation_label"],
            f"{int(top_scroller['avg_daily_social_media_min'])} min/día",
        )
        gk3.metric(
            "Brecha de libros GenZ vs Boomer",
            f"{gen_pais_df[gen_pais_df['generation_label']=='Boomer']['avg_books_per_year'].values[0] - gen_pais_df[gen_pais_df['generation_label']=='GenZ']['avg_books_per_year'].values[0]:.1f}",
            "libros/año de diferencia",
        )

        st.markdown("<div style='margin-top:1rem;'></div>", unsafe_allow_html=True)

        # Gráfico doble: libros/año (barras) + scroll/día (línea)
        fig_gen = go.Figure()
        fig_gen.add_trace(go.Bar(
            x=gen_pais_df["generation_label"],
            y=gen_pais_df["avg_books_per_year"],
            name="Libros al año",
            marker_color="#1D9E75",
            yaxis="y1",
        ))
        fig_gen.add_trace(go.Scatter(
            x=gen_pais_df["generation_label"],
            y=gen_pais_df["avg_daily_social_media_min"],
            name="Minutos de scroll al día",
            mode="lines+markers",
            line=dict(color="#D85A30", width=3),
            marker=dict(size=9),
            yaxis="y2",
        ))
        fig_gen.update_layout(
            template="plotly_white",
            yaxis=dict(title="Libros/año", titlefont=dict(color="#1D9E75")),
            yaxis2=dict(
                title="Min scroll/día",
                titlefont=dict(color="#D85A30"),
                overlaying="y",
                side="right",
            ),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            margin=dict(t=20, b=20, l=20, r=60),
            height=380,
        )
        st.plotly_chart(fig_gen, use_container_width=True)

        # Tabla detallada
        with st.expander("Ver tabla completa por generación"):
            gen_display = gen_pais_df[[
                "generation_label", "age_range", "pct_reads_regularly",
                "avg_books_per_year", "avg_daily_reading_min",
                "avg_daily_social_media_min", "year", "source",
            ]].rename(columns={
                "generation_label": "Generación",
                "age_range": "Edad",
                "pct_reads_regularly": "Lee regularmente (%)",
                "avg_books_per_year": "Libros/año",
                "avg_daily_reading_min": "Lectura (min/día)",
                "avg_daily_social_media_min": "Scroll (min/día)",
                "year": "Año",
                "source": "Fuente",
            })
            st.dataframe(gen_display, hide_index=True, use_container_width=True)

        st.caption(
            f"Fuentes: {', '.join(gen_pais_df['source'].unique())}. "
            "Los datos por generación son desgloses de los informes nacionales indicados "
            "y pueden incluir estimaciones cuando el informe original no desglosa hasta nivel generacional."
        )

with tabs[3]:
    now = datetime.now()
    target = _next_book_day(now)
    delta = target - now
    total_seconds = max(int(delta.total_seconds()), 0)

    days = total_seconds // 86400
    hours = (total_seconds % 86400) // 3600
    minutes_left = (total_seconds % 3600) // 60

    st.markdown(
        "Cuenta atras para activar campaña y cierre de compromisos antes del 23 de abril."
    )
    dc1, dc2, dc3 = st.columns(3)
    dc1.metric("Dias", f"{days}")
    dc2.metric("Horas", f"{hours}")
    dc3.metric("Minutos", f"{minutes_left}")

    st.markdown(f"**Proximo 23 de abril:** {target.strftime('%d/%m/%Y %H:%M')}")
    st.caption(
        "Si hoy defines un bloque diario de 20 minutos de lectura, "
        "llegas al Dia del Libro con una base real de habito."
    )

st.divider()

# ── Bar chart horizontal: actividades del día ─────────────────────────────────
st.subheader(f"¿Cómo pasa el día un habitante de {pais}? ({latest_year})")

actividades = {
    "Redes sociales": row_screen["avg_daily_social_media_min"],
    "Televisión": row_screen["avg_daily_tv_min"],
    "Lectura": row_reading["avg_daily_reading_min"],
    "Sueño (estimado)": 480,
    "Comidas (estimado)": 60,
}
colores = ["#D85A30", "#FF6C1F", "#1D9E75", "#155FCC", "#AEA343"]

fig_bar = go.Figure(go.Bar(
    y=list(actividades.keys()),
    x=list(actividades.values()),
    orientation="h",
    marker_color=colores,
    text=[f"{v} min" for v in actividades.values()],
    textposition="outside",
))
fig_bar.update_layout(
    template="plotly_white",
    xaxis_title="Minutos por día",
    margin=dict(l=10, r=60, t=20, b=30),
    height=320,
)
st.plotly_chart(fig_bar, use_container_width=True)

try:
    img_bytes = export_figure_with_branding(fig_bar, filename="cerebro_lector_tiempo")
    st.download_button(
        label="Descargar imagen",
        data=img_bytes,
        file_name="cerebro_lector_tiempo.png",
        mime="image/png",
    )
except Exception as exc:
    st.error(f"No se pudo exportar la imagen: {exc}")

# ── Línea temporal: evolución lectura vs. pantallas ──────────────────────────
st.subheader(f"Evolución 2019–{screen_df['year'].max()}: pantallas vs. lectura en {pais}")

merged = screen_pais.merge(reading_pais[["year", "avg_daily_reading_min"]], on="year")
merged = merged.sort_values("year")

fig_line = go.Figure()
fig_line.add_trace(go.Scatter(
    x=merged["year"],
    y=merged["avg_daily_total_screen_min"],
    name="Total pantallas",
    line=dict(color="#D85A30", width=3),
    mode="lines+markers",
))
fig_line.add_trace(go.Scatter(
    x=merged["year"],
    y=merged["avg_daily_reading_min"],
    name="Lectura",
    line=dict(color="#1D9E75", width=3),
    mode="lines+markers",
))
fig_line.update_layout(
    template="plotly_white",
    yaxis_title="Minutos por día",
    xaxis=dict(tickvals=sorted(merged["year"].unique())),
    legend=dict(orientation="h", yanchor="bottom", y=-0.3, xanchor="center", x=0.5),
    margin=dict(t=20, b=60),
    height=360,
)
st.plotly_chart(fig_line, use_container_width=True)

try:
    img_line = export_figure_with_branding(fig_line, filename="evolucion_lectura_pantallas")
    st.download_button(
        label="Descargar gráfico evolución",
        data=img_line,
        file_name="evolucion_lectura_pantallas.png",
        mime="image/png",
    )
except Exception as exc:
    st.error(f"No se pudo exportar el gráfico de evolución: {exc}")
