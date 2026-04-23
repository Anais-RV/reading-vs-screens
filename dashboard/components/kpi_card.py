"""
kpi_card.py — Tarjeta de métrica con borde de color personalizado.
"""
from __future__ import annotations

import streamlit as st

_COLOR_MAP: dict[str, str] = {
    "teal":   "#1D9E75",
    "coral":  "#D85A30",
    "purple": "#7F77DD",
    "amber":  "#EF9F27",
}

_CSS_INJECTED_KEY = "_kpi_card_css_injected"


def _inject_css() -> None:
    """Inyecta el CSS de las tarjetas una sola vez por sesión."""
    if st.session_state.get(_CSS_INJECTED_KEY):
        return
    st.markdown(
        """
        <style>
        .kpi-card {
            border-top: 4px solid var(--kpi-color, #1D9E75);
            border-radius: 8px;
            padding: 0.75rem 1rem 0.5rem;
            background: #FAFAFA;
            box-shadow: 0 1px 4px rgba(0,0,0,0.06);
            margin-bottom: 0.5rem;
        }
        .kpi-label {
            font-size: 0.8rem;
            color: #555;
            text-transform: uppercase;
            letter-spacing: 0.04em;
            margin-bottom: 0.2rem;
        }
        .kpi-value {
            font-size: 1.8rem;
            font-weight: 700;
            color: #1A1A1A;
            line-height: 1.2;
        }
        .kpi-delta {
            font-size: 0.85rem;
            color: #1D9E75;
            margin-top: 0.1rem;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
    st.session_state[_CSS_INJECTED_KEY] = True


def kpi_card(
    label: str,
    value: str,
    delta: str | None = None,
    color: str = "teal",
) -> None:
    """Renderiza una tarjeta de métrica estilizada.

    Parameters
    ----------
    label:
        Texto descriptivo de la métrica.
    value:
        Valor principal a mostrar (ej. "+38 %").
    delta:
        Texto secundario opcional (ej. "vs. grupo control").
    color:
        Color del borde superior. Valores aceptados: "teal", "coral", "purple", "amber".
    """
    _inject_css()
    hex_color = _COLOR_MAP.get(color, _COLOR_MAP["teal"])
    delta_html = f'<div class="kpi-delta">↑ {delta}</div>' if delta else ""
    st.markdown(
        f"""
        <div class="kpi-card" style="--kpi-color:{hex_color};">
            <div class="kpi-label">{label}</div>
            <div class="kpi-value" style="color:{hex_color};">{value}</div>
            {delta_html}
        </div>
        """,
        unsafe_allow_html=True,
    )
