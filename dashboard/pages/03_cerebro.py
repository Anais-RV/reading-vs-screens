"""
03_cerebro.py – Qué ocurre en el cerebro durante la lectura vs. el scroll
"""
import sys
from pathlib import Path

import plotly.graph_objects as go
import streamlit as st

sys.path.insert(0, str(Path(__file__).parent.parent))
from data_loader import load_dataset_lazy
from components.image_exporter import export_figure_with_branding
from components.utils import load_css

st.set_page_config(page_title="El cerebro", page_icon="R", layout="wide")

load_css(str(Path(__file__).parent.parent / "assets" / "custom.css"))

LECTURA_PUNTOS = [
    "Activa la red neuronal por defecto: imaginacion, memoria autobiografica y empatia.",
    "Refuerza el cortex prefrontal: razonamiento abstracto, inferencia y control ejecutivo.",
    "Sincroniza lenguaje, emocion e imagen mental en una experiencia mas lenta y profunda.",
    "Favorece ondas alfa y una atencion sostenida compatible con relajacion cognitiva.",
]

SCROLL_PUNTOS = [
    "Sobreactiva el circuito dopaminergico con recompensas variables y bucles de novedad.",
    "Fragmenta la atencion con cambios constantes de contexto, alerta y notificacion.",
    "Empuja a un procesamiento mas superficial, rapido y menos memorable de los contenidos.",
    "Asocia luz azul y activacion emocional con peor desconexion y peor calidad de sueno.",
]

MICRO_METRICAS = [
    {"valor": "68 %", "label": "menos estres tras 6 minutos", "tone": "mint"},
    {"valor": "45 min", "label": "umbral de flujo lector", "tone": "ink"},
    {"valor": "5 dias", "label": "persistencia neurologica observada", "tone": "amber"},
]

st.markdown(
    """
    <section class="brain-hero">
        <div class="brain-hero-copy">
            <span class="brain-kicker">Neurociencia aplicada a la lectura</span>
            <h1>Parar y leer: una decision pequeña con efecto grande en tu autonomia mental</h1>
            <p>
                Leer no solo informa: cambia como atiendes, recuerdas y regulas el estres.
                Esta pagina resume de forma visual por que recuperar minutos de lectura tiene impacto real.
            </p>
        </div>
        <div class="brain-hero-panel">
            <div class="brain-panel-label">Lectura profunda</div>
            <div class="brain-panel-value">Resistencia cognitiva</div>
            <div class="brain-panel-copy">
                Menos interrupcion, mas continuidad narrativa, mas memoria y mejor regulacion emocional.
            </div>
        </div>
    </section>
    """,
    unsafe_allow_html=True,
)

metric_cols = st.columns(len(MICRO_METRICAS))
for col, metrica in zip(metric_cols, MICRO_METRICAS):
    with col:
        st.markdown(
            f"""
            <div class="brain-mini-card {metrica['tone']}">
                <div class="brain-mini-value">{metrica['valor']}</div>
                <div class="brain-mini-label">{metrica['label']}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

st.divider()

st.markdown('<div class="brain-section-eyebrow">Lectura vs. scroll</div>', unsafe_allow_html=True)
st.subheader("Dos arquitecturas mentales distintas")
st.caption(
    "La lectura profunda construye continuidad; el scroll premia el cambio constante. "
    "La diferencia no es moral, es neurologica y conductual."
)

col_lect, col_scroll = st.columns(2)

with col_lect:
    items = "".join(f"<li>{p}</li>" for p in LECTURA_PUNTOS)
    st.markdown(
        f"""
        <div class="brain-contrast-card reading">
            <div class="brain-card-topline">Lectura profunda</div>
            <h3>Atencion sostenida, simulacion mental y lenguaje integrado</h3>
            <ul>{items}</ul>
        </div>
        """,
        unsafe_allow_html=True,
    )

with col_scroll:
    items = "".join(f"<li>{p}</li>" for p in SCROLL_PUNTOS)
    st.markdown(
        f"""
        <div class="brain-contrast-card scroll">
            <div class="brain-card-topline">Scroll infinito</div>
            <h3>Novedad, recompensa intermitente y carga atencional fragmentada</h3>
            <ul>{items}</ul>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.divider()

left_col, right_col = st.columns([1.15, 0.85], gap="large")

fases = [
    dict(
        Fase="Activación sensorial",
        Inicio=0,
        Fin=5,
        Descripcion="El cortex visual procesa el texto y Wernicke arranca la decodificacion semantica.",
        Color="#FDB52A",
    ),
    dict(
        Fase="Inmersión narrativa",
        Inicio=5,
        Fin=20,
        Descripcion="Se activa la red neuronal por defecto y el lector simula escenas, voces y motivaciones.",
        Color="#11A253",
    ),
    dict(
        Fase="Flujo cognitivo",
        Inicio=20,
        Fin=45,
        Descripcion="La lectura entra en continuidad, dominan las ondas alfa y cae la carga de estres.",
        Color="#FCA4E0",
    ),
    dict(
        Fase="Consolidación (post-lectura)",
        Inicio=45,
        Fin=60,
        Descripcion="El hipocampo consolida patrones y favorece memoria a largo plazo tras el cierre.",
        Color="#155FCC",
    ),
]

with left_col:
    st.markdown('<div class="brain-section-eyebrow">Timeline neural</div>', unsafe_allow_html=True)
    st.subheader("Lo que ocurre durante una sesion larga de lectura")

    fig_gantt = go.Figure()

    for f in fases:
        duracion = f["Fin"] - f["Inicio"]
        # barra invisible de base (offset)
        fig_gantt.add_trace(go.Bar(
            y=[f["Fase"]],
            x=[f["Inicio"]],
            orientation="h",
            marker_color="rgba(0,0,0,0)",
            showlegend=False,
            hoverinfo="skip",
        ))
        # barra coloreada
        fig_gantt.add_trace(go.Bar(
            y=[f["Fase"]],
            x=[duracion],
            orientation="h",
            marker=dict(
                color=f["Color"],
                line=dict(color=f["Color"], width=0),
                opacity=0.92,
            ),
            showlegend=False,
            text=f"  {f['Inicio']}–{f['Fin']} min  ",
            textposition="outside",
            textfont=dict(color=f["Color"], size=12, family="monospace"),
            hovertext=f"<b>{f['Fase']}</b><br>{f['Descripcion']}",
            hoverinfo="text",
        ))

    fig_gantt.update_layout(
        barmode="stack",
        bargap=0.38,
        paper_bgcolor="#0F172A",
        plot_bgcolor="#0F172A",
        showlegend=False,
        height=320,
        margin=dict(t=12, b=36, l=0, r=90),
        font=dict(color="#CBD5E1", size=12),
        xaxis=dict(
            range=[0, 70],
            tickvals=[0, 5, 20, 45, 60],
            ticktext=["0", "5 min", "20 min", "45 min", "60 min"],
            tickfont=dict(color="#64748B", size=11),
            title_text="Minutos desde el inicio",
            title_font=dict(color="#64748B", size=11),
            gridcolor="#1E293B",
            showline=False,
            zeroline=False,
        ),
        yaxis=dict(
            tickfont=dict(color="#E2E8F0", size=12),
            showgrid=False,
            autorange="reversed",
        ),
    )

    timeline_col, legend_col = st.columns([0.74, 0.26], gap="small")

    with timeline_col:
        st.plotly_chart(fig_gantt, use_container_width=True)

        try:
            img_bytes = export_figure_with_branding(fig_gantt, filename="cerebro_lector_neuro")
            st.download_button(
                label="Descargar timeline",
                data=img_bytes,
                file_name="cerebro_lector_neuro.png",
                mime="image/png",
            )
        except Exception as exc:
            st.error(f"No se pudo exportar la imagen: {exc}")

    with legend_col:
        fase_items = "".join(
            f'<div class="fase-item"><span class="fase-dot" style="background:{f["Color"]}"></span>'
            f'<span class="fase-nombre">{f["Fase"]}</span>'
            f'<span class="fase-desc">{f["Descripcion"]}</span></div>'
            for f in fases
        )
        st.markdown(
            f'<div class="fase-grid">{fase_items}</div>',
            unsafe_allow_html=True,
        )

with right_col:
    st.markdown(
        """
        <div class="brain-side-note">
            <div class="brain-card-topline">Lectura prolongada</div>
            <h3>Una cadena continua de significado</h3>
            <p>
                El cambio no aparece solo por mirar palabras. Aparece cuando hay tiempo suficiente
                para que el cerebro una lenguaje, memoria, prediccion y emocion en una misma tarea.
            </p>
            <div class="brain-note-divider"></div>
            <p>
                Por eso la lectura larga se parece menos a "consumir contenido" y mas a entrenar una
                forma de atencion que hoy compite con interfaces hechas para interrumpirla.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.divider()

st.markdown(
    """
    <section class="brain-quote-block">
        <div class="brain-quote-mark">"</div>
        <blockquote>
            Cuando eliges leer, no solo cambias de actividad: recuperas la direccion de tu atencion.
        </blockquote>
        <p>
            El cerebro no solo descifra texto: modela escenarios, anticipa significados y mantiene
            una continuidad mental que las interfaces de scroll tienden a romper.
        </p>
        <div class="brain-quote-source">
            Inspirado en Berns et al. (2013) ·
            <a href="https://doi.org/10.1016/j.brainres.2013.11.009" target="_blank">Brain Connectivity</a>
        </div>
    </section>
    """,
    unsafe_allow_html=True,
)

gallery_left, gallery_right = st.columns(2)

with gallery_left:
    st.markdown(
        """
        <div class="brain-gallery-card">
            <span class="brain-gallery-tag">Neurolectura</span>
            <h4>La consolidacion necesita continuidad</h4>
            <p>
                Cuando el texto sostiene una linea narrativa, el cerebro puede integrar contexto,
                simbolos y recuerdo en una misma secuencia.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

with gallery_right:
    st.markdown(
        """
        <div class="brain-gallery-card dark">
            <span class="brain-gallery-tag">Pantallas</span>
            <h4>La atencion paga el precio de la novedad constante</h4>
            <p>
                Cuanto mas se entrena el salto rapido entre estimulos, mas dificil resulta sostener
                una tarea larga sin ansiedad de interrupcion.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.divider()

# ── Sueño y scroll nocturno ──────────────────────────────────────────────────────
st.markdown('<div class="brain-section-eyebrow">Scroll nocturno</div>', unsafe_allow_html=True)
st.subheader("Lo que el móvil le hace a tu sueño – y lo que la lectura no le hace")
st.caption(
    "El scroll antes de dormir no es solo un hábito: es luz azul suprimiendo melatonina, "
    "dopamina aplazando el inicio del sueño y algoritmos diseñados para que sigas. "
    "La lectura en papel activa exactamente el proceso contrario."
)

sleep_df = load_dataset_lazy("sleep_studies")

if sleep_df is not None and not sleep_df.empty:
    # KPIs de sueño
    try:
        row_mel = sleep_df[sleep_df["metric"] == "melatonin_suppression_pct"].iloc[0]
        row_circ = sleep_df[sleep_df["metric"] == "circadian_delay_hours"].iloc[0]
        row_odds = sleep_df[sleep_df["metric"] == "sleep_disturbance_odds_ratio"].iloc[0]

        sk1, sk2, sk3 = st.columns(3)
        sk1.markdown(
            f"""
            <div class="brain-mini-card scroll">
                <div class="brain-mini-value">{int(row_mel['screen_value'])}%</div>
                <div class="brain-mini-label">supresión de melatonina con pantalla</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        sk2.markdown(
            f"""
            <div class="brain-mini-card scroll">
                <div class="brain-mini-value">{row_circ['screen_value']:.1f}h</div>
                <div class="brain-mini-label">retraso del reloj circadiano</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        sk3.markdown(
            f"""
            <div class="brain-mini-card scroll">
                <div class="brain-mini-value">{row_odds['screen_value']:.2f}×</div>
                <div class="brain-mini-label">más probabilidad de alteración del sueño</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    except (IndexError, KeyError):
        pass

    # Gráfico comparativo: pantalla vs lectura
    METRIC_LABELS_SLEEP = {
        "melatonin_suppression_pct": "Supresión melatonina (%)",
        "circadian_delay_hours": "Retraso circadiano (h × 10)",
        "sleep_quality_score_deficit": "Déficit calidad sueño (pts)",
    }
    plot_sleep = sleep_df[sleep_df["metric"].isin(METRIC_LABELS_SLEEP)].copy()
    plot_sleep["label"] = plot_sleep["metric"].map(METRIC_LABELS_SLEEP)

    # Normalizar circadian_delay_hours × 10 para que sea visible en la misma escala
    mask_circ = plot_sleep["metric"] == "circadian_delay_hours"
    plot_sleep.loc[mask_circ, "screen_value"] = plot_sleep.loc[mask_circ, "screen_value"] * 10
    plot_sleep.loc[mask_circ, "reading_value"] = plot_sleep.loc[mask_circ, "reading_value"] * 10

    if not plot_sleep.empty:
        fig_sleep = go.Figure()
        fig_sleep.add_trace(go.Bar(
            x=plot_sleep["label"],
            y=plot_sleep["screen_value"],
            name="Con pantalla / scroll",
            marker_color="#D85A30",
        ))
        fig_sleep.add_trace(go.Bar(
            x=plot_sleep["label"],
            y=plot_sleep["reading_value"],
            name="Con lectura en papel",
            marker_color="#1D9E75",
        ))
        fig_sleep.update_layout(
            barmode="group",
            template="plotly_white",
            yaxis_title="Valor observado",
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            margin=dict(t=20, b=20, l=20, r=20),
            height=360,
        )
        sl_chart_col, sl_note_col = st.columns([2, 1])
        with sl_chart_col:
            st.plotly_chart(fig_sleep, use_container_width=True)
            try:
                img_sleep = export_figure_with_branding(fig_sleep, filename="cerebro_sueno_scroll")
                st.download_button(
                    label="Descargar gráfico",
                    data=img_sleep,
                    file_name="cerebro_sueno_scroll.png",
                    mime="image/png",
                )
            except Exception as exc:
                st.error(f"No se pudo exportar: {exc}")
        with sl_note_col:
            st.markdown(
                """
                <div class="brain-side-note" style="margin-top:0;">
                    <div class="brain-card-topline">Mecanismo</div>
                    <h3>Luz azul + dopamina = reloj roto</h3>
                    <p>
                        La luz LED de 400–490 nm suprime activamente la melatonina
                        e indica al cerebro que es de día. El resultado: tardar
                        más en conciliar el sueño y dormir con menor profundidad.
                    </p>
                    <div class="brain-note-divider"></div>
                    <p>
                        La lectura en papel no emite luz propia. Con luz tenue
                        la melatonina sube con normalidad y el inicio del sueño
                        se adelanta en lugar de retrasarse.
                    </p>
                </div>
                """,
                unsafe_allow_html=True,
            )

    # Tabla de fuentes
    with st.expander("Ver estudios de sueño y fuentes"):
        sleep_display = sleep_df[["study_id", "institution", "year", "metric", "sample_size", "doi", "description"]].copy()
        sleep_display["doi_link"] = sleep_display["doi"].apply(lambda d: f"https://doi.org/{d}")
        sleep_display = sleep_display.drop(columns=["doi"])
        sleep_display = sleep_display.rename(columns={
            "study_id": "ID", "institution": "Institución", "year": "Año",
            "metric": "Métrica", "sample_size": "Muestra",
            "doi_link": "DOI", "description": "Descripción",
        })
        st.dataframe(
            sleep_display,
            column_config={"DOI": st.column_config.LinkColumn("DOI", display_text="→ Ver estudio")},
            hide_index=True,
            use_container_width=True,
        )
else:
    st.info("Dataset de sueño en construcción – volverá pronto.")
"""
03_cerebro.py â€” QuÃ© ocurre en el cerebro durante la lectura vs. el scroll
"""